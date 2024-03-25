import utils

class Action():
    def __init__(self, type, skill, amount, description):
        self.type = type
        self.skill = skill
        self.amount = amount
        self.description = description

class TotalAssaultHelper():
    # update_label_signal = pyqtSignal(str)

    def __init__(self, emitter, action_file_paths, update_display, update_progress_bar):
        self.update_progress = update_progress_bar
        self.update_fn = update_display
        self.actions = self.parse_actions_from_file(action_file_paths[0])
        self.action_file_path_index = 0
        self.action_file_paths = action_file_paths
        self.emitter = emitter
        # self.update_label_signal.emit("New label text")
        self.update_fn("国服S16室外寿司 双亚子 2刀IS(感谢千代大佬)", "","#FF0000", "mika")

    def start(self):
        self.progress = 0
        while True:
            text = utils.get_ingame_time_display()

            if (text is None or text == "" or len(text) != 9):
                continue

            duration = utils.formatted_duration_to_ms(text)

            if (duration is None):
                continue

            # if utils.get_seconds_from_ms(text) != utils.get_seconds_from_ms(utils.format_duration_from_four_minutes(duration)):

            # display_text = f"""current: {text}\n下个技能: {next_action.description}, {next_action.type}: {next_action.amount}"""
            action_index = self.get_index(duration)
            
            if action_index == -1:
                continue
            
            next_action = self.actions[action_index]

            # display_text = f"""下个技能: {next_action.description}, {next_action.type}: {next_action.amount}"""
            display_text = f"""下个技能: {next_action.description}"""
            
            # self.update_fn(display_text, str(next_action.amount), next_action.skill)
            
            previous = utils.formatted_duration_to_ms(self.actions[max(0, action_index - 1)].amount)

            time_between_current_and_next = abs(previous - utils.formatted_duration_to_ms(self.actions[action_index].amount)) + 0.001
            time_already = abs(previous - duration)
            progress = (float(time_already) / float(time_between_current_and_next))

            color = utils.progress_colors[int(max(min(progress, 1), 0) * 9)]
            colored_text = utils.format_duration_from_four_minutes(float(time_between_current_and_next) - float(time_already))
# f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{colored_text}"
            # self.update_fn(display_text, colored_text, color, next_action.skill)
            self.emitter.update_display.emit(display_text, colored_text, color, next_action.skill)
            # print(f"{colored_text}".rjust(25, ' '))
            progress = float(time_already) / float(time_between_current_and_next)
            
            self.update_progress(float(time_already) / float(time_between_current_and_next), progress < self.progress)

            self.progress = progress


    def get_index(self, current_duration):
        for i in range(len(self.actions)):
            current_action_timestep = utils.formatted_duration_to_ms(self.actions[i].amount)

            if current_duration > current_action_timestep:
                return min(i, len(self.actions) - 1)

        return -1

    
    def parse_actions_from_file(self, file_path):
        actions = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                # print(line[line.index(parts[3]):])
                action = Action(type=parts[0], skill=parts[1], amount=parts[2], description=parts[3])
                actions.append(action)
        return actions

    def update_actions(self):
        self.action_file_path_index += 1
        self.actions = self.parse_actions_from_file(self.action_file_paths[self.action_file_path_index % len(self.action_file_paths)])