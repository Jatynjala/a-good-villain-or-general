CREATE TABLE Questions_war (
    id SERIAL PRIMARY KEY, 
    question_war TEXT
);
CREATE TABLE Options_war (
    id SERIAL PRIMARY KEY, 
    option_war TEXT, 
    truth INTEGER, 
    questi INTEGER REFERENCES Questions_war
);
CREATE TABLE Questions_villany (
    id SERIAL PRIMARY KEY, 
    question_villany TEXT
);
CREATE TABLE Options_villany (
    id SERIAL PRIMARY KEY, 
    option_villany TEXT, 
    truth INTEGER, 
    questo INTEGER REFERENCES Questions_villany
);
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    pasword TEXT,
    status TEXT,
    tries INTEGER,
    successes INTEGER
);
