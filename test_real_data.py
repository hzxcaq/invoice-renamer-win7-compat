"""使用真实测试数据测试程序"""
import sys
import os

# 添加项目路径到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from invoice_renamer.core.excel_reader import ExcelReader
from invoice_renamer.core.file_matcher import FileMatcher
from invoice_renamer.core.renamer import Renamer


def test_with_real_data():
    """使用真实数据测试"""
    print("使用真实测试数据测试...")
    
    # 测试数据目录
    test_dir = "D:/Document/ai/4月"
    excel_file = os.path.join(test_dir, "2026.04取得发票.xlsx")
    
    # 检查文件是否存在
    if not os.path.exists(test_dir):
        print(f"测试目录不存在: {test_dir}")
        return False
    
    if not os.path.exists(excel_file):
        print(f"Excel文件不存在: {excel_file}")
        return False
    
    print(f"测试目录: {test_dir}")
    print(f"Excel文件: {excel_file}")
    
    # 1. 读取Excel数据
    print("\n1. 读取Excel数据...")
    excel_reader = ExcelReader()
    try:
        excel_data = excel_reader.read_excel(excel_file)
        excel_headers = excel_reader.get_headers(excel_file)
        
        print(f"  表头数量: {len(excel_headers)}")
        print(f"  数据行数: {len(excel_data)}")
        
        # 显示前3行数据
        print("  前3行数据:")
        for i, row in enumerate(excel_data[:3]):
            print(f"    第{i+1}行: 序号={row.get('序号', '')}, 销方名称={row.get('销方名称', '')}, 金额={row.get('金额', '')}")
        
    except Exception as e:
        print(f"  读取Excel失败: {str(e)}")
        return False
    
    # 2. 测试文件匹配
    print("\n2. 测试文件匹配...")
    file_matcher = FileMatcher()
    try:
        matched_files = file_matcher.match_files_with_excel(test_dir, excel_data)
        
        print(f"  匹配结果: {len(matched_files)} 个文件")
        
        # 显示前5个匹配结果
        print("  前5个匹配结果:")
        for i, (file_path, excel_row) in enumerate(matched_files[:5]):
            file_name = os.path.basename(file_path)
            invoice_number = excel_row.get('数电发票号码', '') or excel_row.get('发票号码', '')
            print(f"    {i+1}. {file_name}")
            print(f"       发票号码: {invoice_number}")
            print(f"       销方名称: {excel_row.get('销方名称', '')}")
            print(f"       金额: {excel_row.get('金额', '')}")
        
        # 统计匹配情况
        total_files = len([f for f in os.listdir(test_dir) if f.lower().endswith('.pdf')])
        matched_count = len(matched_files)
        unmatched_count = total_files - matched_count
        
        print(f"\n  匹配统计:")
        print(f"    总PDF文件数: {total_files}")
        print(f"    成功匹配: {matched_count}")
        print(f"    未匹配: {unmatched_count}")
        print(f"    匹配率: {matched_count/total_files*100:.1f}%")
        
    except Exception as e:
        print(f"  文件匹配失败: {str(e)}")
        return False
    
    # 3. 测试重命名格式
    print("\n3. 测试重命名格式...")
    renamer = Renamer()
    
    # 测试几种格式
    formats = [
        "{销方名称}_{金额}_{数电发票号码}.pdf",
        "{序号}-{货物或应税劳务名称}-{金额}-{销方名称}.pdf",
        "{开票日期}_{销方名称}_{价税合计}.pdf"
    ]
    
    for format_template in formats:
        print(f"\n  格式: {format_template}")
        
        # 用第一个匹配的文件测试
        if matched_files:
            file_path, excel_row = matched_files[0]
            original_name = os.path.basename(file_path)
            new_name = renamer.format_filename(format_template, excel_row)
            
            print(f"    原始文件名: {original_name}")
            print(f"    新文件名: {new_name}")
    
    print("\n真实数据测试完成！")
    return True


if __name__ == "__main__":
    success = test_with_real_data()
    sys.exit(0 if success else 1)