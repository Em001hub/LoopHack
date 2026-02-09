CREATE TABLE integrations (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50),
    config JSONB
);
