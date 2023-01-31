from ursina import Entity, camera, load_texture
from ursina import *


class VisualMenu:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0

        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0

        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0

        self.x_acc = 0
        self.y_acc = 0
        self.z_acc = 0

        self.motor_0 = 0
        self.motor_1 = 0
        self.motor_2 = 0
        self.motor_3 = 0

    def update_menu(self, world_state):
        self.x_pos = world_state["pos"][0]
        self.y_pos = world_state["pos"][1]
        self.z_pos = world_state["pos"][2]

        self.x_rot = world_state["rot"][0]
        self.y_rot = world_state["rot"][1]
        self.z_rot = world_state["rot"][2]

        self.x_vel = world_state["vel"][0]
        self.y_vel = world_state["vel"][1]
        self.z_vel = world_state["vel"][2]

        self.x_acc = world_state["acc"][0]
        self.y_acc = world_state["acc"][1]
        self.z_acc = world_state["acc"][2]

        self.motor_0 = world_state["motor_rots"][0]
        self.motor_1 = world_state["motor_rots"][1]
        self.motor_2 = world_state["motor_rots"][2]
        self.motor_3 = world_state["motor_rots"][3]

    def get_pos(self):
        return [self.x_pos, self.y_pos, self.z_pos]

    def get_rot(self):
        return [self.x_rot, self.y_rot, self.z_rot]


class MainMenu(Entity):
    def __init__(self):
        """Init for Main Menu Entity"""
        super().__init__(
            parent=camera.ui,
            # model='quad',
            scale=(0.9, 0.9),
            texture=load_texture('assets/menu-bg.jpg')
        )
