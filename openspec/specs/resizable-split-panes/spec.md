## ADDED Requirements

### Requirement: PanedWindow布局
系统SHALL使用ttk.PanedWindow组件创建可调整大小的分栏布局，用于并排显示Excel数据预览和PDF文件列表。

#### Scenario: PanedWindow组件初始化
- **WHEN** 系统创建主窗口布局时
- **THEN** 系统SHALL在data_frame区域创建水平方向的ttk.PanedWindow组件
- **AND** PanedWindow组件SHALL包含两个窗格：Excel预览窗格和PDF列表窗格

### Requirement: 可调整的窗格比例
系统SHALL允许用户通过拖动分割条自由调整Excel预览和PDF文件列表的宽度比例。

#### Scenario: 分割条拖动调整比例
- **WHEN** 用户拖动PanedWindow的分割条
- **THEN** 系统SHALL实时调整两个窗格的宽度比例
- **AND** Excel预览窗格SHALL显示调整后的宽度
- **AND** PDF列表窗格SHALL显示调整后的宽度

### Requirement: 默认比例设置
系统SHALL为PanedWindow设置合理的默认权重比例，确保初始状态下两个区域都有足够的显示空间。

#### Scenario: 默认权重设置
- **WHEN** 系统初始化PanedWindow时
- **THEN** Excel预览窗格SHALL设置权重为3
- **AND** PDF列表窗格SHALL设置权重为1
- **AND** 初始分割比例SHALL约为3:1

### Requirement: 最小宽度限制
系统SHALL为两个窗格设置最小宽度限制，防止窗格被压缩到不可用状态。

#### Scenario: 最小宽度约束
- **WHEN** 用户调整窗格比例时
- **THEN** Excel预览窗格SHALL保持至少400像素宽度
- **AND** PDF列表窗格SHALL保持至少300像素宽度
- **AND** 系统SHALL阻止窗格宽度小于最小宽度限制