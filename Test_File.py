import math
import os
from datetime import datetime

class DataProcessor:
    """Handles the main data processing pipeline."""
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.processed = False

    def clean_data(self, raw_data):
        """Removes invalid entries from the dataset."""
        return [x for x in raw_data if x is not None]

def _internal_logger(message, level):
    """Hidden helper function for logging. Should appear lower in the doc list."""
    print(f"[{level}] {message}")

def calculate_statistics(numbers, remove_outliers=True):
    """Calculates statistics and requires a high complexity score due to conditionals and loops."""
    if not numbers:
        return 0
        
    if remove_outliers:
        valid_numbers = []
        for num in numbers:
            try:
                if num > 0:
                    valid_numbers.append(num)
            except TypeError:
                pass
        numbers = valid_numbers
        
    total = sum(numbers)
    return total / len(numbers) if numbers else 0
