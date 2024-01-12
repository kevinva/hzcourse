import json


class PersonState:

    def __init__(self, 
                 will_tags = [], 
                 will_score = 100.0, 
                 manage_tags = [], 
                 manage_score = 100.0, 
                 knowledge_tags = [], 
                 knowledge_score = 100.0,
                 habit_tags = [],
                 habit_score = 100.0,
                 skill_tags = [],
                 skill_score = 100.0,
                 level = None):
        
        self.will_score = will_score
        self.manage_score = manage_score
        self.knowledge_score = knowledge_score
        self.habit_score = habit_score
        self.skill_score = skill_score
        self.will_tags = will_tags
        self.manage_tags = manage_tags
        self.knowledge_tags = knowledge_tags
        self.habit_tags = habit_tags
        self.skill_tags = skill_tags
        self.level = level


    def is_perfect(self):
        return len(self.manage_tags) == 0 \
                and len(self.knowledge_tags) == 0 \
                and len(self.skill_tags) == 0 \
                and len(self.will_tags) == 0 \
                and len(self.habit_tags) == 0
    

    def str_repr(self) -> str:
        manage_list = sorted(self.manage_tags)
        manage_list = [f"管理||{tag}" for tag in manage_list]
        knowledge_list = sorted(self.knowledge_tags)
        knowledge_list = [f"知识||{tag}" for tag in knowledge_list]
        skill_list = sorted(self.skill_tags)
        skill_list = [f"技能||{tag}" for tag in skill_list]
        will_list = sorted(self.will_tags)
        will_list = [f"意愿||{tag}" for tag in will_list]
        habit_ilst = sorted(self.habit_tags)
        habit_ilst = [f"习惯||{tag}" for tag in habit_ilst]

        all_list = []
        all_list.extend(manage_list)
        all_list.extend(knowledge_list)
        all_list.extend(skill_list)
        all_list.extend(will_list)
        all_list.extend(habit_ilst)
        result = json.dumps(all_list, ensure_ascii = False)
        return result

    def __repr__(self) -> str:
        manage_dict = {"管理": self.manage_tags}
        skill_dict = {"技能": self.skill_tags}
        knowledge_dict = {"知识": self.knowledge_tags}
        will_dict = {"意愿": self.will_tags}
        habit_dict = {"习惯": self.habit_tags}
        score_text = f"(管理: {self.manage_score},  技能: {self.skill_score}, 知识: {self.knowledge_score}, 意愿: {self.will_score}, 习惯: {self.habit_score})"
        result = f"{json.dumps(manage_dict, ensure_ascii = False)}\n{json.dumps(skill_dict, ensure_ascii = False)}\n{json.dumps(knowledge_dict, ensure_ascii = False)}\n{json.dumps(will_dict, ensure_ascii = False)}\n{json.dumps(habit_dict, ensure_ascii = False)}\n{score_text}"
        return result


    def __str__(self) -> str:
        return f"manage = {self.manage_score}, knowledge = {self.knowledge_score}, skill = {self.skill_score}, habit = {self.habit_score}, will = {self.will_score}"


    def __eq__(self, other):
        if isinstance(other, PersonState):
            return self.will_score == other.will_score \
                    and self.manage_score == other.manage_score \
                    and self.knowledge_score == other.knowledge_score \
                    and self.habit_score == other.habit_score \
                    and self.skill_score == other.skill_score \
                    and self.will_tags == other.will_tags \
                    and self.manage_tags == other.manage_tags \
                    and self.knowledge_tags == other.knowledge_tags \
                    and self.habit_tags == other.habit_tags \
                    and self.skill_tags == other.skill_tags

        return False