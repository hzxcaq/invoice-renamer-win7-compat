## 1. 修改主窗口布局

- [x] 1.1 在`main_window.py`中，将`data_frame`的Grid布局替换为ttk.PanedWindow布局
- [x] 1.2 创建水平方向的PanedWindow组件
- [x] 1.3 将Excel预览窗格和PDF列表窗格添加到PanedWindow中
- [x] 1.4 设置PanedWindow的默认权重（Excel预览:PDF列表 = 3:1）
- [x] 1.5 设置窗格的最小宽度限制（Excel预览:400px，PDF列表:300px）

## 2. 修改Excel预览组件

- [x] 2.1 在`excel_viewer.py`中，修改列宽计算逻辑，限制每列最大宽度为160px
- [x] 2.2 确保列宽计算公式：min(160, max(80, len(header) * 10))
- [x] 2.3 验证Excel Treeview在限制列宽后的显示效果

## 3. 测试和验证

- [x] 3.1 测试不同列数的Excel文件（7列、10列、15列、20列）
- [x] 3.2 测试分割条拖动功能，验证比例调整是否正常
- [x] 3.3 测试最小宽度限制，验证窗格不会被压缩到小于最小宽度
- [x] 3.4 验证现有功能完整性（文件选择、Excel预览、格式构建、预览重命名等）
- [x] 3.5 测试窗口缩放时的布局表现