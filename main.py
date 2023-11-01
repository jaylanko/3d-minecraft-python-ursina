from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random


app = Ursina()

# Textures for the blocks
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
tree_texture = load_texture('assets/tree_texture.png')
sand_texture = load_texture('assets/sand_block.png')
leaves_texture = load_texture('assets/leafs.png')

block_pick = 1


def update():
    global block_pick
    if held_keys['1']:
        block_pick = 1
    if held_keys['2']:
        block_pick = 2
    if held_keys['3']:
        block_pick = 3
    if held_keys['4']:
        block_pick = 4
    if held_keys['5']:
        block_pick = 5
    if held_keys['6']:
        block_pick = 6
    if held_keys['7']:
        block_pick = 7


# Creating block
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture, model='assets/block', scale=0.5):
        super().__init__(
            parent=scene,  # ensuring that block is added to the scene
            position=position,
            model=model,
            origin_y=0.5,  # vertical origin
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=scale
        )

    def input(self, key):
        if self.hovered:
            if key == 'e':
                if block_pick == 1:
                    Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2:
                    Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 3:
                    Voxel(position=self.position + mouse.normal, texture=brick_texture)
                if block_pick == 4:
                    Voxel(position=self.position + mouse.normal, texture=dirt_texture)
                if block_pick == 5:
                    Voxel(position=self.position + mouse.normal, texture='white_cube', model='plane')
                if block_pick == 6:
                    Voxel(position=self.position + mouse.normal, texture='tree_texture')
                if block_pick == 7:
                    Voxel(position=self.position + mouse.normal, texture='sand_block')

            if key == 'q':
                destroy(self)


# Creating sky with sky_texture, it is sphere and if we scale it a lot we
# are going to be inside the sphere but texture is
# on other side so double_sided set to true makes it visible even from inside
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )


# Function to create leaves above a tree
def create_leaves(x, y, z):  # X,Y,Z Represent position of tree leaves
    for dz in range(-2, 3):  # Dz and Dx are two for loops which are iterating to create 5x5 grid
        for dx in range(-2, 3):
            for dy in range(2, 5):  # Adjust dy range to raise the leaves higher
                if abs(dx) == 2 and abs(dz) == 2 and dy == 4:
                    continue  # Skip corners of the leaves
                if abs(dx) <= 1 and abs(dz) <= 1 and dy == 2:
                    continue  # Skip center of the leaves
                Voxel(
                    position=(x + dx, y + dy, z + dz),
                    texture=leaves_texture,
                    scale=0.5
                )


# Creating a platform with for loop which takes Voxel(block) and makes 25 in z and 25 in x-axis
for z in range(25):
    for x in range(25):
        voxel = Voxel(position=(x, 0, z))

for _ in range(15):
    x = random.randint(0, 19)
    z = random.randint(0, 19)
    y = 0
    while y < 4:
        voxel = Voxel(position=(x, y + 1, z), texture=tree_texture, scale=0.5)
        create_leaves(x, y + 1, z)  # Create leaves above the tree
        y += 1


spawn_position = (12, 0, 12)  # Starting point of player
pyramid_position = Vec3(20, 0, 20)  # Position of pyramid
pyramid_size = 5  # height and width of pyramid, 5x5
for y in range(pyramid_size):  # y represents height level
    for x in range(-y, y + 1):
        for z in range(-y, y + 1):  # x and z are iterating to create square layer on every level
            voxel = Voxel(position=pyramid_position + Vec3(x, pyramid_size - y, z), texture=sand_texture, scale=0.5)

player = FirstPersonController()  # Prebuilt Ursina FP Controller
sky = Sky()  # Calling sky function
app.run()
