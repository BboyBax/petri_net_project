"""utils.py
Hàm tiện ích chung cho toàn bộ dự án Petri Net.
"""

import os
from datetime import datetime

def print_separator(text="---"):
    """In dòng phân tách cho dễ theo dõi log."""
    print("\n" + "="*25 + f" {text} " + "="*25 + "\n")

def save_log(message, file_name="project_log.txt"):
    """Ghi log ra file trong thư mục data/results."""
    os.makedirs("data/results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join("data/results", file_name)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
