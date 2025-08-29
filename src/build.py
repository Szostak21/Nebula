import random
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.vertex_instructions import Quad
from kivy.graphics.vertex_instructions import Triangle
from kivy.graphics import InstructionGroup

def build_vlines(self):
    """(Re)build vertical lines inside a persistent instruction group so their
    z-order stays behind tiles/ship even after width changes.

    Using an InstructionGroup prevents rebuilt lines from being appended to the
    end of the canvas (which previously caused them to draw over the ship and
    tiles after a width mode change).
    """
    # Create group once and add to canvas at initial build (early => behind)
    if not hasattr(self, 'vlines_group'):
        self.vlines_group = InstructionGroup()
        # Add the group now (early in app start) so it stays below later items
        self.canvas.add(self.vlines_group)
    # Clear existing line instructions
    self.vlines_group.clear()
    self.vlines.clear()
    # Re-add color + lines
    self.vlines_group.add(Color(1, 1, 1))
    for _ in range(self.vlines_number):
        line = Line(width=1.1)
        self.vlines_group.add(line)
        self.vlines.append(line)

def build_hlines(self):
    with self.canvas:
        Color(1, 1, 1)
        for i in range (self.hlines_number):
            line = Line(width = 1.1)
            self.hlines.append(line)

def build_tiles(self):
    with self.canvas:
        Color(1, 1, 1,)
        for i in range (self.tiles_number_started):
            self.tiles.append(Quad())
            tile = self.tiles[i]
            tile.points = [0,0,0,0,0,0,0,0]

def build_ship(self):
    with self.canvas:
        Color(0, 0, 0)
        self.ship = Triangle()

def generate_tiles_coordinates(self):
    for i in range(len(self.tiles_coordinates)-1, -1, -1):
        if self.tiles_coordinates[i][1] < self.current_loop:
            del self.tiles_coordinates[i]

    self.tiles_number = self.tiles_number_started if self.state_game_started else self.tiles_number_not_started

    for i in range (len(self.tiles_coordinates), self.tiles_number):
        if not self.state_game_started:
            self.tiles_coordinates.append((0,self.last_y))
            self.last_y += 1
            self.last_x = 0
        if int(self.best_score) < 21 and self.state_game_started:
            self.tiles_coordinates.append((0,self.last_y))
            self.tiles_coordinates.append((-1,self.last_y))
            self.tiles_coordinates.append((1,self.last_y))
            self.last_y += 1
            self.last_x = 0
        elif int(self.best_score) > 20 and int(self.best_score) < 23 and self.state_game_started:
            self.tiles_coordinates.append((0,self.last_y))
            self.last_y += 1
            self.last_x = 0
        elif self.last_y < 8 and self.state_game_started:
            self.tiles_coordinates.append((0,self.last_y))
            self.last_y += 1
            self.last_x = 0
        elif self.state_game_started:
            x = random.randint(0,2)
            if x == 0:
                self.tiles_coordinates.append((self.last_x,self.last_y))
                self.last_y += 1
            elif x == 1:
                if self.last_x > -(self.vlines_number/2-1):
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_x -= 1 
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1                        
                else:                     
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_x += 1 
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1  
            elif x == 2:
                if self.last_x < (self.vlines_number/2-1):
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_x += 1 
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1                        
                else:                     
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_x -= 1 
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1
                    self.tiles_coordinates.append((self.last_x,self.last_y))
                    self.last_y += 1                                        
        
def get_linev_from_index(self, index):
    central_line_v = self.perspective_x
    spacing = self.width * self.vlines_spacing
    offset = index - 0.5
    line_x = central_line_v + offset*spacing + self.movement*spacing
    return line_x

def get_lineh_from_index(self, index):
    spacing_h = self.hlines_spacing*self.height
    line_y = index*spacing_h-self.current_offset
    return line_y

def get_tile_coordinates(self, t_x, t_y):
    x = self.get_linev_from_index(t_x)
    y = self.get_lineh_from_index(t_y - self.current_loop)
    return x, y