import json
from collections import defaultdict



class QTable():
    
    def __init__(self, default = 0.0, character = "基层河长"):
        self.qtable = defaultdict(lambda: default)

        file_path = "../data/courses_values_20240108100829.json"
        with open(file_path, "r", encoding = "utf-8") as f:
            data_dict = json.load(f)
        
        self.data_preprocess(data_dict[character])

    def update(self, state, action, delta):
        self.qtable[(state, action)] = self.qtable[(state, action)] + delta

    def get_q_value(self, state, action):
        return self.qtable[(state, action)]

    def get_max_q(self, state, actions):
        arg_max_q = None
        max_q = float("-inf")
        for action in actions:
            value = self.get_q_value(state, action)
            if max_q < value:
                arg_max_q = action
                max_q = value
        return (arg_max_q, max_q)

    def data_preprocess(self, data_dict):
        result_qtable = {}
        for ability, ability_dict in data_dict.items():
            for tag, tag_dict in ability_dict.items():
                state = f"{ability}-{tag}"
                for course, course_val in tag_dict.items():
                    action = course
                    result_qtable[(state, action)] = course_val
        
        self.qtable = result_qtable



if __name__ == "__main__":
    qfunction = QTable()
    qfunction.update("习惯-履职趋势", "《河长巡河切莫“打卡式”》", 1.3)
    value = qfunction.get_q_value("习惯-履职趋势", "《河长巡河切莫“打卡式”》")
    print(value)