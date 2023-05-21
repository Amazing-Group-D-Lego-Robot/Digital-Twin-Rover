from ursina.prefabs.trail_renderer import TrailRenderer
from ursina.shaders import basic_lighting_shader
from ursinanetworking import *
from networking.client import VisualClient
from elements.menu import VisualMenu
from elements.viewport import Viewport
from elements.agent import Agent
from elements.environment import SimulatedEnvironment
from util.pathfind import predict_path
from ursina import invoke
from time import time

DELAY = 0.5

Client = VisualClient()
last_quad_change = time()
last_prediction = time()

trail_colours = [color.pink, color.blue, color.yellow]

def reset_quad_change():
    global last_quad_change
    last_quad_change = time()


def reset_prediction():
    global last_prediction
    last_prediction = time()


@Client.event
def agent_number(num: int):
    print(f'Currently creating {num} agents')
    for i in range(num):
        # Agent creation
        # agent_offset = [0, -0.04, 0]
        agent_offset = [environment.origin_offset[0], -0.04, environment.origin_offset[1]]
        agents.append(
            Agent(model="legotest",
                  texture="legotest_tex",
                  scale=50,
                  shader=basic_lighting_shader,
                  position=agent_offset,
                  )
        )
        agents[i].add_sensor(Vec3(0, 0.1, 0.17), Vec3(0, 0, 0.05))
        agents[i].add_sensor(Vec3(0, 0.1, -0.17), Vec3(0, 0, -.5))

        # Agent trails
        pivot = Entity(parent=agents[i])
        TrailRenderer(parent=pivot, x=0, y=0.04, thickness=10, color=trail_colours[i], length=10000)


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
    agents[agent_num].move_to(menu.get_pos(), environment.origin_offset)
    agents[agent_num].rotate_to(menu.get_rot())


def update():
    """
    Ursina update function, ran every ursina update, not necessarily every frame
    :return:
    """
    # Process network communications
    while len(Client.events_manager.events) > 0:
        Client.process_net_events()

    # Decrement the chosen block
    if held_keys['-'] and time() - last_quad_change > DELAY:
        environment.selected_block -= 1
        print(f"Selected block: {environment.selected_block % len(environment.blocks)}")
        reset_quad_change()
        invoke(environment.move_selection_orb)

    # Increment the chosen block
    if held_keys['='] and time() - last_quad_change > DELAY:
        environment.selected_block += 1
        print(f"Selected block: {environment.selected_block % len(environment.blocks)}")
        reset_quad_change()
        invoke(environment.move_selection_orb)

    # Predict the path to the selected block
    if held_keys['enter'] and time() - last_prediction > DELAY:
        predicted_path = predict_path(
            agents[0].position,
            environment.selected_block,
            environment.blocks[environment.selected_block].centre,
        )
        environment.draw_waypoints(predicted_path)
        reset_prediction()

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

# Environment
environment = SimulatedEnvironment()

agents = []

viewport = Viewport(speed=1, x=0, z=-0.5)
viewport.gravity = 0
viewport.position = [environment.origin_offset[0], -0.04, environment.origin_offset[1]]

# Handle pausing the visual
pause_camera = EditorCamera(enabled=False, ignore_paused=True)
pause_handler = Entity(ignore_paused=True, input=input_handler)

app.run()
