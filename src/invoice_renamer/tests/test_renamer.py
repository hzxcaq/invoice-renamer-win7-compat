"""重命名逻辑测试"""
import os
import tempfile
import pytest
from ..core.renamer import Renamer


class TestRenamer:
    """重命名逻辑测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.renamer = Renamer()
        
    def test_sanitize_filename(self):
        """测试文件名清理"""
        # 测试非法字符
        assert self.renamer.sanitize_filename("test/file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test\\file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test:file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test*file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test?file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test\"file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test<file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test>file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test|file.pdf") == "test_file.pdf"
        
        # 测试正常文件名
        assert self.renamer.sanitize_filename("test_file.pdf") == "test_file.pdf"
        assert self.renamer.sanitize_filename("test-file.pdf") == "test-file.pdf"
        assert self.renamer.sanitize_filename("test file.pdf") == "test file.pdf"
        
    def test_format_filename(self):
        """测试文件名格式化"""
        # 测试基本格式
        format_template = "{公司名称}_{金额}_{日期}.pdf"
        data = {
            "公司名称": "测试公司",
            "金额": "1000.00",
            "日期": "2026-04-01"
        }
        result = self.renamer.format_filename(format_template, data)
        assert result == "测试公司_1000.00_2026-04-01.pdf"
        
        # 测试带分隔符的格式
        format_template = "{序号}-{货物或应税劳务名称}-{金额}-{公司}-{销方名称}.pdf"
        data = {
            "序号": "1",
            "货物或应税劳务名称": "服务费",
            "金额": "1000.00",
            "公司": "测试公司",
            "销方名称": "供应商A"
        }
        result = self.renamer.format_filename(format_template, data)
        assert result == "1-服务费-1000.00-测试公司-供应商A.pdf"
        
        # 测试缺失字段
        format_template = "{公司名称}_{金额}_{日期}.pdf"
        data = {
            "公司名称": "测试公司",
            "金额": "1000.00"
            # 缺少日期字段
        }
        result = self.renamer.format_filename(format_template, data)
        assert result == "测试公司_1000.00_.pdf"
        
    def test_generate_unique_filename(self):
        """测试生成唯一文件名"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 创建测试文件
            test_file = os.path.join(tmp_dir, "test.pdf")
            with open(test_file, 'w') as f:
                f.write("test content")
            
            # 测试生成唯一文件名
            new_name = self.renamer.generate_unique_filename(tmp_dir, "test.pdf")
            assert new_name == "test_1.pdf"
            
            # 创建另一个文件
            test_file2 = os.path.join(tmp_dir, "test_1.pdf")
            with open(test_file2, 'w') as f:
                f.write("test content 2")
            
            # 再次生成唯一文件名
            new_name2 = self.renamer.generate_unique_filename(tmp_dir, "test.pdf")
            assert new_name2 == "test_2.pdf"
    
    def test_rename_file(self):
        """测试重命名文件"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 创建测试文件
            original_file = os.path.join(tmp_dir, "original.pdf")
            with open(original_file, 'w') as f:
                f.write("test content")
            
            # 重命名文件
            new_name = "new_name.pdf"
            result = self.renamer.rename_file(original_file, new_name)
            
            # 验证结果
            assert result is True
            assert not os.path.exists(original_file)
            assert os.path.exists(os.path.join(tmp_dir, new_name))
            
    def test_batch_rename(self):
        """测试批量重命名"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 创建测试文件
            test_files = [
                "file1.pdf",
                "file2.pdf",
                "file3.pdf"
            ]
            for file_name in test_files:
                file_path = os.path.join(tmp_dir, file_name)
                with open(file_path, 'w') as f:
                    f.write("test content")
            
            # 准备重命名映射
            rename_mapping = [
                (os.path.join(tmp_dir, "file1.pdf"), "new_file1.pdf"),
                (os.path.join(tmp_dir, "file2.pdf"), "new_file2.pdf"),
                (os.path.join(tmp_dir, "file3.pdf"), "new_file3.pdf")
            ]
            
            # 执行批量重命名
            results = self.renamer.batch_rename(rename_mapping)
            
            # 验证结果
            assert len(results) == 3
            assert all(results)
            
            # 验证文件已重命名
            for _, new_name in rename_mapping:
                assert os.path.exists(os.path.join(tmp_dir, new_name))