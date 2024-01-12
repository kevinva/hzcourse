import pandas as pd
import numpy as np
from hz_code.hz_mcts import *

def select_courses(candidate_list, person_state: PersonState):
    course_list = sorted(candidate_list, key = lambda x: x[1], reverse = True)

    # hoho_todo: 如果该维度较低分，是不是在mcts时可以给予更高的奖励？! 这样就可以不用这里又特意排序了
    package1 = [("管理", person_state.manage_score), ("知识", person_state.knowledge_score), ("技能", person_state.skill_score)]
    package2 = [("意愿", person_state.will_score), ("习惯", person_state.habit_score)]
    package1_sorted = sorted(package1, key = lambda x: x[1])
    package2_sorted = sorted(package2, key = lambda x: x[1])

    candidate1 = []
    for ability, _ in package1_sorted:
        for action in course_list:
            if action[0].startswith(ability):
                candidate1.append(action)

    candidate2 = []
    for ability, _ in package2_sorted:
        for action in course_list:
            if action[0].startswith(ability):
                candidate2.append(action) 

    LOGGER.info(f"candidate1: {candidate1}")
    LOGGER.info(f"candidate2: {candidate2}")

    result1 = []
    for action in candidate1:
        segments = action[0].split("||")
        assert len(segments) == 3
        course = segments[2]
        result1.append(course)
        if len(result1) >= 2:
            break

    result2 = []
    for action in candidate2:
        segments = action[0].split("||")
        assert len(segments) == 3
        course = segments[2]
        result2.append(course)
        if len(result2) >= 1:
            break

    LOGGER.info(f"select course from result1: {result1} ")
    LOGGER.info(f"select course from result2: {result2} ")


def app():
    with open("./data/result.json", "r", encoding = "utf8") as f:
        result_list = json.load(f)

    result_pd = pd.DataFrame(result_list)

    # 测试数据
    test_data = result_pd.iloc[0]
    will_tags = test_data["will_tag"]
    will_score = float(test_data["will_score"])
    manage_tags = test_data["manage_tag"]
    manage_score = float(test_data["manage_score"])
    skill_tags = test_data["skill_tag"]
    skill_score = float(test_data["skill_score"])
    knowledge_tags = test_data["knowledge_tag"]
    knowledge_score = float(test_data["knowledge_score"])
    habit_tags = test_data["habit_tag"]
    habit_score = float(test_data["habit_score"])
    # level = test_data["level"]
    level = "基层河长"

    person_state = PersonState(will_tags = will_tags,
                            will_score = will_score,
                            manage_tags = manage_tags,
                            manage_score = manage_score,
                            knowledge_tags = knowledge_tags,
                            knowledge_score = knowledge_score,
                            skill_tags = skill_tags,
                            skill_score = skill_score,
                            habit_tags = habit_tags,
                            habit_score = habit_score,
                            level = level)
    
    print(f"person_state: {person_state}, {person_state.str_repr()}")
    
    world_file_path = "data/courses_values_20240108100829.json"
    course_world = HZCourseWorld(person_state = person_state, file_path = world_file_path)
    qfunction = QTable()
    algorithm = UpperConfidenceBounds()
    model = MCTS(mdp = course_world, qfunction = qfunction, q_algorithm = algorithm)
    root_node = model.mcts()

    # ==========> 结果输出
    suffix = suffix_time()
    output_file_path = f"./outputs/qtable_{suffix}.json"
    qfunction.export(output_file_path)

    tree_dict = mcts_tree_to_dict(root_node, qfunction)
    tree_output_file_path = f"./outputs/mcts_{suffix}.km"
    visual_tree(tree_dict, tree_output_file_path)

    state_str = person_state.str_repr()
    result_list = []
    for key, score in qfunction.qtable.items():
        state = key[0]
        action = key[1]
        if state == state_str:
            result_list.append((action, score))
            LOGGER.info(f"{action}, {score}")

    select_courses(result_list, person_state)

    

app()