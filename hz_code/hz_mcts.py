import math
import time
import random
from collections import defaultdict

from hz_code.hz_utils import LOGGER
from hz_code.hz_constants import *
from hz_code.hz_modules import *
from hz_code.hz_mdp import *
from hz_code.hz_ucb import *
from hz_code.hz_qtable import *



class Node:

    # 记录节点唯一id，以区分节点对应状态
    next_node_id = 0

    # 记录节点对应状态被访问次数
    visits = defaultdict(lambda: 0)

    def __init__(self, mdp: HZCourseWorld, parent, person_state: PersonState, qfunction: QTable, q_algorithm: UpperConfidenceBounds, reward = 0.0, action = None):
        self.mdp = mdp
        self.parent = parent

        # 个人状态：标签、各维度能力分数
        self.person_state = person_state 

        # 状态-动作价值函数
        self.qfunction = qfunction

        # 状态-动作评估算法，如UCB
        self.q_algorithm = q_algorithm

        # 节点立即奖励，用于树的回溯更新
        self.reward = reward

        # 导出该节点的动作，即对应课程
        self.action = action

        # 子节点
        self.children = {}

        self.nid = Node.next_node_id
        Node.next_node_id += 1


    def is_fully_expanded(self):
        valid_actions = self.mdp.get_actions(self.person_state)
        if len(valid_actions) == len(self.children):
            return True
        else:
            return False


    def select(self):
        # 该节点要完全展开完，才会选其子节点
        if not self.is_fully_expanded() or self.mdp.is_terminal(self.person_state):
            return self
        else:
            actions = list(self.children.keys())
            action = self.q_algorithm.select(self.person_state, actions, self.qfunction)
            
            LOGGER.info(f"select child: action = {action}, from state = {str(self.person_state)}")
            return self.get_outcome_child(action).select()


    def expand(self):
        if not self.mdp.is_terminal(self.person_state):
            # 选一个从来没执行过的动作来expand，即每次只展开一个子节点
            actions = set(self.mdp.get_actions(self.person_state)) - set(self.children.keys())
            if len(actions) == 0:
                return self
            
            action = random.choice(list(actions))
            self.children[action] = []
            return self.get_outcome_child(action)
        
        return self


    def back_propagate(self, reward, child):
        action = child.action   # 触发这个child节点的action
        key_state = self.person_state.str_repr()

        Node.visits[key_state] = Node.visits[key_state] + 1
        Node.visits[(key_state, action)] = Node.visits[(key_state, action)] + 1

        q_value = self.qfunction.get_q_value(key_state, action)
        delta = (1.0 / Node.visits[(key_state, action)]) * (reward - q_value)
        self.qfunction.update(key_state, action, delta)

        if self.parent != None:
            self.parent.back_propagate(self.reward + reward, self)


    """ 返回节点的最大价值 """

    def get_value(self):
        actions = self.mdp.get_actions(self.person_state)
        max_q_value = self.qfunction.get_max_q(self.person_state.str_repr(), actions)
        return max_q_value


    """ 访问状态的次数 """

    def get_visits(self):
        return Node.visits[self.person_state.str_repr()]
    

    """ 模拟动作执行，并返回相应的子节点 """

    def get_outcome_child(self, action):
        (next_state, reward) = self.mdp.execute(self.person_state, action)

        for (child, _) in self.children[action]:
            if next_state == child.person_state:
                return child
        
        new_child = Node(
            self.mdp, self, next_state, self.qfunction, self.q_algorithm, reward, action
        )

        probability = 0.0  # hoho_todo：转移概率暂不用
        for (outcome, probability) in self.mdp.get_transitions(self.person_state, action):
            if outcome == next_state:
                self.children[action] += [(new_child, probability)]
                return new_child


class MCTS:

    def __init__(self, mdp: HZCourseWorld, qfunction: QTable, q_algorithm: UpperConfidenceBounds):
        self.mdp = mdp
        self.qfunction = qfunction
        self.q_algorithm = q_algorithm


    def mcts(self, timeout = 1, root_node = None):
        if root_node is None:
            root_node = self.create_root_node()

        start_time = time.time()
        current_time = time.time()
        while current_time < start_time + timeout:
            selected_node = root_node.select()
            if not self.mdp.is_terminal(selected_node.person_state):
                child = selected_node.expand()
                reward = self.simulate(child)
                selected_node.back_propagate(reward, child)

            current_time = time.time()

        return root_node


    def create_root_node(self):
        return Node(
            self.mdp, None, self.mdp.get_initial_state(), self.qfunction, self.q_algorithm
        )



    """ 随机选择一个动作 """

    def choose(self, state: PersonState):
        return random.choice(self.mdp.get_actions(state))


    """ 模拟游走直到终止状态 """

    def simulate(self, node: Node):
        # simulate的意义只在于获得cumulative_reward?! 
        ### 注意：simulate过程中不需要expand
              
        state = node.person_state
        cumulative_reward = 0.0
        depth = 0
        while not self.mdp.is_terminal(state):
            action = self.choose(state)
            (next_state, reward) = self.mdp.execute(state, action)
            cumulative_reward += pow(DISCOUNT_FACTOR, depth) * reward
            depth += 1

            state = next_state

        LOGGER.info(f"simulate end: depth = {depth}, cumulative_reward = {cumulative_reward}")

        return cumulative_reward
    

def visual_mcts_tree(root: Node):
    result_dict = {}
    result_dict["root"] = {}
    data, children = visual_mcts_tree(root)
    result_dict["root"] = {"data": data, "children": children}

    return result_dict


if __name__ == "__main__":
    # state1 = PersonState()
    # state2 = PersonState()

    # my_dict = {}
    # my_dict[state1] = 1
    # my_dict[state2] = 2
    # print(my_dict[state1])
    # my_dict[state1] = my_dict[state1] + 2
    # print(my_dict[state1])

    l1 = ["1", "2", "3"]
    l2 = ["1"]
    print(set(l1) - set(l2))