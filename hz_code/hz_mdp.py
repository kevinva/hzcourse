import json
import copy
from hz_code.hz_constants import *
from hz_code.hz_modules import PersonState



class HZCourseWorld:

    def __init__(self, person_state: PersonState = None, file_path = None):
        self.course_info = {}

        with open(file_path, "r", encoding = "utf-8") as f:
            data_dict = json.load(f)

        self.init_person_state = person_state
        self.data_preprocess(data_dict[person_state.level])


    def get_actions(self, state: PersonState):
        result_list = []
        
        # 注意：在不同能力下，课程可能会重复！！！

        result_list = []

        for tag in state.manage_tags:
            course_dict = self.course_info["管理"].get(tag, {})
            course_list = [f"管理||{tag}||{course}" for course in course_dict.keys()]
            if len(course_list) > 0:
                result_list.extend(course_list)

        for tag in state.knowledge_tags:
            course_dict = self.course_info["知识"].get(tag, {})
            course_list = [f"知识||{tag}||{course}" for course in course_dict.keys()]
            if len(course_list) > 0:
                result_list.extend(course_list)

        for tag in state.skill_tags:
            course_dict = self.course_info["技能"].get(tag, {})
            course_list = [f"技能||{tag}||{course}" for course in course_dict.keys()]
            if len(course_list) > 0:
                result_list.extend(course_list)

        for tag in state.will_tags:
            course_dict = self.course_info["意愿"].get(tag, {})
            course_list = [f"意愿||{tag}||{course}" for course in course_dict.keys()]
            if len(course_list) > 0:
                result_list.extend(course_list)

        for tag in state.habit_tags:
            course_dict = self.course_info["习惯"].get(tag, {})
            course_list = [f"习惯||{tag}||{course}" for course in course_dict.keys()]
            if len(course_list) > 0:
                result_list.extend(course_list)

        # action格式："能力维度||标签||课程名字"

        return result_list
        

    def is_terminal(self, state: PersonState):
        return state.is_perfect()
    

    def execute(self, state: PersonState, action):
        found_tag = None
        reward = None

        segments = action.split("||")
        course = segments[-1]
        
        next_state = copy.deepcopy(state)

        
        for tag in state.manage_tags:
            course_dict = self.course_info["管理"][tag]
            reward = course_dict.get(course, None)
            if reward is not None:
                found_tag = tag
                break
        
        if found_tag is not None:
            next_state.manage_tags = [tag for tag in next_state.manage_tags if tag != found_tag]
            check_tags_count = len(self.course_info["管理"].keys())
            next_state.manage_score = (check_tags_count - len(next_state.manage_tags)) * 100.0 / check_tags_count
            return next_state, reward
        
        # ==============================================
        for tag in state.knowledge_tags:
            course_dict = self.course_info["知识"][tag]
            reward = course_dict.get(course, None)
            if reward is not None:
                found_tag = tag
                break

        if found_tag is not None:
            next_state.knowledge_tags = [tag for tag in next_state.knowledge_tags if tag != found_tag]
            check_tags_count = len(self.course_info["知识"].keys())
            next_state.knowledge_score = (check_tags_count - len(next_state.knowledge_tags)) * 100.0 / check_tags_count
            return next_state, reward

        # ==============================================
        for tag in state.skill_tags:
            course_dict = self.course_info["技能"][tag]
            reward = course_dict.get(course, None)
            if reward is not None:
                found_tag = tag
                break

        if found_tag is not None:
            next_state.skill_tags = [tag for tag in next_state.skill_tags if tag != found_tag]
            check_tags_count = len(self.course_info["技能"].keys())
            next_state.skill_score = (check_tags_count - len(next_state.skill_tags)) * 100.0 / check_tags_count
            return next_state, reward

        # ==============================================
        for tag in state.will_tags:
            course_dict = self.course_info["意愿"][tag]
            reward = course_dict.get(course, None)
            if reward is not None:
                found_tag = tag
                break

        if found_tag is not None:
            next_state.will_tags = [tag for tag in next_state.will_tags if tag != found_tag]
            check_tags_count = len(self.course_info["意愿"].keys())
            next_state.will_score = (check_tags_count - len(next_state.will_tags)) * 100.0 / check_tags_count
            return next_state, reward

        # ==============================================
        for tag in state.habit_tags:
            course_dict = self.course_info["习惯"][tag]
            reward = course_dict.get(course, None)
            if reward is not None:
                found_tag = tag
                break

        if found_tag is not None:
            next_state.habit_tags = [tag for tag in next_state.habit_tags if tag != found_tag]
            check_tags_count = len(self.course_info["习惯"].keys())
            next_state.habit_score = (check_tags_count - len(next_state.habit_tags)) * 100.0 / check_tags_count
            return next_state, reward
        
        return next_state, 0


    def get_transitions(self, state: PersonState, action):
        next_state, _ = self.execute(state, action)
        return [(next_state, 1.0)] # hoho_todo: 转移概率暂写死

    def get_initial_state(self):
        return self.init_person_state
    
    def data_preprocess(self, data_dict):
        for ability, ability_dict in data_dict.items():
            avg_score = 1 / len(ability_dict.keys())
            for tag, tag_dict in ability_dict.items():
                for course, score in tag_dict.items():
                    tag_dict[course] = avg_score
        
        self.course_info = data_dict


if __name__ == "__main__":
    # state = PersonState(level = "区级河长")
    # mdp = HZCourseWorld(state)
    # print(mdp.course_info)

    # state_copied = copy.deepcopy(state)

    # print(id(state), id(state_copied))

    # l1 = ["l1", "我", "问答法"]
    # l2 = ["l1", "我"]
    # print(l1 == l2)

    # def test_change(l):
    #     # l = copy.deepcopy(l)
    #     l[0] = "1111"

    
    # l1 = ["l1", "我", "问答法"]
    # l2 = ["l1", "我"]
    # l3 = ["12", "34k", "问答法《》"]
    # print(len(set(l1) & set(l2)))
    # print(len(set(l1) & set(l3)))

    # print(test_change(l1))
    # print(l1)

    # state = PersonState(will_tags=["年度考核"], will_score=83.33, level = "区级河长")
    # print(str(state))
    # mdp = HZCourseWorld(state)

    # next_state, reward = mdp.execute(state, "《河长制激励问责机制》")
    # print(str(next_state), reward)

    # state = PersonState()
    # state1 = PersonState()
    # print(state == state1)
    # print(state.str_repr())

    # state = PersonState(will_tags=["年度考核"], will_score=83.33, level = "区级河长")
    # print(state.str_repr())

    state1 = PersonState(will_tags=["年度考核", "巡河质量"], will_score=83.33, level = "区级河长")
    state2 = PersonState(will_tags=["年度考核", "巡河质量"], will_score=83.33, knowledge_tags=["下级管理"], level = "区级河长")
    state3 = PersonState(will_tags=["巡河质量", "年度考核"], will_score=83.33, level = "区级河长")

    print(state1.str_repr())
    print(state2.str_repr())
    print(state3.str_repr())
    print(state1 == state3)
    print(state1.str_repr() == state3.str_repr())

    # state_dict = {}
    # state_dict[state] = 1

    # l1 = ["围绕", "1"]
    # l2 = ["1", "围绕"]
    # l3 = ["围绕", "1"]
    # print(l1 == l2)
    # print(l1 == l3)
    # print(sorted(l1) == sorted(l2))