## Why

当前主窗口布局中，Excel数据预览区域和PDF文件列表区域使用Grid布局并排放置。当Excel文件加载后，由于Excel Treeview的列宽计算（每列最小100px），多列Excel的总宽度会超出分配的空间，导致Grid布局将PDF文件列表压缩到0宽度或不可用状态。这使得用户在选择Excel文件后无法同时查看Excel数据和PDF文件列表，严重影响使用体验。

## What Changes

- 将`data_frame`中的Grid布局替换为`ttk.PanedWindow`布局
- Excel数据预览和PDF文件列表放置在PanedWindow的两个窗格中
- 用户可以拖动分割条自由调整两个区域的宽度比例
- 为两个窗格设置合理的默认权重和最小宽度
- 限制Excel Treeview的列宽最大值，防止内容过度溢出

## Capabilities

### New Capabilities

- `resizable-split-panes`: 可调整的分栏布局，允许用户通过拖动分割条自由调整Excel预览和PDF列表的宽度比例

### Modified Capabilities

- `file-preview`: 修改文件预览组件的布局方式，从固定Grid改为可调整的PanedWindow

## Impact

- **GUI布局代码**: 主要修改`src/invoice_renamer/gui/main_window.py`中的`data_frame`布局
- **Excel预览组件**: 可能需要调整`src/invoice_renamer/gui/excel_viewer.py`中的列宽计算
- **用户体验**: 改善文件预览的可用性，解决内容挤压问题
- **无破坏性变更**: 不影响现有功能逻辑，仅修改布局方式