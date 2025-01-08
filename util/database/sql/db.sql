CREATE TABLE IF NOT EXISTS sections (
    scene_id INT(32) NOT NULL,
    id INT(32) NOT NULL,
    name VARCHAR(32) NOT NULL,
    start_led INT(32) NOT NULL,
    end_led INT(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS scenes (
    id INT(32) NOT NULL,
    name VARCHAR(32) NOT NULL,
    description VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS scene_animations (
    scene_id INT(32) NOT NULL,
    animation_id INT(32) NOT NULL,
    section_id INT(32) NOT NULL,
    color_sequence_id INT(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS section_animations (
    scene_id INT(32) NOT NULL,
    section_id INT(32) NOT NULL,
    animation_id INT(32) NOT NULL,
    variation INT(32) NOT NULL DEFAULT 0, -- If multiple variations are possible
    direction INT(32) NOT NULL DEFAULT 0, -- 0: normal, 1: reverse, 2: inner to outer, 3: outer to inner, 
                                          -- 4, 5, 6, 7: switching every time, second, fourth, eighth time (between normal and reverse)
    off_set INT(32) NOT NULL DEFAULT 0    -- Beats the color selection is ahead
);

CREATE TABLE IF NOT EXISTS color_sequences (
    scene_id INT(32) NOT NULL,
    id INT(32) NOT NULL,
    name VARCHAR(32) NOT NULL,
    description VARCHAR(128) NOT NULL,
    selection INT(32) NOT NULL, -- 0 skip all selected colors, 1, 2, 3, 4... move on one, two, three, four... color(s)
    color_amount INT(32) NOT NULL DEFAULT 1     -- How many colors should be selected at once 
                                                -- (also skips given amount of colors to next color-set)
);

CREATE TABLE IF NOT EXISTS colors (
    scene_id INT(32) NOT NULL,
    id INT(32) NOT NULL,
    color_sequence_id VARCHAR(32) NOT NULL,
    position INT(32) NOT NULL, -- Position in sequence
    red INT(32) NOT NULL DEFAULT 0,
    green INT(32) NOT NULL DEFAULT 0,
    blue INT(32) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS animations (
    id INT(32) PRIMARY KEY NOT NULL,
    name VARCHAR(32) NOT NULL,
    description VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS frequency_color (
    scene_id INT(32) NOT NULL,
    color_sequence_id_1 INT(32) NOT NULL,
    color_sequence_id_2 INT(32) NOT NULL,
    color_sequence_id_3 INT(32) NOT NULL,
);
