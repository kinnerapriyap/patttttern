# Measurements in mm
size = 14

bust = 880
bust_ease = 50
bust_to_dart = 25
waist = 700
waist_ease = 30
hip = 1000
nape_to_waist = 410
waist_to_hip = 206
armscye_depth = 210
neck_size = 370
shoulder = 122.5
shoulder_dart = 10
back_width = 344
back_width_ease = 5
dart = 70
chest = 324

front_dart = 45
back_dart = 35
front_side_dart = 15
back_side_dart = 15

size_above_14 = max(size - 14, 0)
distance_from_p14 = 22.5 if 6 <= size <= 8 \
    else 25 if 10 <= size <= 14 \
    else 30 if 16 <= size <= 20 \
    else 35 if 22 <= size <= 26 \
    else 30
distance_from_p22 = 17.5 if 6 <= size <= 8 \
    else 20 if 10 <= size <= 14 \
    else 25 if 16 <= size <= 20 \
    else 30 if 22 <= size <= 26 \
    else 25

