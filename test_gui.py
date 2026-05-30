"""GUI测试脚本"""
import sys
import os

# 添加项目路径到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from invoice_renamer.gui.main_window import MainWindow


def test_gui():
    """测试GUI是否可以正常启动"""
    try:
        # 创建主窗口
        app = MainWindow()
        
        # 设置窗口标题
        app.title("发票批量重命名工具 - 测试")
        
        # 显示窗口
        app.update()
        
        print("GUI测试成功！窗口已创建。")
        print("窗口大小:", app.winfo_width(), "x", app.winfo_height())
        
        # 运行一小段时间后关闭
        app.after(2000, app.destroy)
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"GUI测试失败: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_gui()
    sys.exit(0 if success else 1)