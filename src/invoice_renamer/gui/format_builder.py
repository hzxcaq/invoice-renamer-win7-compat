"""格式构建器组件"""
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Optional

# 响应式布局阈值（像素）
RESPONSIVE_THRESHOLD = 1200


class FormatBuilder(ttk.Frame):
    """格式构建器组件"""
    
    def __init__(self, parent, main_window):
        """初始化格式构建器组件"""
        super().__init__(parent)
        
        self.main_window = main_window
        
        # 存储列信息
        self.columns = []
        self.selected_columns = []
        
        # 窗口宽度缓存
        self._last_window_width = 0
        self._configure_after_id = None
        
        # 创建界面组件
        self._create_widgets()
        
        # 绑定主窗口的Configure事件
        self.main_window.bind("<Configure>", self._on_window_configure)
        
        # 延迟设置初始布局，等待窗口显示
        self.after(200, self._update_button_layout)
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.X)
        
        # 使用Grid布局来精确控制三列的宽度
        main_frame.columnconfigure(0, weight=1)  # 可用列区域，可缩放
        main_frame.columnconfigure(1, weight=0)  # 中间按钮区域，固定宽度
        main_frame.columnconfigure(2, weight=2)  # 已选列区域，可缩放
        main_frame.rowconfigure(0, weight=0)
        
        # 左侧：列选择区域
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        ttk.Label(left_frame, text="可用列:").pack(anchor=tk.W)
        
        # 列列表框
        self.columns_listbox = tk.Listbox(left_frame, selectmode=tk.EXTENDED, height=6)
        self.columns_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        columns_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.columns_listbox.yview)
        columns_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.columns_listbox.configure(yscrollcommand=columns_scrollbar.set)
        
        # 中间：操作按钮区域
        middle_frame = ttk.Frame(main_frame)
        middle_frame.grid(row=0, column=1, padx=5)
        
        self.add_button = ttk.Button(middle_frame, text="添加 >>", command=self._add_columns)
        self.add_button.pack(pady=2)
        
        self.remove_button = ttk.Button(middle_frame, text="<< 移除", command=self._remove_columns)
        self.remove_button.pack(pady=2)
        
        self.clear_button = ttk.Button(middle_frame, text="清空", command=self._clear_columns)
        self.clear_button.pack(pady=2)
        
        # 右侧：已选列区域
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky="nsew")
        
        ttk.Label(right_frame, text="已选列 (按顺序):").pack(anchor=tk.W)
        
        # 已选列列表框
        self.selected_listbox = tk.Listbox(right_frame, selectmode=tk.EXTENDED, height=6)
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        selected_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.selected_listbox.yview)
        selected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.selected_listbox.configure(yscrollcommand=selected_scrollbar.set)
        
        # 上移/下移按钮 - 放在右侧框架的底部
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        # 使用网格布局确保按钮始终可见
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        self.up_button = ttk.Button(button_frame, text="上移", command=self._move_up)
        self.down_button = ttk.Button(button_frame, text="下移", command=self._move_down)
        
        # 初始布局将在窗口显示后通过_update_button_layout设置
        
        # 分隔符选择区域
        separator_frame = ttk.Frame(self)
        separator_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(separator_frame, text="分隔符:").pack(side=tk.LEFT)
        
        self.separator_var = tk.StringVar(value="_")
        separator_options = ["_", "-", " ", ".", "无"]
        self.separator_combo = ttk.Combobox(
            separator_frame, 
            textvariable=self.separator_var,
            values=separator_options,
            state="readonly",
            width=10
        )
        self.separator_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        # 格式预览区域
        preview_frame = ttk.Frame(self)
        preview_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(preview_frame, text="格式预览:").pack(side=tk.LEFT)
        
        self.preview_var = tk.StringVar()
        self.preview_entry = ttk.Entry(preview_frame, textvariable=self.preview_var, state="readonly")
        self.preview_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # 绑定事件
        self.columns_listbox.bind("<<ListboxSelect>>", self._on_column_select)
        self.selected_listbox.bind("<<ListboxSelect>>", self._on_selected_select)
        self.separator_combo.bind("<<ComboboxSelected>>", self._on_separator_change)
    
    def update_columns(self, columns: List[str]):
        """更新可用列"""
        self.columns = columns
        
        # 清空列表框
        self.columns_listbox.delete(0, tk.END)
        
        # 添加列
        for column in columns:
            self.columns_listbox.insert(tk.END, column)
    
    def clear(self):
        """清空所有列"""
        self.columns = []
        self.selected_columns = []
        
        # 清空列表框
        self.columns_listbox.delete(0, tk.END)
        self.selected_listbox.delete(0, tk.END)
        
        # 清空预览
        self.preview_var.set("")
        
        # 更新格式模板
        self.main_window.update_format_template("")
    
    def _add_columns(self):
        """添加选中的列"""
        # 获取选中的列
        selection = self.columns_listbox.curselection()
        
        for index in selection:
            column = self.columns_listbox.get(index)
            
            # 避免重复添加
            if column not in self.selected_columns:
                self.selected_columns.append(column)
                self.selected_listbox.insert(tk.END, column)
        
        # 更新格式预览
        self._update_preview()
        
        # 更新格式模板
        self._update_format_template()
    
    def _remove_columns(self):
        """移除选中的列"""
        # 获取选中的列
        selection = self.selected_listbox.curselection()
        
        # 从后往前删除，避免索引问题
        for index in reversed(selection):
            del self.selected_columns[index]
            self.selected_listbox.delete(index)
        
        # 更新格式预览
        self._update_preview()
        
        # 更新格式模板
        self._update_format_template()
    
    def _clear_columns(self):
        """清空已选列"""
        self.selected_columns = []
        self.selected_listbox.delete(0, tk.END)
        
        # 更新格式预览
        self._update_preview()
        
        # 更新格式模板
        self._update_format_template()
    
    def _move_up(self):
        """上移选中的列"""
        selection = self.selected_listbox.curselection()
        
        if not selection:
            return
        
        index = selection[0]
        
        if index == 0:
            return
        
        # 交换位置
        self.selected_columns[index], self.selected_columns[index-1] = \
            self.selected_columns[index-1], self.selected_columns[index]
        
        # 更新列表框
        self.selected_listbox.delete(0, tk.END)
        for column in self.selected_columns:
            self.selected_listbox.insert(tk.END, column)
        
        # 保持选中状态
        self.selected_listbox.selection_set(index-1)
        
        # 更新格式预览
        self._update_preview()
        
        # 更新格式模板
        self._update_format_template()
    
    def _move_down(self):
        """下移选中的列"""
        selection = self.selected_listbox.curselection()
        
        if not selection:
            return
        
        index = selection[0]
        
        if index == len(self.selected_columns) - 1:
            return
        
        # 交换位置
        self.selected_columns[index], self.selected_columns[index+1] = \
            self.selected_columns[index+1], self.selected_columns[index]
        
        # 更新列表框
        self.selected_listbox.delete(0, tk.END)
        for column in self.selected_columns:
            self.selected_listbox.insert(tk.END, column)
        
        # 保持选中状态
        self.selected_listbox.selection_set(index+1)
        
        # 更新格式预览
        self._update_preview()
        
        # 更新格式模板
        self._update_format_template()
    
    def _on_column_select(self, event):
        """列选择事件处理"""
        # 这里可以添加选中列的处理逻辑
        pass
    
    def _on_selected_select(self, event):
        """已选列选择事件处理"""
        # 这里可以添加选中列的处理逻辑
        pass
    
    def _on_separator_change(self, event):
        """分隔符改变事件处理"""
        # 更新格式预览
        self._update_preview()
        
        # 更新格式模板
        self._update_format_template()
    
    def _update_preview(self):
        """更新格式预览"""
        if not self.selected_columns:
            self.preview_var.set("")
            return
        
        # 获取分隔符
        separator = self.separator_var.get()
        if separator == "无":
            separator = ""
        
        # 构建预览格式
        preview = separator.join([f"{{{col}}}" for col in self.selected_columns])
        preview += ".pdf"
        
        self.preview_var.set(preview)
    
    def _update_format_template(self):
        """更新格式模板"""
        if not self.selected_columns:
            self.main_window.update_format_template("")
            return
        
        # 获取分隔符
        separator = self.separator_var.get()
        if separator == "无":
            separator = ""
        
        # 构建格式模板
        template = separator.join([f"{{{col}}}" for col in self.selected_columns])
        template += ".pdf"
        
        # 更新主窗口的格式模板
        self.main_window.update_format_template(template)
    
    def get_format_template(self) -> str:
        """获取格式模板"""
        if not self.selected_columns:
            return ""
        
        # 获取分隔符
        separator = self.separator_var.get()
        if separator == "无":
            separator = ""
        
        # 构建格式模板
        template = separator.join([f"{{{col}}}" for col in self.selected_columns])
        template += ".pdf"
        
        return template
    
    def _update_button_layout(self):
        """根据窗口宽度更新按钮布局"""
        try:
            window_width = self.winfo_toplevel().winfo_width()
            
            # 获取按钮所在的父容器
            button_frame = self.up_button.master
            
            # 清除现有的网格布局
            self.up_button.grid_forget()
            self.down_button.grid_forget()
            
            if window_width >= RESPONSIVE_THRESHOLD:
                # 宽屏模式：水平排列
                button_frame.columnconfigure(0, weight=1)
                button_frame.columnconfigure(1, weight=1)
                self.up_button.grid(row=0, column=0, padx=(0, 2), sticky="ew")
                self.down_button.grid(row=0, column=1, padx=(2, 0), sticky="ew")
            else:
                # 窄屏模式：垂直排列
                button_frame.columnconfigure(0, weight=1)
                button_frame.columnconfigure(1, weight=0)
                self.up_button.grid(row=0, column=0, padx=(0, 2), pady=(0, 2), sticky="ew")
                self.down_button.grid(row=1, column=0, padx=(0, 2), pady=(2, 0), sticky="ew")
        except Exception as e:
            # 如果出错，使用默认水平排列
            try:
                button_frame = self.up_button.master
                button_frame.columnconfigure(0, weight=1)
                button_frame.columnconfigure(1, weight=1)
                self.up_button.grid(row=0, column=0, padx=(0, 2), sticky="ew")
                self.down_button.grid(row=0, column=1, padx=(2, 0), sticky="ew")
            except Exception:
                pass
    
    def _on_window_configure(self, event):
        """窗口大小变化事件处理"""
        try:
            # 只处理主窗口的Configure事件
            if event.widget != self.main_window:
                return
            
            # 获取当前窗口宽度
            current_width = self.main_window.winfo_width()
            
            # 检查宽度变化是否超过阈值（10像素）
            if abs(current_width - self._last_window_width) < 10:
                return
            
            # 更新缓存的宽度
            self._last_window_width = current_width
            
            # 节流处理，避免频繁更新
            if self._configure_after_id:
                self.after_cancel(self._configure_after_id)
            
            # 延迟100毫秒执行布局更新
            self._configure_after_id = self.after(100, self._update_button_layout)
        except Exception:
            pass