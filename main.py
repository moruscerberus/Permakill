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
from core.assets import Assets

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load assets
Assets.load()

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

cursor = Assets.get('cursor')
cursor_offset = pygame.Vector2(15, 15)
cursor_pos = pygame.Vector2(pygame.mouse.get_pos())
prev_mouse_x = cursor_pos.x
cursor_angle = 0

pygame.mouse.set_visible(False)

def draw_cursor(pos, angle):
    if cursor:
        rotated = pygame.transform.rotate(cursor, angle)
        rect = rotated.get_rect(center=(pos.x, pos.y))
        screen.blit(rotated, rect)

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

    # Update and draw swaying, rotating cursor
    target = pygame.mouse.get_pos()
    cursor_pos += (pygame.Vector2(target) - cursor_pos) * 0.3

    mouse_x = target[0]
    dx = mouse_x - prev_mouse_x
    prev_mouse_x = mouse_x

    # Calculate and smooth cursor rotation
    target_angle = max(-45, min(45, dx * 2))
    cursor_angle += (target_angle - cursor_angle) * 0.3

    draw_cursor(cursor_pos, cursor_angle)

    pygame.display.flip()

pygame.quit()
