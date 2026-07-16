"""
Script nâng khối lớp năm học mới
- Xóa toàn bộ học sinh Lớp 12 và dữ liệu liên quan
- Tăng khối lớp còn lại lên 1 (Lớp 6→7, Lớp 7→8, ...)
Chạy: python upgrade_grades.py
"""

import sqlite3
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_DB = os.path.join(BASE_DIR, 'instance', 'students.db')
ATTENDANCE_DB = os.path.join(BASE_DIR, 'instance', 'attendance.db')

def get_tables(conn):
    return [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

def main():
    print("=" * 60)
    print(f"Bat dau nang khoi lop - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    if not os.path.exists(STUDENTS_DB):
        print(f"LOI: Khong tim thay {STUDENTS_DB}")
        return
    if not os.path.exists(ATTENDANCE_DB):
        print(f"LOI: Khong tim thay {ATTENDANCE_DB}")
        return

    sconn = sqlite3.connect(STUDENTS_DB)
    aconn = sqlite3.connect(ATTENDANCE_DB)
    s_tables = get_tables(sconn)
    a_tables = get_tables(aconn)
    print(f"Tables trong students.db : {s_tables}")
    print(f"Tables trong attendance.db: {a_tables}")

    # ─── BƯỚC 1: Xem tổng quan khối lớp hiện tại ────────────────
    print("\n[BUOC 1] Khoi lop hien tai:")
    rows = sconn.execute("SELECT grade, COUNT(*) FROM student GROUP BY grade ORDER BY grade").fetchall()
    for grade, count in rows:
        print(f"  {grade}: {count} hoc sinh")

    # ─── BƯỚC 2: Xóa Lớp 12 ─────────────────────────────────────
    print("\n[BUOC 2] Xoa Lop 12...")
    grade12_ids = [r[0] for r in sconn.execute("SELECT id FROM student WHERE grade='Lớp 12'").fetchall()]
    print(f"  Tim thay {len(grade12_ids)} hoc sinh Lop 12: {grade12_ids}")

    if grade12_ids:
        ph = ','.join('?' * len(grade12_ids))

        # Xóa trong students.db
        if 'schedule' in s_tables:
            c = sconn.execute(f'DELETE FROM schedule WHERE student_id IN ({ph})', grade12_ids).rowcount
            print(f"  - Da xoa {c} schedule records")
        if 'tuition' in s_tables:
            c = sconn.execute(f'DELETE FROM tuition WHERE student_id IN ({ph})', grade12_ids).rowcount
            print(f"  - Da xoa {c} tuition records (students.db)")
        c = sconn.execute(f'DELETE FROM student WHERE id IN ({ph})', grade12_ids).rowcount
        print(f"  - Da xoa {c} hoc sinh khoi students.db")
        sconn.commit()

        # Xóa trong attendance.db
        if 'attendance' in a_tables:
            c = aconn.execute(f'DELETE FROM attendance WHERE student_id IN ({ph})', grade12_ids).rowcount
            print(f"  - Da xoa {c} attendance records")
        if 'tuition' in a_tables:
            c = aconn.execute(f'DELETE FROM tuition WHERE student_id IN ({ph})', grade12_ids).rowcount
            print(f"  - Da xoa {c} tuition records (attendance.db)")
        if 'teacher_student_assignment' in a_tables:
            c = aconn.execute(f'DELETE FROM teacher_student_assignment WHERE student_id IN ({ph})', grade12_ids).rowcount
            print(f"  - Da xoa {c} teacher_student_assignment records")
        aconn.commit()
    else:
        print("  Khong co hoc sinh Lop 12, bo qua.")

    # ─── BƯỚC 3: Nâng khối lớp ──────────────────────────────────
    print("\n[BUOC 3] Nang khoi lop...")

    # Lấy danh sách các lớp còn lại, sắp xếp GIẢM DẦN để tránh xung đột
    grades = sconn.execute(
        "SELECT DISTINCT grade FROM student WHERE grade LIKE 'L%' ORDER BY grade DESC"
    ).fetchall()

    total_updated = 0
    for (grade,) in grades:
        match = re.search(r'\d+', grade)
        if not match:
            print(f"  Bo qua grade khong xac dinh: '{grade}'")
            continue
        old_num = int(match.group())
        new_num = old_num + 1
        new_grade = f'Lớp {new_num}'
        count = sconn.execute(
            "UPDATE student SET grade=? WHERE grade=?", (new_grade, grade)
        ).rowcount
        sconn.commit()
        print(f"  Lop {old_num} -> Lop {new_num}: cap nhat {count} hoc sinh")
        total_updated += count

    print(f"\n  Tong cong: {total_updated} hoc sinh da duoc nang khoi.")

    # ─── BƯỚC 4: Kết quả sau khi cập nhật ───────────────────────
    print("\n[BUOC 4] Khoi lop sau khi cap nhat:")
    rows = sconn.execute("SELECT grade, COUNT(*) FROM student GROUP BY grade ORDER BY grade").fetchall()
    for grade, count in rows:
        print(f"  {grade}: {count} hoc sinh")

    sconn.close()
    aconn.close()

    print("\n" + "=" * 60)
    print("HOAN THANH!")
    print("=" * 60)

if __name__ == '__main__':
    main()
