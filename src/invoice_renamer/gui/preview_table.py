"""预览表格组件"""
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Optional


class PreviewTable(ttk.Frame):
    """预览表格组件"""
    
    def __init__(self, parent, main_window):
        """初始化预览表格组件"""
        super().__init__(parent)
        
        self.main_window = main_window
        
        # 创建界面组件
        self._create_widgets()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建表格
        self.tree = ttk.Treeview(self, show="headings", selectmode="browse")
        
        # 设置列
        self.tree["columns"] = ("original", "new", "path")
        
        # 设置列标题
        self.tree.heading("original", text="原始文件名")
        self.tree.heading("new", text="新文件名")
        self.tree.heading("path", text="文件路径")
        
        # 设置列宽度
        self.tree.column("original", width=200, minwidth=100)
        self.tree.column("new", width=200, minwidth=100)
        self.tree.column("path", width=400, minwidth=200)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 绑定事件
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
    
    def update_data(self, data: List[tuple]):
        """更新表格数据"""
        # 清空表格
        self.tree.delete(*self.tree.get_children())
        
        # 插入数据
        for original_name, new_name, file_path in data:
            self.tree.insert("", tk.END, values=(original_name, new_name, file_path))
    
    def clear(self):
        """清空表格"""
        self.tree.delete(*self.tree.get_children())
    
    def _on_select(self, event):
        """选择事件处理"""
        # 获取选中的行
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            
            # 这里可以添加选中行的处理逻辑
            # 比如高亮显示对应的文件等