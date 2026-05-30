"""工具函数模块"""
import os
import re
from typing import List, Dict, Any, Optional


def get_pdf_files(directory: str) -> List[str]:
    """
    获取目录中的所有PDF文件
    
    Args:
        directory: 目录路径
        
    Returns:
        PDF文件路径列表
    """
    if not os.path.exists(directory):
        return []
    
    pdf_files = []
    for file_name in os.listdir(directory):
        if file_name.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(directory, file_name))
    
    return pdf_files


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 非法字符正则表达式
    illegal_chars_pattern = re.compile(r'[\\/:*?"<>|]')
    
    # 将非法字符替换为下划线
    sanitized = illegal_chars_pattern.sub('_', filename)
    
    # 移除前后的空格
    sanitized = sanitized.strip()
    
    # 如果文件名为空，使用默认名称
    if not sanitized:
        sanitized = "unnamed"
        
    return sanitized


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def create_backup_file(directory: str, filename: str) -> str:
    """
    创建备份文件
    
    Args:
        directory: 目录路径
        filename: 文件名
        
    Returns:
        备份文件路径
    """
    backup_dir = os.path.join(directory, ".backup")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    backup_file = os.path.join(backup_dir, filename)
    return backup_file


def log_operation(operation: str, details: Dict[str, Any], log_file: str = "operation.log"):
    """
    记录操作日志
    
    Args:
        operation: 操作类型
        details: 操作详情
        log_file: 日志文件路径
    """
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{timestamp}] {operation}: {details}\n"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)