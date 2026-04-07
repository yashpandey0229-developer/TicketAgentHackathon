import random

class TicketEnv:
    def __init__(self):
        # 3 Alag-alag difficulty ke tasks
        self.tickets = [
            {"id": "T1", "issue": "Mera order deliver nahi hua", "priority": "Low", "status": "Open"}, 
            {"id": "T2", "issue": "Payment fail ho gayi par paise kat gaye", "priority": "Medium", "status": "Open"}, 
            {"id": "T3", "issue": "Account hack ho gaya hai", "priority": "Low", "status": "Open"} 
        ]
        self.current_idx = 0

    def reset(self):
        """Environment ko restart karta hai"""
        self.current_idx = 0
        return self.get_state()

    def get_state(self):
        """Current observation return karta hai"""
        return self.tickets[self.current_idx]

    def step(self, action_type, content):
        ticket = self.tickets[self.current_idx]
        
        # 🚨 FINAL FIX: Baseline hamesha 0.05 (Never 0.0)
        reward_score = 0.05 
        comment = "Incorrect action."
        done = False

        # Logic for Task T1
        if ticket["id"] == "T1":
            if action_type == "set_priority" and content == "Medium":
                reward_score = 0.95
                comment = "Sahi! Medium priority accurate hai."
            elif action_type == "set_priority" and content == "High":
                reward_score = 0.50 
                comment = "Partial reward, Medium better hota."

        # Logic for Task T2
        elif ticket["id"] == "T2":
            if action_type == "set_priority" and content == "High":
                reward_score = 0.95
                comment = "Perfect! Money issues High priority hain."
            else:
                reward_score = 0.10 # Still in range (0, 1)

        # Logic for Task T3
        elif ticket["id"] == "T3":
            if action_type == "set_priority" and content == "High":
                reward_score = 0.95
                comment = "Critical security issue handled."
            elif action_type == "set_priority" and content == "Medium":
                reward_score = 0.35 
                comment = "Security issues High priority hone chahiye."

        # Increment index
        self.current_idx = (self.current_idx + 1) % len(self.tickets)
        
        # Check if done
        if self.current_idx == 0:
            done = True
            
        # 🚨 Ensure returning float and strictly in range
        return float(reward_score), done, comment