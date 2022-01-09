import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import main
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

    def get_config_info(self):
        return self.config_info

    # function to call the settings_window
    def settings_window(self):

        # creates a new layout for each variable needed
        def generate_new_var_inputs_layout(i):
            return [[
                sg.Text(f"VAR {i}:"),
                sg.InputText(key=("VAR", i)),
                sg.Radio("Single Line",
                         group_id=f"Group {i}", key=f"SINGLE_LINE_{i}"),
                sg.Radio(
                    "Multiline", group_id=f"Group {i}", key=f"MULTILINE_{i}")
            ]]

        # puts all the variables into a list
        def var_to_text_type_dic(values: dict):
            var_dic = {}
            for key in values.keys():
                if type(key) is tuple and values[key]:
                    updated_var = values[key].replace(" ", "")
                    var_num = key[1]

                    if values[f"SINGLE_LINE_{var_num}"]:
                        text_type = "SINGLELINE"
                    elif values[f"MULTILINE_{var_num}"]:
                        text_type = "MULTILINE"
                    elif not(values[f"SINGLE_LINE_{var_num}"]) and not(values[f"MULTILINE_{var_num}"]):
                        text_type = "SINGLELINE"

                    var_dic[updated_var] = text_type

            return var_dic

        variable_layout = [[sg.Text("VAR 0: "),
                            sg.InputText(key=("VAR", 0)),
                            sg.Radio("Single Line", group_id="Group 1",
                                     key=f"SINGLE_LINE_{0}"),
                            sg.Radio("Multiline", group_id="Group 1",
                                     key=f"MULTILINE_{0}"),
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
                           [sg.Input("", key="SAVE_DIR"), sg.FolderBrowse()],
                           [sg.Column(save_dir_layout, key="SAVE_NO_MSG"),
                           sg.Column(input_confirmed_save_layout, key="SAVE_MSG", visible=False)],

                           [sg.HorizontalSeparator()],

                           [sg.Text(
                               "Input variable names to be replaced AND type of input box needed")],

                           [sg.Column(variable_layout, key="VAR_COLUMN")],
                           [sg.Submit(button_text="Update", key="SUBMIT")]
                           ]

        settings_window = sg.Window("Settings", layout=settings_layout)

        # event loop
        i = 1
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
                    settings_window["VAR_COLUMN"], generate_new_var_inputs_layout(i))
                i += 1

            if event == "SUBMIT":
                self.config_info["VAR_TO_TEXT_TYPE_DIC"] = var_to_text_type_dic(
                    values)

        settings_window.close()

        print("---------------EXITING SETTINGS MENU-----------------")

        # return self.config_info

    def main(self):

        def generate_var_inputs_layout():
            var_layout = []

            for var_and_type in self.config_info["VAR_TO_TEXT_TYPE_DIC"].items():
                if var_and_type[1] == "SINGLELINE":
                    var_layout.append([sg.Text(f"{var_and_type[0]}: "),
                                       sg.Input(
                                           key=f"{var_and_type[0]}_INPUT"),

                                       # Save Button Functionality
                                       sg.Button(
                                           "Save", key=f"{var_and_type[0]}_VAR_INPUT_CONFIRM"),
                                       sg.Text("Input Saved!", visible=False, key=f"{var_and_type[0]}_SAVED_MSG")])
                # Multiline
                else:
                    var_layout.append([sg.Text(f"{var_and_type[0]}: ")])
                    var_layout.append(
                        [[sg.Multiline(key=f"{var_and_type[0]}_INPUT")],

                         # Save Button Functionality
                         [sg.Button("Save", key=f"{var_and_type[0]}_VAR_INPUT_CONFIRM"),
                          sg.Text("Input Saved!", visible=False, key=f"{var_and_type[0]}_SAVED_MSG")]
                         ])

            return var_layout

        def check_for_saved_settings():
            main_window_layout = []

            # User has not inputted necessary information
            if not(self.config_info.get("VAR_TO_TEXT_TYPE_DIC", "")):
                main_window_layout.append(
                    [sg.Text("ERROR: VARIABLES NOT FOUND! PLEASE GO TO SETTINGS AND INPUT VARIABLES.")])
            if not(self.config_info.get("SAVE_DIR", "")):
                main_window_layout.append([sg.Text(
                    "ERROR: NO SAVE DIRECTORY FOUND! PLEASE GO TO SETTINGS AND INPUT SAVE DIRECTORY.")])
            if not(self.config_info.get("TEMPLATE_DIR", "")):
                main_window_layout.append([sg.Text(
                    "ERROR: NO TEMPLATE FOUND! PLEASE GO TO SETTINGS AND INPUT TEMPLATE DIRECTORY.")])

            if main_window_layout:
                main_window_layout.append(
                    [sg.Text("Please relaunch the program to apply new settings!")])

            if self.config_info.get("VAR_TO_TEXT_TYPE_DIC"):
                main_window_layout.append(generate_var_inputs_layout())

            return main_window_layout

        def var_to_input_dic(event, values):
            if not(self.config_info.get("VAR_TO_INPUT_DIC", "")):
                self.config_info["VAR_TO_INPUT_DIC"] = {}

            var = event.replace("_VAR_INPUT_CONFIRM", "")
            user_input = values[f"{var}_INPUT"]

            self.config_info["VAR_TO_INPUT_DIC"].update({var: user_input})

        # main menu layout
        menu_layout = [
            ["Tools", ["Settings"]],
            ["Help", ["About"]]
        ]

        layout = [
            [sg.Menu(menu_layout)],
            [check_for_saved_settings()]
        ]

        window = sg.Window("Cover Letter Generator",
                           layout,
                           resizable=True,
                           location=(400, 200),
                           grab_anywhere=True)

        # event loop
        while True:
            event, values = window.read()
            if event in (None, "Exit"):
                break
            if event in ("Settings"):
                print("---------------SETTINGS MENU-----------------")
                self.settings_window()
            if "VAR_INPUT_CONFIRM" in event:
                window[event.replace("VAR_INPUT_CONFIRM", "SAVED_MSG")].update(
                    visible=True)
                var_to_input_dic(event, values)

            print(self.config_info)

        window.close()
