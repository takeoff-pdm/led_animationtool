CREATE TABLE IF NOT EXISTS sections (
    name VARCHAR(32) UNIQUE NOT NULL,
    start_led INT(32) NOT NULL,
    end_led INT(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS color_sequences (
    name VARCHAR(32) UNIQUE NOT NULL,
    description VARCHAR(128) NOT NULL,
    selection INT(32) NOT NULL, -- 0 regular, 1 switching every fourth time, 2 random
    color_amount INT(32) NOT NULL DEFAULT 1 -- How many colors should be selected at once 
                                        -- (also skips given amount of colors to next color-set)
);

CREATE TABLE IF NOT EXISTS colors (
    color_sequence VARCHAR(32) UNIQUE NOT NULL, -- Name of the sequence
    position INT(32) NOT NULL, -- Position in sequence
    red INT(32) NOT NULL DEFAULT 0,
    green INT(32) NOT NULL DEFAULT 0,
    blue INT(32) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS animations (
    name VARCHAR(32) UNIQUE NOT NULL,
    description VARCHAR(128) NOT NULL,
    variation INT(32) NOT NULL DEFAULT 0, -- If multiple variations are possible
    direction INT(32) NOT NULL DEFAULT 0 -- 0 normal, 1 reverse, 2, 3, 4, 5 switching every time, second, fourth, eighth time
);
