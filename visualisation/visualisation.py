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

Client = UrsinaNetworkingClient("localhost", 25565)


@Client.event
def onConnectionEstablished():
    print("I'm connected to the server !")


@Client.event
def onConnectionError(reason):
    print(f"Error ! Reason : {reason}")


@Client.event
def update_twin_rot(world_state):
    # update visualisation with new world state
    # print(f"Message from server (update_twin_rot): {world_state}")
    rover.rotate_to(world_state)


@Client.event
def update_twin_pos(world_state):
    # update visualisation with new world state
    # print(f"Message from server (update_twin_pos): {world_state}")
    rover.move_to(world_state)


def update_menu():
    # Update the menu
    rover_pos = rover.getPos()
    x_pos.text = f"X Position: {rover_pos[0]:.2f}"
    y_pos.text = f"Y Position: {rover_pos[1]:.2f}"
    z_pos.text = f"Z Position: {rover_pos[2]:.2f}"


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
        quit()

    update_menu()


class Rover(Entity):
    def move_to(self, pos):
        self.animate('position', pos, duration=.1)

    def rotate_to(self, rot):
        self.animate('rotation', rot, duration=.1)


class Viewport(FirstPersonController):
    def input(self, key):
        if key == 'space':
            self.position += (0, 0.03, 0)

        if key == 'shift':
            self.position -= (0, 0.03, 0)


# Init ursina
app = Ursina(forced_aspect_ratio=4/3, size=(1000, 1000), vsync=False)
skybox = load_texture("assets/mars_skybox.png")
sky = Sky(texture=skybox, color=color.rgb(185, 157, 118))

# Menu Values
x_pos = Text(text="XXXXXXXXX", parent=app, scale=.75, x=0.1, y=0.0)
y_pos = Text(text="XXXXXXXXX", parent=app, scale=.75, x=0.1, y=0.03)
z_pos = Text(text="XXXXXXXXX", parent=app, scale=.75, x=0.1, y=0.06)

# Initialise the ground, rover and basic environment bounds
ground = Entity(model='plane', collider='box', scale=2048, texture='grass_tintable', color=color.rgb(193, 68, 14),
                texture_scale=(32, 32))

rover = Rover(model="RoverDebug", texture="rover_box", z=0, origin_y=-0.04)
#rover.collider = BoxCollider(rover, Vec3(0, 0, 0), Vec3(1, 1, 1))

viewport = Viewport(speed=1, x=0, z=-0.5)
viewport.gravity = 0
viewport.position += (0, 0.4, 0)

# Rover trails
pivot = Entity(parent=rover)
trail_renderer = TrailRenderer(parent=pivot, x=0, y=0.04, thickness=10, color=color.blue, length=10000)

# Handle pausing the visual
pause_camera = EditorCamera(enabled=False, ignore_paused=True)
pause_handler = Entity(ignore_paused=True, input=input_handler)

#window.size = (1280, 800)
app.run()
