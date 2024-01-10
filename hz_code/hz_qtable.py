from collections import defaultdict



class QTable:
    
    def __init__(self):
        self.qtable = defaultdict(lambda: 0.0)


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



if __name__ == "__main__":
    qfunction = QTable()
    qfunction.update("习惯-履职趋势", "《河长巡河切莫“打卡式”》", 1.3)
    value = qfunction.get_q_value("习惯-履职趋势", "《河长巡河切莫“打卡式”》")
    print(value)