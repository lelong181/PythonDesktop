import tkinter as tk
from tkinter import ttk, messagebox
from services import user_service

class LoginWindow:
    def __init__(self, parent):
        self.parent = parent  # parent là instance của ExamBankApp
        self.window = tk.Toplevel(self.parent.root)
        self.window.title("Đăng nhập")
        self.window.geometry("350x220")
        self.window.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var).grid(row=0, column=1, pady=(0, 10))

        ttk.Label(frame, text="Mật khẩu:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=(0, 10))

        self.login_btn = ttk.Button(frame, text="Đăng nhập", command=self.login)
        self.login_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.window.bind('<Return>', lambda e: self.login())

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        try:
            user = user_service.login(username, password)
            self.parent.current_user = user
            messagebox.showinfo("Thành công", f"Đăng nhập thành công! Xin chào {user['full_name']}")
            self.window.destroy()
            self.parent.show_main_window_after_login()
        except Exception as e:
            messagebox.showerror("Lỗi đăng nhập", str(e))