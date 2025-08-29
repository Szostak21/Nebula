from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock


ACTIVE_COLOR = (0.2, 0.8, 0.2, 1)
INACTIVE_COLOR = (1, 0.3, 0.4, 1)

class Modes(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_toggle_buttons)

    def initialize_toggle_buttons(self, dt):
        # Speed mode buttons (Mode 1 & 2)
        self.ids.toggle_button_1.bind(on_press=self.on_turtle_pressed)
        self.ids.toggle_button_2.bind(on_press=self.on_sonic_pressed)
        # Width mode buttons (Tight / Wide)
        if 'tight_button' in self.ids:
            self.ids.tight_button.bind(on_press=self.on_tight_pressed)
        if 'wide_button' in self.ids:
            self.ids.wide_button.bind(on_press=self.on_wide_pressed)
        self.ids.return_button.bind(on_press=self.return_to_menu)
        self.update_speed_buttons()
        self.update_width_buttons()

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super().on_touch_down(touch)

    def toggle_button_state(self, instance):
        pass  # Removed extra modes

    # --- Speed mode logic ---
    def on_turtle_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        # Toggle turtle; if already turtle -> revert to normal
        new_speed = 'normal' if parent.mode_speed == 'turtle' else 'turtle'
        parent.update_mode_settings(speed=new_speed)
        self.update_speed_buttons()

    def on_sonic_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        # Toggle sonic; if already sonic -> revert to normal
        new_speed = 'normal' if parent.mode_speed == 'sonic' else 'sonic'
        parent.update_mode_settings(speed=new_speed)
        self.update_speed_buttons()

    def update_speed_buttons(self):
        parent = self.parent
        if not parent:
            return
        mode = parent.mode_speed
        turtle_btn = self.ids.toggle_button_1
        sonic_btn = self.ids.toggle_button_2
        if mode == 'turtle':
            turtle_btn.background_color = ACTIVE_COLOR
            sonic_btn.background_color = INACTIVE_COLOR
        elif mode == 'sonic':
            turtle_btn.background_color = INACTIVE_COLOR
            sonic_btn.background_color = ACTIVE_COLOR
        else:  # normal
            turtle_btn.background_color = INACTIVE_COLOR
            sonic_btn.background_color = INACTIVE_COLOR

    # --- Width mode logic ---
    def on_tight_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        # Toggle tight; revert to normal if already tight
        new_width = 'normal' if parent.mode_width == 'tight' else 'tight'
        parent.update_mode_settings(width=new_width)
        self.update_width_buttons()

    def on_wide_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        # Toggle wide; revert to normal if already wide
        new_width = 'normal' if parent.mode_width == 'wide' else 'wide'
        parent.update_mode_settings(width=new_width)
        self.update_width_buttons()

    def update_width_buttons(self):
        parent = self.parent
        if not parent:
            return
        mode = parent.mode_width
        tight_btn = self.ids.get('tight_button')
        wide_btn = self.ids.get('wide_button')
        if not tight_btn or not wide_btn:
            return
        if mode == 'tight':
            tight_btn.background_color = ACTIVE_COLOR
            wide_btn.background_color = INACTIVE_COLOR
        elif mode == 'wide':
            tight_btn.background_color = INACTIVE_COLOR
            wide_btn.background_color = ACTIVE_COLOR
        else:  # normal
            tight_btn.background_color = INACTIVE_COLOR
            wide_btn.background_color = INACTIVE_COLOR

    def return_to_menu(self, instance):
        # Ensure modes applied before returning
        if self.parent:
            self.parent.apply_selected_modes()
            self.parent.menu_widget.opacity = 1
            self.parent.modes_widget.opacity = 0
