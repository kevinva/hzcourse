import pandas as pd
import numpy as np
from hz_code.hz_mcts import *

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
    
    world_file_path = "data/courses_values_20240108100829.json"
    course_world = HZCourseWorld(person_state = person_state, file_path = world_file_path)
    qfunction = QTable()
    algorithm = UpperConfidenceBounds()
    model = MCTS(mdp = course_world, qfunction = qfunction, q_algorithm = algorithm)
    root_node = model.mcts()

    suffix = suffix_time()
    output_file_path = f"./outputs/qtable_{suffix}.json"
    qfunction.export(output_file_path)

    # 打印候选结果
    state_str = person_state.str_repr()
    result_dict = dict(qfunction.qtable)
    for key, score in qfunction.qtable.items():
        state = key[0]
        action = key[1]
        if state == state_str:
            print(f"{action}: {score}")

    tree_dict = mcts_tree_to_dict(root_node)
    tree_output_file_path = f"./outputs/mcts_{suffix}.km"
    visual_tree(tree_dict, tree_output_file_path)



app()