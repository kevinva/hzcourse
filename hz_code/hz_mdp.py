import json
from hz_constants import *



class PersonState:

    def __init__(self, 
                 will_tags = [], 
                 will_score = 100.0, 
                 manage_tags = [], 
                 manage_score = 100.0, 
                 knowledge_tags = [], 
                 knowldege_score = 100.0,
                 habit_tags = [],
                 habit_score = 100.0,
                 skill_tags = [],
                 skill_score = 100.0,
                 level = None):
        
        self.will_score = will_score
        self.manage_score = manage_score
        self.knowledge_score = knowldege_score
        self.habit_score = habit_score
        self.skill_score = skill_score
        self.will_tags = will_tags
        self.manage_tags = manage_tags
        self.knowledge_tags = knowledge_tags
        self.habit_tags = habit_tags
        self.skill_tags = skill_tags
        self.level = level

    def __str__(self):
        return f"manage = {self.manage_score}, knowledge = {self.knowledge_score}, skill = {self.skill_score}, habit = {self.habit_score}, will = {self.will_score}"

    def __eq__(self, other):
        if isinstance(other, PersonState):
            pass

        return False


class HZCourseWorld:

    def __init__(self, person_state: PersonState = None):
        self.all_course_info = {}

        file_path = "../data/courses_values_20240108100829.json"
        with open(file_path, "r", encoding = "utf-8") as f:
            data_dict = json.load(f)

        self.init_person_state = person_state
        self.data_preprocess(data_dict[person_state.level])


    def get_actions(self, state):
        key_list = []
        result_list = []
        
        if len(self.init_person_state.manage_tags) > 0:
            manage_key_list = [f"管理-{tag}" for tag in self.init_person_state.manage_tags]
            key_list.extend(manage_key_list)

        if len(self.init_person_state.knowledge_tags) > 0:
            knowledge_key_list = [f"知识-{tag}" for tag in self.init_person_state.knowledge_tags]
            key_list.extend(knowledge_key_list)

        if len(self.init_person_state.skill_tags) > 0:
            skill_key_list = [f"技能-{tag}" for tag in self.init_person_state.skill_tags]
            key_list.extend(skill_key_list)

        if len(self.init_person_state.habit_tags) > 0:
            habit_key_list = [f"习惯-{tag}" for tag in self.init_person_state.habit_tags]
            key_list.extend(habit_key_list)

        if len(self.init_person_state.will_tags) > 0:
            will_key_list = [f"意愿-{tag}" for tag in self.init_person_state.will_tags]
            key_list.extend(will_key_list)

        for key in key_list:
            course_list = self.all_course_info.get(key, [])
            if len(course_list) > 0:
                result_list.extend(course_list)

        return course_list
        

    def is_terminal(self, state):
        # 可以忽略，或者按推送的期数作为终止条件
        return False
    
    def execute(self, state, action):
        pass

    def get_discount_factor(self):
        return DISCOUNT_FACTOR

    def get_transitions(self, state, action):
        pass

    def get_initial_state(self):
        return self.init_person_state
    
    def data_preprocess(self, data_dict):
        result_dict = {}
        for ability, ability_dict in data_dict.items():
            for tag, tag_dict in ability_dict.items():
                state = f"{ability}-{tag}"
                actions = list(tag_dict.keys())
                result_dict[state] = actions
        
        self.course_info = result_dict


if __name__ == "__main__":
    # state = PersonState(level = "区级河长")
    # mdp = HZCourseWorld(state)
    # print(mdp.course_info)

    l1 = ["l1", "我", "问答法"]
    l2 = ["l1", "我"]
    print(l1 == l2)