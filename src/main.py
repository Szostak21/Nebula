from kivy.config import Config
Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '900')

from kivy import platform
import os
from pathlib import Path
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.properties import Clock
from kivy.lang.builder import Builder
from kivy.resources import resource_add_path

# Ensure all relative resource paths (kv, fonts, images, audio, data files)
# resolve from this file's directory, regardless of where the app is launched.
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
FONTS_DIR = PROJECT_ROOT / 'fonts'
IMAGES_DIR = PROJECT_ROOT / 'images'
AUD_DIR = PROJECT_ROOT / 'audio'
resource_add_path(str(FONTS_DIR))
resource_add_path(str(IMAGES_DIR))
resource_add_path(str(AUD_DIR))
try:
    os.chdir(APP_DIR)
except Exception:
    # On some embedded runtimes chdir can be restricted; it's safe to ignore.
    pass

Builder.load_file('menu.kv')
Builder.load_file('modes.kv')

class MainWidget(RelativeLayout):
    from build import build_hlines, build_ship, build_tiles, build_vlines, generate_tiles_coordinates, get_lineh_from_index, get_linev_from_index, get_tile_coordinates
    from updates import update_best_score, update_hlines, update_ship, update_tiles, update_vlines, check_collision, get_check_coordinates
    from transforms import transform, transform_perspective
    from user_interactions import on_keyboard_down, on_touch_down, keyboard_closed, h_movement
    modes_widget = ObjectProperty()
    menu_widget = ObjectProperty()
    perspective_x = NumericProperty(0)
    perspective_y = NumericProperty(0)

    vlines_number = 8                          
    vlines_spacing = 0.3
    vlines = []                                                          #liczba lini i odstępy

    hlines_number = 8
    hlines_spacing = 0.2
    hlines = []

    tiles = []
    tiles_coordinates = []
    tiles_number_started = 30
    tiles_number_not_started = 8

    ship = None
    ship_width = 0.1
    ship_height = 0.035
    ship_base = 0.04
    ship_point = ()

    current_loop = 0
    current_offset = 0
    last_y = 0
    movement = 0
    speed = 8
    score = 0
    best_score = 0

    state_game_over = False
    state_game_started = False

    menu_title = StringProperty("N    E    B    U    L    A")
    menu_button_title = StringProperty("START")
    menu_modes_title = StringProperty("MODES")
    score_label = StringProperty("SCORE: " + str(score))
    best_score_label = StringProperty("BEST SCORE: " + str(best_score))

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.build_vlines()
        self.build_hlines()
        self.build_tiles()
        self.build_ship()
        self.generate_tiles_coordinates()
        self.load()
        self.width = self.width
        self.height = self.height
        self.label = None
        if self.is_pc():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)

        Clock.schedule_interval(self.update, 1/60)                       #FPS

    def reset_game(self):
        self.current_loop = 0
        self.current_offset = 0
        self.last_y = 0
        self.movement = 0
        self.speed = 8
        self.score = 0
        self.load()

        self.tiles_coordinates.clear()
        self.generate_tiles_coordinates()

        self.state_game_started = True
        self.state_game_over = False

    def load(self):
        best_score_path = APP_DIR / 'best_score.txt'
        try:
            with open(best_score_path, 'r') as file:
                self.best_score = str(file.readline()).strip() or '0'
        except FileNotFoundError:
            self.best_score = 0
        try:
            if int(self.best_score) <= 30:
                self.best_score = 0
        except ValueError:
            self.best_score = 0

    def is_pc(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def on_size(self, *args):
        self.perspective_x = self.width/2
        self.perspective_y = self.height * 0.75

    def tutorial(self):
        if int(self.best_score) < 30:
            if self.label is None:  
                self.label = Label(
                    text='WELCOME',
                    font_name='Sackers-Gothic-Std-Light.ttf',
                    font_size=self.width * 0.023,
                    pos_hint={'center_x': 0.5, 'center_y': 0.9},
                    color=(1, 1, 1, 1))
                self.add_widget(self.label)

            if int(self.best_score) < 20 and int(self.best_score) > 5 and not self.is_pc():
                self.label.text = 'CLICK ON EITHER SIDE OF THE SCREEN TO PILOT YOUR SHIP'

            if int(self.best_score) < 20 and int(self.best_score) > 5 and self.is_pc():
                self.label.text = 'USE LEFT AND RIGHT ARROWS TO PILOT YOUR SHIP'

            if int(self.best_score) < 29 and int(self.best_score) > 19:
                self.label.text = 'KEEP THE SHIP ON THE WHITE TRACK!'

            if int(self.best_score) == 29:
                self.label.text = ''
    
    def update(self, time):
            time_fix = time*60
            self.update_vlines()
            self.update_hlines()
            self.update_tiles()
            self.update_ship()
            self.update_best_score()
            self.best_score_label = "BEST SCORE: " + str(self.best_score)
            if not self.state_game_over:
                self.generate_tiles_coordinates()
                self.score_label = "SCORE: " + str(self.score)
                spacing_y = self.hlines_spacing*self.height
                while self.current_offset >= spacing_y:
                        self.current_offset -= spacing_y
                        self.current_loop += 1
                self.current_offset += time_fix*self.speed*self.height/1000
            if not self.state_game_over and self.state_game_started:
                self.score = self.current_loop
                if self.speed < 25:
                    self.speed += self.current_loop*0.00005

                if not self.get_check_coordinates() and not self.state_game_over and int(self.best_score)>29:
                    self.state_game_over = True
                    self.menu_title = "G A M E    O V E R"
                    self.menu_button_title = "RESTART"
                    self.menu_modes_title = "MENU"
                    self.menu_widget.opacity = 1
            if int(self.best_score) < 30 and self.state_game_started:
                self.tutorial()

    def on_menu_modes(self):
        if self.menu_modes_title == "MODES":
            self.state_game_over = False
            self.state_game_started = False
            self.menu_widget.opacity = 0
            self.modes_widget.opacity = 1

        if self.menu_modes_title == "MENU":
            self.current_loop = 0
            self.current_offset = 0
            self.last_y = 0
            self.movement = 0
            self.speed = 8
            self.score = 0
            self.state_game_started = False
            self.tiles_coordinates.clear()
            self.generate_tiles_coordinates()
            self.update_tiles()

            self.state_game_over = False
            
            self.menu_title = "N   E   B   U   L   A"
            self.menu_button_title = "START"
            self.menu_modes_title = "MODES"

    def on_menu_button(self):
        self.reset_game()
        self.state_game_started = True
        self.menu_widget.opacity = 0

    def on_modes_button(self):
        print('test')

class NebulaApp(App):
    pass

if __name__ == '__main__':
    NebulaApp().run()

