"""Scene timing helpers for The Kumar Method intro videos."""


def compute_speaking_scene_time(voiceover: str) -> float:
    """Return Seedance clip duration (seconds) for a speaking scene voiceover.

    Formula: word_count / 2, with a minimum of 3 seconds.
    """
    word_count = len(voiceover.split())
    computed_time = word_count // 2
    return max(3, computed_time)
