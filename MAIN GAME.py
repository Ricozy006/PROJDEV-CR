from ursina import *
import random

app = Ursina()

EditorCamera()

ground = Entity(model="cube", scale=(80,1,80), texture="grass")

win_text = Text(text="YOU WIN", scale=5, position=(900,900), color=color.yellow, origin=(0,0))
player = Entity(model="cube", scale=1, color=color.blue, position=(0,1,-30), texture="white_cube")

scale_x = 20
position_z = -20

for i in range(5):
    road = Entity(model="cube", scale=(scale_x,0.1,4), color=color.gray, position=(0,0.6,position_z), texture="white_cube")
    tunnel1 = Entity(model="cube", scale=(10,5,5), color=color.white, position=(-15,2.5,position_z), texture="white_cube")
    tunnel2 = Entity(model="cube", scale=(10,5,5), color=color.white, position=(15,2.5,position_z), texture="white_cube" )
    position_z += 8

class Enemy(Entity):
    def __init__(self, x, y, z):
        super().__init__(
            parent=scene,
            model="cube",
            color=color.red,
            scale=(1,2,1),
            position=(x,y,z),
            collider="box",
            texture="white_cube"
        )
        self.speed = random.uniform(0.3, 0.7)  # vitesse fixée par ennemi

num = 5
enemies = []

for i in range(num):
    ex = random.randint(-30, -15)
    ez = random.randint(0, 4)
    ez = (ez * 8) - 20
    ey = 2
    enemy = Enemy(ex, ey, ez)
    enemies.append(enemy)

Sky()

def update():
    global position_z

    for enemy in enemies:
        enemy.x += enemy.speed

        if enemy.x > 20:
            enemy.x = random.randint(-30, -15)
            ez = random.randint(0, 4)
            enemy.z = (ez * 8) - 20
            enemy.speed = random.uniform(0.3, 0.7)  # vitesse remise à jour

        if distance(enemy, player) < 2:
            player.position = (0,1,-30)

    if player.z > position_z:
        win_text.position = (0,0)
    else:
        win_text.position = (900,900)  # correction faute de frappe

    # Caméra lissée vers le joueur
    target_cam_pos = Vec3(player.x, player.y + 15, player.z - 25)
    camera.position = lerp(camera.position, target_cam_pos, time.dt * 4)
    camera.look_at(player)

    # Limites strictes en X
    if held_keys['a'] and player.x > -15:
        player.x -= 0.1
    if held_keys['d'] and player.x < 15:
        player.x += 0.1
    if held_keys['w']:
        player.z += 0.1
    if held_keys['s']:
        player.z -= 0.1

app.run()
