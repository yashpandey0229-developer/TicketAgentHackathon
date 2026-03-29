import random

class TicketEnv:
    def __init__(self):
        # Initial Tickets
        self.tickets = [
            {"id": "T1", "issue": "Mera order deliver nahi hua", "priority": "Low", "status": "Open"},
            {"id": "T2", "issue": "Payment fail ho gayi par paise kat gaye", "priority": "Medium", "status": "Open"},
            {"id": "T3", "issue": "Account hack ho gaya hai", "priority": "Low", "status": "Open"}
        ]
        self.current_idx = 0

    def get_state(self):
        if self.current_idx < len(self.tickets):
            return self.tickets[self.current_idx]
        # Agar tickets khatam ho jayein toh pehla wala hi wapas de do (Looping)
        self.current_idx = 0 
        return self.tickets[0]

    def step(self, action_type, content):
        ticket = self.tickets[self.current_idx]
        reward_score = 0.0
        comment = "Incorrect action."

        # Task: Security issues (T3) must be High Priority
        if ticket["id"] == "T3" and action_type == "set_priority" and content == "High":
            reward_score = 1.0
            comment = "Excellent! High priority for security issues."
            ticket["priority"] = "High"
        
        self.current_idx = (self.current_idx + 1) % len(self.tickets)
        done = False # Keep it running for the hackathon
        return reward_score, done, comment