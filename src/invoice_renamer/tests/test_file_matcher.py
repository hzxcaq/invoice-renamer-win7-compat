"""文件匹配功能测试"""
import os
import tempfile
import pytest
from ..core.file_matcher import FileMatcher


class TestFileMatcher:
    """文件匹配功能测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.matcher = FileMatcher()
        
    def test_extract_invoice_number_from_filename(self):
        """测试从文件名中提取发票号码"""
        # 测试DZFP格式
        assert self.matcher.extract_invoice_number_from_filename("DZFP12345678.pdf") == "12345678"
        assert self.matcher.extract_invoice_number_from_filename("DZFP_12345678.pdf") == "12345678"
        assert self.matcher.extract_invoice_number_from_filename("DZFP-12345678.pdf") == "12345678"
        
        # 测试其他格式
        assert self.matcher.extract_invoice_number_from_filename("invoice_12345678.pdf") == "12345678"
        assert self.matcher.extract_invoice_number_from_filename("12345678.pdf") == "12345678"
        
        # 测试没有数字的情况
        assert self.matcher.extract_invoice_number_from_filename("invoice.pdf") is None
        
    def test_match_files_with_excel(self):
        """测试将文件与Excel数据匹配"""
        # 创建测试目录和文件
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 创建测试PDF文件
            test_files = [
                "DZFP12345678.pdf",
                "DZFP87654321.pdf",
                "invoice_11111111.pdf"
            ]
            for file_name in test_files:
                file_path = os.path.join(tmp_dir, file_name)
                with open(file_path, 'w') as f:
                    f.write("test content")
            
            # 创建测试Excel数据
            excel_data = [
                {"发票号码": "12345678", "日期": "2026-04-01", "金额": "1000.00"},
                {"发票号码": "87654321", "日期": "2026-04-02", "金额": "2000.00"},
                {"发票号码": "11111111", "日期": "2026-04-03", "金额": "3000.00"}
            ]
            
            # 执行匹配
            result = self.matcher.match_files_with_excel(tmp_dir, excel_data)
            
            # 验证结果
            assert result is not None
            assert len(result) == 3
            
            # 验证每个文件都匹配到了正确的Excel行
            for file_path, excel_row in result:
                file_name = os.path.basename(file_path)
                if "12345678" in file_name:
                    assert excel_row["发票号码"] == "12345678"
                elif "87654321" in file_name:
                    assert excel_row["发票号码"] == "87654321"
                elif "11111111" in file_name:
                    assert excel_row["发票号码"] == "11111111"
    
    def test_match_files_without_excel(self):
        """测试没有Excel时的文件匹配"""
        # 创建测试目录和文件
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 创建测试PDF文件
            test_files = [
                "DZFP12345678.pdf",
                "DZFP87654321.pdf",
                "invoice_11111111.pdf"
            ]
            for file_name in test_files:
                file_path = os.path.join(tmp_dir, file_name)
                with open(file_path, 'w') as f:
                    f.write("test content")
            
            # 执行匹配（没有Excel数据）
            result = self.matcher.match_files_without_excel(tmp_dir)
            
            # 验证结果
            assert result is not None
            assert len(result) == 3
            
            # 验证返回的是文件路径列表
            for file_path in result:
                assert os.path.exists(file_path)
                assert file_path.endswith('.pdf')