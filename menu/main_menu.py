import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

import threading
from platform import system
from controller.controller import Controller
from visualisation.util.generate import EnvironmentConverter
from time import sleep
import os
import sys


class MainMenu:
    def __init__(self):
        # Create the window

        self.controller = None
        self.filename = None
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=500, height=500)
        self.root.maxsize(width=500, height=500)

        # Get Menu Cover Image
        self.title_img = Image.open("menu/assets/MainMenuTitle.png")
        self.title_img = self.title_img.resize((500, 112))
        self.title_img = ImageTk.PhotoImage(self.title_img)

        # Load Title and Covering Image
        self.cover = tk.Label(image=self.title_img)
        self.title = tk.Label(text="Main Menu", font='Helvetica 18 bold')

        # Create the buttons
        self.buttons = [tk.Button(text="Generate Environment", command=self.generate_environment, font="Helvetica"),
                        tk.Button(text="Play Offline Scenario", command=self.play_offline, font="Helvetica"),
                        tk.Button(text="Play Live Scenario", command=self.play_live, font="Helvetica"),
                        tk.Button(text="Generate Prediction (only dump)", command=self.generate_prediction, font="Helvetica"),
                        tk.Button(text="Play Prediction", command=self.play_prediction, font="Helvetica"),
                        tk.Button(text="Exit", command=self.close, font="Helvetica")]

    def _packer(self):
        """Private class to pack components into window"""
        self.cover.pack()
        self.title.pack(pady=20)
        for button in self.buttons:
            button.pack(pady=10)

    def launch(self):
        """Launches the window"""
        self._packer()
        self.root.mainloop()

    def show(self):
        """Shows a window if hidden"""
        self.root.deiconify()

    def hide(self):
        """Hides the window"""
        self.root.withdraw()

    def close(self):
        """Destroys an open window"""
        self.root.destroy()

        # hacky solution to ursinanetworking not cleaning up its threads
        os._exit(0)
        sys.exit(0)

    def play_live(self):
        """Functionality for launching 'live' bot"""
        tk.messagebox.showinfo("Unavailable Menu Option", "Sorry this version is still in development")

    def play_offline(self):
        """Functionality for launching offline play"""

        while self.filename is None:
            self.filename = fd.askopenfilename()

        # create threads
        thread_controller = threading.Thread(target=self.start_offline_controller)
        thread_vis = threading.Thread(target=self.start_offline_vis)

        # start threads
        thread_controller.start()
        thread_vis.start()

        # end threads
        thread_controller.join()
        thread_vis.join()
        self.filename = None

    def generate_environment(self):
        """Functionality for generating new environment from selected file"""

        while self.filename is None:
            self.filename = fd.askopenfilename()

        environment_manager = EnvironmentConverter(self.filename)

        # create threads
        thread_converter = threading.Thread(target=environment_manager.convert())

        # start threads
        thread_converter.start()

        # end threads
        thread_converter.join()
        self.filename = None

    def play_prediction(self):
        """Functionality for launching predictive play"""

        while self.filename is None:
            self.filename = fd.askopenfilename()

        # create threads
        thread_controller = threading.Thread(target=self.start_prediction)
        thread_vis = threading.Thread(target=self.start_offline_vis)

        # start threads
        thread_controller.start()
        thread_vis.start()

        # end threads
        thread_controller.join()
        thread_vis.join()
        self.filename = None

    def generate_prediction(self):
        """Functionality for launching predictive play"""

        while self.filename is None:
            self.filename = fd.askopenfilename()

        self.load_prediction()

        self.filename = None

    def start_offline_controller(self):
        """
        Send whole recorded file to visualisation, send to agent 0 as only 1 agent is recorded
        """
        self.controller = Controller(agent_count=2)
        self.controller.load_data(self.filename)

        sleep(2)

        # run the controller until we reach the end of the dataset
        # send to agent 0
        while self.controller.update(agent_num=0):
            sleep(0.1)

    def start_prediction(self):
        self.controller = Controller()
        with open(self.filename, "r") as f:
            instructions = f.readlines()

        for i in range(len(instructions)):
            instructions[i] = instructions[i].rstrip()

        instructions = list(filter(None, instructions))

        self.controller.load_prediction(instructions)

        sleep(2)

        # run the controller until we reach the end of the dataset
        while self.controller.visualise_dataframe(agent_num=0):
            sleep(0.1)

    def load_prediction(self):
        self.controller = Controller(headless=True)
        with open(self.filename, "r") as f:
            instructions = f.readlines()

        for i in range(len(instructions)):
            instructions[i] = instructions[i].rstrip()

        instructions = list(filter(None, instructions))

        self.controller.load_prediction(instructions)

    @staticmethod
    def start_offline_vis():
        plt = system()

        if plt == "Windows":
            os.system("cd visualisation && cmd.exe /c python visualisation.py")
        elif plt == "Linux":
            os.system("cd visualisation && python3 visualisation.py")
