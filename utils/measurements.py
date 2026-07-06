# Measurements in mm
size = 18

bust = 1000
bust_ease = 50
bust_to_dart = 40
waist = 840
waist_ease = 30
hip = 1040
nape_to_waist = 410
waist_to_hip = 210
armscye_depth = 230
neck_size = 400
shoulder = 130
shoulder_dart = 10
back_width = 374
back_width_ease = 5
dart = 88
chest = 360

front_dart = 45
back_dart = 35
front_side_dart = 10
back_side_dart = 10

size_above_14 = max(size - 14, 0)
distance_from_p14 = (
    22.5
    if 6 <= size <= 8
    else (
        25
        if 10 <= size <= 14
        else 30 if 16 <= size <= 20 else 35 if 22 <= size <= 26 else 30
    )
)
distance_from_p22 = (
    17.5
    if 6 <= size <= 8
    else (
        20
        if 10 <= size <= 14
        else 25 if 16 <= size <= 20 else 30 if 22 <= size <= 26 else 25
    )
)

skirt_length = 600
skirt_hip_ease = 15
skirt_back_waist_ease = 42.5
skirt_front_waist_ease = 22.5

body_rise = 300
waist_to_floor = 1070
waist_to_knee = 600
trouser_bottom_width = 240

distance_from_t5 = 30 if 8 <= size <= 14 else (32.5 if 14 <= size <= 20 else 35)
distance_from_t16 = 42.5 if 8 <= size <= 14 else (45 if 14 <= size <= 20 else 47.5)
distance_for_knee = 13 if 8 <= size <= 16 else (15 if 16 <= size <= 20 else 17)
