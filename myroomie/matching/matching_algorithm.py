import math
from datetime import datetime


# --------------------------------------------------
# 1. WEIGHTS
# --------------------------------------------------

WEIGHTS = {
    "budget": 30,
    "location": 20,
    "food": 15,
    "smoking": 10,
    "sleep": 10,
    "cleanliness": 15,
}


# --------------------------------------------------
# 2. NORMALIZE VALUES
# --------------------------------------------------

def normalize_value(value):
    """
    Convert a value to a common format.
    """

    if value is None:
        return ""

    return str(value).strip().casefold()


# --------------------------------------------------
# 3. EXACT PREFERENCE COMPARISON
# --------------------------------------------------

def compare_preference(value1, value2):
    """
    Same preference = 100
    Different preference = 0
    Missing preference = None
    """

    value1 = normalize_value(value1)
    value2 = normalize_value(value2)

    if not value1 or not value2:
        return None

    if value1 == value2:
        return 100.0

    return 0.0


# --------------------------------------------------
# 4. BUDGET COMPATIBILITY
# --------------------------------------------------

def compare_budget(preference1, preference2):
    """
    Compare two budget ranges.

    Identical ranges = 100
    Partial overlap = partial score
    No overlap = 0
    Missing/invalid budget = None
    """

    min1 = preference1.budget_min
    max1 = preference1.budget_max

    min2 = preference2.budget_min
    max2 = preference2.budget_max

    if None in (min1, max1, min2, max2):
        return None

    try:
        min1, max1, min2, max2 = map(
            float,
            (min1, max1, min2, max2)
        )
    except (ValueError, TypeError):
        return None

    # Invalid budget ranges
    if min1 < 0 or min2 < 0:
        return None

    if min1 > max1 or min2 > max2:
        return None

    # Calculate the overlapping range.
    overlap_start = max(min1, min2)
    overlap_end = min(max1, max2)

    overlap = max(0, overlap_end - overlap_start)

    # Calculate the total range covered by both budgets.
    total_range = max(max1, max2) - min(min1, min2)

    # Handle budgets where both ranges have the same value.
    if total_range == 0:
        return 100.0

    # Similarity score based on overlap.
    score = (overlap / total_range) * 100

    return round(max(0, min(100, score)), 2)


# --------------------------------------------------
# 5. LOCATION DISTANCE
# --------------------------------------------------

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the approximate distance between
    two geographic coordinates using the Haversine formula.

    Returns distance in kilometres.
    """

    try:
        lat1, lon1, lat2, lon2 = map(
            float,
            (lat1, lon1, lat2, lon2)
        )
    except (ValueError, TypeError):
        return None

    # Validate coordinates.
    if not (-90 <= lat1 <= 90):
        return None

    if not (-90 <= lat2 <= 90):
        return None

    if not (-180 <= lon1 <= 180):
        return None

    if not (-180 <= lon2 <= 180):
        return None

    # Convert degrees into radians.
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula.
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    a = max(0.0, min(1.0, a))

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    earth_radius_km = 6371.0

    return earth_radius_km * c


def compare_location(profile1, profile2):
    lat1 = profile1.ref_latitude
    lon1 = profile1.ref_longitude
    lat2 = profile2.ref_latitude
    lon2 = profile2.ref_longitude

    # Check whether coordinates are available
    if any(
        value is None or value == ""
        for value in (lat1, lon1, lat2, lon2)
    ):
        return None

    # Calculate distance in kilometers
    distance = calculate_distance(lat1, lon1, lat2, lon2)

    if distance is None:
        return None

    # Distance-based location matching score
    if distance <= 0:
        score = 100
    elif distance <= 0.5:
        score = 100 - (distance / 0.5) * 20
    elif distance <= 1:
        score = 80 - ((distance - 0.5) / 0.5) * 30
    elif distance <= 1.5:
        score = 50 - ((distance - 1) / 0.5) * 30
    elif distance < 2:
        score = 20 - ((distance - 1.5) / 0.5) * 20
    else:
        score = 0

    return round(max(0, min(100, score)), 2)


# --------------------------------------------------
# 6. CONVERT SLEEP TIME TO MINUTES
# --------------------------------------------------

def parse_sleep_time(value):
    """
    Convert a clock time into minutes after midnight.

    Supported examples:
    11 PM
    11:00 PM
    23:00
    7 AM
    07:30 AM
    """

    if value is None:
        return None

    value = str(value).strip()

    formats = [
        "%I %p",
        "%I:%M %p",
        "%I:%M:%S %p",
        "%H:%M",
        "%H:%M:%S",
    ]

    for time_format in formats:
        try:
            parsed_time = datetime.strptime(
                value.upper(),
                time_format
            )

            return (
                parsed_time.hour * 60
                + parsed_time.minute
            )

        except ValueError:
            continue

    return None


# --------------------------------------------------
# 7. SLEEP TIME COMPATIBILITY
# --------------------------------------------------

def compare_sleep_time(value1, value2):
    """
    Same sleep time = 100
    Greater time difference = lower score
    Circular difference >= 12 hours = 0
    Missing/unrecognised time = None
    """

    if not normalize_value(value1):
        return None

    if not normalize_value(value2):
        return None

    minutes1 = parse_sleep_time(value1)
    minutes2 = parse_sleep_time(value2)

    # If the values are identical but aren't clock times,
    # an exact match still receives 100.
    if minutes1 is None or minutes2 is None:

        if normalize_value(value1) == normalize_value(value2):
            return 100.0

        # Different values that cannot be parsed
        # cannot be compared by time difference.
        return None

    difference = abs(minutes1 - minutes2)

    # Account for midnight.
    difference = min(
        difference,
        1440 - difference
    )

    max_difference = 720  # 12 hours

    score = (
        1 - difference / max_difference
    ) * 100

    return round(max(0, min(100, score)), 2)


# --------------------------------------------------
# 8. FINAL COMPATIBILITY SCORE
# --------------------------------------------------

def calculate_compatibility(
    preference1,
    preference2,
    profile1,
    profile2
):
    """
    Calculate weighted compatibility between two users.
    """

    scores = {
        "budget": compare_budget(
            preference1,
            preference2
        ),

        "location": compare_location(
            profile1,
            profile2
        ),

        "food": compare_preference(
            preference1.food_type,
            preference2.food_type
        ),

        "smoking": compare_preference(
            preference1.smoking,
            preference2.smoking
        ),

        "sleep": compare_sleep_time(
            preference1.sleep_time,
            preference2.sleep_time
        ),

        "cleanliness": compare_preference(
            preference1.cleanliness,
            preference2.cleanliness
        ),
    }

    # Ignore missing factors.
    available_factors = {
        name: score
        for name, score in scores.items()
        if score is not None
    }

    if not available_factors:
        return {
            "score": 0,
            "details": scores,
            "compared_factors": 0,
        }

    # Add weights for available factors only.
    total_weight = sum(
        WEIGHTS[name]
        for name in available_factors
    )

    # Calculate weighted score.
    weighted_score = sum(
        available_factors[name] * WEIGHTS[name]
        for name in available_factors
    )

    # Final weighted average.
    final_score = round(
        weighted_score / total_weight,
        2
    )

    return {
        "score": final_score,
        "details": scores,
        "compared_factors": len(available_factors),
    }