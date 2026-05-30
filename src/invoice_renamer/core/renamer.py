"""重命名逻辑模块"""
import os
import re
import shutil
from typing import List, Dict, Any, Tuple, Optional


class Renamer:
    """文件重命名器"""
    
    def __init__(self):
        """初始化重命名器"""
        # 非法字符正则表达式
        self.illegal_chars_pattern = re.compile(r'[\\/:*?"<>|]')
        
    def sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除非法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        # 将非法字符替换为下划线
        sanitized = self.illegal_chars_pattern.sub('_', filename)
        
        # 移除前后的空格
        sanitized = sanitized.strip()
        
        # 如果文件名为空，使用默认名称
        if not sanitized:
            sanitized = "unnamed"
            
        return sanitized
    
    def format_filename(self, format_template: str, data: Dict[str, Any]) -> str:
        """
        根据模板和数据格式化文件名
        
        Args:
            format_template: 格式模板，如 "{公司名称}_{金额}_{日期}.pdf"
            data: 数据字典
            
        Returns:
            格式化后的文件名
        """
        # 替换模板中的占位符
        formatted = format_template
        
        # 查找所有占位符 {xxx}
        placeholders = re.findall(r'\{([^}]+)\}', format_template)
        
        for placeholder in placeholders:
            value = data.get(placeholder, "")
            formatted = formatted.replace(f"{{{placeholder}}}", str(value))
        
        # 清理文件名
        formatted = self.sanitize_filename(formatted)
        
        return formatted
    
    def generate_unique_filename(self, directory: str, filename: str) -> str:
        """
        生成唯一的文件名，避免重名
        
        Args:
            directory: 目标目录
            filename: 原始文件名
            
        Returns:
            唯一的文件名
        """
        base_name, ext = os.path.splitext(filename)
        counter = 1
        
        while True:
            new_filename = f"{base_name}_{counter}{ext}"
            new_path = os.path.join(directory, new_filename)
            
            if not os.path.exists(new_path):
                return new_filename
            
            counter += 1
    
    def rename_file(self, original_path: str, new_filename: str) -> bool:
        """
        重命名单个文件
        
        Args:
            original_path: 原始文件路径
            new_filename: 新文件名
            
        Returns:
            是否成功重命名
        """
        try:
            directory = os.path.dirname(original_path)
            new_path = os.path.join(directory, new_filename)
            
            # 检查目标文件是否已存在
            if os.path.exists(new_path):
                # 生成唯一文件名
                new_filename = self.generate_unique_filename(directory, new_filename)
                new_path = os.path.join(directory, new_filename)
            
            # 重命名文件
            os.rename(original_path, new_path)
            return True
            
        except Exception as e:
            print(f"重命名文件失败: {str(e)}")
            return False
    
    def batch_rename(self, rename_mapping: List[Tuple[str, str]]) -> List[bool]:
        """
        批量重命名文件
        
        Args:
            rename_mapping: 重命名映射列表，每个元素为(原始路径, 新文件名)的元组
            
        Returns:
            每个文件的重命名结果列表
        """
        results = []
        
        for original_path, new_filename in rename_mapping:
            result = self.rename_file(original_path, new_filename)
            results.append(result)
        
        return results
    
    def backup_original_names(self, rename_mapping: List[Tuple[str, str]], backup_file: str) -> bool:
        """
        备份原始文件名映射
        
        Args:
            rename_mapping: 重命名映射列表
            backup_file: 备份文件路径
            
        Returns:
            是否成功备份
        """
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                for original_path, new_filename in rename_mapping:
                    f.write(f"{original_path}\t{new_filename}\n")
            return True
            
        except Exception as e:
            print(f"备份原始文件名失败: {str(e)}")
            return False
    
    def restore_from_backup(self, backup_file: str) -> bool:
        """
        从备份恢复文件名
        
        Args:
            backup_file: 备份文件路径
            
        Returns:
            是否成功恢复
        """
        try:
            if not os.path.exists(backup_file):
                print(f"备份文件不存在: {backup_file}")
                return False
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) != 2:
                        continue
                    
                    original_path, current_filename = parts
                    
                    directory = os.path.dirname(original_path)
                    
                    # current_filename 是重命名后的文件名，检查它是否存在
                    current_path = os.path.join(directory, current_filename)
                    if not os.path.exists(current_path):
                        continue
                    
                    # 重命名回原始文件名
                    os.rename(current_path, original_path)
            
            return True
            
        except Exception as e:
            print(f"从备份恢复失败: {str(e)}")
            return False