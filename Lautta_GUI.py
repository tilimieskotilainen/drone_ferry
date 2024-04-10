import PySimpleGUI as sg
import Specs
#import backbone

layout = [
    [sg.OptionMenu(values=("Select route", "Olari", "Tonttari", "Jarvi"), default_value = "Select route", expand_x=True)],
    [sg.Text("Direction"), sg.Radio("Forward", group_id="direction", default=True),sg.Radio("Backward", group_id="direction", default=False)],
    [sg.Button("Calculate route", expand_x=True, key="Calculate")],

    [[sg.Text("Aim")],
     [sg.Slider(range=(1, 10), expand_x=True, default_value=3, resolution=1, tick_interval=1, orientation="horizontal", key="closest_plus")]],
    [[sg.Text("Turn range (mm)")],
     [sg.Slider(range=(10, 30), expand_x=True, default_value=20, resolution=1, tick_interval=5, orientation="horizontal", key="tof_range")]],    
    [[sg.Text("Turn tolerance (deg)")],
     [sg.Slider(range=(0, 20), expand_x=True, default_value=5, resolution=1, tick_interval=5, orientation="horizontal", key="steer_toler")]],
    [sg.Button("Update", expand_x=True, key="Update")],
    [sg.Text("Selected route"), sg.Text()],
    [sg.Text("Closest crumb"), sg.Text()],
    [sg.Text("Turn status"), sg.Text()],
    [sg.Text("Heading"), sg.Text()],
    [sg.Text("Battery voltage"), sg.Text()],

    [sg.Button("Start", button_color="Green", expand_x=True, key="Start")],
    [sg.Button("Stop", button_color="Red", expand_x=True, key="Stop")],
    ]

# Create the window
window = sg.Window("Lautta GUI", layout)

# Create an event loop
while True:
    event, values = window.read()

    if event == "Calculate":
        print("Calculated")
        Specs.update_calc()
        #Make start available
        #Make update available

    if event == "Update":

        #Tähän koodi jolla tehdään gui_input, joka sisältää kaikki GUI:ssa muutetut variablet
        closest_plus = int(values["closest_plus"])
        turn_range = int(values["tof_range"])
        turn_toler = int(values["steer_toler"])
        gui_input = {"closest_plus":int(values["closest_plus"]), "tof_range":int(values["tof_range"]), "steer_toler":int(values["steer_toler"])} 
        Specs.update_vars(gui_input)

        print(closest_plus, turn_range, turn_toler)


    if event == "Start":

        print("Started")
        backbone.run()
        #Make stop available

    if event == "Stop":
        print("Stopped")
        #Return to initial state
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

window.close()