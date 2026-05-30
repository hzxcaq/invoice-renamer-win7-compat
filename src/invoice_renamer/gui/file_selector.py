"""文件选择器组件"""
import tkinter as tk
from tkinter import ttk, filedialog
import os
from typing import Optional, Callable


class FileSelector(ttk.Frame):
    """文件选择器组件"""
    
    def __init__(self, parent, main_window):
        """初始化文件选择器"""
        super().__init__(parent)
        
        self.main_window = main_window
        
        # 创建界面组件
        self._create_widgets()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 目录选择区域
        dir_frame = ttk.Frame(self)
        dir_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(dir_frame, text="发票目录:").pack(side=tk.LEFT)
        
        self.dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var, state="readonly")
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.dir_button = ttk.Button(dir_frame, text="选择目录", command=self._select_directory)
        self.dir_button.pack(side=tk.RIGHT)
        
        # Excel文件选择区域
        excel_frame = ttk.Frame(self)
        excel_frame.pack(fill=tk.X)
        
        ttk.Label(excel_frame, text="Excel文件:").pack(side=tk.LEFT)
        
        self.excel_var = tk.StringVar()
        self.excel_entry = ttk.Entry(excel_frame, textvariable=self.excel_var, state="readonly")
        self.excel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.excel_button = ttk.Button(excel_frame, text="选择Excel", command=self._select_excel)
        self.excel_button.pack(side=tk.RIGHT)
        
        # 清除Excel按钮
        self.clear_excel_button = ttk.Button(excel_frame, text="清除", command=self._clear_excel)
        self.clear_excel_button.pack(side=tk.RIGHT, padx=(5, 0))
    
    def _select_directory(self):
        """选择目录"""
        directory = filedialog.askdirectory(title="选择发票目录")
        
        if directory:
            self.dir_var.set(directory)
            self.main_window.set_directory(directory)
    
    def _select_excel(self):
        """选择Excel文件"""
        excel_file = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        
        if excel_file:
            self.excel_var.set(excel_file)
            self.main_window.set_excel_file(excel_file)
    
    def _clear_excel(self):
        """清除Excel文件"""
        self.excel_var.set("")
        self.main_window.current_excel_file = None
        self.main_window.excel_data = []
        self.main_window.excel_headers = []
        
        # 清除Excel预览
        self.main_window.excel_viewer.clear()
        
        # 清除格式构建器
        self.main_window.format_builder.clear()
        
        # 更新按钮状态
        self.main_window._update_button_states()