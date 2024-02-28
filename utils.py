import pytesseract
import pyautogui
import re

pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def round_started():
        return pyautogui.pixel(807, 89) == (214, 134, 7)

def get_ingame_time_display():
    return screenshot_and_recognize_text(1604, 34, 115, 45)

def screenshot_and_recognize_text(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    text = pytesseract.image_to_string(screenshot, config='--psm 6')
    time_format_regex = r'\d{2}:\d{2}'
    matches = re.findall(time_format_regex, text)
    
    return matches[0] + ":000" if matches else None

def formatted_duration_to_ms(formatted_duration):
    minutes, seconds, milliseconds = formatted_duration.split(':')

    return int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds) 

def get_seconds_from_ms(formatted_duration):
    minutes, seconds, milliseconds = str(formatted_duration).split(':')

    return seconds

def format_duration_from_four_minutes(duration_ms):
    four_minutes_in_ms = 4 * 60 * 1000

    # ms = four_minutes_in_ms - duration_ms
    ms = duration_ms
    minutes = ms // 60000
    ms = ms % 60000
    seconds = ms // 1000
    milliseconds = ms % 1000

    formatted_duration = f"{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"
    return formatted_duration