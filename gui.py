import PySimpleGUI as sg
import generator

"""
TODO
    - make a settings window
        o change the latex file being used
        o allow changing of save directory
        o allow changing of variables being used in the latex file
            - beside each variable, select what kind of text is being inputted
            - save this as a dict with key and values
                ex. ["companyName", "singleLine"]

    - auto generate the input fields for each variable needed
        o make sure the appropriate input text field is being used
        o add a submit button to confirm the submission of text

    - check every loop for inputs using the EVENT and VALUE variables
        o save the input in the previously made variable dict
            ex. {"companyName": ["singleLine", "Enbridge"]}

    - create a preview pane for the generated PDF
        o this pane will showcase a live preview of the changes being made
    """


class GUI:

    def __init__(self, config_info: dict) -> None:
        self.config_info = config_info

    # function to call the settings_window
    def settings_window(self):

        # creates a new layout for each variable needed
        def make_new_input_layout(i):
            return [[
                sg.Text("VAR " + str(i) + ": "),
                sg.InputText(key=("VAR", i))
            ]]

        # puts all the variables into a list
        def var_to_list(values: dict):
            var_list = []
            for key in values.keys():
                if type(key) is tuple and values[key]:
                    updated_var = values[key].replace(" ", "")
                    var_list.append(updated_var)
            return var_list

        variable_layout = [[sg.Text("VAR 1: "),
                            sg.InputText(key=("VAR", 0)),
                            sg.Button("+", enable_events=True, key="PLUS")]
                           ]

        input_confirmed_save_layout = [
            [sg.Text("Input Saved!", key="INPUT_CONFIRM_MSG")]]
        input_confirmed_template_layout = [
            [sg.Text("Input Saved!", key="INPUT_CONFIRM_MSG")]]

        template_dir_layout = [[sg.Button("Save", key="TEMPLATE_CONFIRM")]]
        save_dir_layout = [[sg.Button("Save", key="SAVE_CONFIRM")]]

        settings_layout = [[sg.Text("Select .tex file template")],
                           [sg.Text("Current Template: " +
                                    self.config_info.get("TEMPLATE_DIR", ""))],
                           [sg.Input("", key="TEMPLATE_DIR"), sg.FileBrowse()],
                           [sg.Column(template_dir_layout, key="TEMPLATE_NO_MSG"),
                           sg.Column(input_confirmed_template_layout, key="TEMPLATE_MSG", visible=False)],

                           [sg.HorizontalSeparator()],

                           [sg.Text("Select directory to save Cover Letter")],
                           [sg.Text("Current Directory: " +
                                    self.config_info.get("SAVE_DIR", ""))],
                           [sg.Input("", key="SAVE_DIR"), sg.FileBrowse()],
                           [sg.Column(save_dir_layout, key="SAVE_NO_MSG"),
                           sg.Column(input_confirmed_save_layout, key="SAVE_MSG", visible=False)],

                           [sg.HorizontalSeparator()],

                           [sg.Text("Input variable names to be replaced")],

                           [sg.Column(variable_layout, key="VAR_COLUMN")],
                           [sg.Submit(button_text="Update", key="SUBMIT")]
                           ]

        settings_window = sg.Window("Settings", layout=settings_layout)
        sg.Folder
        # event loop
        i = 2
        while True:
            event, values = settings_window.read(timeout=50)

            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            if event == "TEMPLATE_CONFIRM" and values["TEMPLATE_DIR"]:
                self.config_info["TEMPLATE_DIR"] = values["TEMPLATE_DIR"]
                settings_window["TEMPLATE_NO_MSG"].update(visible=False)
                settings_window["TEMPLATE_MSG"].update(visible=True)

            if event == "SAVE_CONFIRM" and values["SAVE_DIR"]:
                self.config_info["SAVE_DIR"] = values["SAVE_DIR"]
                settings_window["SAVE_NO_MSG"].update(visible=False)
                settings_window["SAVE_MSG"].update(visible=True)

            if event == "PLUS":
                settings_window.extend_layout(
                    settings_window["VAR_COLUMN"], make_new_input_layout(i))
                i += 1

            if event == "SUBMIT":
                self.config_info["VARIABLE_LIST"] = var_to_list(values)
                print(self.config_info)

        settings_window.close()

        print("---------------EXITING SETTINGS MENU-----------------")

        # return self.config_info

    def main(self):
        # main menu layout

        menu_layout = [
            ["Tools", ["Settings"]],
            ["Help", ["About"]]
        ]

        layout = [
            [sg.Menu(menu_layout)],
            []
        ]

        window = sg.Window("Cover Letter Generator", layout)

        # event loop
        while True:
            event, values = window.read()
            if event in (None, "Exit"):
                break
            if event in ("Settings"):
                print("---------------SETTINGS MENU-----------------")
                # self.config_info.update(self.settings_window())
                self.settings_window()

        print(self.config_info)

        window.close()
