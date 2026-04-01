import sys
import os

# Root ko path mein dalo taaki main.py mil jaye
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

if __name__ == "__main__":
    main()