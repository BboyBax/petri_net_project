# Petri Net Project
## Symbolic and Algebraic Reasoning in Petri Nets


## 📑 Mục lục
- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Cách sử dụng](#cách-sử-dụng)
- [Tính năng](#tính-năng)
- [Ví dụ](#ví-dụ)
- [Liên hệ](#liên-hệ)
- [Thành viên](#thành-viên)

## Giới thiệu
    Một công cụ phân tích Petri net 1-safe từ file PNML, hỗ trợ kiểm tra tính nhất quán, tính toán tập trạng thái reachable, phát hiện deadlock và tối ưu hóa theo hàm mục tiêu tuyến tính.
## Cài đặt

Yêu cầu:
- Python 
- Các thư viện: `numpy`, `pyeda`, `pulp`, `dd`, `pytest`

Cài đặt:
```bash
git clone https://github.com/BboyBax/petri_net_project
cd petri_net_project
conda env create -f environment.yml
conda activate petri-net-env
```
## Cách sử dụng
```bash
python src/main.py <đường_dẫn_file_pnml> --task <số_task> [tùy_chọn]

```
- <đường_dẫn_file_pnml>: đường dẫn đến file PNML (ví dụ models/token_ring.pnml)

- --task <số_task>: chọn task muốn chạy (1–5)

- [tùy_chọn]: các tham số bổ sung (chỉ Task 5 cần --c)


## Tính năng
- Task 1: PNML parsing (task1_parser.py)
- Task 2: Explicit computation of reachable markings (BFS or DFS) (task2_explicit_reachablility.py)
- Task 3: Symbolic computation of reachable markings (BDD) (task3_symbolic_reachability)
- Task 4: Deadlock detection (ILP and BDD) (task4_deadlock_detection.py)
- Task 5: Optimization over reachable markings (task5_optimize_reachable_marking.py)

## Ví dụ
    python src/main.py data/pnml/phylosopher.pnml --task 1
    python src/main.py data/pnml/example.pnml --task 2
    python src/main.py data/pnml/example.pnml --task 3
    python src/main.py data/pnml/example.pnml --task 4
    python src/main.py data/pnml/optimization1.pnml --task 5 --c 0 2 5 3

## Liên hệ
- Nhóm trưởng: Hà Trọng Sơn
- Email: son.hatrong@hcmut.edu.vn
- GitHub: github.com/BboyBax

## Thành viên
- Hà Trọng Sơn
- Nguyễn Hoàng Minh Phú
- Lê Thanh Phong 
- Lê Nguyễn Minh Quân
- Nguyễn Đức Phúc

## 


