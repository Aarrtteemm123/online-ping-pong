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

data = [['127.0.0.1','8080','1/2'] for __ in range(5)]
headings=['IP address','Port','Players']
servers_list_layout = [
    [sg.Text('Available servers', justification='center', size=(100, 2))],
    [sg.Table(values=data, justification='right', headings=headings,size=(10, 7),
              display_row_numbers=True,pad=(65,10),
              auto_size_columns=True,
              key='-TABLE-',
              row_height=30)],
    [sg.Button('Update',size=(100,2))],
    [sg.Button('Back to menu',size=(100,2))],
]

layouts = [[sg.Column(main_menu_layout, key='-COL1-'),
            sg.Column(multiplayer_menu_layout, visible=False, key='-COL2-'),
            sg.Column(servers_list_layout, visible=False, key='-COL3-')]]

# Create the Window
window = sg.Window('Ping pong menu', layouts, size=(400, 400), icon='menu_icon.ico')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event,values)
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    elif event == 'Single player game':
        pass
    elif event == 'Connect to server':
        pass
    elif event == 'Run server':
        pass
    elif event == 'Update':
        data.append(['127.0.0.1','8080','1/2'])
        window['-TABLE-'].update(values=data)
    elif event == 'Back to menu':
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=True)
        window['-COL3-'].update(visible=False)
    elif event == 'Show available servers list':
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=True)
    elif event == 'Multiplayer game':
        window['-COL1-'].update(visible=False)
        window['-COL3-'].update(visible=False)
        window['-COL2-'].update(visible=True)
    elif event == 'Back':
        window['-COL1-'].update(visible=True)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=False)

window.close()