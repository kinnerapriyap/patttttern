# Measurements in mm, loaded from a per-person profile.
#
# Select a profile with the PATTERN_PROFILE environment variable
# (defaults to "default"), either set in the shell or in a .env file
# at the repo root (see .env.example), e.g.:
#
#   PATTERN_PROFILE=kaveri python -m aldrich_tailored_skirt.base.main
#   python run.py --profile kaveri
#
# Profiles live in utils/profiles/<name>.json and hold the raw inputs;
# this module fills in the grading values derived from them.

import json
import os

from dotenv import load_dotenv

load_dotenv()

_PROFILES_DIR = os.path.join(os.path.dirname(__file__), "profiles")


def _load_profile(name: str) -> dict:
    path = os.path.join(_PROFILES_DIR, f"{name}.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"No measurement profile named {name!r} at {path}. "
            f"Add utils/profiles/{name}.json or pick an existing profile."
        )
    with open(path) as f:
        return json.load(f)


_profile = _load_profile(os.environ.get("PATTERN_PROFILE", "default"))

size = _profile["size"]

bust = _profile["bust"]
bust_ease = _profile["bust_ease"]
bust_to_dart = _profile["bust_to_dart"]
waist = _profile["waist"]
waist_ease = _profile["waist_ease"]
hip = _profile["hip"]
nape_to_waist = _profile["nape_to_waist"]
waist_to_hip = _profile["waist_to_hip"]
armscye_depth = _profile["armscye_depth"]
neck_size = _profile["neck_size"]
shoulder = _profile["shoulder"]
shoulder_dart = _profile["shoulder_dart"]
back_width = _profile["back_width"]
back_width_ease = _profile["back_width_ease"]
dart = _profile["dart"]
chest = _profile["chest"]

front_dart = _profile["front_dart"]
back_dart = _profile["back_dart"]
front_side_dart = _profile["front_side_dart"]
back_side_dart = _profile["back_side_dart"]

skirt_length = _profile["skirt_length"]
skirt_hip_ease = _profile["skirt_hip_ease"]
skirt_back_waist_ease = _profile["skirt_back_waist_ease"]
skirt_front_waist_ease = _profile["skirt_front_waist_ease"]

body_rise = _profile["body_rise"]
waist_to_floor = _profile["waist_to_floor"]
waist_to_knee = _profile["waist_to_knee"]
trouser_bottom_width = _profile["trouser_bottom_width"]

# Grading values derived from size, not stored in the profile.
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
distance_from_t5 = 30 if 8 <= size <= 14 else (32.5 if 14 <= size <= 20 else 35)
distance_from_t16 = 42.5 if 8 <= size <= 14 else (45 if 14 <= size <= 20 else 47.5)
distance_for_knee = 13 if 8 <= size <= 16 else (15 if 16 <= size <= 20 else 17)
