import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services import subject_service, question_service
from utils.docx_reader import DocxReader

class QuestionCreatorWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.current_user = self.parent.current_user
        self.docx_reader = DocxReader()
        self.window = tk.Toplevel(self.parent.root)
        self.setup_ui()
        self.load_subjects()
    
    def setup_ui(self):
        """Thiết lập giao diện người làm đề với scroll toàn màn hình"""
        self.window.title("Người làm đề - Hệ thống Quản lý Đề thi")
        self.window.geometry("900x700")

        # Canvas + Scrollbar
        canvas = tk.Canvas(self.window, borderwidth=0)
        vscroll = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        vscroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame chính trong canvas
        main_frame = ttk.Frame(canvas)
        self.main_frame = main_frame
        main_frame_id = canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        main_frame.bind("<Configure>", on_frame_configure)

        def on_canvas_configure(event):
            canvas.itemconfig(main_frame_id, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        user_info = self.current_user
        ttk.Label(header_frame, text=f"Chào mừng: {user_info['full_name']}", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Đăng xuất", 
                  command=self.logout).pack(side=tk.RIGHT)
        
        # Frame chọn môn học
        subject_frame = ttk.LabelFrame(main_frame, text="Chọn môn học", padding="10")
        subject_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(subject_frame, text="Môn học:").grid(row=0, column=0, sticky="w")
        
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(subject_frame, textvariable=self.subject_var, 
                                         state="readonly", width=30)
        self.subject_combo.grid(row=0, column=1, padx=(10, 0), sticky="w")
        
        # Frame upload file
        upload_frame = ttk.LabelFrame(main_frame, text="Upload file .docx", padding="10")
        upload_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50).grid(row=0, column=0, sticky="ew")
        
        ttk.Button(upload_frame, text="Chọn file", 
                  command=self.select_file).grid(row=0, column=1, padx=(10, 0))
        
        ttk.Button(upload_frame, text="Đọc file", 
                  command=self.read_file).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Frame hướng dẫn
        guide_frame = ttk.LabelFrame(main_frame, text="Hướng dẫn định dạng", padding="10")
        guide_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        guide_text = self.docx_reader.get_template_instructions()
        guide_label = ttk.Label(guide_frame, text=guide_text, justify=tk.LEFT)
        guide_label.grid(row=0, column=0, sticky="w")

        # Frame thống kê
        stats_frame = ttk.LabelFrame(main_frame, text="Thống kê câu hỏi", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        # Treeview cho thống kê
        columns = ("Môn học", "Tổng câu hỏi", "Dễ", "Trung bình", "Khó")
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, show="headings", height=5)
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=100)
        self.stats_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar dọc
        scrollbar_y = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.stats_tree.configure(yscrollcommand=scrollbar_y.set)

        # Scrollbar ngang
        scrollbar_x = ttk.Scrollbar(stats_frame, orient="horizontal", command=self.stats_tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.stats_tree.configure(xscrollcommand=scrollbar_x.set)

        # Cấu hình grid cho stats_frame
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)

        # Nút refresh thống kê
        ttk.Button(stats_frame, text="Làm mới thống kê",
                  command=self.load_statistics).grid(row=1, column=0, pady=10)

        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        upload_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(0, weight=1)
        # Gọi load_statistics để auto load dữ liệu khi mở cửa sổ
        self.load_statistics()
        self.stats_tree.bind('<Double-1>', self.on_stats_tree_double_click)

    def on_stats_tree_double_click(self, event):
        selected = self.stats_tree.selection()
        if not selected:
            return
        item = self.stats_tree.item(selected[0])
        subject_name = item['values'][0]
        subject_id = self.subject_dict.get(subject_name)
        if subject_id:
            from gui.question_list_window import QuestionListWindow
            QuestionListWindow(self.window, subject_id, subject_name)
    
    def load_subjects(self):
        """Tải danh sách môn học"""
        try:
            subjects = subject_service.get_subjects()
            
            subject_dict = {}
            subject_names = []
            
            for subject in subjects:
                subject_dict[subject['name']] = subject['id']
                subject_names.append(subject['name'])
            
            self.subject_combo['values'] = subject_names
            self.subject_dict = subject_dict
            
            if subject_names:
                self.subject_combo.set(subject_names[0])
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {str(e)}")
    
    def select_file(self):
        """Chọn file .docx"""
        file_path = filedialog.askopenfilename(
            title="Chọn file .docx",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
    
    def read_file(self):
        """Đọc file .docx và import câu hỏi"""
        file_path = self.file_path_var.get().strip()
        subject_name = self.subject_var.get()
        
        if not file_path or not subject_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file và môn học!")
            return
        
        subject_id = self.subject_dict.get(subject_name)
        
        try:
            # Đọc file .docx và import từng câu hỏi qua question_service.create_question
            # Sử dụng hàm read_docx_file đúng signature
            success, message = self.docx_reader.read_docx_file(file_path, subject_id, self.current_user['id'])
            if success:
                messagebox.showinfo("Thành công", message)
                self.file_path_var.set("")  # Xóa đường dẫn file
                self.load_statistics()  # Cập nhật thống kê
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể import câu hỏi: {str(e)}")
    
    def load_statistics(self):
        try:
            subjects = subject_service.get_subjects()
            # Xóa dữ liệu cũ
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            for subject in subjects:
                questions = question_service.get_questions(subject['id'])
                total = len(questions)
                easy = sum(1 for q in questions if q.get('difficulty_level') == 'easy')
                medium = sum(1 for q in questions if q.get('difficulty_level') == 'medium')
                hard = sum(1 for q in questions if q.get('difficulty_level') == 'hard')
                self.stats_tree.insert("", "end", values=(
                    subject['name'], total, easy, medium, hard
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải thống kê: {str(e)}")
    
    def logout(self):
        self.parent.current_user = None
        self.window.destroy()
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!") 