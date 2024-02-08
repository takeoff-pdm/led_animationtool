CREATE TABLE IF NOT EXISTS sections (
    id INT(32) PRIMARY KEY NOT NULL,
    name VARCHAR(32) NOT NULL,
    start_led INT(32) NOT NULL,
    end_led INT(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS color_sequences (
    id INT(32) PRIMARY KEY NOT NULL,
    name VARCHAR(32) NOT NULL,
    description VARCHAR(128) NOT NULL,
    selection INT(32) NOT NULL, -- 0 regular, 1 switching every fourth time, 2 random
    color_amount INT(32) NOT NULL DEFAULT 1 -- How many colors should be selected at once 
                                        -- (also skips given amount of colors to next color-set)
);

CREATE TABLE IF NOT EXISTS colors (
    id INT(32) PRIMARY KEY NOT NULL,
    color_sequence_id VARCHAR(32) NOT NULL,
    position INT(32) NOT NULL, -- Position in sequence
    red INT(32) NOT NULL DEFAULT 0,
    green INT(32) NOT NULL DEFAULT 0,
    blue INT(32) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS animations (
    id INT(32) PRIMARY KEY NOT NULL,
    name VARCHAR(32) NOT NULL,
    description VARCHAR(128) NOT NULL,
    variation INT(32) NOT NULL DEFAULT 0, -- If multiple variations are possible
    direction INT(32) NOT NULL DEFAULT 0  -- 0: normal, 1: reverse, 2: inner to outer, 3: outer to inner, 
                                          -- 4, 5, 6, 7: switching every time, second, fourth, eighth time (between normal and reverse)
);
