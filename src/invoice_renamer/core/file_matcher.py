"""文件匹配模块"""
import os
import re
from typing import List, Dict, Any, Optional, Tuple


class FileMatcher:
    """文件匹配器"""
    
    def __init__(self):
        """初始化文件匹配器"""
        # 发票号码提取的正则表达式
        self.patterns = [
            r'DZFP[_-]?(\d+)',  # DZFP格式：DZFP12345678, DZFP_12345678, DZFP-12345678
            r'invoice[_-]?(\d+)',  # invoice格式：invoice_12345678
            r'(\d{8,})',  # 8位以上数字序列
        ]
    
    def extract_invoice_number_from_filename(self, filename: str) -> Optional[str]:
        """
        从文件名中提取发票号码
        
        Args:
            filename: 文件名
            
        Returns:
            提取的发票号码，如果没找到则返回None
        """
        # 移除文件扩展名
        name_without_ext = os.path.splitext(filename)[0]
        
        # 尝试所有正则表达式模式
        for pattern in self.patterns:
            match = re.search(pattern, name_without_ext, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def match_files_with_excel(self, directory: str, excel_data: List[Dict[str, Any]]) -> List[Tuple[str, Dict[str, Any]]]:
        """
        将目录中的文件与Excel数据匹配
        
        Args:
            directory: 包含PDF文件的目录
            excel_data: Excel数据列表
            
        Returns:
            匹配结果列表，每个元素为(文件路径, Excel行数据)的元组
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        # 获取目录中的所有PDF文件
        pdf_files = []
        for file_name in os.listdir(directory):
            if file_name.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(directory, file_name))
        
        # 创建发票号码到Excel行的映射
        invoice_to_excel = {}
        for row in excel_data:
            # 尝试多个可能的发票号码列
            invoice_number = row.get("数电发票号码", "") or row.get("发票号码", "")
            if invoice_number:
                invoice_to_excel[str(invoice_number)] = row
        
        # 匹配文件
        matched_files = []
        unmatched_files = []
        
        for file_path in pdf_files:
            file_name = os.path.basename(file_path)
            invoice_number = self.extract_invoice_number_from_filename(file_name)
            
            if invoice_number and invoice_number in invoice_to_excel:
                matched_files.append((file_path, invoice_to_excel[invoice_number]))
            else:
                unmatched_files.append(file_path)
        
        # 对于未匹配的文件，尝试从文件内容中提取发票号码（简化版本）
        # 这里可以添加PDF内容提取逻辑
        
        # 如果还有未匹配的文件，按文件名排序后与剩余Excel行匹配
        if unmatched_files:
            # 获取已匹配的发票号码
            matched_invoices = set()
            for _, excel_row in matched_files:
                matched_invoices.add(excel_row.get("发票号码", ""))
            
            # 获取未匹配的Excel行
            unmatched_excel = [row for row in excel_data if row.get("发票号码", "") not in matched_invoices]
            
            # 按文件名排序
            unmatched_files.sort()
            unmatched_excel.sort(key=lambda x: x.get("发票号码", ""))
            
            # 按顺序匹配
            for i, file_path in enumerate(unmatched_files):
                if i < len(unmatched_excel):
                    matched_files.append((file_path, unmatched_excel[i]))
        
        return matched_files
    
    def match_files_without_excel(self, directory: str) -> List[str]:
        """
        没有Excel时的文件匹配
        
        Args:
            directory: 包含PDF文件的目录
            
        Returns:
            PDF文件路径列表
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        # 获取目录中的所有PDF文件
        pdf_files = []
        for file_name in os.listdir(directory):
            if file_name.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(directory, file_name))
        
        # 按文件名排序
        pdf_files.sort()
        
        return pdf_files