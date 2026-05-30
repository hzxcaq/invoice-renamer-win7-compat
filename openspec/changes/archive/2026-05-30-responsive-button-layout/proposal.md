## Why

当窗口未全屏时，格式构建器中的"上移"和"下移"按钮会被挤掉不显示，影响用户体验。当前布局使用水平排列的按钮，需要约160像素的宽度，当窗口宽度不足时按钮会被压缩到不可见状态。

## What Changes

- 修改格式构建器（FormatBuilder）中的按钮布局，实现响应式设计
- 当窗口宽度充足时（≥1200像素），按钮保持水平排列
- 当窗口宽度不足时（<1200像素），按钮自动切换为垂直排列
- 添加窗口宽度监听，动态调整按钮布局
- 确保按钮在任何窗口尺寸下都可见且可点击

## Capabilities

### New Capabilities
- `responsive-button-layout`: 响应式按钮布局能力，根据窗口宽度动态调整按钮排列方式

### Modified Capabilities
- `resizable-split-panes`: 修改现有spec，确保格式构建器区域也能适应窗口大小变化

## Impact

- **受影响代码**: `src/invoice_renamer/gui/format_builder.py` 中的按钮布局逻辑
- **新增依赖**: 无
- **兼容性**: 向后兼容，不影响现有功能
- **用户体验**: 显著改善，按钮在任何窗口尺寸下都可见