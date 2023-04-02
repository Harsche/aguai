from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from main import most_similar_string

web: WebDriver


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


def wait_for_element(xpath, max_time):
    try:
        element = WebDriverWait(web, max_time).until(lambda x: x.find_element(By.XPATH, xpath))
        return element
    except TimeoutException:
        print('COULD NOT FIND ELEMENT IN TIME')



def change_to_tab(tab):
    for tab_handle in web.window_handles:
        if tab_handle == tab:
            web.switch_to.window(tab_handle)
            break
