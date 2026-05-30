"""打包成exe文件的脚本"""
import os
import sys
import subprocess


def build_exe():
    """打包成exe文件"""
    print("开始打包...")
    
    # 检查是否安装了PyInstaller
    try:
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # 打包成单个exe文件
        "--windowed",  # 无控制台窗口
        "--name=发票批量重命名工具",  # exe文件名
        "--icon=NONE",  # 图标（可以设置为.ico文件路径）
        "--hidden-import=invoice_renamer.gui",
        "--hidden-import=invoice_renamer.gui.main_window",
        "--hidden-import=invoice_renamer.gui.file_selector",
        "--hidden-import=invoice_renamer.gui.excel_viewer",
        "--hidden-import=invoice_renamer.gui.format_builder",
        "--hidden-import=invoice_renamer.gui.preview_table",
        "--hidden-import=invoice_renamer.core",
        "--hidden-import=invoice_renamer.core.excel_reader",
        "--hidden-import=invoice_renamer.core.file_matcher",
        "--hidden-import=invoice_renamer.core.renamer",
        "src/invoice_renamer/main.py"  # 主程序入口
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("打包成功！")
        print(f"输出目录: {os.path.join(os.getcwd(), 'dist')}")
        print(f"exe文件: {os.path.join(os.getcwd(), 'dist', '发票批量重命名工具.exe')}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {str(e)}")
        print(f"错误输出: {e.stderr}")
        return False


def create_build_script():
    """创建Windows批处理文件"""
    bat_content = """@echo off
echo 发票批量重命名工具打包脚本
echo ========================

echo 1. 安装依赖...
pip install -r requirements.txt
pip install pyinstaller

echo 2. 打包程序...
python -m PyInstaller --onefile --windowed --name="发票批量重命名工具" src/invoice_renamer/main.py

echo 3. 完成！
echo exe文件位于: dist\\发票批量重命名工具.exe
pause
"""
    
    with open("build.bat", "w", encoding="gbk") as f:
        f.write(bat_content)
    
    print("Windows批处理文件已创建: build.bat")


if __name__ == "__main__":
    # 创建构建脚本
    create_build_script()
    
    # 执行打包
    success = build_exe()
    
    if success:
        print("\n打包完成！")
        print("您可以在dist目录中找到exe文件。")
    else:
        print("\n打包失败，请检查错误信息。")