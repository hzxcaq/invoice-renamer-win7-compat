## Why

当前界面存在以下显示问题：

1. **空白行问题**：
   - PDF文件列表下方有空白行（无实际内容）
   - 可用列下方有空白行（Treeview固定height=8导致）
   - 已选列下方有空白行（Listbox固定height=6导致）
   - Excel数据预览下方有空白行（Treeview固定height=15导致）

2. **布局调整问题**：
   - 格式构建器（重命名格式定义）与数据预览区域位置固定，无法调整大小
   - 用户无法根据需要调整这两个区域的比例
   - 与操作和预览栏可以左右调整的体验不一致

这些问题影响了用户体验，特别是当用户需要查看更多数据或调整界面布局时。

## What Changes

### 1. 移除固定高度设置
- 移除 `format_builder.py` 中 Treeview 的 `height=8` 设置
- 移除 `format_builder.py` 中 Listbox 的 `height=6` 设置  
- 移除 `excel_viewer.py` 中 Treeview 的 `height=15` 设置
- 让这些组件完全由容器控制大小，通过 `fill=tk.BOTH, expand=True` 实现自适应

### 2. 添加垂直 PanedWindow
- 在左侧区域内部添加垂直方向的 `PanedWindow`
- 将数据预览区域和格式构建器放入垂直 PanedWindow
- 实现格式构建器 ↔ 数据预览区域的垂直调整功能

### 3. 设置合理的默认比例和最小值
- 数据预览区域占 70%，格式构建器占 30%
- 设置最小高度限制：格式构建器最小 80 像素
- 确保用户可以自由调整，但不会将某个区域拖动得太小

### 4. 保持滚动条功能
- 当内容超出容器大小时，显示滚动条让用户滚动查看
- 确保 Treeview 和 Listbox 的滚动条正常工作

## Capabilities

### New Capabilities
- `vertical-resizable-panes`: 左侧区域内部的垂直调整能力，允许数据预览区域和格式构建器之间上下拖动调整
- `adaptive-component-height`: 自适应组件高度能力，移除固定高度设置，让组件根据容器大小自动调整

### Modified Capabilities
- `resizable-split-panes`: 修改现有spec，扩展为支持水平和垂直两个方向的调整
- `file-preview`: 修改现有spec，确保预览组件在无固定高度下正常工作

## Impact

### 代码影响
- **修改文件**：
  - `src/invoice_renamer/gui/main_window.py`：添加垂直 PanedWindow，调整布局结构
  - `src/invoice_renamer/gui/format_builder.py`：移除固定高度设置，调整组件打包方式
  - `src/invoice_renamer/gui/excel_viewer.py`：移除固定高度设置

### 用户体验影响
- **正面影响**：
  - 消除所有空白行，界面更加紧凑
  - 用户可以自由调整数据预览和格式定义区域的大小
  - 保持现有的左右调整功能，同时增加上下调整功能
  - 界面更加灵活，适应不同屏幕尺寸和用户需求

- **潜在风险**：
  - 用户需要适应新的调整方式（垂直拖动）
  - 初始布局可能需要用户手动调整到舒适的比例

### 兼容性
- 完全向后兼容，不影响现有功能
- 保持现有的键盘和鼠标操作方式
- 不影响数据处理和重命名逻辑

### 技术实现
- 使用 tkinter 的 `ttk.PanedWindow` 实现垂直调整
- 通过 `weight` 参数设置初始比例（70:30）
- 通过 `minsize` 参数设置最小高度限制（80像素）
- 保持现有的滚动条机制，确保内容过多时可以滚动查看