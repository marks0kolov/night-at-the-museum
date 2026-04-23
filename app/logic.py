import random

def generate_target_positions(difficulty):
    """generate gem, artifact and guard positions based on the difficulty level"""
    match difficulty:
        case 'easy':
            return {
                