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
import os

athletes: [Athlete] = []
current_athlete: Athlete
web: WebDriver
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


def log_in_cbf():
    if data[config.DATA_LOGIN_CBF_KEY] == '' or data[config.DATA_PASSWORD_CBF_KEY] == '':
        return

    options = Options()
    # options.set_preference('profile', config.FIREFOX_PROFILE_PATH)
    service = Service(config.GECKODRIVER_PATH)
    service.creation_flags = CREATE_NO_WINDOW
    global web
    web = webdriver.Chrome(service=service, options=options)
    web.get(config.CBF_LOGIN_URL)
    global cbf_tab
    cbf_tab = web.current_window_handle

    time.sleep(2)

    element = web.find_element(By.XPATH, config.LOGIN_EMAIL_XPATH)
    element.send_keys(data[config.DATA_LOGIN_CBF_KEY])
    element = web.find_element(By.XPATH, config.LOGIN_PASSWORD_XPATH)
    element.send_keys(data[config.DATA_PASSWORD_CBF_KEY])
    element = web.find_element(By.XPATH, config.LOGIN_BUTTON_XPATH)
    element.click()

    try:
        WebDriverWait(web, 60).until(lambda x: x.find_element(By.ID, config.CHECK_LOGGED_ID))
    except TimeoutException:
        print('COULD NOT LOG IN')


def start_ui():
    form_paths = data[config.DATA_FORMS_KEY]
    docs_paths = data[config.DATA_DOCS_KEY]

    configs = [
        [
            sg.Text(text='Formulário:', size=10),
            sg.Input(enable_events=True, key='-FORM_PATH-', default_text=form_paths),
            sg.FileBrowse('Procurar...', file_types=(('CSV', '.csv'),))
        ],
        [
            sg.Text(text='Documentos:', size=10),
            sg.Input(enable_events=True, key='-DOCS_PATH-', default_text=docs_paths),
            sg.FolderBrowse('Procurar...')
        ],
        [
            sg.Text(text='Login CBF:', size=10),
            sg.Input(enable_events=True, key='-LOGIN_CBF-', default_text=data.get(config.DATA_LOGIN_CBF_KEY))
        ],
        [
            sg.Text(text='Senha CBF:', size=10),
            sg.Input(enable_events=True, key='-PASSWORD_CBF-', default_text=data.get(config.DATA_PASSWORD_CBF_KEY))
        ],
        sg.HSeparator(),
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

    command_list_column = [
        [sg.Button(button_text='CBF', key='-CBF-', enable_events=True)],
        [sg.Button(button_text='FPF', key='-FPF-', enable_events=True)],
        [sg.Button(button_text='Registrar', key='-REGISTER-', enable_events=True)],
        [sg.Button(button_text='Atualizar documentos', key='-UPDATE_ATHLETE-', enable_events=True)],
        [sg.Button(button_text='Atualizar responsável', key='-UPDATE_GUARDIAN-', enable_events=True)],
        [sg.Button(button_text='Gerar boleto', key='-GENERATE_TICKET-', enable_events=True)],
        [sg.Button(button_text='Gerar contrato', key='-GENERATE_CONTRACT-', enable_events=True)]
    ]

    layout = [
        [
            configs,
            sg.Column(athlete_info_column),
            sg.VSeparator(),
            sg.Column(command_list_column)
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

    if event_name == '-REGISTER-':
        if current_athlete is None:
            return
        try:
            register_athlete()
        except:
            return

    if event_name == '-UPDATE_ATHLETE-':
        if current_athlete is None:
            return
        # try:
        update_athlete()
        # except:
        #     return

    if event_name == '-UPDATE_GUARDIAN-':
        if current_athlete is None:
            return
        try:
            set_athlete_guardian()
        except:
            return

    if event_name == '-GENERATE_TICKET-':
        if current_athlete is None:
            return
        try:
            generate_ticket()
        except:
            return

    if event_name == '-GENERATE_CONTRACT-':
        if current_athlete is None:
            return
        try:
            generate_contract()
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

    if event_name == '-CBF-':
        try:
            log_in_cbf()
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


def get_doc_extension(path):
    pdf_path = path + '.pdf'
    if os.path.isfile(pdf_path):
        return pdf_path
    jpg_path = path + '.jpg'
    if os.path.isfile(jpg_path):
        return jpg_path
    jpeg_path = path + '.jpeg'
    if os.path.isfile(jpeg_path):
        return jpeg_path
    png_path = path + '.png'
    if os.path.isfile(png_path):
        return png_path


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


def register_athlete():
    # REGISTERING ATHLETE PERSONAL DATA
    if web.current_url != config.NEW_ATHLETE_URL:
        web.get(config.NEW_ATHLETE_URL)
        time.sleep(2)

    # fill_field(config.CPF_FIELD_XPATH, current_athlete.cpf)
    fill_field(config.NAME_FIELD_XPATH, current_athlete.name)
    fill_field(config.NICKNAME_FIELD_XPATH, current_athlete.nickname)
    fill_field(config.BIRTHDAY_FIELD_XPATH, current_athlete.birthday)
    select_dropdown_option(config.GENDER_FIELD_XPATH, current_athlete.gender.upper())
    select_dropdown_option(config.CIVIL_STATE_FIELD_XPATH, current_athlete.civilState.replace('(a)', ''))
    select_dropdown_option(config.SCHOLARSHIP_FIELD_XPATH, current_athlete.scholarship.replace('-', '_'))
    fill_field(config.FATHER_NAME_FIELD_XPATH, current_athlete.fatherName)
    fill_field(config.MOTHER_NAME_FIELD_XPATH, current_athlete.motherName)
    select_dropdown_option(config.COUNTRY_BORN_FIELD_XPATH, 'BRASIL')
    select_dropdown_option(config.STATE_BORN_FIELD_XPATH, current_athlete.stateBorn)
    select_dropdown_option(config.CITY_BORN_FIELD_XPATH, current_athlete.cityBorn)
    fill_field(config.EMAIL_FIELD_XPATH, current_athlete.email)
    fill_field(config.CONFIRMATION_EMAIL_FIELD_XPATH, current_athlete.email)
    fill_field(config.CPF_FIELD_XPATH, current_athlete.cpf)

    click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(1)

    # ADDING DOCUMENT FIELDS TO SEND LATER
    select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'RG')
    click_button(config.ADD_DOC_BUTTON_XPATH)
    select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'FOTO')
    click_button(config.ADD_DOC_BUTTON_XPATH)
    select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Certidão de Nascimento')
    click_button(config.ADD_DOC_BUTTON_XPATH)
    select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Comprovante Residência')
    click_button(config.ADD_DOC_BUTTON_XPATH)
    select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Comprovante de Escolaridade')
    click_button(config.ADD_DOC_BUTTON_XPATH)
    if not current_athlete.isMinor:
        select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Certificado de Reservista')
        click_button(config.ADD_DOC_BUTTON_XPATH)

    click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(1)

    # FILLING ADDRESS INFO
    fill_field(config.ADDRESS_STREET_FIELD_XPATH, current_athlete.addressStreet)
    fill_field(config.ADDRESS_NUMBER_FIELD_XPATH, current_athlete.addressNum)
    fill_field(config.ADDRESS_COMPLEMENT_FIELD_XPATH, current_athlete.addressComplement)
    fill_field(config.ADDRESS_NEIGHBOURHOOD_FIELD_XPATH, current_athlete.addressNeighbourhood)
    select_dropdown_option(config.ADDRESS_STATE_DROPDOWN_XPATH, current_athlete.addressState)
    select_dropdown_option(config.ADDRESS_CITY_DROPDOWN_XPATH, unidecode(current_athlete.addressCity))
    fill_field(config.CEP_FIELD_XPATH, current_athlete.cep)

    click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(1)

    # SAVING REGISTRATION
    click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(3)


def update_athlete():
    search_athlete()

    click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
    click_button(config.EDIT_ATHLETE_BUTTON_XPATH)
    time.sleep(2)

    total_docs = 6 if current_athlete.isMinor else 7

    # EDITING ATHLETE FILES
    for i in range(1, total_docs + 1):
        click_button(config.EDIT_NEXT_BUTTON_XPATH)
        doc_name = get_text(config.EDIT_SELECT_DOC_TYPE_XPATH.replace('index', str(i)))
        doc_type = docs.get_doc_type(doc_name)
        click_button(config.EDIT_SELECT_DOC_BUTTON_XPATH.replace('index', str(i)))
        doc_name = get_doc_extension(current_athlete.get_doc_path(doc_type))
        if not os.path.isfile(doc_name):
            print(f'File is missing: {doc_name}')
            return
        file_elem = web.find_elements(By.XPATH, config.EDIT_SET_FILE_FIELD_XPATH)[1]
        file_elem.send_keys(doc_name.replace('/', r'\\'))
        click_button(config.EDIT_SEND_FILE_BUTTON_XPATH)
        time.sleep(1)

    for i in range(2):
        click_button(config.EDIT_NEXT_BUTTON_XPATH)

    clear_fill_field(config.ADDRESS_STREET_FIELD_XPATH, current_athlete.addressStreet)
    clear_fill_field(config.ADDRESS_NEIGHBOURHOOD_FIELD_XPATH, current_athlete.addressNeighbourhood)
    select_dropdown_option(config.ADDRESS_STATE_DROPDOWN_XPATH, current_athlete.addressState)
    select_dropdown_option(config.ADDRESS_CITY_DROPDOWN_XPATH, unidecode(current_athlete.addressCity))

    for i in range(2):
        click_button(config.EDIT_NEXT_BUTTON_XPATH)

    # FILLING ANTHROPOMETRY
    select_dropdown_option_by_index(config.SHIRT_DROPDOWN, 1)
    select_dropdown_option_by_index(config.BLOUSE_DROPDOWN, 1)
    select_dropdown_option_by_index(config.PANTS_DROPDOWN, 1)
    select_dropdown_option_by_index(config.SHORT_DROPDOWN, 1)
    select_dropdown_option_by_index(config.SHOES_DROPDOWN, 1)

    # FINISHING EDITING
    for i in range(3):
        click_button(config.EDIT_NEXT_BUTTON_XPATH)

    time.sleep(2)


def set_athlete_guardian():
    if not current_athlete.isMinor:
        print('O atleta é maior de idade.')
        return

    web.get(config.ATHLETE_LIST_URL)
    time.sleep(2)

    # SEARCHING FOR ATHLETE
    select_dropdown_option(config.CODE_DROPDOWN_XPATH, 'CPF')
    fill_field(config.CPF_SEARCH_FIELD_XPATH, current_athlete.cpf)
    click_button(config.SEARCH_BUTTON_XPATH)
    time.sleep(3)

    click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
    click_button(config.EDIT_GUARDIAN_BUTTON_XPATH)
    time.sleep(2)

    # FILLING GUARDIAN FORM
    fill_field(config.GUARDIAN_CPF_FIELD, str(current_athlete.guardianCpf))
    click_button(config.GUARDIAN_CPF_SEARCH_BUTTON)
    fill_field(config.GUARDIAN_IS_PARENT_DROPDOWN, 'Sim')
    fill_field(config.GUARDIAN_ACTIVE_DROPDOWN, 'Sim')
    send_file_to_field(config.GUARDIAN_DOC_FILE_FIELD, get_doc_extension(current_athlete.doc_guardianCpf))
    time.sleep(1)
    click_button(config.GUARDIAN_SAVE_BUTTON)


def generate_ticket():
    search_athlete()

    click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
    click_button(config.EDIT_CONTRACT_BUTTON_XPATH)
    time.sleep(2)

    # GENERATING TICKET
    click_button(config.CONTRACT_TICKET_BUTTON)
    time.sleep(1)
    select_dropdown_option_by_index(config.CONTRACT_TICKET_TYPE_DROPDOWN, 1)
    click_button(config.CONTRACT_FINALIZE_BUTTON)

    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)


def generate_contract():
    if web.current_url != config.ATHLETE_CONTRACT_URL:
        web.get(config.ATHLETE_LIST_URL)
        time.sleep(2)

        # SEARCHING FOR ATHLETE
        select_dropdown_option(config.CODE_DROPDOWN_XPATH, 'CPF')
        fill_field(config.CPF_SEARCH_FIELD_XPATH, current_athlete.cpf)
        click_button(config.SEARCH_BUTTON_XPATH)
        time.sleep(3)

        click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
        click_button(config.EDIT_CONTRACT_BUTTON_XPATH)
        time.sleep(2)

    # GENERATING CONTRACT
    click_button(config.CONTRACT_NEW_BUTTON)
    time.sleep(1)
    fill_field(config.CONTRACT_DAYS_FIELD, '730')
    fill_field(config.CONTRACT_START_DATE_FIELD, '26/03/2023')
    click_button(config.CONTRACT_NEXT_1_BUTTON)

    select_dropdown_option_by_index(config.CONTRACT_DOCTOR_DROPDOWN, 1)
    click_button(config.CONTRACT_EXAM_BUTTON)
    click_button(config.CONTRACT_EXAM2_BUTTON)
    click_button(config.CONTRACT_EXAM3_BUTTON)
    fill_field(config.CONTRACT_EXAM_DATE_FIELD, '25/03/2023')
    click_button(config.CONTRACT_NEXT_2_BUTTON)
    click_button(config.CONTRACT_SAVE_BUTTON)


def search_athlete():
    if web.current_url != config.ATHLETE_LIST_URL:
        web.get(config.ATHLETE_LIST_URL)
        time.sleep(2)

    # SEARCHING FOR ATHLETE
    select_dropdown_option(config.CODE_DROPDOWN_XPATH, 'CPF')
    fill_field(config.CPF_SEARCH_FIELD_XPATH, current_athlete.cpf)
    click_button(config.SEARCH_BUTTON_XPATH)
    time.sleep(3)


if __name__ == '__main__':
    setup()

    while True:
        event, values = window.read()

        if event == 'OK' or event == sg.WIN_CLOSED:
            break
        manage_event(event, values)

    window.close()
    web.quit()
