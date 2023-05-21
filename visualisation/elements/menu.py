class VisualMenu:
    """
    Helper class to store all relevant world state data for the visualisation
    """
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

        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_z = 0

    def update_menu(self, world_state, viewport):
        """
        Input a world_state dict and store locally for the visualisations needs
        :param world_state:
        :return:
        """
        self.x_pos = world_state["_pos"][0]*100
        self.y_pos = world_state["_pos"][1]*100
        self.z_pos = world_state["_pos"][2]*100

        self.x_rot = world_state["_rot"][0]
        self.y_rot = world_state["_rot"][1]
        self.z_rot = world_state["_rot"][2]

        self.x_vel = world_state["_vel"][0]
        self.y_vel = world_state["_vel"][1]
        self.z_vel = world_state["_vel"][2]

        self.x_acc = world_state["_acc"][0]
        self.y_acc = world_state["_acc"][1]
        self.z_acc = world_state["_acc"][2]

        self.motor_0 = world_state["A"]
        self.motor_1 = world_state["B"]
        self.motor_2 = world_state["C"]
        self.motor_3 = world_state["D"]

        self.viewport_x = viewport[0]
        self.viewport_y = viewport[1]
        self.viewport_z = viewport[2]

    def get_pos(self):
        """
        Get the current rover position from the last world state
        :return:
        """
        return [self.x_pos, self.y_pos, self.z_pos]

    def get_rot(self):
        """
        Get the current rover rotation from the last world state
        :return:
        """
        return [self.x_rot, self.y_rot, self.z_rot]
