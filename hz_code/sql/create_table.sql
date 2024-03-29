CREATE TABLE HZXCX_COURSE_RM (
    ID NUMBER DEFAULT 1 PRIMARY KEY NOT NULL,
    TASK_ID VARCHAR2(64),
    PUSH_PERIOD VARCHAR2(64),
    CHIEF_NAME VARCHAR2(128),
    CHIEF_ID VARCHAR2(128),
    CHIEF_TYPE VARCHAR2(64),
    MANAGEMENT_SCORE NUMBER,
    SKILL_SCORE NUMBER,
    KNOWLEDGE_SCORE NUMBER,
    WILL_SCORE NUMBER,
    HABIT_SCORE NUMBER,
    MANAGEMENT_LABEL VARCHAR2(255),
    SKILL_LABEL VARCHAR2(255),
    KNOWLEDGE_LABEL VARCHAR2(255),
    WILL_LABEL VARCHAR2(255),
    HABIT_LABEL VARCHAR2(255),
    COURSE_NAME VARCHAR2(255),
    COURSE_ID VARCHAR2(255),
    PUSH_TYPE INT
);