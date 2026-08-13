DROP TABLE IF EXISTS calendar;
DROP SEQUENCE IF EXISTS calendar_id_seq;

CREATE SEQUENCE IF NOT EXISTS calendar_id_seq;
CREATE TABLE calendar (
    id SERIAL PRIMARY KEY,
    date DATE,
    start_time TIME,
    end_time TIME,
    content VARCHAR(255),
    title VARCHAR(255),
    is_recurring BOOLEAN NOT NULL DEFAULT FALSE,
    recurrence_group_id VARCHAR(36)
);


INSERT INTO calendar (date, start_time, end_time, content, title) VALUES ('2026-08-20', '01:00', '23:59', 'Going to go theatre', 'Monica Birthday')