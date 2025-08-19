from ursina import *
import random

app = Ursina()

EditorCamera()

ground = Entity(model = "cube", scale = (80,1,80), texture = "grass")

win_text = Text(text = "YOU WIN", scale = 5, position = (900, 900), color = color.yellow, origin = (0,0))
player = Entity(model = "cube", scale = 1, color = color.blue, position = (0,1,-30), texture = "white_cube")


scale_x = 20
position_z = -20

for i in range(5):
    road = Entity(model = "cube", scale = (scale_x,0.1,4), color = color.gray, position = (0,0.6,position_z), texture = "white_cube")
    tunnel1 = Entity(model = "cube", scale = (10,5,5), color = color.white, position = (-15,2.5,position_z), texture = "white_cube")
    tunnel2 = Entity(model = "cube", scale = (10,5,5), color = color.white, position = (15,2.5,position_z), texture = "white_cube" )
    position_z += 8

class Enemy(Entity):
    def __init__(self, x, y, z):
        super().__init__(
        parent=scene,
        model="cube",
        color = color.red,
        scale=(1,2,1),
        position=(x,y,z),
        collider="box",
        texture = "white_cube"
        )

num = 5
enemies = [None] * num

ex = 0
enemy_speed = 0

for i in range(num):
    ex = random.randint(-30, -15)
    ez = random.randint(0, 4)

    ez = (ez*8)-20
    ey = 2

    enemies[i] = Enemy(ex,ey,ez)

Sky()

def update():
    global enemy_speed
    for enemy in enemies:
        enemy_speed = random.uniform(0.3,0.7)
        enemy.x += enemy_speed

        if enemy.x > 20:
            enemy.x = random.randint(-30,-15)
            ez = random.randint(0, 4)

            enemy.z = (ez*8)-20

app.run()