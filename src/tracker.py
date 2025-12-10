
class PerformanceTracker:
    def __init__(self):
        # storing list of dicts: {'difficulty': str, 'correct': bool, 'time_taken': float}
        self.history = []

    def log_attempt(self, difficulty, correct, time_taken):
        self.history.append({
            'difficulty': difficulty,
            'correct': correct,
            'time_taken': time_taken
        })

    def get_metrics(self):
        if not self.history:
            return {
                'total_attempts': 0,
                'accuracy': 0.0,
                'average_response_time': 0.0
            }
        
        total = len(self.history)
        correct_count = sum(1 for h in self.history if h['correct'])
        total_time = sum(h['time_taken'] for h in self.history)
        
        return {
            'total_attempts': total,
            'accuracy': (correct_count / total) * 100,
            'average_response_time': total_time / total
        }

    def get_recent_history(self, n=3):
        return self.history[-n:]

    def get_data_as_csv(self):
        """
        Returns the history as a CSV formatted string.
        """
        import pandas as pd
        if not self.history:
            return ""
        
        # Calculate running metrics for the CSV
        data = []
        correct_count = 0
        total_time = 0
        
        for i, h in enumerate(self.history):
            correct_count += 1 if h['correct'] else 0
            total_time += h['time_taken']
            running_accuracy = (correct_count / (i + 1)) * 100
            running_avg_time = total_time / (i + 1)
            
            data.append({
                'Question Index': i + 1,
                'Difficulty': h['difficulty'],
                'Answer Correct': h['correct'],
                'Time Taken (s)': round(h['time_taken'], 2),
                'Running Accuracy (%)': round(running_accuracy, 1),
                'Running Avg Time (s)': round(running_avg_time, 2)
            })
            
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    
    def get_data_frame(self):
        import pandas as pd
        if not self.history:
            return pd.DataFrame()
        return pd.DataFrame(self.history)

