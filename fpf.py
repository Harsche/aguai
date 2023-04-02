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
import os

web: WebDriver
tab: str
data: dict


def log_in():
    global web
    global tab
    if not tab:
        web.switch_to.new_window('tab')
        tab = web.current_window_handle

    if web.current_url != config.FPF_LOGIN_URL:
        web.get(config.FPF_LOGIN_URL)

