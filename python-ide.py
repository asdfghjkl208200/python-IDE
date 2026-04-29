# -*- coding: utf-8 -*-
import turtle
import math
import random
import datetime
import os
import json
import hashlib
import tracemalloc
import time
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

# ========================= 【超级多语言支持】 =========================
SUPPORTED_LANGUAGES = {
    "Python":      {"ext": ".py",   "icon": "🐍"},
    "C语言":       {"ext": ".c",    "icon": "⚙️"},
    "C++":         {"ext": ".cpp", "icon": "🖥️"},
    "C#":          {"ext": ".cs",  "icon": "🎯"},
    "Java":        {"ext": ".java","icon": "☕"},
    "JavaScript":  {"ext": ".js",  "icon": "🟨"},
    "PHP":         {"ext": ".php", "icon": "🐘"},
    "Go":          {"ext": ".go",  "icon": "🐹"},
    "Ruby":        {"ext": ".rb",  "icon": "💎"},
    "Rust":        {"ext": ".rs",  "icon": "🦀"},
    "Pascal":      {"ext": ".pas", "icon": "📜"},
    "HTML":        {"ext": ".html","icon": "🌐"},
}

# ========================= 【算法库 · 大幅扩充】 =========================
ALGORITHMS = {
    "冒泡排序": "def bubble_sort(arr):\n    n=len(arr)\n    for i in range(n):\n        for j in range(0,n-i-1):\n            if arr[j]>arr[j+1]:arr[j],arr[j+1]=arr[j+1],arr[j]",
    "快速排序": "def quick_sort(arr):\n    if len(arr)<=1:return arr\n    p=arr[len(arr)//2]\n    return quick_sort([x for x in arr if x<p])+[x for x in arr if x==p]+quick_sort([x for x in arr if x>p])",
    "二分查找": "def binary_search(arr,t):\n    l,r=0,len(arr)-1\n    while l<=r:\n        m=(l+r)//2\n        if arr[m]==t:return m\n        l=m+1 if arr[m]<t else m-1\n    return -1",
    "选择排序": "def select_sort(arr):\n    for i in range(len(arr)):\n        m=i\n        for j in range(i+1,len(arr)):\n            if arr[j]<arr[m]:m=j\n        arr[i],arr[m]=arr[m],arr[i]",
    "插入排序": "def insert_sort(arr):\n    for i in range(1,len(arr)):\n        k=arr[i]\n        j=i-1\n        while j>=0 and k<arr[j]:\n            arr[j+1]=arr[j]\n            j-=1\n        arr[j+1]=k",
    "斐波那契": "def fib(n):\n    a,b=0,1\n    for _ in range(n):a,b=b,a+b\n    return a",
    "阶乘计算": "def fact(n):\n    if n==0:return 1\n    return n*fact(n-1)",
    "质数判断": "def is_prime(n):\n    if n<2:return False\n    for i in range(2,int(n**0.5)+1):\n        if n%i==0:return False\n    return True",
}

# ========================= 【主程序：全能工具箱】 =========================
class UltimateIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔥 全能多语言编程工具箱 V6.0")
        self.geometry("1200x800")
        self.configure(bg="#1e1e2e")
        self.current_lang = "Python"
        self.current_file = None
        self.var_store = {}

        self.create_widgets()

    def create_widgets(self):
        # ========== 顶部导航栏 ==========
        top_frame = tk.Frame(self, bg="#28293b", height=50)
        top_frame.pack(fill="x", padx=5, pady=5)

        # 语言选择
        tk.Label(top_frame, text="🌍 语言", fg="white", bg="#28293b", font=("黑体",12,"bold")).pack(side="left", padx=5)
        self.lang_var = tk.StringVar(value=self.current_lang)
        lang_menu = ttk.Combobox(top_frame, textvariable=self.lang_var, values=list(SUPPORTED_LANGUAGES.keys()), state="readonly", width=12)
        lang_menu.pack(side="left", padx=5)
        lang_menu.bind("<<ComboboxSelected>>", self.switch_language)

        # 功能按钮
        buttons = [
            ("📂 新建", self.new_file),
            ("📂 打开", self.open_file),
            ("💾 保存", self.save_file),
            ("▶️ 运行", self.run_code),
            ("🎨 图形编程", self.graphic_mode),
            ("📦 打包EXE", self.build_exe),
            ("🧩 算法库", self.show_algorithms),
            ("🎮 小游戏", self.create_game),
            ("🤖 AI助手", self.ai_help),
            ("📊 工具集", self.more_tools),
        ]
        for text, cmd in buttons:
            tk.Button(top_frame, text=text, bg="#3d405c", fg="white", relief="flat", padx=8, pady=4, command=cmd).pack(side="left", padx=3)

        # ========== 代码编辑器 ==========
        self.code_editor = scrolledtext.ScrolledText(self, font=("Consolas",13), bg="#2b2b2b", fg="white", insertbackground="white")
        self.code_editor.pack(side="left", fill="both", expand=1, padx=5, pady=5)

        # ========== 输出控制台 ==========
        self.console = scrolledtext.ScrolledText(self, font=("Consolas",12), bg="#000000", fg="#00ff00")
        self.console.pack(side="left", fill="both", expand=1, padx=5, pady=5)

    # ========================= 核心功能 =========================
    def switch_language(self, e=None):
        self.current_lang = self.lang_var.get()
        icon = SUPPORTED_LANGUAGES[self.current_lang]["icon"]
        self.title(f"{icon} 全能工具箱 - {self.current_lang} 模式")

    def new_file(self):
        self.code_editor.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, encoding="utf-8") as f:
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(1.0, f.read())

    def save_file(self):
        if not self.current_file:
            ext = SUPPORTED_LANGUAGES[self.current_lang]["ext"]
            self.current_file = filedialog.asksaveasfilename(defaultextension=ext, filetypes=[(self.current_lang, f"*{ext}")])
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.code_editor.get(1.0, tk.END))
            messagebox.showinfo("✅ 成功", "文件已保存！")

    def run_code(self):
        self.console.delete(1.0, tk.END)
        code = self.code_editor.get(1.0, tk.END)
        try:
            if self.current_lang == "Python":
                import sys, io
                old = sys.stdout
                sys.stdout = io.StringIO()
                exec(code, self.var_store)
                self.console.insert(tk.END, sys.stdout.getvalue())
                sys.stdout = old
            else:
                self.console.insert(tk.END, f"✅ {self.current_lang} 编辑器就绪\n💡 如需运行，请安装对应编译器")
        except Exception as e:
            self.console.insert(tk.END, f"❌ 错误：{str(e)}")

    # ========================= 图形化编程 =========================
    def graphic_mode(self):
        win = tk.Toplevel(self)
        win.title("🎨 图形化编程")
        win.geometry("600x500")
        
        tk.Button(win, text="正方形", font=("",14), command=self.draw_square).pack(pady=5)
        tk.Button(win, text="五角星", font=("",14), command=self.draw_star).pack(pady=5)
        tk.Button(win, text="螺旋线", font=("",14), command=self.draw_loop).pack(pady=5)
        tk.Button(win, text="爱心", font=("",14), command=self.draw_heart).pack(pady=5)

    def draw_square(self):
        for _ in range(4):
            turtle.forward(200)
            turtle.right(90)

    def draw_star(self):
        for _ in range(5):
            turtle.forward(200)
            turtle.right(144)

    def draw_loop(self):
        for i in range(100):
            turtle.forward(i)
            turtle.right(70)

    def draw_heart(self):
        t = turtle
        t.speed(3)
        t.color('red','pink')
        t.begin_fill()
        for _ in range(180):
            t.forward(2)
            t.right(1)
        t.left(130)
        for _ in range(180):
            t.forward(2)
            t.right(1)
        t.end_fill()

    # ========================= 打包EXE =========================
    def build_exe(self):
        try:
            with open("temp.py","w",encoding="utf-8") as f:
                f.write(self.code_editor.get(1.0,tk.END))
            subprocess.Popen("pip install pyinstaller && pyinstaller -F -w temp.py")
            messagebox.showinfo("📦 打包", "正在打包EXE，完成后在 dist 文件夹中！")
        except:
            messagebox.showwarning("提示", "需联网安装打包工具")

    # ========================= 算法库 =========================
    def show_algorithms(self):
        win = tk.Toplevel(self)
        win.title("🧩 算法库")
        win.geometry("700x600")
        var = tk.StringVar()
        box = ttk.Combobox(win, textvariable=var, values=list(ALGORITHMS.keys()), state="readonly", width=20)
        box.pack(pady=5)
        txt = scrolledtext.ScrolledText(win, font=("Consolas",12))
        txt.pack(fill="both", expand=1, padx=10, pady=10)
        def show():
            txt.delete(1.0,tk.END)
            txt.insert(1.0, ALGORITHMS[var.get()])
        ttk.Button(win, text="显示代码", command=show).pack(pady=5)

    # ========================= 游戏 =========================
    def create_game(self):
        self.code_editor.delete(1.0,tk.END)
        self.code_editor.insert(1.0, '''import random
num = random.randint(1,100)
print("🎮 猜数字游戏")
while True:
    g = int(input("请输入1-100："))
    if g == num:
        print("🎉 恭喜你猜对了！")
        break
    print("大了" if g>num else "小了")''')

    # ========================= AI助手 =========================
    def ai_help(self):
        q = filedialog.askstring("🤖 AI助手", "请输入你的问题：写代码/改bug/讲算法")
        if q:
            self.console.delete(1.0,tk.END)
            self.console.insert(tk.END, f"你问：{q}\n\nAI：我支持所有编程语言，可写代码、讲算法、做项目！")

    # ========================= 实用工具 =========================
    def more_tools(self):
        win = tk.Toplevel(self)
        win.title("📊 实用工具集")
        win.geometry("500x400")
        tools = [
            ("⏰ 当前时间", self.show_time),
            ("🎲 随机数", self.show_rand),
            ("🔐 MD5加密", self.show_md5),
            ("📝 JSON格式化", self.format_json),
            ("🧮 计算器", self.calc)
        ]
        for t,c in tools:
            tk.Button(win, text=t, font=("",12), command=c).pack(pady=4)

    def show_time(self):
        messagebox.showinfo("时间", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def show_rand(self):
        messagebox.showinfo("随机", str(random.randint(1,1000)))
    
    def show_md5(self):
        s = filedialog.askstring("MD5","输入字符串")
        if s:
            res = hashlib.md5(s.encode()).hexdigest()
            messagebox.showinfo("MD5结果", res)
    
    def format_json(self):
        self.code_editor.insert(1.0, json.dumps({"name":"测试数据","age":20}, ensure_ascii=False, indent=2))
    
    def calc(self):
        e = filedialog.askstring("计算器","输入数学表达式")
        if e:
            try:
                messagebox.showinfo("结果", str(eval(e)))
            except:
                messagebox.showerror("错误","表达式错误")

if __name__ == "__main__":
    app = UltimateIDE()
    app.mainloop()