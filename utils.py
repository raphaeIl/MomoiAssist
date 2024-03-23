import pytesseract
import pyautogui
import re
from PyQt5.QtGui import QColor
pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'

rainbow_colors = [QColor(255, 0, 0, 120),
 QColor(255, 14, 0, 120),
 QColor(255, 29, 0, 120),
 QColor(255, 44, 0, 120),
 QColor(255, 59, 0, 120),
 QColor(255, 74, 0, 120),
 QColor(255, 89, 0, 120),
 QColor(255, 104, 0, 120),
 QColor(255, 119, 0, 120),
 QColor(255, 133, 0, 120),
 QColor(255, 149, 0, 120),
 QColor(255, 165, 0, 120),
 QColor(255, 179, 0, 120),
 QColor(255, 195, 0, 120),
 QColor(255, 209, 0, 120),
 QColor(255, 224, 0, 120),
 QColor(255, 240, 0, 120),
 QColor(255, 254, 0, 120),
 QColor(255, 255, 0, 120),
 QColor(255, 255, 0, 120),
 QColor(255, 255, 0, 120),
 QColor(255, 255, 0, 120),
 QColor(255, 255, 0, 120),
 QColor(255, 255, 0, 120),
 QColor(255, 255, 0, 120),
 QColor(240, 255, 0, 120),
 QColor(210, 255, 0, 120),
 QColor(180, 255, 0, 120),
 QColor(149, 255, 0, 120),
 QColor(119, 255, 0, 120),
 QColor(89, 255, 0, 120),
 QColor(59, 255, 0, 120),
 QColor(29, 255, 0, 120),
 QColor(0, 255, 0, 120),
 QColor(0, 255, 29, 120),
 QColor(0, 255, 59, 120),
 QColor(0, 240, 89, 120),
 QColor(0, 210, 119, 120),
 QColor(0, 180, 149, 120),
 QColor(0, 149, 180, 120),
 QColor(0, 119, 210, 120),
 QColor(0, 89, 240, 120),
 QColor(0, 59, 255, 120),
 QColor(0, 29, 255, 120),
 QColor(0, 0, 255, 120),
 QColor(7, 0, 255, 120),
 QColor(16, 0, 255, 120),
 QColor(26, 0, 255, 120),
 QColor(35, 0, 255, 120),
 QColor(44, 0, 255, 120),
 QColor(52, 0, 241, 120),
 QColor(61, 0, 227, 120),
 QColor(70, 0, 213, 120),
 QColor(79, 0, 197, 120),
 QColor(88, 0, 183, 120),
 QColor(97, 0, 169, 120),
 QColor(105, 0, 178, 120),
 QColor(114, 0, 187, 120),
 QColor(122, 0, 197, 120),
 QColor(131, 0, 206, 120),
 QColor(140, 0, 215, 120),
 QColor(148, 0, 226, 120),
 QColor(157, 0, 235, 120),
 QColor(166, 0, 244, 120),
 QColor(174, 0, 254, 120),
 QColor(183, 0, 255, 120),
 QColor(192, 0, 255, 120),
 QColor(204, 0, 248, 120),
 QColor(217, 0, 223, 120),
 QColor(230, 0, 198, 120),
 QColor(241, 0, 174, 120),
 QColor(254, 0, 149, 120),
 QColor(255, 0, 123, 120),
 QColor(255, 0, 98, 120),
 QColor(255, 0, 74, 120),
 QColor(255, 0, 49, 120),
 QColor(255, 0, 24, 120),
 QColor(255, 0, 0, 120)]
def round_started():
        return pyautogui.pixel(807, 89) == (214, 134, 7)

def get_ingame_time_display():
    # return screenshot_and_recognize_text(1604, 34, 115, 45)
    return screenshot_and_recognize_text(1604, 34, 200, 45)

def screenshot_and_recognize_text(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    text = pytesseract.image_to_string(screenshot, config='--psm 6')
    time_format_regex = r'\d{2}:\d{2}.\d{3}'
    matches = re.findall(time_format_regex, text)

    return matches[0] if matches else None


def formatted_duration_to_ms(formatted_duration):
    try:
        minutes, seconds_milliseconds = formatted_duration.split(':')
        seconds, milliseconds = seconds_milliseconds.split('.')
        return int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds) 
    except:
        return None
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