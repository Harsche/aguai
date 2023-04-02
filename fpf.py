from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from athlete import Athlete
import docs
import web_methods as wm
import config
import time
import os

web: WebDriver
current_athlete: Athlete
tab: str = ''
data: dict


def log_in():
    if data[config.DATA_LOGIN_FPF_KEY] == '' or data[config.DATA_PASSWORD_FPF_KEY] == '':
        return

    global web, tab
    if not tab:
        web.switch_to.new_window('tab')
        tab = web.current_window_handle
    else:
        wm.change_to_tab(tab)
        return

    if web.current_url != config.FPF_LOGIN_URL:
        web.get(config.FPF_LOGIN_URL)

    wm.fill_field(config.FPF_LOGIN_PATH, data[config.DATA_LOGIN_FPF_KEY])
    wm.fill_field(config.FPF_PASSWORD_PATH, data[config.DATA_PASSWORD_FPF_KEY])
    wm.click_button(config.FPF_LOGIN_BUTTON_PATH)
    wm.wait_for_element(config.FPF_HOMEPAGE, 10)
    wm.click_button(config.FPF_AUTH_DROPDOWN)
    wm.click_button(config.FPF_AUTH_REGISTER)
    time.sleep(0.2)
    tab = wm.get_next_tab(tab)
    wm.change_to_tab(tab)
    # close_tab = ActionChains(web)
    # close_tab.key_down(Keys.CONTROL).send_keys('W').key_up(Keys.CONTROL).perform()
    # time.sleep(0.2)


    # new_tab = web.current_window_handle
    # wm.change_to_tab(tab)
    # web.refresh()
    # wm.change_to_tab(new_tab)
    # web.close()
    # if web.current_window_handle != tab:
    #     wm.change_to_tab(tab)


def register_athlete():
    if current_athlete is None:
        return
    wm.change_to_tab(tab)

    # Type CPF
    web.get(config.FPF_NEW_ATHLETE_URL)
    wm.click_button(config.FPF_NEW_ATHLETE_BUTTON)
    wm.fill_field(config.FPF_NEW_ATHLETE_CPF_INPUT_FIELD, current_athlete.cpf)
    wm.click_button(config.FPF_NEW_ATHLETE_GO_BUTTON)

    # Fill form
    wm.fill_field(config.FPF_NAME_INPUT_FIELD, current_athlete.name)
    wm.fill_field(config.FPF_NICKNAME_INPUT_FIELD, current_athlete.nickname)
    wm.fill_field(config.FPF_FATHER_NAME_INPUT_FIELD, current_athlete.fatherName)
    wm.fill_field(config.FPF_MOTHER_NAME_INPUT_FIELD, current_athlete.motherName)
    wm.fill_field(config.FPF_BIRTHDAY_INPUT_FIELD, current_athlete.birthday)
    wm.select_dropdown_option(config.FPF_GENDER_DROPDOWN, current_athlete.gender)
    wm.select_dropdown_option(config.FPF_BIRTH_STATE_DROPDOWN, current_athlete.stateBorn)
    time.sleep(0.5)
    wm.select_dropdown_option(config.FPF_BIRTH_CITY_DROPDOWN, current_athlete.cityBorn)
    wm.fill_field(config.FPF_RG_INPUT_FIELD, current_athlete.rg)

    wm.select_dropdown_option(config.FPF_RG_ORG_DROPDOWN, f'SSP - {current_athlete.stateBorn}')
    # org_dropdown = Select(wm.wait_for_element(config.FPF_RG_ORG_DROPDOWN, 2))
    # for opt in org_dropdown.options:
    #     if current_athlete.stateBorn not in opt.text:
    #         continue
    #     org_dropdown.select_by_visible_text(opt)
    #     break

    wm.fill_field(config.FPF_BIRTH_CERT_NUM_INPUT_FIELD, '000')
    wm.fill_field(config.FPF_BIRTH_CERT_PAGE_INPUT_FIELD, '000')
    wm.fill_field(config.FPF_BIRTH_CERT_BOOK_INPUT_FIELD, '000')
    wm.fill_field(config.FPF_MILITARY_CERT_INPUT_FIELD, '000')
    wm.fill_field(config.FPF_CTPS_INPUT_FIELD, '000')
    wm.fill_field(config.FPF_GRADE_INPUT_FIELD, '000')

    wm.fill_field(config.FPF_CEP_INPUT_FIELD, current_athlete.cep)
    wm.fill_field(config.FPF_STREET_INPUT_FIELD, current_athlete.addressStreet)
    wm.fill_field(config.FPF_HOUSE_NUM_INPUT_FIELD, current_athlete.addressNum)
    wm.fill_field(config.FPF_COMPLEMENT_INPUT_FIELD, current_athlete.addressComplement)
    wm.fill_field(config.FPF_NEIGHBOURHOOD_INPUT_FIELD, current_athlete.addressNeighbourhood)
    wm.select_dropdown_option(config.FPF_STATE_DROPDOWN, current_athlete.addressState)
    time.sleep(0.5)
    wm.select_dropdown_option(config.FPF_CITY_DROPDOWN, current_athlete.addressCity)


def add_docs():
    if current_athlete is None:
        return
    wm.change_to_tab(tab)

    # Go to profile
    web.get(config.FPF_NEW_ATHLETE_URL)
    wm.fill_field(config.FPF_SEARCH_CPF_INPUT_FIELD, current_athlete.cpf)  # current_athlete.cpf)
    wm.click_button(config.FPF_SEARCH_CPF_BUTTON)
    time.sleep(0.5)
    wm.click_button(config.FPF_SEARCH_EDIT_BUTTON)
    wm.click_button(config.FPF_UPDATE_ATHLETE_DOCS_BUTTON)

    # Add documents
    path = docs.get_doc_extension(current_athlete.doc_photo)
    if os.path.isfile(path):
        wm.send_file_to_field(config.FPF_PHOTO_INPUT_FILE, path)
        wm.click_button(config.FPF_PHOTO_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_rg)
    if os.path.isfile(path):
        wm.send_file_to_field(config.FPF_RG_INPUT_FILE, path)
        wm.click_button(config.FPF_RG_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_cpf)
    if os.path.isfile(path):
        wm.send_file_to_field(config.FPF_CPF_INPUT_FILE, path)
        wm.click_button(config.FPF_CPF_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_guardianCpf)
    if current_athlete.isMinor and os.path.isfile(path):
        wm.send_file_to_field(config.FPF_GUARDIAN_DOC_INPUT_FILE, path)
        wm.click_button(config.FPF_GUARDIAN_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_medicalExam)
    if os.path.isfile(path):
        wm.send_file_to_field(config.FPF_HEALTH_EXAM_INPUT_FILE, path)
        wm.click_button(config.FPF_HEALTH_EXAM_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_birthCertificate)
    if os.path.isfile(path):
        wm.send_file_to_field(config.FPF_BIRTH_CERT_INPUT_FILE, path)
        wm.click_button(config.FPF_BIRTH_CERT_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_militaryService)
    if not current_athlete.isMinor and os.path.isfile(path):
        wm.send_file_to_field(config.FPF_MILITARY_SERV_INPUT_FILE, path)
        wm.click_button(config.FPF_MILITARY_SERV_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_scholarship)
    if os.path.isfile(path):
        wm.send_file_to_field(config.FPF_SCHOLARSHIP_INPUT_FILE, path)
        wm.click_button(config.FPF_SCHOLARSHIP_SEND_BUTTON)

    path = docs.get_doc_extension(current_athlete.doc_residenceCertificate_)
    if os.path.isfile(path):
        wm.send_file_to_field(config.FPF_ADDRESS_INPUT_FILE, path)
        wm.click_button(config.FPF_ADDRESS_SEND_BUTTON)


def generate_contract():
    if current_athlete is None:
        return
    wm.change_to_tab(tab)

    web.get(config.FPF_ATHLETE_REGISTER_URL)
    wm.fill_field(config.FPF_CONTRACT_CPF_INPUT_FIELD, current_athlete.cpf)  # current_athlete.cpf)
    wm.click_button(config.FPF_CONTRACT_CPF_SEARCH_BUTTON)
    wm.select_dropdown_option(config.FPF_CONTRACT_TYPE_DROPDOWN, 'Inscrição Atleta Amador')
    wm.click_button(config.FPF_CONTRACT_SEND_BUTTON)
    wm.click_button(config.FPF_CONTRACT_FINALIZE_BUTTON)
    wm.wait_for_element(config.FPF_CONTRACT_FINALIZE_CONFIRM, 10)
    wm.click_button(config.FPF_FORM_SELECT_ATHLETE)
    wm.click_button(config.FPF_FORM_EDIT)
    wm.click_button(config.FPF_GENERATE_FORM_BUTTON)

    generate_form()


def generate_form():
    if current_athlete is None:
        return
    wm.change_to_tab(tab)

    wm.fill_field(config.FPF_DOCTOR_NAME_INPUT_FIELD, 'Geraldo Fornari Junior')
    wm.fill_field(config.FPF_DOCTOR_CRM_INPUT_FIELD, '44121')
    wm.fill_field(config.FPF_DOCTOR_CPF_INPUT_FIELD, '28613503691')
    wm.click_button(config.FPF_GENERATE_FORM_BUTTON)
