## MODIFIED Requirements

### Requirement: 文件预览布局
系统SHALL在主窗口中显示文件预览区域，包含Excel数据预览和PDF文件列表两个并排显示的组件。

#### Scenario: Excel预览和PDF列表并排显示
- **WHEN** 用户选择目录和/或Excel文件时
- **THEN** 系统SHALL在data_frame区域并排显示Excel数据预览和PDF文件列表
- **AND** 两个区域SHALL使用PanedWindow布局，允许用户调整比例
- **AND** Excel预览区域SHALL显示Excel文件的内容预览
- **AND** PDF文件列表SHALL显示目录中的PDF文件列表

#### Scenario: Excel数据预览显示
- **WHEN** 用户选择Excel文件后
- **THEN** 系统SHALL在Excel预览窗格中显示Excel文件的表头和数据
- **AND** Excel预览组件SHALL使用ttk.Treeview显示数据
- **AND** Excel预览组件SHALL提供横向和纵向滚动条

#### Scenario: PDF文件列表显示
- **WHEN** 用户选择包含PDF文件的目录后
- **THEN** 系统SHALL在PDF列表窗格中显示目录中的PDF文件
- **AND** PDF文件列表SHALL使用tk.Listbox显示文件列表
- **AND** PDF文件列表SHALL提供纵向滚动条

## ADDED Requirements

### Requirement: Excel列宽限制
系统SHALL限制Excel预览组件中每列的最大宽度，防止内容过度溢出影响布局。

#### Scenario: Excel列宽最大值限制
- **WHEN** 系统设置Excel Treeview列宽时
- **THEN** 每列宽度SHALL限制在最大160像素以内
- **AND** 每列宽度SHALL至少为80像素
- **AND** 列宽计算SHALL使用公式：min(160, max(80, len(header) * 10))