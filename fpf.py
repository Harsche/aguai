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
import web_methods as wm
import unicodedata
import pyautogui
import config
import json
import pandas as pd
import time
import os

web: WebDriver
current_athlete: Athlete
tab: str
data: dict


def log_in():
    if data[config.DATA_LOGIN_FPF_KEY] == '' or data[config.DATA_PASSWORD_FPF_KEY] == '':
        return

    global web
    global tab
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


def register_athlete():
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
    wm.select_dropdown_option(config.FPF_BIRTH_CITY_DROPDOWN, current_athlete.cityBorn)
    wm.fill_field(config.FPF_RG_INPUT_FIELD, current_athlete.rg)

    org_dropdown: Select = wm.wait_for_element(2)
    for opt in org_dropdown.options:
        if current_athlete.stateBorn not in opt:
            continue
        org_dropdown.select_by_visible_text(opt)
        break

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
    wm.select_dropdown_option(config.ADDRESS_STATE_DROPDOWN_XPATH, current_athlete.addressState)
    wm.select_dropdown_option(config.ADDRESS_CITY_DROPDOWN_XPATH, current_athlete.addressCity)
