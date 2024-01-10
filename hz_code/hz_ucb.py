import math
import random
from collections import defaultdict
from hz_constants import *
from hz_utils import *


def fetch_key_state_action(action):
    segments = action.split("||")
    assert len(segments) == 3

    ability = segments[0]
    tag = segments[1]
    key_action = segments[2]
    key_state = f"{ability}-{tag}"

    return key_state, key_action


class UpperConfidenceBounds:
    
    def __init__(self):
        # 遇到指定状态的次数
        self.state_times = defaultdict(lambda: 0)

        # 指定状态下动作被选择的次数
        self.state_action_selected_times = defaultdict(lambda: 0)

    def select(self, person_state, actions, qfunction):

        for action in actions:
            key_state, key_action = fetch_key_state_action(action)
        
            if (key_state, key_action) not in self.state_action_selected_times.keys():
                self.state_action_selected_times[(key_state, key_action)] = 1
                self.state_times[key_state] += 1
                return action

        max_actions = []
        max_value = float("-inf")
        for action in actions:
            key_state, key_action = fetch_key_state_action(action)

            q = qfunction.get_q_value(key_state, key_action)
            u = C_PUTS * math.sqrt(math.log(self.state_times[key_state]) / self.state_action_selected_times[(key_state, key_action)])
            value = q + u
            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions += [action]

        result_action = random.choice(max_actions)

        r_key_state, r_key_action = fetch_key_state_action(result_action)

        self.state_action_selected_times[(r_key_state, r_key_action)] = self.state_action_selected_times[(r_key_state, r_key_action)] + 1
        self.state_times[r_key_state] += 1

        LOGGER.info(f"state = {self.state_times}, action_state = {self.state_action_selected_times}")

        return result_action
    


if __name__ == "__main__":
    l1 = [("1", "2"), ("3", "4")]
    print(("1", "2") in l1)

    d1 = defaultdict(lambda: 0)
    print(d1["我"])
