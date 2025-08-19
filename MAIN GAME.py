from ursina import *
import random

app = Ursina()

EditorCamera()

ground = Entity(model = "cube", scale = (80,1,80), texture = "grass")

scale_x = 20
position_z = -20

for i in range(5):
    road = Entity(model = "cube", scale = (scale_x,0.1,4), color = color.gray, position = (0,0.6,position_z), texture = "white_cube")
    tunnel1 = Entity(model = "cube", scale = (10,5,5), color = color.white, position = (-15,2.5,position_z), texture = "white_cube")
    tunnel2 = Entity(model = "cube", scale = (10,5,5), color = color.white, position = (15,2.5,position_z), texture = "white_cube" )
    position_z += 8

app.run()