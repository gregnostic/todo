DROP TABLE IF EXISTS item;

CREATE TABLE item (
    id serial PRIMARY KEY,
    description text NOT NULL,
    is_completed boolean NOT NULL DEFAULT FALSE
)
