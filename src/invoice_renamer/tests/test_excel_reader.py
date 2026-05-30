"""Excel读取功能测试"""
import os
import tempfile
import pytest
from openpyxl import Workbook
from ..core.excel_reader import ExcelReader


class TestExcelReader:
    """Excel读取功能测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.reader = ExcelReader()
        
    def test_read_excel_file(self):
        """测试读取Excel文件"""
        # 创建临时Excel文件
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            # 创建测试数据
            wb = Workbook()
            ws = wb.active
            ws.title = "Sheet1"
            
            # 添加表头
            headers = ["发票号码", "日期", "金额", "公司名称"]
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            
            # 添加数据行
            test_data = [
                ["12345678", "2026-04-01", "1000.00", "测试公司A"],
                ["87654321", "2026-04-02", "2000.00", "测试公司B"],
            ]
            for row_idx, row_data in enumerate(test_data, 2):
                for col_idx, value in enumerate(row_data, 1):
                    ws.cell(row=row_idx, column=col_idx, value=value)
            
            wb.save(tmp_path)
            
            # 读取Excel文件
            result = self.reader.read_excel(tmp_path)
            
            # 验证结果
            assert result is not None
            assert len(result) == 2
            assert result[0]["发票号码"] == "12345678"
            assert result[0]["日期"] == "2026-04-01"
            assert result[0]["金额"] == "1000.00"
            assert result[0]["公司名称"] == "测试公司A"
            
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_get_headers(self):
        """测试获取表头"""
        # 创建临时Excel文件
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            # 创建测试数据
            wb = Workbook()
            ws = wb.active
            ws.title = "Sheet1"
            
            # 添加表头
            headers = ["发票号码", "日期", "金额", "公司名称"]
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            
            wb.save(tmp_path)
            
            # 获取表头
            result = self.reader.get_headers(tmp_path)
            
            # 验证结果
            assert result is not None
            assert len(result) == 4
            assert result == headers
            
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        with pytest.raises(FileNotFoundError):
            self.reader.read_excel("nonexistent.xlsx")