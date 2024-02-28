import time
import pyautogui

class Action():
    def __init__(self, type, amount, description):
        self.type = type
        self.amount = amount
        self.description = description

class TotalAssaultHelper():
    def __init__(self, update_text_display):
        self.update_fn = update_text_display
        self.actions = self.parse_actions_from_file("./rotation.txt")

    def start(self):
        self.has_started = False
        self.start_time = 0 
        self.action_index = 0
        while True:
            if self.round_started():
                self.has_started = True
                self.start_time = time.time() * 1000
                print("has started")
                
            if self.has_started:
                next_action = self.actions[self.action_index]
                duration = (time.time() * 1000) - self.start_time
                display_text = f"""current: {self.format_duration_from_four_minutes(duration)}\n下个技能: {next_action.description}, {next_action.type}: {next_action.amount}"""
                print(self.format_duration_from_four_minutes(duration))
                self.update_fn(display_text)

                self.action_index = self.get_index(duration)

    def get_index(self, current_duration):
        for i in range(len(self.actions)):
            current_action_timestep = (4 * 60 * 1000 - self.formatted_duration_to_ms(self.actions[i].amount))

            if current_action_timestep > (current_duration + int(1.75 * 1000)):
                return min(i, len(self.actions) - 1)

    def round_started(self):
        return (pyautogui.pixel(1087, 512) == (11, 186, 253)) or \
                (pyautogui.pixel(979, 570) == (16, 190, 253))
    
    def formatted_duration_to_ms(self, formatted_duration):
        minutes, seconds, milliseconds = formatted_duration.split(':')

        return int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds) 
    
    def format_duration_from_four_minutes(self, duration_ms):
        four_minutes_in_ms = 4 * 60 * 1000 - int(1.75 * 1000)

        ms = four_minutes_in_ms - duration_ms
        minutes = ms // 60000
        ms = ms % 60000
        seconds = ms // 1000
        milliseconds = ms % 1000

        formatted_duration = f"{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"
        return formatted_duration
    
    def parse_actions_from_file(self, file_path):
        actions = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(' ')
                if len(parts) == 3:  # Ensure the line has exactly 3 components
                    action = Action(type=parts[0], amount=parts[1], description=parts[2])
                    actions.append(action)
        return actions


def start(update_text_display):
    helper = TotalAssaultHelper(update_text_display)
    helper.start()