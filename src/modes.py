from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock

class Modes(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_toggle_buttons)

    def initialize_toggle_buttons(self, dt):
        self.ids.toggle_button_1.bind(on_press=self.toggle_button_state)
        self.ids.toggle_button_2.bind(on_press=self.toggle_button_state)
        self.ids.toggle_button_3.bind(on_press=self.toggle_button_state)
        self.ids.toggle_button_4.bind(on_press=self.toggle_button_state)
        self.ids.toggle_button_5.bind(on_press=self.toggle_button_state)
        self.ids.return_button.bind(on_press=self.return_to_menu)

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super().on_touch_down(touch)

    def toggle_button_state(self, instance):
        if instance.text == "OFF":
            instance.text = "ON"
            instance.background_color = (0.2, 0.8, 0.2, 1)
        else:
            instance.text = "OFF"
            instance.background_color = ( 1, .3, .4)

    def return_to_menu(self, instance):
        self.parent.menu_widget.opacity = 1
        self.parent.modes_widget.opacity = 0
