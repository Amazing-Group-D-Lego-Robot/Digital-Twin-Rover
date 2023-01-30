from ursina import Ursina, Entity, mouse, application, camera, window, Text
from ursina.collider import BoxCollider
from ursina.mesh_importer import obj_to_ursinamesh
from ursina.vec3 import Vec3
from ursina.input_handler import held_keys
from ursina.prefabs.editor_camera import EditorCamera
from ursina.prefabs.trail_renderer import TrailRenderer
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import color
from ursinanetworking import *
from client import VisualClient
from menu import VisualMenu

Client = VisualClient()


@Client.event
def new_position(world_state):
    # Update the menu
    menu.update_menu(world_state)

    for i, [key, val] in enumerate(menu.__dict__.items()):
        menu_fields[i].text = f"{key}: {val:.2f}"

    # Update the rover
    rover.move_to(menu.get_pos())
    rover.rotate_to(menu.get_rot())


def update():
    # Process network communications
    Client.process_net_events()

    # Press tab to toggle free cam mode
    # if held_keys['tab']:
    #     pause_camera.enabled = not pause_camera.enabled
    #     viewport.visible_self = pause_camera.enabled
    #     viewport.cursor.enabled = not pause_camera.enabled
    #     mouse.locked = not pause_camera.enabled
    #     pause_camera.position = viewport.position
    #     application.paused = pause_camera.enabled

    if held_keys['escape']:
        Client.close()
        quit()


class Rover(Entity):
    def move_to(self, pos):
        self.animate_position(pos, duration=0.1)

    def rotate_to(self, rot):
        self.animate_rotation(rot, duration=0.1)


class Viewport(FirstPersonController):
    def input(self, key):
        if key == 'space':
            self.position += (0, 0.03, 0)

        if key == 'shift':
            self.position -= (0, 0.03, 0)


# Init ursina
app = Ursina(forced_aspect_ratio=4 / 3, size=(1000, 1000), vsync=False)
skybox = load_texture("assets/mars_skybox.png")
sky = Sky(texture=skybox, color=color.rgb(185, 157, 118))
menu = VisualMenu()

# Menu Values
corner = (round(window.top_left[0], 2) + .025, round(window.top_left[1], 2) - .025)

menu_fields = [Text(text="X", parent=app, scale=.75, x=corner[0], y=corner[1] - i * .025)
               for i in range(len(menu.__dict__))]

# Initialise the ground, rover and basic environment bounds
ground = Entity(model='plane', collider='box', scale=2048, texture='grass_tintable', color=color.rgb(193, 68, 14),
                texture_scale=(32, 32))

rover = Rover(model="RoverDebug", texture="rover_box", z=0, origin_y=-0.04)
# rover.collider = BoxCollider(rover, Vec3(0, 0, 0), Vec3(1, 1, 1))

viewport = Viewport(speed=1, x=0, z=-0.5)
viewport.gravity = 0
viewport.position += (0, 0.4, 0)

# Rover trails
pivot = Entity(parent=rover)
trail_renderer = TrailRenderer(parent=pivot, x=0, y=0.04, thickness=10, color=color.blue, length=10000)

# Handle pausing the visual
pause_camera = EditorCamera(enabled=False, ignore_paused=True)
pause_handler = Entity(ignore_paused=True, input=input_handler)

# window.size = (1280, 800)
app.run()
