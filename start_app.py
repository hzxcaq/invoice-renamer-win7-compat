"""启动发票批量重命名工具"""
import sys
import os

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from invoice_renamer.gui.main_window import MainWindow

def main():
    """启动应用程序"""
    print("正在启动发票批量重命名工具...")
    print("请稍候，窗口即将出现...")
    
    # 创建主窗口
    app = MainWindow()
    
    # 运行应用程序
    app.mainloop()

if __name__ == "__main__":
    main()