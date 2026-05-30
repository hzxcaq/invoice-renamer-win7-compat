@echo off
echo 发票批量重命名工具打包脚本
echo ========================

echo 1. 安装依赖...
pip install -r requirements.txt
pip install pyinstaller

echo 2. 打包程序...
python -m PyInstaller --onefile --windowed --name="发票批量重命名工具" src/invoice_renamer/main.py

echo 3. 完成！
echo exe文件位于: dist\发票批量重命名工具.exe
pause
