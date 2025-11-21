""" 
Task 5 - Thành viên 5
Tối ưu hóa trên các trạng thái có thể đạt được.
"""

def maximize_over_markings(graph, bdd, deadlock):
    print("🔹 Đang thực hiện tối ưu hóa...")
    # TODO: Implement Optimization over reachable markings
    # Example: if deadlock, print and save result
    if deadlock:
        print("⚠️ Deadlock detected - perform further analysis.")
    else:
        print("ℹ️ No deadlock detected - continue reasoning.")
