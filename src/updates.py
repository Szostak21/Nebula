from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
def update_vlines(self):
    start_index = -int(self.vlines_number/2) + 1
    for i in range (start_index, start_index+self.vlines_number):
        line_v = self.get_linev_from_index(i)
        x1, y1 = self.transform(line_v, 0)
        x2, y2 = self.transform(line_v, self.height)
        self.vlines[i].points = [x1, y1, x2, y2]

def update_hlines(self):
    start_index = -int(self.vlines_number/2) + 1
    xmin = self.get_linev_from_index(start_index)
    xmax = self.get_linev_from_index(start_index+self.vlines_number - 1)
    for i in range (self.hlines_number):
        line_h =  self.get_lineh_from_index(i)
        x1, y1 = self.transform(xmin, line_h)
        x2, y2 = self.transform(xmax, line_h)
        self.hlines[i].points = [x1, y1, x2, y2]
    
def update_tiles(self):
    for i in range(0, self.tiles_number):
        tile = self.tiles[i]
        tile_coordinates = self.tiles_coordinates[i]
        xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
        xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)
        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)

        tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

def update_ship(self):
    center_x = self.width/2
    x1 = center_x - self.ship_width*self.width/2
    x2 = center_x
    x3 = center_x + self.ship_width*self.width/2
    y1 = self.height*self.ship_base
    y2 = y1 + self.ship_height*self.height
    y3 = y1
    self.ship_point = (x2,y2)
    x1, y1 = self.transform(x1, y1)
    x2, y2 = self.transform(x2, y2)
    x3, y3 = self.transform(x3, y3)
    self.ship.points = [x1, y1, x2, y2, x3, y3]

def update_best_score(self):
    best_score_path = APP_DIR / 'best_score.txt'
    try:
        current_best_int = int(self.best_score)
    except Exception:
        current_best_int = 0
    if int(self.score) > current_best_int:
        self.best_score = int(self.score)
    try:
        with open(best_score_path, 'w') as file:
            file.write(str(self.best_score))
    except OSError:
        pass

def get_check_coordinates(self):
    for i in range(0, len(self.tiles_coordinates)):
        x, y = self.tiles_coordinates[i]
        if y > self.current_loop + 1:
            return False
        if self.check_collision(x, y):
            return True
    return False

def check_collision(self, tile_x, tile_y):
    xmin, ymin = self.get_tile_coordinates(tile_x, tile_y)
    xmax, ymax = self.get_tile_coordinates(tile_x + 1, tile_y + 1)
    ship_x, ship_y = self.ship_point

    if xmin <= ship_x <= xmax and ymin <= ship_y <= ymax:
        return True
    return False