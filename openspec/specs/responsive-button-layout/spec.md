## ADDED Requirements

### Requirement: 响应式按钮布局
系统SHALL根据窗口宽度动态调整"上移"和"下移"按钮的排列方式，确保按钮在任何窗口尺寸下都可见且可点击。

#### Scenario: 宽屏模式下按钮水平排列
- **WHEN** 窗口宽度大于或等于1200像素
- **THEN** 系统SHALL将"上移"和"下移"按钮水平排列
- **AND** 按钮SHALL保持原有大小和样式
- **AND** 按钮SHALL保持原有的功能

#### Scenario: 窄屏模式下按钮垂直排列
- **WHEN** 窗口宽度小于1200像素
- **THEN** 系统SHALL将"上移"和"下移"按钮垂直排列
- **AND** 按钮SHALL填满可用宽度
- **AND** 按钮SHALL保持原有的功能

### Requirement: 动态布局切换
系统SHALL在窗口大小变化时自动切换按钮布局，无需用户手动操作。

#### Scenario: 窗口大小变化触发布局切换
- **WHEN** 用户调整窗口大小导致宽度跨越1200像素阈值
- **THEN** 系统SHALL自动切换按钮排列方式
- **AND** 切换过程SHALL平滑无闪烁
- **AND** 按钮状态SHALL在切换后保持不变

#### Scenario: 布局切换节流处理
- **WHEN** 用户频繁调整窗口大小
- **THEN** 系统SHALL对布局切换进行节流处理
- **AND** 系统SHALL避免频繁的布局重计算
- **AND** 系统SHALL保持界面响应性

### Requirement: 按钮功能一致性
系统SHALL确保在任何布局模式下，按钮的功能完全一致。

#### Scenario: 水平排列模式下按钮功能
- **WHEN** 按钮处于水平排列模式
- **AND** 用户点击"上移"按钮
- **THEN** 系统SHALL将选中的列上移一位
- **AND** 用户点击"下移"按钮
- **THEN** 系统SHALL将选中的列下移一位

#### Scenario: 垂直排列模式下按钮功能
- **WHEN** 按钮处于垂直排列模式
- **AND** 用户点击"上移"按钮
- **THEN** 系统SHALL将选中的列上移一位
- **AND** 用户点击"下移"按钮
- **THEN** 系统SHALL将选中的列下移一位