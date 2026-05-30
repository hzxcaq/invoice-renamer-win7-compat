# Tasks for fix-gui-and-undo

- [x] 1. 修复撤销重命名逻辑反转 bug
  - 文件: `src/invoice_renamer/core/renamer.py`
  - 修改 `restore_from_backup` 方法，反转存在性检查逻辑

- [x] 2. 修复Excel预览挤掉PDF文件列表
  - 文件: `src/invoice_renamer/gui/main_window.py`
  - 修改 `data_frame` 的布局方式，确保两个区域并排显示且互不挤压

- [x] 3. 添加Excel预览高度约束
  - 文件: `src/invoice_renamer/gui/excel_viewer.py`
  - 为 Excel Treeview 设置最大显示高度

- [x] 4. 验证修复效果
  - 测试文件列表显示正常
  - 测试Excel预览和PDF列表并排显示
  - 测试撤销重命名功能正常
