import PySimpleGUI as sg

sg.theme()   # Add a touch of color
# All the stuff inside your window.
main_menu_layout = [[sg.Text('Start menu', justification='center', size=(100, 3))],
                    [sg.Button('Single player game',size=(100,2))],
                    [sg.Button('Multiplayer game',size=(100,2))],
                    [sg.Button('Exit',size=(100,2))]]

multiplayer_menu_layout = [
                    [sg.Text('Multiplayer game', justification='center', size=(100, 2))],
                    [sg.Text('Name:  '),sg.Input()],
                    [sg.Text('IP:       '),sg.Input()],
                    [sg.Text('Port:    '),sg.Input()],
                    [sg.Button('Run server',size=(100,2))],
                    [sg.Button('Connect to server',size=(100,2))],
                    [sg.Button('Show available servers list',size=(100,2))],
                    [sg.Button('Back',size=(100,2))]]

layouts = [[sg.Column(main_menu_layout, key='-COL1-'), sg.Column(multiplayer_menu_layout, visible=False, key='-COL2-')]]

# Create the Window
window = sg.Window('Ping pong menu', layouts, size=(400, 400), icon='menu_icon.ico')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(values)
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    elif event == 'Single player game':
        pass
    elif event == 'Connect to server':
        pass
    elif event == 'Run server':
        pass
    elif event == 'Show available servers list':
        pass
    elif event == 'Multiplayer game':
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=True)
    elif event == 'Back':
        window[f'-COL1-'].update(visible=True)
        window[f'-COL2-'].update(visible=False)

window.close()