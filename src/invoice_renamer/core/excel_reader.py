"""Excel读取模块"""
import os
from openpyxl import load_workbook
from typing import List, Dict, Any, Optional


class ExcelReader:
    """Excel文件读取器"""
    
    def __init__(self):
        """初始化Excel读取器"""
        pass
    
    def read_excel(self, file_path: str) -> List[Dict[str, Any]]:
        """
        读取Excel文件内容
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            包含所有行数据的字典列表
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式错误
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if not file_path.endswith('.xlsx'):
            raise ValueError("仅支持.xlsx格式的Excel文件")
        
        try:
            workbook = load_workbook(file_path, read_only=True, data_only=True)
            worksheet = workbook.active
            
            # 获取表头
            headers = []
            for cell in worksheet[1]:
                if cell.value is not None:
                    headers.append(str(cell.value))
                else:
                    headers.append(f"Column_{cell.column}")
            
            # 读取数据行
            data = []
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                row_dict = {}
                for col_idx, value in enumerate(row):
                    if col_idx < len(headers):
                        # 将值转换为字符串，保持格式
                        if value is None:
                            row_dict[headers[col_idx]] = ""
                        else:
                            row_dict[headers[col_idx]] = str(value)
                data.append(row_dict)
            
            workbook.close()
            return data
            
        except Exception as e:
            raise ValueError(f"读取Excel文件失败: {str(e)}")
    
    def get_headers(self, file_path: str) -> List[str]:
        """
        获取Excel文件的表头
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            表头列表
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if not file_path.endswith('.xlsx'):
            raise ValueError("仅支持.xlsx格式的Excel文件")
        
        try:
            workbook = load_workbook(file_path, read_only=True, data_only=True)
            worksheet = workbook.active
            
            # 获取表头
            headers = []
            for cell in worksheet[1]:
                if cell.value is not None:
                    headers.append(str(cell.value))
                else:
                    headers.append(f"Column_{cell.column}")
            
            workbook.close()
            return headers
            
        except Exception as e:
            raise ValueError(f"读取Excel表头失败: {str(e)}")