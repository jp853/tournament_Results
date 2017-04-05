-- Table definitions for the tournament project.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;


DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players (
    player_id SERIAL primary key,
    name TEXT
);


DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES players (player_id),
    loser INTEGER REFERENCES players (player_id)
);
