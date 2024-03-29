from ursina.prefabs.trail_renderer import TrailRenderer
from ursina.shaders import basic_lighting_shader
from ursinanetworking import *
from networking.client import VisualClient
from elements.menu import VisualMenu
from elements.viewport import Viewport
from elements.agent import Agent
from elements.environment import SimulatedEnvironment

Client = VisualClient()

@Client.event
def agent_number(num: int):
    print(f'Currently creating {num} agents')
    for i in range(num):
        # Agent creation
        agent_offset = [0, -0.04, 0]
        agents.append(
            Agent(model="legotest",
                  texture="legotest_tex",
                  shader=basic_lighting_shader,
                  z=agent_offset[2],
                  origin_y=agent_offset[1])
        )
        agents[i].add_sensor(Vec3(0, 0.1, 0.17), Vec3(0, 0, 0.05))
        agents[i].add_sensor(Vec3(0, 0.1, -0.17), Vec3(0, 0, -.5))

        # Agent trails
        pivot = Entity(parent=agents[i])
        TrailRenderer(parent=pivot, x=0, y=0.04, thickness=10, color=color.blue, length=10000)

@Client.event
def new_position(data_packet: list):
    """
    Process the incoming world state and, update the menu, update the rover position / rotation
    :param data_packet:
    :return:
    """
    # Parse packet
    agent_num = data_packet[0]
    world_state = data_packet[1]

    # Update the menu if main agent
    if agent_num == 0:
        menu.update_menu(world_state, viewport.position)

        for i, [key, val] in enumerate(menu.__dict__.items()):
            menu_fields[i].text = f"{key}: {val:.2f}"

    # Update the agent
    agents[agent_num].move_to(menu.get_pos())
    agents[agent_num].rotate_to(menu.get_rot())


def update():
    """
    Ursina update function, ran every ursina update, not necessarily every frame
    :return:
    """
    # Process network communications
    while len(Client.events_manager.events) > 0:
        Client.process_net_events()

    if held_keys['escape']:
        Client.close()
        quit()


# Init ursina
app = Ursina(forced_aspect_ratio=4 / 3, size=(1000, 1000), vsync=True)
skybox = load_texture("assets/mars_skybox.png")
sky = Sky(texture=skybox, color=color.rgb(185, 157, 118))
menu = VisualMenu()

# Menu Values
corner = (round(window.top_left[0], 2) + .025, round(window.top_left[1], 2) - .025)

menu_fields = [Text(text="X", parent=app, scale=.75, x=corner[0], y=corner[1] - i * .025)
               for i in range(len(menu.__dict__))]

# Initialise the ground, agent and basic environment bounds
ground = Entity(model='plane', collider='box', scale=2048, texture='grass_tintable', color=color.rgb(193, 68, 14),
                texture_scale=(32, 32))

agents = []

viewport = Viewport(speed=1, x=0, z=-0.5)
viewport.gravity = 0
viewport.position += (0, 0.4, 0)

# Environment
environment = SimulatedEnvironment()

# Handle pausing the visual
pause_camera = EditorCamera(enabled=False, ignore_paused=True)
pause_handler = Entity(ignore_paused=True, input=input_handler)

app.run()
