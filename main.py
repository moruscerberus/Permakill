import pygame
from settings import *
from core.manager import GameStateManager
from core.transition import TransitionManager

# States
from core.states.splash import SplashState
from core.states.menu import MenuState
from core.states.gameplay import GamePlayState
from core.states.gameover import GameOverState
from core.states.settings import SettingsState

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Setup transition system
transition = TransitionManager(screen)

# Setup state manager with transition support
manager = GameStateManager(screen, transition)

# Register states
manager.register("splash", SplashState(manager, screen))
manager.register("menu", MenuState(manager, screen))
manager.register("gameplay", GamePlayState(manager, screen))
manager.register("game_over", GameOverState(manager, screen))
manager.register("settings", SettingsState(manager, screen))

# Set initial state WITHOUT transition
manager.force_state("splash")

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not transition.is_transitioning():
            manager.handle_event(event)

    manager.update(dt)
    transition.update(dt)

    manager.draw()
    transition.draw()

    pygame.display.flip()

pygame.quit()
