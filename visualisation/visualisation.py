from ursina import Ursina, Entity, mouse, application, camera, window, Text
from ursina.collider import BoxCollider
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
def update_pos(world_state):
    # update visualisation with new world state
    print(f"Message from server: {world_state}")
    rover.set_position(world_state)


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
    if held_keys['tab']:
        pause_camera.enabled = not pause_camera.enabled
        rover.visible_self = pause_camera.enabled
        rover.cursor.enabled = not pause_camera.enabled
        mouse.locked = not pause_camera.enabled
        pause_camera.position = rover.position
        application.paused = pause_camera.enabled

    if held_keys['escape']:
        quit()

    update_menu()


# Init ursina
app = Ursina()
skybox = load_texture("assets/mars_skybox.png")
sky = Sky(texture=skybox, color=color.rgb(185, 157, 118))

# Menu Values
x_pos = Text(text="XXXXXXXXX", parent=app, scale=.75, x=-1.15, y=0.450)
y_pos = Text(text="XXXXXXXXX", parent=app, scale=.75, x=-1.15, y=0.425)
z_pos = Text(text="XXXXXXXXX", parent=app, scale=.75, x=-1.15, y=0.400)

# Initialise the ground, rover and basic environment bounds
ground = Entity(model='plane', collider='box', scale=2048, texture='grass_tintable', color=color.rgb(193, 68, 14),
                texture_scale=(32, 32))
rover = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-2.5, speed=8)
rover.collider = BoxCollider(rover, Vec3(0, 1, 0), Vec3(1, 2, 1))
camera.x = 5
camera.z = -20

# Rover trails
pivot = Entity(parent=rover)
trail_renderer = TrailRenderer(parent=pivot, x=.1, y=2.5, thickness=20, color=color.white, length=100)

# Handle pausing the visual
pause_camera = EditorCamera(enabled=False, ignore_paused=True)
pause_handler = Entity(ignore_paused=True, input=input_handler)

# window.size = (1600, 800)
app.run()
