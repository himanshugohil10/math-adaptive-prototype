
def determine_next_difficulty(current_difficulty, recent_history):
    """
    Determines the next difficulty level based on recent performance.
    
    Args:
        current_difficulty (str): 'Easy', 'Medium', 'Hard'
        recent_history (list): List of dicts with 'correct' and 'time_taken'.
            Expected to be the last 3 attempts for the rule check.
            
    Returns:
        str: Next difficulty level.
    """
    # Expected time thresholds (in seconds)
    EXPECTED_TIME = {
        'Easy': 7.0,
        'Medium': 15.0,
        'Hard': 40.0
    }
    
    levels = ['Easy', 'Medium', 'Hard']
    try:
        current_idx = levels.index(current_difficulty)
    except ValueError:
        return 'Easy' # Default fallback

    # Need at least 3 questions to apply the specific "last 3" rules
    if len(recent_history) < 3:
        return current_difficulty

    last_3 = recent_history[-3:]
    
    # Check correctness
    correct_count = sum(1 for h in last_3 if h['correct'])
    incorrect_count = 3 - correct_count
    
    # Calculate average time for last 3
    avg_time_last_3 = sum(h['time_taken'] for h in last_3) / 3.0
    expected = EXPECTED_TIME.get(current_difficulty, 10.0)
    
    # Rule 1: Increase Difficulty
    if correct_count == 3 and avg_time_last_3 < expected:
        if current_idx < 2: # Can increase
            return levels[current_idx + 1]
            
    # Rule 2: Decrease Difficulty
    if incorrect_count >= 2 or avg_time_last_3 >= (1.5 * expected):
        if current_idx > 0: # Can decrease
            return levels[current_idx - 1]
            
    # Else: Maintain
    return current_difficulty
