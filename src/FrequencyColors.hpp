#pragma once
#include <optional>

class FrequencyColors {
public:
    int scene_id;
    int color_sequence_id_1;
    int color_sequence_id_2;
    int color_sequence_id_3;

    FrequencyColors(std::optional<int> scene_id = std::nullopt,
                    std::optional<int> color_sequence_id_1 = std::nullopt,
                    std::optional<int> color_sequence_id_2 = std::nullopt,
                    std::optional<int> color_sequence_id_3 = std::nullopt);

    bool sync_changes_to_db(bool is_new = false);
};
