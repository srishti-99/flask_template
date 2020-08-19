DROP TABLE IF EXISTS users;


CREATE TABLE users (
    username TEXT PRIMARY KEY,
    firstname TEXT,
    lastname TEXT,
    description TEXT
);

/* This extension sometimes causes issues importing to Google Cloud SQL */
DROP EXTENSION IF EXISTS plpgsql;