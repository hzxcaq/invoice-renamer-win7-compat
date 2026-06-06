"""主窗口模块"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import datetime
import glob
from typing import Optional, List, Dict, Any

from .file_selector import FileSelector
from .excel_viewer import ExcelViewer
from .format_builder import FormatBuilder
from .preview_table import PreviewTable
from ..core.excel_reader import ExcelReader
from ..core.file_matcher import FileMatcher
from ..core.renamer import Renamer


class MainWindow(tk.Tk):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        
        # 设置窗口标题
        self.title("发票批量重命名工具")
        
        # 设置窗口大小 - 增加高度确保按钮可见
        self.geometry("1200x900")
        
        # 设置最小尺寸
        self.minsize(1000, 700)
        
        # 初始化核心模块
        self.excel_reader = ExcelReader()
        self.file_matcher = FileMatcher()
        self.renamer = Renamer()
        
        # 初始化变量
        self.current_directory = None
        self.current_excel_file = None
        self.excel_data = []
        self.excel_headers = []
        self.pdf_files = []
        self.matched_files = []
        self.format_template = ""
        
        # 记录最近一次备份文件路径（供撤销使用）
        self.last_backup_file = None
        
        # 创建界面
        self._create_widgets()
        
        # 设置窗口居中
        self._center_window()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 使用PanedWindow布局来实现左右两部分的拖动调整
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建水平方向的PanedWindow
        self.main_paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧区域：文件选择 + 数据预览 + 格式定义
        left_frame = ttk.Frame(self.main_paned)
        
        # 文件选择器
        self.file_selector = FileSelector(left_frame, self)
        self.file_selector.pack(fill=tk.X, padx=5, pady=(5, 10))
        
        # 创建垂直PanedWindow，允许数据预览区域和格式构建器之间调整大小
        vertical_paned = ttk.PanedWindow(left_frame, orient=tk.VERTICAL)
        vertical_paned.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Excel预览和PDF列表 - 使用PanedWindow布局，允许用户调整比例
        data_frame = ttk.Frame(vertical_paned)
        
        # 创建水平方向的PanedWindow
        self.paned = ttk.PanedWindow(data_frame, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # Excel预览窗格
        excel_frame = ttk.LabelFrame(self.paned, text="Excel数据预览", padding="5")
        
        self.excel_viewer = ExcelViewer(excel_frame, self)
        self.excel_viewer.pack(fill=tk.BOTH, expand=True)
        
        # PDF文件列表窗格
        pdf_frame = ttk.LabelFrame(self.paned, text="PDF文件列表", padding="5")
        
        # PDF文件列表 - 添加滚动条
        pdf_scrollbar = ttk.Scrollbar(pdf_frame, orient=tk.VERTICAL)
        pdf_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pdf_listbox = tk.Listbox(pdf_frame, selectmode=tk.EXTENDED, yscrollcommand=pdf_scrollbar.set, height=0)
        self.pdf_listbox.pack(fill=tk.BOTH, expand=True)
        pdf_scrollbar.config(command=self.pdf_listbox.yview)
        
        # 将窗格添加到PanedWindow，设置权重
        self.paned.add(excel_frame, weight=3)
        self.paned.add(pdf_frame, weight=1)
        
        # 格式构建器
        format_frame = ttk.LabelFrame(vertical_paned, text="重命名格式定义", padding="5")
        
        # 将数据预览区域和格式构建器添加到垂直PanedWindow
        vertical_paned.add(data_frame, weight=7)  # 数据预览区域占70%
        vertical_paned.add(format_frame, weight=3)  # 格式构建器占30%
        
        self.format_builder = FormatBuilder(format_frame, self)
        self.format_builder.pack(fill=tk.BOTH, expand=True)
        
        # 右侧区域：操作按钮 + 预览表格
        right_frame = ttk.Frame(self.main_paned)
        
        # 将窗格添加到PanedWindow，设置权重
        self.main_paned.add(left_frame, weight=3)  # 左侧权重3
        self.main_paned.add(right_frame, weight=2)  # 右侧权重2
        
        # 操作按钮 - 固定在右侧顶部
        button_frame = ttk.LabelFrame(right_frame, text="操作", padding="10")
        button_frame.pack(fill=tk.X, padx=5, pady=(5, 10))
        
        # 操作步骤提示
        help_frame = ttk.Frame(button_frame)
        help_frame.pack(fill=tk.X, pady=(0, 10))
        
        steps = [
            "1. 选择目录",
            "2. 选择Excel(可选)",
            "3. 定义格式",
            "4. 点击'预览重命名'",
            "5. 确认后点击'开始重命名'"
        ]
        for step in steps:
            ttk.Label(help_frame, text=step, font=("", 9)).pack(anchor=tk.W, pady=1)
        
        # 预览按钮
        self.preview_button = ttk.Button(
            button_frame, 
            text="预览重命名", 
            command=self._preview_rename,
            state=tk.DISABLED,
            width=15
        )
        self.preview_button.pack(fill=tk.X, pady=(10, 5))
        
        # 开始重命名按钮
        self.rename_button = ttk.Button(
            button_frame, 
            text="开始重命名", 
            command=self._start_rename,
            state=tk.DISABLED,
            width=15
        )
        self.rename_button.pack(fill=tk.X, pady=5)
        
        # 撤销按钮
        self.undo_button = ttk.Button(
            button_frame, 
            text="撤销重命名", 
            command=self._undo_rename,
            state=tk.DISABLED,
            width=15
        )
        self.undo_button.pack(fill=tk.X, pady=5)
        
        # 预览表格 - 放在按钮下方
        preview_frame = ttk.LabelFrame(right_frame, text="重命名预览", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        self.preview_table = PreviewTable(preview_frame, self)
        self.preview_table.pack(fill=tk.BOTH, expand=True)
    
    def _center_window(self):
        """将窗口居中显示"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def set_directory(self, directory: str):
        """设置当前目录"""
        self.current_directory = directory
        
        # 更新PDF文件列表
        self._update_pdf_list()
        
        # 更新按钮状态
        self._update_button_states()
    
    def set_excel_file(self, excel_file: str):
        """设置Excel文件"""
        self.current_excel_file = excel_file
        
        # 读取Excel数据（优先尝试多sheet合并）
        try:
            try:
                merged_data, grouped_columns = self.excel_reader.read_excel_merged(excel_file)
                self.excel_data = merged_data
                self.excel_headers = list(merged_data[0].keys()) if merged_data else []
                has_groups = len(grouped_columns) > 1
            except Exception:
                # 多sheet合并失败，退化为单sheet读取
                self.excel_data = self.excel_reader.read_excel(excel_file)
                self.excel_headers = self.excel_reader.get_headers(excel_file)
                grouped_columns = {}
                has_groups = False
            
            # 更新Excel预览
            self.excel_viewer.update_data(self.excel_headers, self.excel_data)
            
            # 更新格式构建器（根据是否有分组选择不同方法）
            if has_groups:
                self.format_builder.update_columns_grouped(self.excel_headers, grouped_columns)
            else:
                self.format_builder.update_columns(self.excel_headers)
            
            # 更新按钮状态
            self._update_button_states()
            
        except Exception as e:
            messagebox.showerror("错误", f"读取Excel文件失败: {str(e)}")
    
    def _update_pdf_list(self):
        """更新PDF文件列表"""
        self.pdf_listbox.delete(0, tk.END)
        
        if not self.current_directory:
            return
        
        # 获取目录中的PDF文件
        self.pdf_files = []
        for file_name in os.listdir(self.current_directory):
            if file_name.lower().endswith('.pdf'):
                self.pdf_files.append(file_name)
                self.pdf_listbox.insert(tk.END, file_name)
    
    def _update_button_states(self):
        """更新按钮状态"""
        # 预览按钮需要目录和格式模板
        has_directory = self.current_directory is not None
        has_format = bool(self.format_builder.get_format_template())
        has_preview = bool(self.matched_files)
        
        # 预览按钮：需要目录和格式模板
        self.preview_button.config(state=tk.NORMAL if (has_directory and has_format) else tk.DISABLED)
        
        # 开始重命名按钮：需要目录、格式模板和已预览
        self.rename_button.config(state=tk.NORMAL if (has_directory and has_format and has_preview) else tk.DISABLED)
    
    def update_format_template(self, template: str):
        """更新格式模板"""
        self.format_template = template
        self._update_button_states()
    
    def _preview_rename(self):
        """预览重命名结果"""
        if not self.current_directory:
            messagebox.showwarning("警告", "请先选择目录")
            return
        
        if not self.format_template:
            messagebox.showwarning("警告", "请先定义重命名格式")
            return
        
        try:
            # 匹配文件
            if self.excel_data:
                self.matched_files = self.file_matcher.match_files_with_excel(
                    self.current_directory, 
                    self.excel_data
                )
            else:
                pdf_files = self.file_matcher.match_files_without_excel(self.current_directory)
                self.matched_files = [(file_path, {}) for file_path in pdf_files]
            
            # 生成预览数据
            preview_data = []
            for file_path, excel_row in self.matched_files:
                original_name = os.path.basename(file_path)
                new_name = self.renamer.format_filename(self.format_template, excel_row)
                preview_data.append((original_name, new_name, file_path))
            
            # 更新预览表格
            self.preview_table.update_data(preview_data)
            
            # 更新按钮状态（启用开始重命名按钮）
            self._update_button_states()
            
        except Exception as e:
            messagebox.showerror("错误", f"预览重命名失败: {str(e)}")
    
    def _start_rename(self):
        """开始重命名"""
        if not self.current_directory:
            messagebox.showwarning("警告", "请先选择目录")
            return
        
        if not self.format_template:
            messagebox.showwarning("警告", "请先定义重命名格式")
            return
        
        if not self.matched_files:
            messagebox.showwarning("警告", "请先预览重命名结果")
            return
        
        # 确认重命名
        if not messagebox.askyesno("确认", f"确定要重命名 {len(self.matched_files)} 个文件吗？"):
            return
        
        try:
            # 备份原始文件名
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(
                self.current_directory,
                "rename_backup_{}.txt".format(ts),
            )
            self.last_backup_file = backup_file
            rename_mapping = []
            
            for file_path, excel_row in self.matched_files:
                new_name = self.renamer.format_filename(self.format_template, excel_row)
                rename_mapping.append((file_path, new_name))
            
            # 备份
            self.renamer.backup_original_names(rename_mapping, backup_file)
            
            # 执行批量重命名
            results = self.renamer.batch_rename(rename_mapping)
            
            # 统计结果
            success_count = sum(results)
            fail_count = len(results) - success_count
            
            # 显示结果
            if fail_count == 0:
                messagebox.showinfo("成功", f"成功重命名 {success_count} 个文件")
            else:
                messagebox.showwarning("警告", f"成功重命名 {success_count} 个文件，{fail_count} 个文件重命名失败")
            
            # 更新PDF文件列表
            self._update_pdf_list()
            
            # 启用撤销按钮
            self.undo_button.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("错误", f"重命名失败: {str(e)}")
    
    def _undo_rename(self):
        """撤销重命名"""
        if not self.current_directory:
            messagebox.showwarning("警告", "请先选择目录")
            return
        
        backup_file = self.last_backup_file
        if not backup_file or not os.path.exists(backup_file):
            # 回退：按时间倒序找目录里最新的备份文件
            candidates = sorted(
                glob.glob(os.path.join(self.current_directory, "rename_backup_*.txt")),
                reverse=True,
            )
            if candidates:
                backup_file = candidates[0]

        if not backup_file or not os.path.exists(backup_file):
            messagebox.showwarning("警告", "没有找到备份文件，无法撤销")
            return
        
        # 确认撤销
        if not messagebox.askyesno("确认", "确定要撤销重命名吗？"):
            return
        
        try:
            # 从备份恢复
            success = self.renamer.restore_from_backup(backup_file)
            
            if success:
                messagebox.showinfo("成功", "撤销重命名成功")
                
                # 更新PDF文件列表
                self._update_pdf_list()
                
                # 禁用撤销按钮
                self.undo_button.config(state=tk.DISABLED)
            else:
                messagebox.showerror("错误", "撤销重命名失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"撤销重命名失败: {str(e)}")
