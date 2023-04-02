from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from subprocess import CREATE_NO_WINDOW
from unidecode import unidecode
import web_methods as wm
from athlete import Athlete

import docs
import pyautogui
import config
import time
import os

web: WebDriver
current_athlete: Athlete
tab: str
data: dict


def log_in():
    if data[config.DATA_LOGIN_CBF_KEY] == '' or data[config.DATA_PASSWORD_CBF_KEY] == '':
        return

    options = Options()
    # options.set_preference('profile', config.FIREFOX_PROFILE_PATH)
    service = Service(config.GECKODRIVER_PATH)
    service.creation_flags = CREATE_NO_WINDOW
    global web
    web = webdriver.Chrome(service=service, options=options)
    web.get(config.CBF_LOGIN_URL)
    global tab
    tab = web.current_window_handle

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


def register_athlete():
    # REGISTERING ATHLETE PERSONAL DATA
    if web.current_url != config.NEW_ATHLETE_URL:
        web.get(config.NEW_ATHLETE_URL)
        time.sleep(2)

    # fill_field(config.CPF_FIELD_XPATH, current_athlete.cpf)
    wm.fill_field(config.NAME_FIELD_XPATH, current_athlete.name)
    wm.fill_field(config.NICKNAME_FIELD_XPATH, current_athlete.nickname)
    wm.fill_field(config.BIRTHDAY_FIELD_XPATH, current_athlete.birthday)
    wm.select_dropdown_option(config.GENDER_FIELD_XPATH, current_athlete.gender.upper())
    wm.select_dropdown_option(config.CIVIL_STATE_FIELD_XPATH, current_athlete.civilState.replace('(a)', ''))
    wm.select_dropdown_option(config.SCHOLARSHIP_FIELD_XPATH, current_athlete.scholarship.replace('-', '_'))
    wm.fill_field(config.FATHER_NAME_FIELD_XPATH, current_athlete.fatherName)
    wm.fill_field(config.MOTHER_NAME_FIELD_XPATH, current_athlete.motherName)
    wm.select_dropdown_option(config.COUNTRY_BORN_FIELD_XPATH, 'BRASIL')
    wm.select_dropdown_option(config.STATE_BORN_FIELD_XPATH, current_athlete.stateBorn)
    wm.select_dropdown_option(config.CITY_BORN_FIELD_XPATH, current_athlete.cityBorn)
    wm.fill_field(config.EMAIL_FIELD_XPATH, current_athlete.email)
    wm.fill_field(config.CONFIRMATION_EMAIL_FIELD_XPATH, current_athlete.email)
    wm.fill_field(config.CPF_FIELD_XPATH, current_athlete.cpf)

    wm.click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(1)

    # ADDING DOCUMENT FIELDS TO SEND LATER
    wm.select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'RG')
    wm.click_button(config.ADD_DOC_BUTTON_XPATH)
    wm.select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'FOTO')
    wm.click_button(config.ADD_DOC_BUTTON_XPATH)
    wm.select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Certidão de Nascimento')
    wm.click_button(config.ADD_DOC_BUTTON_XPATH)
    wm.select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Comprovante Residência')
    wm.click_button(config.ADD_DOC_BUTTON_XPATH)
    wm.select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Comprovante de Escolaridade')
    wm.click_button(config.ADD_DOC_BUTTON_XPATH)
    if not current_athlete.isMinor:
        wm.select_dropdown_option(config.DOC_TYPE_DROPDOWN_XPATH, 'Certificado de Reservista')
        wm.click_button(config.ADD_DOC_BUTTON_XPATH)

    wm.click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(1)

    # FILLING ADDRESS INFO
    wm.fill_field(config.ADDRESS_STREET_FIELD_XPATH, current_athlete.addressStreet)
    wm.fill_field(config.ADDRESS_NUMBER_FIELD_XPATH, current_athlete.addressNum)
    wm.fill_field(config.ADDRESS_COMPLEMENT_FIELD_XPATH, current_athlete.addressComplement)
    wm.fill_field(config.ADDRESS_NEIGHBOURHOOD_FIELD_XPATH, current_athlete.addressNeighbourhood)
    wm.select_dropdown_option(config.ADDRESS_STATE_DROPDOWN_XPATH, current_athlete.addressState)
    wm.select_dropdown_option(config.ADDRESS_CITY_DROPDOWN_XPATH, unidecode(current_athlete.addressCity))
    wm.fill_field(config.CEP_FIELD_XPATH, current_athlete.cep)

    wm.click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(1)

    # SAVING REGISTRATION
    wm.click_button(config.NEXT_BUTTON_XPATH)
    time.sleep(3)


def update_athlete():
    search_athlete()

    wm.click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
    wm.click_button(config.EDIT_ATHLETE_BUTTON_XPATH)
    time.sleep(2)

    total_docs = 6 if current_athlete.isMinor else 7

    # EDITING ATHLETE FILES
    for i in range(1, total_docs + 1):
        wm.click_button(config.EDIT_NEXT_BUTTON_XPATH)
        doc_name = wm.get_text(config.EDIT_SELECT_DOC_TYPE_XPATH.replace('index', str(i)))
        doc_type = docs.get_doc_type(doc_name)
        wm.click_button(config.EDIT_SELECT_DOC_BUTTON_XPATH.replace('index', str(i)))
        doc_name = docs.get_doc_extension(current_athlete.get_doc_path(doc_type))
        if not os.path.isfile(doc_name):
            print(f'File is missing: {doc_name}')
            return
        file_elem = web.find_elements(By.XPATH, config.EDIT_SET_FILE_FIELD_XPATH)[1]
        file_elem.send_keys(doc_name.replace('/', r'\\'))
        wm.click_button(config.EDIT_SEND_FILE_BUTTON_XPATH)
        time.sleep(1)

    for i in range(2):
        wm.click_button(config.EDIT_NEXT_BUTTON_XPATH)

    wm.clear_fill_field(config.ADDRESS_STREET_FIELD_XPATH, current_athlete.addressStreet)
    wm.clear_fill_field(config.ADDRESS_NEIGHBOURHOOD_FIELD_XPATH, current_athlete.addressNeighbourhood)
    wm.select_dropdown_option(config.ADDRESS_STATE_DROPDOWN_XPATH, current_athlete.addressState)
    wm.select_dropdown_option(config.ADDRESS_CITY_DROPDOWN_XPATH, unidecode(current_athlete.addressCity))

    for i in range(2):
        wm.click_button(config.EDIT_NEXT_BUTTON_XPATH)

    # FILLING ANTHROPOMETRY
    wm.select_dropdown_option_by_index(config.SHIRT_DROPDOWN, 1)
    wm.select_dropdown_option_by_index(config.BLOUSE_DROPDOWN, 1)
    wm.select_dropdown_option_by_index(config.PANTS_DROPDOWN, 1)
    wm.select_dropdown_option_by_index(config.SHORT_DROPDOWN, 1)
    wm.select_dropdown_option_by_index(config.SHOES_DROPDOWN, 1)

    # FINISHING EDITING
    for i in range(3):
        wm.click_button(config.EDIT_NEXT_BUTTON_XPATH)

    time.sleep(2)


def set_athlete_guardian():
    if not current_athlete.isMinor:
        print('O atleta é maior de idade.')
        return

    search_athlete()

    wm.click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
    wm.click_button(config.EDIT_GUARDIAN_BUTTON_XPATH)
    time.sleep(2)

    # FILLING GUARDIAN FORM
    wm.fill_field(config.GUARDIAN_CPF_FIELD, str(current_athlete.guardianCpf))
    wm.click_button(config.GUARDIAN_CPF_SEARCH_BUTTON)
    wm.fill_field(config.GUARDIAN_IS_PARENT_DROPDOWN, 'Sim')
    wm.fill_field(config.GUARDIAN_ACTIVE_DROPDOWN, 'Sim')
    wm.send_file_to_field(config.GUARDIAN_DOC_FILE_FIELD, docs.get_doc_extension(current_athlete.doc_guardianCpf))
    time.sleep(1)
    wm.click_button(config.GUARDIAN_SAVE_BUTTON)


def generate_ticket():
    search_athlete()

    wm.click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
    wm.click_button(config.EDIT_CONTRACT_BUTTON_XPATH)
    time.sleep(2)

    # GENERATING TICKET
    wm.click_button(config.CONTRACT_TICKET_BUTTON)
    time.sleep(1)
    wm.select_dropdown_option_by_index(config.CONTRACT_TICKET_TYPE_DROPDOWN, 1)
    wm.click_button(config.CONTRACT_FINALIZE_BUTTON)

    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)


def generate_contract():
    if web.current_url != config.ATHLETE_CONTRACT_URL:
        search_athlete()

    wm.click_button(config.ACTIONS_ATHLETE_BUTTON_XPATH)
    wm.click_button(config.EDIT_CONTRACT_BUTTON_XPATH)
    time.sleep(2)

    # GENERATING CONTRACT
    wm.click_button(config.CONTRACT_NEW_BUTTON)
    time.sleep(1)
    wm.fill_field(config.CONTRACT_DAYS_FIELD, '730')
    wm.fill_field(config.CONTRACT_START_DATE_FIELD, '26/03/2023')
    wm.click_button(config.CONTRACT_NEXT_1_BUTTON)

    wm.select_dropdown_option_by_index(config.CONTRACT_DOCTOR_DROPDOWN, 1)
    wm.click_button(config.CONTRACT_EXAM_BUTTON)
    wm.click_button(config.CONTRACT_EXAM2_BUTTON)
    wm.click_button(config.CONTRACT_EXAM3_BUTTON)
    wm.fill_field(config.CONTRACT_EXAM_DATE_FIELD, '25/03/2023')
    wm.click_button(config.CONTRACT_NEXT_2_BUTTON)
    wm.click_button(config.CONTRACT_SAVE_BUTTON)


def search_athlete():
    if web.current_url != config.ATHLETE_LIST_URL:
        web.get(config.ATHLETE_LIST_URL)
        time.sleep(2)

    # SEARCHING FOR ATHLETE
    wm.select_dropdown_option(config.CODE_DROPDOWN_XPATH, 'CPF')
    wm.fill_field(config.CPF_SEARCH_FIELD_XPATH, current_athlete.cpf)
    wm.click_button(config.SEARCH_BUTTON_XPATH)
    time.sleep(3)
