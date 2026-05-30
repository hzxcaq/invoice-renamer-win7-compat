"""发票批量重命名工具主程序"""
import sys
import os

# 添加src目录到Python路径，使invoice_renamer包可被正确导入
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

from invoice_renamer.gui.main_window import MainWindow


def main():
    """主函数"""
    # 创建主窗口
    app = MainWindow()
    
    # 运行应用程序
    app.mainloop()


if __name__ == "__main__":
    main()