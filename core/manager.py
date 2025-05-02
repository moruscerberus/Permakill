# core/manager.py

class GameStateManager:
    def __init__(self, screen, transition):
        self.screen = screen
        self.transition = transition
        self.states = {}
        self.current = None

    def register(self, name, state):
        self.states[name] = state

    def force_state(self, name):
        """Use for initial state only (no fade)."""
        if name in self.states:
            self.current = self.states[name]
            self.current.enter()
            print(f"[STATE] Forced initial state: {name}")
        else:
            print(f"[ERROR] State '{name}' not registered.")

    def set_state(self, name):
        if name not in self.states:
            print(f"[ERROR] State '{name}' not registered.")
            return

        def _fade_to_new_state():
            print(f"[DEBUG] Fade out complete, switching to {name}")
            self._set_state_fade_in(name)

        print(f"[STATE] Transitioning to '{name}'")
        self.transition.start_fade_out(on_complete=_fade_to_new_state)

    def _set_state_fade_in(self, name):
        self.current = self.states[name]
        self.current.enter()
        print(f"[STATE] Now in {name}")
        self.transition.start_fade_in()

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self):
        if self.current:
            self.current.draw()

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)
