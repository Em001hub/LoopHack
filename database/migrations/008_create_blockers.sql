CREATE TABLE blockers (
    id SERIAL PRIMARY KEY,
    task_id INT,
    reason TEXT
);
