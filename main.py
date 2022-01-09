import mpu
from os.path import exists
import gui


def load_settings():

    config_info = {}

    # checking if the settings.dat file exists
    file_exists = exists("settings.pickle")

    # if file exists, update the config_info dict
    if file_exists:
        config_info.update(mpu.io.read("settings.pickle", format=dict))

    return config_info


def save_settings(new_config_info):
    old_config_info = load_settings()

    for key in old_config_info:
        # key exists in old settings, but there was no value stored
        # updating the key to now store a value
        if not(old_config_info[key]) and (new_config_info[key]):
            old_config_info[key] = new_config_info[key]

        # key and value exists in both old settings and new settings
        # overriding the old settings with a new setting
        if old_config_info[key] and new_config_info[key]:
            old_config_info[key] = new_config_info[key]

    # key did not exist in the old settings
    # adding new key and new value
    for key in new_config_info:
        if not(old_config_info.get(key, "")):
            old_config_info[key] = new_config_info[key]

    updated_config_info = old_config_info.copy()
    mpu.io.write("settings.pickle", updated_config_info)


if __name__ == "__main__":
    config_info = load_settings()

    # methods
    gui = gui.GUI(config_info)
    gui.main()

    save_settings(gui.get_config_info())
