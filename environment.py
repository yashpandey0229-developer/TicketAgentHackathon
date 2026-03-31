import random

class TicketEnv:
    def __init__(self):
        # 3 Alag-alag difficulty ke tasks
        self.tickets = [
            {"id": "T1", "issue": "Mera order deliver nahi hua", "priority": "Low", "status": "Open"}, # Easy
            {"id": "T2", "issue": "Payment fail ho gayi par paise kat gaye", "priority": "Medium", "status": "Open"}, # Medium
            {"id": "T3", "issue": "Account hack ho gaya hai", "priority": "Low", "status": "Open"} # Hard (Security)
        ]
        self.current_idx = 0

    def reset(self):
        """Environment ko restart karta hai (Mandatory for RL)"""
        self.current_idx = 0
        return self.get_state()

    def get_state(self):
        """Current observation return karta hai"""
        return self.tickets[self.current_idx]

    def step(self, action_type, content):
        ticket = self.tickets[self.current_idx]
        reward_score = 0.0
        comment = "Incorrect action."
        done = False

        # --- TASK 1 (Easy): T1 - Delivery issue -> Medium Priority ---
        if ticket["id"] == "T1":
            if action_type == "set_priority" and content == "Medium":
                reward_score = 1.0
                comment = "Sahi! Delivery issues ko Medium priority milni chahiye."
            elif action_type == "set_priority" and content == "High":
                reward_score = 0.5  # Partial Reward!
                comment = "Theek hai, par Medium zyada accurate hota."

        # --- TASK 2 (Medium): T2 - Payment issue -> High Priority ---
        elif ticket["id"] == "T2":
            if action_type == "set_priority" and content == "High":
                reward_score = 1.0
                comment = "Perfect! Money issues hamesha High priority hote hain."

        # --- TASK 3 (Hard): T3 - Security issue -> High Priority & Action ---
        elif ticket["id"] == "T3":
            if action_type == "set_priority" and content == "High":
                reward_score = 1.0
                comment = "Excellent! Critical security issue handled."
            elif action_type == "set_priority" and content == "Medium":
                reward_score = 0.3 # Penalizing low effort for security
                comment = "Security issue hai, priority aur badhao."

        # Move to next ticket
        self.current_idx = (self.current_idx + 1) % len(self.tickets)
        
        # Agar aakhri ticket handle ho gaya, toh done = True
        if self.current_idx == 0:
            done = True
            
        return reward_score, done, comment