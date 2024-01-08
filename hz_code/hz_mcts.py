import math
import time
import random
from collections import defaultdict

from hz_utils import LOGGER
from hz_mdp import *


class Node:

    # Record a unique node id to distinguish duplicated states
    next_node_id = 0

    # Records the number of times states have been visited
    visits = defaultdict(lambda: 0)

    def __init__(self, mdp, parent, person_state, qfunction, q_algorithm, reward = 0.0, action = None):
        self.mdp = mdp
        self.parent = parent

        # 个人状态：标签、各维度能力分数
        self.person_state = person_state 

        # 状态-动作价值函数
        self.qfunction = qfunction

        # 状态-动作评估算法，如UCB
        self.q_algorithm = q_algorithm

        # The immediate reward received for reaching this state, used for backpropagation
        self.reward = reward

        # 导出该节点的动作，即对应课程名称
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
            
            LOGGER.info(f"select child: action = {action}， from state = {str(self.person_state)}")
            return self.get_outcome_child(action).select()


    def expand(self):
        if not self.mdp.is_terminal(self.person_state):
            # Randomly select an unexpanded action to expand
            # 其实就是选一个从来没执行过的动作来expand，即每次只展开一个子节点
            actions = self.mdp.get_actions(self.person_state) - self.children.keys()
            action = random.choice(list(actions))

            self.children[action] = []
            return self.get_outcome_child(action)
        
        return self


    def back_propagate(self, reward, child):
        action = child.action   # 触发这个child节点的action

        Node.visits[self.state] = Node.visits[self.state] + 1
        Node.visits[(self.state, action)] = Node.visits[(self.state, action)] + 1

        q_value = self.qfunction.get_q_value(self.state, action)
        delta = (1 / (Node.visits[(self.state, action)])) * (
            reward - self.qfunction.get_q_value(self.state, action)
        )
        self.qfunction.update(self.state, action, delta)

        if self.parent != None:
            self.parent.back_propagate(self.reward + reward, self)


    """ Return the value of this node """

    def get_value(self):
        (_, max_q_value) = self.qfunction.get_max_q(
            self.state, self.mdp.get_actions(self.state)
        )
        return max_q_value


    """ Get the number of visits to this state """

    def get_visits(self):
        return Node.visits[self.state]
    

    """ Simulate the outcome of an action, and return the child node """

    def get_outcome_child(self, action):
        # Choose one outcome based on transition probabilities
        (next_state, reward) = self.mdp.execute(self.state, action)

        # Find the corresponding state and return if this already exists
        for (child, _) in self.children[action]:
            if next_state == child.state:
                return child

        # This outcome has not occured from this state-action pair previously
        new_child = Node(
            self.mdp, self, next_state, self.qfunction, self.q_algorithm, reward, action
        )

        # Find the probability of this outcome (only possible for model-based) for visualising tree
        probability = 0.0
        for (outcome, probability) in self.mdp.get_transitions(self.state, action):
            if outcome == next_state:
                self.children[action] += [(new_child, probability)]
                return new_child


class MCTS:
    def __init__(self, mdp, qfunction, q_algorithm):
        self.mdp = mdp
        self.qfunction = qfunction
        self.q_algorithm = q_algorithm


    def mcts(self, timeout=1, root_node=None):
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


    """ Create a root node representing an initial state """

    def create_root_node(self):
        return Node(
            self.mdp, None, self.mdp.get_initial_state(), self.qfunction, self.q_algorithm
        )


    """ Choose a random action. Heustics can be used here to improve simulations. """


    def choose(self, state):
        return random.choice(self.mdp.get_actions(state))


    """ Simulate until a terminal state """

    def simulate(self, node):
        # simulate的意义只在于获得cumulative_reward?! 
        ### 注意： simulate过程中不需要expand
        print(f"simulate: start at = {node.state}")
              
        state = node.state
        cumulative_reward = 0.0
        depth = 0
        while not self.mdp.is_terminal(state):
            # Choose an action to execute
            action = self.choose(state)

            # Execute the action
            (next_state, reward) = self.mdp.execute(state, action)

            # Discount the reward
            cumulative_reward += pow(self.mdp.get_discount_factor(), depth) * reward
            depth += 1

            state = next_state

        print(f"simulate end: depth = {depth}, cumulative_reward = {cumulative_reward}")
        print("===========================================\n\n")

        return cumulative_reward

if __name__ == "__main__":
    state1 = PersonState()
    state2 = PersonState()

    my_dict = {}
    my_dict[state1] = 1
    my_dict[state2] = 2
    print(my_dict[state1])
    my_dict[state1] = my_dict[state1] + 2
    print(my_dict[state1])