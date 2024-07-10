
import os
from generator.generator import generate_form
import dearpygui.dearpygui as dpg

# Global variables, TODO better way to handle this?
json_str = ""

dpg.create_context()


def select_path(sender, app_data):
    """ Function to get all files and directories within the selected directory.
    Will populate the listbox "files_listbox" with the items.

    Args:
        sender (obj): Dear PyGui sender widget
        app_data ([obj]): information from the file dialog: file_path_name, file_name, current_path, current_filter, selections[]
    """
    global json_str

    savepath = os.path.join(app_data['file_path_name'], 'generated.json')

    print('saving file to', savepath)

    # save json file
    with open(savepath, 'w') as f:
        f.write(json_str)



def callback_generate():
    global json_str

    n_entries = int(dpg.get_value("input_n_entries"))
    n_members = int(dpg.get_value("input_n_members"))
    phacode = dpg.get_value("input_phacode")

    with dpg.window(pos=[575, 275], width=50, height=50, no_collapse=True, no_resize=True, no_close=True, no_move=True, no_title_bar=True) as loading:
        dpg.add_text(default_value="Processing...")
        json_str = generate_form(n_entries, n_members, phacode)
        dpg.delete_item(loading)

    dpg.show_item("file_dialog")


def cancel_callback():
    pass


def main_window_setup():
    dpg.create_viewport(title="SDF-HUD", width=1250, height=750)

    dpg.add_file_dialog(
        directory_selector=True, show=False, tag="file_dialog",
        callback=select_path, cancel_callback=cancel_callback, width=700 ,height=400)


    with dpg.window(pos=[400, 150], width=450, height=450, no_collapse=True, no_resize=True, no_close=True, no_move=True, no_title_bar=True) as main_window:
        dpg.add_text(default_value="Synthetic data generator for HUD")
        dpg.add_spacer(height=5)

        dpg.add_text(default_value="Parameters:")
        dpg.add_input_text(
            width=150,
            tag="input_n_entries",
            label="Number of entries to generate",
            default_value="500",
        )

        dpg.add_input_text(
            width=150,
            tag="input_n_members",
            label="Number of max member in a household",
            default_value="3",
        )

        dpg.add_input_text(
            width=150,
            tag="input_phacode",
            label="PhaCode",
            default_value="",
        )

        dpg.add_spacer(height=5)
        dpg.add_button(label="Generate", width=-1, height=30, callback=callback_generate)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

main_window_setup()