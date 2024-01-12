import math
import random
from collections import defaultdict
from hz_code.hz_constants import *
from hz_code.hz_utils import *
from hz_code.hz_modules import PersonState
from hz_code.hz_qtable import QTable



class UpperConfidenceBounds:
    
    def __init__(self):
        # 遇到指定状态的次数
        self.state_times = defaultdict(lambda: 0)

        # 指定状态下动作被选择的次数
        self.state_action_times = defaultdict(lambda: 0)

    def select(self, person_state: PersonState, actions, qfunction: QTable):
        key_state = person_state.str_repr()

        for action in actions:
            if (key_state, action) not in self.state_action_times.keys():
                self.state_action_times[(key_state, action)] = 1
                self.state_times[key_state] += 1
                return action

        max_actions = []
        max_value = float("-inf")
        for action in actions:
            q = qfunction.get_q_value(key_state, action)
            u = C_PUTS * math.sqrt(math.log(self.state_times[key_state]) / self.state_action_times[(key_state, action)])
            value = q + u
            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions += [action]

        result_action = random.choice(max_actions)

        self.state_action_times[(key_state, result_action)] = self.state_action_times[(key_state, result_action)] + 1
        self.state_times[result_action] += 1

        # LOGGER.info(f"state = {self.state_times}, action_state = {self.state_action_times}")

        return result_action
    


if __name__ == "__main__":
    l1 = [("1", "2"), ("3", "4")]
    print(("1", "2") in l1)

    d1 = defaultdict(lambda: 0)
    print(d1["我"])
