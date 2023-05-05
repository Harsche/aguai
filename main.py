from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from subprocess import CREATE_NO_WINDOW
from unidecode import unidecode
from PIL import Image, ImageTk

import web_methods
from athlete import Athlete

import docs
import PySimpleGUI as sg
import unicodedata
import subprocess
import pyautogui
import config
import json
import pandas2 as pd
import time
import fpf
import cbf
import os

athletes: [Athlete] = []
current_athlete: Athlete
web: WebDriver = None
cbf_tab = None
window: sg.Window = None
endProgram = False
data = {}
names: [str] = []


def setup():
    get_data()
    get_athlete_data()
    athletes.sort(key=lambda athlete: athlete.name)
    start_ui()


def start_web():
    global web
    if web is not None:
        return

    options = Options()
    # options.set_preference('profile', config.FIREFOX_PROFILE_PATH)
    print(data[config.DATA_GECKODRIVER_KEY])
    driver_path = data[config.DATA_GECKODRIVER_KEY]
    service = Service(f'{driver_path}')
    service.creation_flags = CREATE_NO_WINDOW
    web = webdriver.Firefox(service=service, options=options)
    cbf.web = web
    fpf.web = web
    web_methods.web = web


def get_data():
    global data
    if not os.path.isfile('data.json'):
        data = {
            'formPath': '',
            'docsPath': '',
            'geckodriverPath': '',
            'loginCBF': '',
            'passwordCBF': '',
            'loginFPF': '',
            'passwordFPF': ''
        }
        save_data()
    else:
        with open('data.json', 'r') as dt:
            data = json.load(dt)

    cbf.data = data
    fpf.data = data


def save_data():
    with open('data.json', 'w') as dt:
        json.dump(data, dt)


def start_ui():
    form_paths = data.get(config.DATA_FORMS_KEY)
    docs_paths = data.get(config.DATA_DOCS_KEY)
    geckodriver_paths = data.get(config.DATA_GECKODRIVER_KEY)

    configs = [
        [
            sg.Push(),
            sg.Text(text='Formulário:', size=10),
            sg.Input(enable_events=True, key='-FORM_PATH-', default_text=form_paths),
            sg.FileBrowse('Procurar...', file_types=(('CSV', '.csv'),)),
            sg.Push()
        ],
        [
            sg.Push(),
            sg.Text(text='Documentos:', size=10),
            sg.Input(enable_events=True, key='-DOCS_PATH-', default_text=docs_paths),
            sg.FolderBrowse('Procurar...'),
            sg.Push()
        ],
        [
            sg.Push(),
            sg.Text(text='Geckodriver:', size=10),
            sg.Input(enable_events=True, key='-GECKODRIVER_PATH-', default_text=geckodriver_paths),
            sg.FileBrowse('Procurar...', file_types=(('EXE', '.exe'),)),
            sg.Push()
        ],
        [
            sg.HSeparator(pad=((10, 10), (20, 20)))
        ],
        [
            sg.Column(
                [
                    [
                        sg.Text(text='Login CBF:', size=9),
                        sg.Input(enable_events=True, key='-LOGIN_CBF-',
                                 default_text=data.get(config.DATA_LOGIN_CBF_KEY),
                                 size=25)
                    ],
                    [
                        sg.Text(text='Senha CBF:', size=9),
                        sg.Input(enable_events=True, key='-PASSWORD_CBF-',
                                 default_text=data.get(config.DATA_PASSWORD_CBF_KEY),
                                 size=25)
                    ],
                ]
            ),
            sg.VSeparator(),
            sg.Column(
                [
                    [
                        sg.Text(text='Login FPF:', size=9),
                        sg.Input(enable_events=True, key='-LOGIN_FPF-',
                                 default_text=data.get(config.DATA_LOGIN_FPF_KEY),
                                 size=25)
                    ],
                    [
                        sg.Text(text='Senha FPF:', size=9),
                        sg.Input(enable_events=True, key='-PASSWORD_FPF-',
                                 default_text=data.get(config.DATA_PASSWORD_FPF_KEY),
                                 size=25)
                    ],
                ]
            ),
        ],
        [
            sg.Push(),
            sg.Button('Atualizar Dados', key='-UPDATE_DATA-', pad=10),
            sg.Push()
        ]
    ]

    athlete_info_column = [
        [
            sg.Text(text="ATLETA:"),
            sg.Combo(values=names, key='-GET_ATHLETE_DATA-', enable_events=True, expand_x=True)
        ],
        [
            sg.HSeparator(pad=((30, 30), (30, 15)))
        ],
        [
            sg.Text(text=f'NOME:', size=7),
            sg.InputText(
                key='-ATHLETE_NAME-',
                use_readonly_for_disable=True,
                disabled=True,
                disabled_readonly_background_color='#64778d',
                border_width=0)
        ],
        [
            sg.Text(text=f'CPF:', size=7),
            sg.InputText(
                key='-ATHLETE_CPF-',
                use_readonly_for_disable=True,
                disabled=True,
                disabled_readonly_background_color='#64778d',
                border_width=0)
        ],
        [
            sg.Text(text=f'NASCIM.:', size=7),
            sg.InputText(
                key='-ATHLETE_BIRTHDAY-',
                use_readonly_for_disable=True,
                disabled=True,
                disabled_readonly_background_color='#64778d',
                border_width=0)
        ],
        [
            sg.Text(text=f'EMAIL:', size=7),
            sg.InputText(
                key='-ATHLETE_EMAIL-',
                use_readonly_for_disable=True,
                disabled=True,
                disabled_readonly_background_color='#64778d',
                border_width=0)
        ],
        [
            sg.VStretch(),
            sg.Push(),
            sg.Image(key='-ATHLETE_PHOTO-', size=(50, 50,)),
            sg.Push(),
            sg.VStretch()
        ]
    ]

    cbf_command_list = [
        [sg.Push(), sg.Text('CBF', font='bold'), sg.Push()],
        [sg.Push(), sg.Button(button_text='Login', key='-CBF-', enable_events=True, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Registrar', key='-REGISTER-', enable_events=True, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Atualizar documentos', key='-UPDATE_ATHLETE-', enable_events=True, size=20),
         sg.Push()],
        [sg.Push(),
         sg.Button(button_text='Atualizar responsável', key='-UPDATE_GUARDIAN-', enable_events=True, size=20),
         sg.Push()],
        [sg.Push(), sg.Button(button_text='Gerar boleto', key='-GENERATE_TICKET-', enable_events=True, size=20),
         sg.Push()],
        [sg.Push(), sg.Button(button_text='Gerar contrato', key='-GENERATE_CONTRACT-', enable_events=True, size=20),
         sg.Push()]
    ]

    fpf_command_list = [
        [sg.Push(), sg.Text('FBF', font='bold'), sg.Push()],
        [sg.Push(), sg.Button(button_text='Login', key='-FPF-', enable_events=True, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Registrar', key='-FPF_REGISTER-', enable_events=True, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Documentos', key='-FPF_DOCS-', enable_events=True, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Contrato', key='-FPF_CONTRACT-', enable_events=True, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Formulário', key='-FPF_FORM-', enable_events=True, size=20), sg.Push()]
    ]

    commands = cbf_command_list + [[sg.HSeparator(pad=10)]] + fpf_command_list

    layout = [
        [
            sg.TabGroup([
                [
                    sg.Tab('Atletas',
                           [[sg.Column(athlete_info_column, vertical_alignment='top', pad=10), sg.VSeparator(),
                             sg.Column(commands, pad=10)]]),
                    sg.Tab('Configurações', [[sg.Column(configs, pad=15)]])
                ]
            ], tab_background_color='#516173')
        ]
    ]

    global window
    with open('icon.txt', 'r') as dt:
        icon = dt.read()
        icon = bytes(icon, 'ascii')
    window = sg.Window(title="Dados do Atleta - Aguaí", layout=layout, icon=icon)


def manage_event(event_name: str, values: dict):
    if event_name == '-GET_ATHLETE_DATA-':
        set_current_athlete(values['-GET_ATHLETE_DATA-'])
        window['-ATHLETE_NAME-'].update(current_athlete.name)
        window['-ATHLETE_CPF-'].update(current_athlete.cpf)
        window['-ATHLETE_EMAIL-'].update(current_athlete.email)
        window['-ATHLETE_BIRTHDAY-'].update(current_athlete.birthday)
        current_athlete.compress_files()
        img = Image.open(current_athlete.doc_photo)
        img.thumbnail((250, 250), Image.LANCZOS)
        window['-ATHLETE_PHOTO-'].update(data=ImageTk.PhotoImage(img))
        return

    if event_name == '-MENU-':
        window.layout()

        return

    if event_name == '-UPDATE_DATA-':
        get_athlete_data()

        return

    if event_name == '-REGISTER-':
        if current_athlete is None:
            return
        try:
            cbf.register_athlete()
        except:
            return

    if event_name == '-UPDATE_ATHLETE-':
        if current_athlete is None:
            return
        try:
            cbf.update_athlete()
        except:
            return

    if event_name == '-UPDATE_GUARDIAN-':
        if current_athlete is None:
            return
        try:
            cbf.set_athlete_guardian()
        except:
            return

    if event_name == '-GENERATE_TICKET-':
        if current_athlete is None:
            return
        try:
            cbf.generate_ticket()
        except:
            return

    if event_name == '-GENERATE_CONTRACT-':
        if current_athlete is None:
            return
        try:
            cbf.generate_contract()
        except:
            return

    if event_name == '-FORM_PATH-':
        try:
            data[config.DATA_FORMS_KEY] = values['-FORM_PATH-']
            save_data()
            get_athlete_data()
        except:
            return

    if event_name == '-GECKODRIVER_PATH-':
        try:
            data[config.DATA_GECKODRIVER_KEY] = values['-GECKODRIVER_PATH-']
            save_data()
        except:
            return

    if event_name == '-DOCS_PATH-':
        try:
            data[config.DATA_DOCS_KEY] = values['-DOCS_PATH-']
            save_data()
            get_athlete_data()
        except:
            return

    if event_name == '-LOGIN_CBF-':
        try:
            data[config.DATA_LOGIN_CBF_KEY] = values['-LOGIN_CBF-']
            save_data()
        except:
            return

    if event_name == '-PASSWORD_CBF-':
        try:
            data[config.DATA_PASSWORD_CBF_KEY] = values['-PASSWORD_CBF-']
            save_data()
        except:
            return

    if event_name == '-LOGIN_FPF-':
        try:
            data[config.DATA_LOGIN_FPF_KEY] = values['-LOGIN_FPF-']
            save_data()
        except:
            return

    if event_name == '-PASSWORD_FPF-':
        try:
            data[config.DATA_PASSWORD_FPF_KEY] = values['-PASSWORD_FPF-']
            save_data()
        except:
            return

    if event_name == '-FPF_REGISTER-':
        try:
            fpf.register_athlete()
        except:
            return

    if event_name == '-FPF_DOCS-':
        try:
            fpf.add_docs()
        except:
            return

    if event_name == '-FPF_CONTRACT-':
        try:
            fpf.generate_contract()
        except:
            return

    if event_name == '-FPF_FORM-':
        try:
            fpf.generate_form()
        except:
            return

    if event_name == '-CBF-':
        # try:
        start_web()
        cbf.log_in()
        # except:
        #     return

    if event_name == '-FPF-':
        # try:
        start_web()
        fpf.log_in()
        # except:
        #     return


def set_current_athlete(name: str):
    found = False
    for athlete in athletes:
        if athlete.name == name:
            global current_athlete
            current_athlete = athlete
            fpf.current_athlete = current_athlete
            cbf.current_athlete = current_athlete
            found = True
    if not found:
        print("Could not find athlete.")


def most_similar_string(strings, word):
    # Normalize the word by removing accents
    word_normalized = unicodedata.normalize('NFD', word).encode('ascii', 'ignore').decode('utf-8').lower()

    # Initialize variables to keep track of the best match
    best_match = None
    best_similarity = 0

    # Iterate over the strings and compare them to the normalized word
    for string in strings:
        # Normalize the string by removing accents
        string_normalized = unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode('utf-8').lower()

        # Compute the similarity between the normalized string and word
        similarity = sum(1 for c1, c2 in zip(string_normalized, word_normalized) if c1 == c2)

        # If the similarity is higher than the current best match, update the best match
        if similarity > best_similarity:
            best_match = string
            best_similarity = similarity

    # Return the best match
    return best_match


def get_athlete_data():
    if data[config.DATA_FORMS_KEY] == '':
        return
    if data[config.DATA_DOCS_KEY] == '':
        return
    if not os.path.isfile(data[config.DATA_FORMS_KEY]):
        return

    athletes_data = pd.read_csv(data[config.DATA_FORMS_KEY])

    global names
    names.clear()
    athletes.clear()
    for row in athletes_data:
        new_athlete = Athlete(row, data)
        athletes.append(new_athlete)
        names.append(new_athlete.name)

    names.sort()

    if window:
        window['-GET_ATHLETE_DATA-'].update(values=names)

if __name__ == '__main__':
    setup()

    while True:
        event, values = window.read()

        if event == 'OK' or event == sg.WIN_CLOSED:
            break
        manage_event(event, values)

    window.close()
    if web is not None:
        web.quit()
