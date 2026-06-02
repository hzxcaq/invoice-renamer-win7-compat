"""Excel预览组件"""
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Optional


class ExcelViewer(ttk.Frame):
    """Excel预览组件"""
    
    def __init__(self, parent, main_window):
        """初始化Excel预览组件"""
        super().__init__(parent)
        
        self.main_window = main_window
        
        # 创建界面组件
        self._create_widgets()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建表格，设置默认显示10行
        self.tree = ttk.Treeview(self, show="headings", selectmode="browse", height=10)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 布局
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
    
    def update_data(self, headers: List[str], data: List[Dict[str, Any]]):
        """更新表格数据"""
        # 清空表格
        self.tree.delete(*self.tree.get_children())
        
        # 清除列
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        
        # 设置列
        self.tree["columns"] = headers
        
        # 设置列标题和宽度
        for i, header in enumerate(headers):
            self.tree.heading(header, text=header)
            # 根据内容设置列宽，限制最大宽度为160px，最小宽度为80px
            width = min(160, max(80, len(header) * 10))
            self.tree.column(header, width=width, minwidth=50)
        
        # 插入数据
        for row_idx, row_data in enumerate(data):
            values = [row_data.get(header, "") for header in headers]
            self.tree.insert("", tk.END, values=values)
    
    def clear(self):
        """清空表格"""
        self.tree.delete(*self.tree.get_children())
        
        # 清除列
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        
        self.tree["columns"] = ()
    
    def _on_select(self, event):
        """选择事件处理"""
        # 获取选中的行
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            
            # 这里可以添加选中行的处理逻辑
            # 比如高亮显示对应的PDF文件等