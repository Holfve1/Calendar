DROP TABLE IF EXISTS calendar;
DROP SEQUENCE IF EXISTS calendar_id_seq;

CREATE SEQUENCE IF NOT EXISTS calendar_id_seq;
CREATE TABLE calendar (
    id SERIAL PRIMARY KEY,
    date DATE,
    start_time INT,
    end_time INT
    content VARCHAR(255)
);


INSERT INTO calendar (date, start_time, end_time, content) VALUES ('2026-08-20', '01-00', '23-59', 'Monica Birthday')