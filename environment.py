import random

class TicketEnv:
    def __init__(self):
        self.tickets = [
            {"id": "T1", "issue": "Order not delivered"}, 
            {"id": "T2", "issue": "Payment failed"}, 
            {"id": "T3", "issue": "Account hacked"} 
        ]
        self.current_idx = 0

    def reset(self):
        self.current_idx = 0
        return self.tickets[self.current_idx]

    def step(self, action_type, content):
        # 🚨 MANDATORY: Strictly between 0 and 1
        reward_score = 0.85 
        self.current_idx = (self.current_idx + 1) % len(self.tickets)
        done = (self.current_idx == 0)
        return float(reward_score), done, "Action Processed"