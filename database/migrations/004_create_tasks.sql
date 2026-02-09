CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    project_id INT REFERENCES projects(id)
);
