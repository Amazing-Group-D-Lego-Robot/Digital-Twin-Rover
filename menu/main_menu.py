import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image


class MainMenu():
    def __init__(self):
        # Create the window
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=500, height=500)
        self.root.maxsize(width=500, height=500)

        # Get Menu Cover Image
        self.title_img = Image.open("assets/MainMenuTitle.png")
        self.title_img = self.title_img.resize((500, 112))
        self.title_img = ImageTk.PhotoImage(self.title_img)

        # Load Title and Covering Image
        self.cover = tk.Label(image=self.title_img)
        self.title = tk.Label(text="Main Menu", font='Helvetica 18 bold')

        # Create the buttons
        self.buttons = [tk.Button(text="Play Offline Scenario", command=self.play_offline, font="Helvetica"),
                        tk.Button(text="Play Live Scenario", command=self.play_live, font="Helvetica"),
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

    def play_live(self):
        """Functionality for launching 'live' bot"""
        tk.messagebox.showinfo("Unavailable Menu Option", "Sorry this version is still in development")

    def play_offline(self):
        """Functionality for launching offline play"""
        filename = fd.askopenfilename(parent=self.root)
        print(filename)


def test_menu() -> int:
    """
    test loop for running main menu
    :return: status code based on menu exit
    """
    window = MainMenu()
    window.launch()
