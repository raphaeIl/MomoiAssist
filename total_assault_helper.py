import time
import pyautogui
import utils

class Action():
    def __init__(self, type, amount, description):
        self.type = type
        self.amount = amount
        self.description = description

class TotalAssaultHelper():
    def __init__(self, update_text_display, update_progress_bar):
        self.update_progress = update_progress_bar
        self.update_fn = update_text_display
        self.actions = self.parse_actions_from_file("./res/rotation.txt")

    def start(self):
        self.action_index = 0

        while True:
            next_action = self.actions[self.action_index]
            text = utils.get_ingame_time_display()
            duration = utils.formatted_duration_to_ms(text)

            if (text is None or duration is None):
                self.update_fn("Idle")
                continue
            
            # if utils.get_seconds_from_ms(text) != utils.get_seconds_from_ms(utils.format_duration_from_four_minutes(duration)):

            display_text = f"""下个技能: {next_action.description}, {next_action.type}: {next_action.amount}"""
            # display_text = f"""current: {text}\n下个技能: {next_action.description}, {next_action.type}: {next_action.amount}"""
            self.update_fn(display_text)
            self.action_index = self.get_index(duration)

            previous = utils.formatted_duration_to_ms(self.actions[max(0, self.action_index - 1)].amount)
            time_between_current_and_next = abs(previous - utils.formatted_duration_to_ms(self.actions[self.action_index].amount)) + 0.001
            time_already = abs(previous - duration)
        
            self.update_progress(float(time_already) / float(time_between_current_and_next))

    def get_index(self, current_duration):
        for i in range(len(self.actions)):
            current_action_timestep = (utils.formatted_duration_to_ms(self.actions[i].amount))

            if current_action_timestep < current_duration:
                return min(i, len(self.actions) - 1)

    
    def parse_actions_from_file(self, file_path):
        actions = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(' ')
                if len(parts) == 3:  # Ensure the line has exactly 3 components
                    action = Action(type=parts[0], amount=parts[1], description=parts[2])
                    actions.append(action)
        return actions


def start(update_text_display, update_progress_bar):
    helper = TotalAssaultHelper(update_text_display, update_progress_bar)
    helper.start()