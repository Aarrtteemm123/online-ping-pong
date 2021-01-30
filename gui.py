import PySimpleGUI as sg
import threading

class Gui:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__is_running = True

        self.__main_menu_layout = [[sg.Text('Start menu', justification='center', size=(100, 3))],
                                   [sg.Button('Single player game',key='-SPG-', size=(100, 2))],
                                   [sg.Button('Multiplayer game',key='-MPG-', size=(100, 2))],
                                   [sg.Button('Exit',key='-EXIT-', size=(100, 2))]]

        self.__multiplayer_menu_layout = [
            [sg.Text('Multiplayer game', justification='center', size=(100, 2))],
            [sg.Text('Name:          '), sg.Input(key='name')],
            [sg.Text('Server name:'), sg.Input(key='server name')],
            [sg.Text('IP:               '), sg.Input(key='ip')],
            [sg.Text('Port:            '), sg.Input(key='port')],
            [sg.Text('Select number of players'), sg.Combo(['2', '3', '4'],key='number players', default_value=2, size=(10, 2))],
            [sg.Button('Run server',key='-RUN-SERVER-', size=(100, 2))],
            [sg.Button('Connect to server',key='-CONNECT-', size=(100, 2))],
            [sg.Button('Show available servers list',key='-SHOW-SERVERS-', size=(100, 2))],
            [sg.Button('Back',key='-BACK-', size=(100, 2))]]

        self.__table_data = [['qwerty', '127.0.0.1', '8080', '1/2'] for __ in range(5)]
        self.__table_headings = ['Server name', 'IP address', 'Port', 'Players']

        self.__servers_list_layout = [
            [sg.Text('Available servers', justification='center', size=(100, 2))],
            [sg.Table(values=self.__table_data, headings=self.__table_headings, size=(20, 7),
                      display_row_numbers=True, pad=(10, 10),
                      auto_size_columns=True,
                      key='-TABLE-', row_height=30)],
            [sg.Button('Update',key='-UPDATE-SERVERS-TABLE-', size=(100, 2))],
            [sg.Button('Back to menu',key='-BACK-TO-MENU-', size=(100, 2))],
        ]

        self.__layouts = [[sg.Column(self.__main_menu_layout, key='-MAIN_MENU-'),
                           sg.Column(self.__multiplayer_menu_layout, visible=False, key='-MUPTIPLAYER_MENU-'),
                           sg.Column(self.__servers_list_layout, visible=False, key='-SERVERS_MENU-')]]

        self.__window = sg.Window('Ping pong menu', self.__layouts, size=(400, 400), icon='menu_icon.ico')

    def start(self):
        thread = threading.Thread(target=self.__run)
        thread.start()

    def close(self):
        self.__is_running = False

    def __run(self):
        sg.theme()  # Add a touch of color
        while self.__is_running:
            event, values = self.__window.read(timeout=10)
            print(event, values)
            if event == sg.WIN_CLOSED or event == '-EXIT-':  # if user closes window or clicks cancel
                self.close()

            elif event == '-SPG-':
                pass

            elif event == '-CONNECT-':
                pass

            elif event == '-RUN-SERVER-':
                pass

            elif event == '-UPDATE-SERVERS-TABLE-':
                self.__table_data.append(['my server', '127.0.0.1', '8080', '1/2'])
                self.__window['-TABLE-'].update(values=self.__table_data)

            elif event == '-BACK-TO-MENU-':
                self.__window['-MAIN_MENU-'].update(visible=False)
                self.__window['-MUPTIPLAYER_MENU-'].update(visible=True)
                self.__window['-SERVERS_MENU-'].update(visible=False)

            elif event == '-SHOW-SERVERS-':
                self.__window['-MAIN_MENU-'].update(visible=False)
                self.__window['-MUPTIPLAYER_MENU-'].update(visible=False)
                self.__window['-SERVERS_MENU-'].update(visible=True)

            elif event == '-MPG-':
                self.__window['-MAIN_MENU-'].update(visible=False)
                self.__window['-MUPTIPLAYER_MENU-'].update(visible=True)
                self.__window['-SERVERS_MENU-'].update(visible=False)

            elif event == '-BACK-':
                self.__window['-MAIN_MENU-'].update(visible=True)
                self.__window['-MUPTIPLAYER_MENU-'].update(visible=False)
                self.__window['-SERVERS_MENU-'].update(visible=False)

        self.__window.close()