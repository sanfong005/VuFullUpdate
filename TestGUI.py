import tkinter as tk
from tkinter import messagebox
import re
import requests
import os

# ฟังก์ชันสำหรับสแกนช่องโหว่ SQL Injection
def detect_sql_injection(code):
    sql_patterns = [
        r'\bSELECT\b.*\bFROM\b',
        r'\bINSERT\b.*\bINTO\b',
        r'\bUPDATE\b.*\bSET\b',
        r'\bDELETE\b.*\bFROM\b',
        r'\bWHERE\b.*=.*'
    ]
    for pattern in sql_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return f"พบความเป็นไปได้ของ SQL Injection: {pattern}"
    return "ไม่พบ SQL Injection"

# ฟังก์ชันสำหรับสแกน URL
def scan_url():
    url = url_entry.get().strip()

    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    try:
        response = requests.get(url)
        if response.status_code == 200:
            result_text.insert(tk.END, f"การเชื่อมต่อสำเร็จ: {url}\n")
            # ตรงนี้สามารถเพิ่มการติดตามลิงก์ หรือทำงานสแกนลึกๆ ได้ตามฟังก์ชันที่คุณมี
            result_text.insert(tk.END, "การสแกน URL เริ่มขึ้น...\n")
        else:
            result_text.insert(tk.END, "การเชื่อมต่อไม่สำเร็จ\n")
    except requests.exceptions.RequestException:
        result_text.insert(tk.END, "ไม่สามารถเชื่อมต่อกับเว็บไซต์ได้\n")

# ฟังก์ชันสำหรับการสแกน SQL Injection
def scan_sql():
    code_to_scan = code_entry.get("1.0", tk.END)
    result = detect_sql_injection(code_to_scan)
    result_text.insert(tk.END, result + "\n")

# ฟังก์ชันสำหรับการล้างผลลัพธ์
def clear_results():
    result_text.delete("1.0", tk.END)

# ฟังก์ชันสำหรับการแสดงข้อความ About
def show_about():
    messagebox.showinfo("About", "โปรแกรมนี้เป็นเครื่องมือสำหรับสแกนหาช่องโหว่ SQL Injection และ URL ภายในเว็บไซต์")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Vulnerability Scanner Tool")
root.geometry("600x400")

# กรอบ URL
url_frame = tk.Frame(root)
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="ใส่ URL:")
url_label.pack(side=tk.LEFT)

url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT, padx=5)

scan_url_button = tk.Button(url_frame, text="สแกน URL", command=scan_url)
scan_url_button.pack(side=tk.LEFT)

# กรอบ SQL Injection
sql_frame = tk.Frame(root)
sql_frame.pack(pady=10)

code_label = tk.Label(sql_frame, text="ใส่โค้ดที่ต้องการสแกน SQL:")
code_label.pack()

code_entry = tk.Text(sql_frame, height=5, width=50)
code_entry.pack()

scan_sql_button = tk.Button(sql_frame, text="สแกน SQL Injection", command=scan_sql)
scan_sql_button.pack(pady=5)

# แสดงผลการสแกน
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

result_label = tk.Label(result_frame, text="ผลการสแกน:")
result_label.pack()

result_text = tk.Text(result_frame, height=10, width=70)
result_text.pack()

# ปุ่มล้างผลลัพธ์
clear_button = tk.Button(root, text="ล้างผลลัพธ์", command=clear_results)
clear_button.pack(pady=5)

# เมนู About
menu = tk.Menu(root)
root.config(menu=menu)

help_menu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

root.mainloop()
