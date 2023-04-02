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
from athlete import Athlete

import docs
import PySimpleGUI as sg
import unicodedata
import pyautogui
import config
import json
import pandas as pd
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


def get_data():
    global data
    if not os.path.isfile('data.json'):
        data = {
            'formPath': '',
            'docsPath': '',
            'loginCBF': '',
            'passwordCBF': '',
            'loginFPF': '',
            'passwordFPF': ''
        }
        save_data()
    else:
        with open('data.json', 'r') as dt:
            data = json.load(dt)


def save_data():
    with open('data.json', 'w') as dt:
        json.dump(data, dt)


def start_ui():
    form_paths = data[config.DATA_FORMS_KEY]
    docs_paths = data[config.DATA_DOCS_KEY]

    configs = [
        [sg.VStretch()],
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
        [sg.VStretch()]
    ]

    athlete_info_column = [
        [
            sg.Text(text="ATLETA:"),
            sg.Combo(values=names, key='-GET_ATHLETE_DATA-', enable_events=True, expand_x=True)
        ],
        [
            sg.Text(text=f'NOME:', size=5),
            sg.InputText(
                key='-ATHLETE_NAME-',
                use_readonly_for_disable=True,
                disabled=True,
                disabled_readonly_background_color='#64778d',
                border_width=0)
        ],
        [
            sg.Text(text=f'CPF:', size=5),
            sg.InputText(
                key='-ATHLETE_CPF-',
                use_readonly_for_disable=True,
                disabled=True,
                disabled_readonly_background_color='#64778d',
                border_width=0)
        ],
        [
            sg.Text(text=f'EMAIL:', size=5),
            sg.InputText(
                key='-ATHLETE_EMAIL-',
                use_readonly_for_disable=True,
                disabled=True,
                disabled_readonly_background_color='#64778d',
                border_width=0)
        ],
        [
            sg.Push(),
            sg.Image(key='-ATHLETE_PHOTO-', size=(50, 50,)),
            sg.Push()
        ]
    ]

    cbf_command_list = [
        [sg.Button(button_text='CBF', key='-CBF-', enable_events=True)],
        [sg.Button(button_text='Registrar', key='-REGISTER-', enable_events=True)],
        [sg.Button(button_text='Atualizar documentos', key='-UPDATE_ATHLETE-', enable_events=True)],
        [sg.Button(button_text='Atualizar responsável', key='-UPDATE_GUARDIAN-', enable_events=True)],
        [sg.Button(button_text='Gerar boleto', key='-GENERATE_TICKET-', enable_events=True)],
        [sg.Button(button_text='Gerar contrato', key='-GENERATE_CONTRACT-', enable_events=True)]
    ]

    fpf_command_list = [
        [sg.Button(button_text='FPF', key='-FPF-', enable_events=True)],
        [sg.Button(button_text='Registrar', key='-REGISTER-', enable_events=True)],
        [sg.Button(button_text='Atualizar documentos', key='-UPDATE_ATHLETE-', enable_events=True)],
        [sg.Button(button_text='Atualizar responsável', key='-UPDATE_GUARDIAN-', enable_events=True)],
        [sg.Button(button_text='Gerar boleto', key='-GENERATE_TICKET-', enable_events=True)],
        [sg.Button(button_text='Gerar contrato', key='-GENERATE_CONTRACT-', enable_events=True)]
    ]

    layout = [
        [
            sg.TabGroup([
                [
                    sg.Tab('Atletas',
                           [[sg.Column(athlete_info_column), sg.VSeparator(), sg.Column(cbf_command_list)]]),
                    sg.Tab('Configurações', configs)
                ]
            ], tab_background_color='#516173')
        ]
    ]

    global window
    window = sg.Window(title="Dados do Atleta - Aguaí", layout=layout, icon=config.ICON_BASE64)


def manage_event(event_name: str, values: dict):
    if event_name == '-GET_ATHLETE_DATA-':
        set_current_athlete(values['-GET_ATHLETE_DATA-'])
        window['-ATHLETE_NAME-'].update(current_athlete.name)
        window['-ATHLETE_CPF-'].update(current_athlete.cpf)
        window['-ATHLETE_EMAIL-'].update(current_athlete.email)
        if os.path.isfile(current_athlete.doc_photo + '.png'):
            png = Image.open(current_athlete.doc_photo + '.png')
            png = png.convert('RGB')
            png.save(current_athlete.doc_photo + '.jpg')
            os.remove(current_athlete.doc_photo + '.png')
        img = Image.open(current_athlete.doc_photo + '.jpg')
        img.thumbnail((200, 200), Image.LANCZOS)
        window['-ATHLETE_PHOTO-'].update(data=ImageTk.PhotoImage(img))
        return

    if event_name == '-MENU-':
        window.layout()

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
        # try:
        cbf.update_athlete()
        # except:
        #     return

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
        data[config.DATA_FORMS_KEY] = values['-FORM_PATH-']
        save_data()
        get_athlete_data()
        return

    if event_name == '-DOCS_PATH-':
        data[config.DATA_DOCS_KEY] = values['-DOCS_PATH-']
        save_data()
        get_athlete_data()
        return

    if event_name == '-LOGIN_CBF-':
        data[config.DATA_LOGIN_CBF_KEY] = values['-LOGIN_CBF-']
        save_data()
        return

    if event_name == '-PASSWORD_CBF-':
        data[config.DATA_PASSWORD_CBF_KEY] = values['-PASSWORD_CBF-']
        save_data()
        return

    if event_name == '-LOGIN_FPF-':
        data[config.DATA_LOGIN_FPF_KEY] = values['-LOGIN_FPF-']
        save_data()
        return

    if event_name == '-PASSWORD_FPF-':
        data[config.DATA_PASSWORD_FPF_KEY] = values['-PASSWORD_FPF-']
        save_data()
        return

    if event_name == '-CBF-':
        try:
            cbf.log_in()
        except:
            return

    if event_name == '-FPF-':
        try:
            fpf.web = web
            fpf.log_in()
        except:
            return


def fill_field(xpath, info):
    try:
        field = WebDriverWait(web, 10).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        print('COULD NOT FIND FIELD')
    else:
        field.click()
        field.send_keys(info)


def clear_fill_field(xpath, info):
    try:
        field = WebDriverWait(web, 10).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        print('COULD NOT FIND FIELD')
    else:
        field.click()
        field.clear()
        field.send_keys(info)


def get_text(xpath):
    try:
        text = WebDriverWait(web, 10).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        print('COULD NOT FIND TEXT')
    else:
        return text.text


def send_file_field_execute_script_on_id(element_id, file):
    try:
        web.execute_script(f"document.getElementById('{element_id}').value = '{file}'")
    except TimeoutException:
        print('COULD NOT UPLOAD FILE')


def send_file_to_field(xpath, file):
    try:
        field = WebDriverWait(web, 10).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        print('COULD NOT FIND ELEMENT')
    else:
        field.send_keys(file.replace('/', r'\\'))


def click_button(xpath):
    try:
        button = WebDriverWait(web, 10).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        print('COULD NOT FIND FIELD')
    else:
        button.click()


def set_current_athlete(name: str):
    found = False
    for athlete in athletes:
        if athlete.name == name:
            global current_athlete
            current_athlete = athlete
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


def select_dropdown_option(xpath, option_name):
    try:
        dropdown = WebDriverWait(web, 10).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        print('COULD NOT FIND DROPDOWN')
    else:
        select = Select(dropdown)
        options_list = []
        for option in select.options:
            options_list.append(option.text)
        best_match = most_similar_string(options_list, option_name)
        select.select_by_visible_text(best_match)


def select_dropdown_option_by_index(xpath, index):
    try:
        dropdown = WebDriverWait(web, 10).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        print('COULD NOT FIND DROPDOWN')
    else:
        select = Select(dropdown)
        select.select_by_index(index)


def get_athlete_data():
    if data[config.DATA_FORMS_KEY] == '':
        return
    if data[config.DATA_DOCS_KEY] == '':
        return

    data_frame = pd.read_csv(data[config.DATA_FORMS_KEY], sep=',', header=0, dtype=str)
    athletes_data = data_frame.to_dict(orient='records')

    global names
    for row in athletes_data:
        new_athlete = Athlete(row, data)
        athletes.append(new_athlete)
        names.append(new_athlete.name)

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
