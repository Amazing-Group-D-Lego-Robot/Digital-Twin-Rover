import tkinter as tk
from PIL import ImageTk, Image


class MainMenu():
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=720, height=720)

        self.title_img = ImageTk.PhotoImage(Image.open("assets/MainMenuTitle.png"))
        self.cover = tk.Label(image=self.title_img)
        self.title = tk.Label(text="Main Menu")

        self.buttons = [tk.Button(text="Play Offline Scenario", command = self.play_offline),
                        tk.Button(text="Play Live Scenario", command=self.play_live),
                        tk.Button(text="Exit", command=self.close)]

    def _packer(self):
        """Private class to pack into window"""
        self.cover.pack()
        self.title.pack(pady=20)
        for button in self.buttons:
            button.pack(pady=10)

    def launch(self):
        self._packer()
        self.root.mainloop()

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

    def close(self):
        self.root.destroy()

    def play_live(self):
        pass

    def play_offline(self):
        pass


def main() -> int:
    """
    Main Loop for running main menu
    :return: status code based on menu exit
    """
    window = MainMenu()
    window.launch()


if __name__ == "__main__":
    main()
