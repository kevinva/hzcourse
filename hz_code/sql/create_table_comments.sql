CREATE TABLE HZXCX_COURSE_RM (
    ID NUMBER DEFAULT 1 PRIMARY KEY NOT NULL,
    TASK_ID VARCHAR2(64),                           -- '任务ID'
    PUSH_PERIOD VARCHAR2(64),                       -- '推送周期'
    CHIEF_NAME VARCHAR2(128),                       -- '河长姓名'
    CHIEF_ID VARCHAR2(128),                         -- '河长ID'
    CHIEF_TYPE VARCHAR2(64),                        -- '河长类型'
    MANAGEMENT_SCORE NUMBER,                        -- '管理维度得分'
    SKILL_SCORE NUMBER,                             -- '技能维度得分'
    KNOWLEDGE_SCORE NUMBER,                         -- '知识维度得分'
    WILL_SCORE NUMBER,                              -- '意愿维度得分'
    HABIT_SCORE NUMBER,                             -- '习惯维度得分'
    MANAGEMENT_LABEL VARCHAR2(255),                 -- '管理标签列表'
    SKILL_LABEL VARCHAR2(255),                      -- '技能标签列表'
    KNOWLEDGE_LABEL VARCHAR2(255),                  -- '知识标签列表'
    WILL_LABEL VARCHAR2(255),                       -- '意愿标签列表'
    HABIT_LABEL VARCHAR2(255),                      -- '习惯标签列表'
    COURSE_NAME VARCHAR2(255),                      -- '推送课程列表'
    COURSE_ID VARCHAR2(255),                        -- '推送课程ID列表'
    PUSH_TYPE INT                                   -- '推送类型：模型推送=1，手动推送=2'
);
