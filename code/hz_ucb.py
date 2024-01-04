import math
import random
from hz_constants import *


class UpperConfidenceBounds:
    def __init__(self):
        self.total = 0

        # 动作被选择的次数
        self.times_selected = {}

    def select(self, state, actions, qfunction):

        for action in actions:
            if action not in self.times_selected.keys():
                self.times_selected[action] = 1
                self.total += 1
                return action

        max_actions = []
        max_value = float("-inf")
        for action in actions:
            value = qfunction.get_q_value(state, action) + C_PUTS * math.sqrt(
                math.log(self.total) / self.times_selected[action]
            )
            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions += [action]

        result_action = random.choice(max_actions)

        self.times_selected[result_action] = self.times_selected[result_action] + 1
        self.total += 1

        return result_action
    


if __name__ == "__main__":
    pass
