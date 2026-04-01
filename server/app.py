import sys
import os
import uvicorn

# Root ko path mein dalo taaki main.py mil jaye
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # Hum direct app object import kar rahe hain logic ke liye

def main():
    """Validator isse hi call karega."""
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()