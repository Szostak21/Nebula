def transform(self, x, y):                                           #2d --> 3d
    #return x ,y
    return self.transform_perspective(x,y)

def transform_perspective(self, x, y):
    lin_y = y*self.perspective_y/self.height
    if lin_y > self.perspective_y:
        lin_y = self.perspective_y

    delta_x = x-self.perspective_x
    delta_y = self.perspective_y-lin_y
    proportion = delta_y/self.perspective_y
    proportion = pow(proportion, 2.5)                                  #perspektywa bloków

    x3d = self.perspective_x + delta_x*proportion
    y3d = self.perspective_y - proportion*self.perspective_y

    return int(x3d), int(y3d)
