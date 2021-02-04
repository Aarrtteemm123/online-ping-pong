import PySimpleGUI as sg
import ctypes
from client import Client
from game_objects import Game
import requests, json
from config import *
from server import Server


class Gui:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)
        return cls.instance

    def __init__(self):

        self.server = None
        self.user_data = UserData()
        self.client = None

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

        self.__table_data = [['', '', '', '', '']]
        self.__table_headings = ['Server name', 'IP address', 'Port', 'Players', 'Limit']

        self.__servers_list_layout = [
            [sg.Text('Available servers', justification='center', size=(100, 2))],
            [sg.Table(values=self.__table_data, headings=self.__table_headings, size=(30, 7),
                      display_row_numbers=False,pad=(10,10),
                      auto_size_columns=True,
                      key='-TABLE-', row_height=30)],
            [sg.Button('Update',key='-UPDATE-SERVERS-TABLE-', size=(100, 2))],
            [sg.Button('Back to menu',key='-BACK-TO-MENU-', size=(100, 2))],
        ]

        self.__layouts = [[sg.Column(self.__main_menu_layout, key='-MAIN_MENU-'),
                           sg.Column(self.__multiplayer_menu_layout, visible=False, key='-MUPTIPLAYER_MENU-'),
                           sg.Column(self.__servers_list_layout, visible=False, key='-SERVERS_MENU-')]]

        self.__window = sg.Window('Ping pong menu', self.__layouts, size=(400, 400), icon='menu_icon.ico')

    def __load_servers(self):
        try:
            res = requests.get(f'{BASIC_URL}/get_servers')
            data = json.loads(res.text)
            self.__table_data = []
            for item in data:
                self.__table_data.append(list(item.values()))
        except Exception as e:
            print(e)

    def start(self):
        sg.theme()  # Add a touch of color
        while True:
            try:
                event, values = self.__window.read(timeout=10)
                #print(event, values)
                if self.server and self.server.connections == self.user_data.max_players - 1:
                    print('running game')
                if event == sg.WIN_CLOSED or event == '-EXIT-':  # if user closes window or clicks cancel
                    if self.client is not None:
                        self.client.disconnect()
                    if self.server is not None:
                        self.server.stop()
                    if self.user_data and self.user_data.server_name != '' and self.user_data.is_server:
                        res = requests.delete(f'{BASIC_URL}/delete_server', data=dict(
                            name=self.user_data.server_name))
                    break

                elif event == '-SPG-':
                    player_name = 'Player'
                    if values['name'] != '':
                        player_name = values['name']
                    self.__window.hide()
                    game = Game([player_name])
                    game.start_game()
                    self.__window.un_hide()

                elif event == '-CONNECT-':
                    if self.user_data.is_server:
                        res = requests.delete(f'{BASIC_URL}/delete_server', data=dict(
                            name=self.user_data.server_name))
                    if values['server name'] != '' and values['ip'] != '' and values['port'] != '':
                        if self.server is not None:
                            self.server.stop()
                            self.server = None
                        if self.client:
                            self.client.disconnect()
                        res = requests.put(f'{BASIC_URL}/connect_to_server', data=dict(name=values['server name']))
                        if res.status_code == 200:
                            self.user_data = UserData(values['name'],values['server name'],values['ip'],int(values['port']))
                            self.client = Client(values['ip'], int(values['port']))
                            self.client.connect()
                            ctypes.windll.user32.MessageBoxA(None, bytes(f"You successfully connected to server {self.user_data.server_name}",'utf-8'), b"Info", 0x40 | 0x0)
                        else:
                            ctypes.windll.user32.MessageBoxA(None, bytes(res.text,'utf-8'), b"Warning", 0x30 | 0x0)
                    else:
                        ctypes.windll.user32.MessageBoxA(None, b"Server name, ip and port are required", b"Info", 0x40 | 0x0)

                elif event == '-RUN-SERVER-':
                    if self.client:
                        self.client.disconnect()
                        self.client = None
                    if self.server:
                        self.server.stop()
                        self.server = None
                        res = requests.delete(f'{BASIC_URL}/delete_server', data=dict(
                            name=self.user_data.server_name))
                        if res.status_code != 200:
                            ctypes.windll.user32.MessageBoxA(None, bytes(res.text,'utf-8'), b"Warning", 0x30 | 0x0)

                    if values['server name'] != '' and values['ip'] != '' and values['port'] != '':

                        res = requests.post(f'{BASIC_URL}/register_server',data=dict(
                            name=values['server name'],ip=values['ip'],port=values['port'],
                            players=1,max_players=values['number players']))
                        if res.status_code == 200:
                            self.user_data = UserData(values['name'],values['server name'],values['ip'],int(values['port']),1,int(values['number players']),True)
                            self.server = Server('localhost',int(values['port']))
                            self.server.start()
                            ctypes.windll.user32.MessageBoxA(None, b"Server successfully started", b"Info", 0x40 | 0x0)
                        else:
                            ctypes.windll.user32.MessageBoxA(None, bytes(res.text,'utf-8'), b"Warning", 0x30 | 0x0)
                    else:
                        ctypes.windll.user32.MessageBoxA(None, b"Server name, ip and port are required", b"Info", 0x40 | 0x0)

                elif event == '-UPDATE-SERVERS-TABLE-':
                    self.__load_servers()
                    self.__window['-TABLE-'].update(values=self.__table_data)

                elif event == '-BACK-TO-MENU-':
                    self.__window['-MAIN_MENU-'].update(visible=False)
                    self.__window['-MUPTIPLAYER_MENU-'].update(visible=True)
                    self.__window['-SERVERS_MENU-'].update(visible=False)

                elif event == '-SHOW-SERVERS-':
                    self.__load_servers()
                    self.__window['-TABLE-'].update(values=self.__table_data)
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

            except Exception as e:
                ctypes.windll.user32.MessageBoxA(None, bytes(str(e),'utf-8'), b"Warning", 0x30 | 0x0)

        self.__window.close()

class UserData:
    def __init__(self,player_name='',server_name='',ip='',port=0, players = 0, max_players=0,is_server = False):
        self.player_name = player_name
        self.server_name = server_name
        self.ip = ip
        self.port = port
        self.players = players
        self.max_players = max_players
        self.is_server = is_server