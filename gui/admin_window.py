import tkinter as tk
from tkinter import ttk, messagebox
from services import user_service
from gui.exam_generator_window import ExamGeneratorWindow

class AdminWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.current_user = self.parent.current_user
        self.window = tk.Toplevel(self.parent.root)
        self.window.title("Trang chủ Quản trị viên - Hệ thống Quản lý Đề thi")
        self.window.geometry("600x400")
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="30")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text=f"Xin chào, Quản trị viên: {self.current_user['full_name']}", font=("Arial", 16, "bold")).pack(pady=(0, 30))
        
        btn_user = ttk.Button(main_frame, text="Quản lý người dùng", command=self.open_user_management, width=30)
        btn_user.pack(pady=10)
        
        btn_exam = ttk.Button(main_frame, text="Quản lý đề thi", command=self.open_exam_management, width=30)
        btn_exam.pack(pady=10)
        
        btn_logout = ttk.Button(main_frame, text="Đăng xuất", command=self.logout, width=30)
        btn_logout.pack(pady=30)
    
    def open_user_management(self):
        UserManagementWindow(self)
    
    def open_exam_management(self):
        ExamGeneratorWindow(self, None)
    
    def logout(self):
        self.parent.current_user = None
        self.window.destroy()
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!")

# Tách phần quản lý người dùng thành class riêng
class UserManagementWindow:
    def __init__(self, parent):
        self.parent = parent  # parent phải có current_user
        self.window = tk.Toplevel(parent.window if hasattr(parent, 'window') else parent)
        self.window.title("Quản lý người dùng")
        self.window.geometry("1000x700")
        self.setup_ui()
        self.load_users()
    
    def setup_ui(self):
        """Thiết lập giao diện admin"""
        self.window.title("Quản trị hệ thống - Hệ thống Quản lý Đề thi")
        self.window.geometry("1000x700")
        
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        user_info = self.parent.current_user
        ttk.Label(header_frame, text=f"Chào mừng Admin: {user_info['full_name']}", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Đăng xuất", 
                  command=self.logout).pack(side=tk.RIGHT)
        
        # Frame quản lý người dùng
        users_frame = ttk.LabelFrame(main_frame, text="Quản lý người dùng", padding="10")
        users_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Treeview cho danh sách người dùng
        columns = ("ID", "Tên đăng nhập", "Họ tên", "Vai trò", "Ngày tạo")
        self.users_tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)
        
        self.users_tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=self.users_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame nút chức năng
        button_frame = ttk.Frame(users_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Thêm người dùng", 
                  command=self.add_user).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Sửa người dùng", 
                  command=self.edit_user).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Đổi mật khẩu", 
                  command=self.change_password).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Xóa người dùng", 
                  command=self.delete_user).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Làm mới", 
                  command=self.load_users).pack(side=tk.RIGHT)
        
        # Cấu hình grid
        users_frame.columnconfigure(0, weight=1)
        users_frame.rowconfigure(0, weight=1)
        
        # Bind events
        self.users_tree.bind("<Double-1>", lambda e: self.edit_user())
    
    def load_users(self):
        """Tải danh sách người dùng"""
        try:
            users = user_service.get_users()
            
            # Xóa dữ liệu cũ
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Thêm dữ liệu mới
            for user in users:
                created_at = user.get('created_at')
                if isinstance(created_at, str):
                    try:
                        import datetime
                        created_date = datetime.datetime.fromisoformat(created_at).strftime('%d/%m/%Y %H:%M')
                    except Exception:
                        created_date = created_at
                else:
                    created_date = created_at.strftime('%d/%m/%Y %H:%M')
                
                role_display = {
                    'student': 'Học sinh',
                    'question_creator': 'Người làm đề',
                    'exam_generator': 'Người sinh đề',
                    'admin': 'Quản trị viên'
                }.get(user['role'], user['role'])
                
                self.users_tree.insert("", "end", values=(
                    user['id'],
                    user['username'],
                    user['full_name'],
                    role_display,
                    created_date
                ), tags=(user['id'],))
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách người dùng: {str(e)}")
    
    def get_selected_user_id(self):
        """Lấy ID người dùng được chọn"""
        selection = self.users_tree.selection()
        if not selection:
            return None
        item = self.users_tree.item(selection[0])
        return item['tags'][0]
    
    def add_user(self):
        """Thêm người dùng mới"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Thêm người dùng mới")
        dialog.geometry("400x350")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Form fields
        ttk.Label(frame, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w", pady=5)
        username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=username_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Mật khẩu:").grid(row=1, column=0, sticky="w", pady=5)
        password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=password_var, show="*", width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Họ tên:").grid(row=2, column=0, sticky="w", pady=5)
        fullname_var = tk.StringVar()
        ttk.Entry(frame, textvariable=fullname_var, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Vai trò:").grid(row=3, column=0, sticky="w", pady=5)
        role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(frame, textvariable=role_var, 
                                 values=["student", "question_creator", "exam_generator", "admin"],
                                 state="readonly", width=27)
        role_combo.grid(row=3, column=1, pady=5)
        
        def save():
            username = username_var.get().strip()
            password = password_var.get().strip()
            fullname = fullname_var.get().strip()
            role = role_var.get()
            
            if not all([username, password, fullname, role]):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            try:
                user_service.create_user(username, password, fullname, role)
                messagebox.showinfo("Thành công", "Đã thêm người dùng mới!")
                dialog.destroy()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm người dùng: {str(e)}")
        
        ttk.Button(frame, text="Lưu", command=save).grid(row=4, column=0, columnspan=2, pady=20)
    
    def edit_user(self):
        """Sửa thông tin người dùng"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng để sửa!")
            return
        
        try:
            user = user_service.get_user(user_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin người dùng: {str(e)}")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Sửa thông tin người dùng")
        dialog.geometry("400x300")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Form fields
        ttk.Label(frame, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w", pady=5)
        username_var = tk.StringVar(value=user['username'])
        ttk.Entry(frame, textvariable=username_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Họ tên:").grid(row=1, column=0, sticky="w", pady=5)
        fullname_var = tk.StringVar(value=user['full_name'])
        ttk.Entry(frame, textvariable=fullname_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Vai trò:").grid(row=2, column=0, sticky="w", pady=5)
        role_var = tk.StringVar(value=user['role'])
        role_combo = ttk.Combobox(frame, textvariable=role_var, 
                                 values=["student", "question_creator", "exam_generator", "admin"],
                                 state="readonly", width=27)
        role_combo.grid(row=2, column=1, pady=5)
        
        def save():
            username = username_var.get().strip()
            fullname = fullname_var.get().strip()
            role = role_var.get()
            
            if not all([username, fullname, role]):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            try:
                user_service.update_user(user_id, {
                    "username": username,
                    "full_name": fullname,
                    "role": role
                })
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin người dùng!")
                dialog.destroy()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")
        
        ttk.Button(frame, text="Lưu", command=save).grid(row=3, column=0, columnspan=2, pady=20)
    
    def change_password(self):
        """Đổi mật khẩu người dùng"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng để đổi mật khẩu!")
            return
        
        try:
            user = user_service.get_user(user_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin người dùng: {str(e)}")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Đổi mật khẩu - {user['username']}")
        dialog.geometry("400x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text=f"Đổi mật khẩu cho: {user['full_name']}").pack(pady=(0, 10))
        
        ttk.Label(frame, text="Mật khẩu mới:").pack(anchor="w")
        password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=password_var, show="*", width=30).pack(pady=5)
        
        ttk.Label(frame, text="Xác nhận mật khẩu:").pack(anchor="w")
        confirm_var = tk.StringVar()
        ttk.Entry(frame, textvariable=confirm_var, show="*", width=30).pack(pady=5)
        
        def save():
            password = password_var.get().strip()
            confirm = confirm_var.get().strip()
            
            if not password:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập mật khẩu mới!")
                return
            
            if password != confirm:
                messagebox.showwarning("Cảnh báo", "Mật khẩu xác nhận không khớp!")
                return
            
            try:
                user_service.change_password(user_id, password)
                messagebox.showinfo("Thành công", "Đã đổi mật khẩu!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đổi mật khẩu: {str(e)}")
        
        ttk.Button(frame, text="Lưu", command=save).pack(pady=20)
    
    def delete_user(self):
        """Xóa người dùng"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng để xóa!")
            return
        
        try:
            user = user_service.get_user(user_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin người dùng: {str(e)}")
            return
        
        result = messagebox.askyesno("Xác nhận", 
                                   f"Bạn có chắc chắn muốn xóa người dùng {user['full_name']}?\n"
                                   f"Tên đăng nhập: {user['username']}")
        
        if result:
            try:
                user_service.delete_user(user_id)
                messagebox.showinfo("Thành công", "Đã xóa người dùng!")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa người dùng: {str(e)}")
    
    def logout(self):
        self.parent.current_user = None
        self.window.destroy()
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!") 