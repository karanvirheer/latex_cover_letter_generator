import pickle
from os.path import exists
import gui

CONFIG_INFO = {}

# checking if the settings.dat file exists
file_exists = exists("settings.dat")

# if file exists, update the CONFIG_INFO dict
if file_exists:
    CONFIG_INFO.update(pickle.load(open("settings.dat", "rb")))

if __name__ == "__main__":
    # methods
    gui = gui.GUI(CONFIG_INFO)
    gui.main()
