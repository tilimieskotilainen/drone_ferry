import PySimpleGUI as sg

layout = [
    [sg.OptionMenu(values=("Select route", "Olari", "Tonttari", "J�rvi"), default_value = "Select route", expand_x=True)],
    [sg.Text("Direction"), sg.Radio("Forward", group_id="direction", default=True),sg.Radio("Backward", group_id="direction", default=False)],
    [sg.Button("Calculate", expand_x=True)],

    [[sg.Text("Aim")],
     [sg.Slider(range=(1, 10), expand_x=True, default_value=3, resolution=1, tick_interval=1, orientation="horizontal")]],
    [[sg.Text("Turn range (mm)")],
     [sg.Slider(range=(10, 30), expand_x=True, default_value=20, resolution=1, tick_interval=5, orientation="horizontal")]],    
    [[sg.Text("Turn tolerance (deg)")],
     [sg.Slider(range=(0, 20), expand_x=True, default_value=5, resolution=1, tick_interval=5, orientation="horizontal")]],
    [sg.Button("Update", expand_x=True)],
    [sg.Text("Selected route"), sg.Text()],
    [sg.Text("Closest crumb"), sg.Text()],
    [sg.Text("Turn status"), sg.Text()],
    [sg.Text("Heading"), sg.Text()],
    [sg.Text("Battery voltage"), sg.Text()],

    [sg.Button("Start", button_color="Green", expand_x=True)],
    [sg.Button("Stop", button_color="Red", expand_x=True)],
    ]

# Create the window
window = sg.Window("Lautta GUI", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()