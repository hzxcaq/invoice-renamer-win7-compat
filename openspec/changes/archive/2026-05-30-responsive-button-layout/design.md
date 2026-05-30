## Context

当前格式构建器（FormatBuilder）中的"上移"和"下移"按钮使用水平排列，当窗口宽度不足时按钮会被挤掉不显示。用户需要在任何窗口尺寸下都能访问这些按钮来调整列顺序。

### 当前布局结构
- `FormatBuilder` 组件位于主窗口的左侧区域
- 按钮位于 `right_frame` 底部，使用 `pack(side=tk.LEFT)` 水平排列
- 窗口最小宽度设置为1000像素

## Goals / Non-Goals

**Goals:**
- 实现响应式按钮布局，根据窗口宽度动态调整排列方式
- 确保按钮在任何窗口尺寸下都可见且可点击
- 保持现有功能不变，只改进布局逻辑
- 添加平滑的布局切换，避免界面跳动

**Non-Goals:**
- 不改变按钮的功能逻辑
- 不调整其他UI组件的布局
- 不修改窗口的最小尺寸设置
- 不添加新的UI组件或功能

## Decisions

### 决策1：布局切换策略
**选择**：基于窗口宽度的动态切换
- 宽度 ≥ 1200像素：水平排列
- 宽度 < 1200像素：垂直排列

**理由**：
- 1200像素是常见的屏幕宽度阈值
- 水平排列在宽屏时更符合用户习惯
- 垂直排列在窄屏时更节省空间

**备选方案**：
1. 固定垂直排列：简单但改变用户习惯
2. 使用网格布局：更灵活但实现复杂
3. 添加滚动条：复杂且用户体验差

### 决策2：监听方式
**选择**：监听窗口的 `<Configure>` 事件
- 绑定到主窗口的 Configure 事件
- 在事件处理中检查窗口宽度
- 动态调整按钮布局

**理由**：
- `<Configure>` 事件在窗口大小变化时触发
- 可以实时响应窗口大小变化
- 实现简单，性能开销小

### 决策3：布局切换实现
**选择**：重新打包按钮组件
- 在宽度变化时，先移除所有按钮
- 根据新宽度重新打包按钮
- 使用 `pack_forget()` 和 `pack()` 方法

**理由**：
- Tkinter 的 pack 布局管理器支持动态重新打包
- 实现简单，不需要复杂的布局计算
- 可以保持按钮的原有样式和大小

## Risks / Trade-offs

### 风险1：布局切换时的闪烁
**风险**：在布局切换时可能出现短暂的界面闪烁
**缓解措施**：
- 使用 `after_idle()` 延迟执行布局切换
- 在切换前保存按钮状态，切换后恢复
- 测试不同窗口尺寸下的切换效果

### 风险2：性能影响
**风险**：频繁的窗口大小变化可能导致性能问题
**缓解措施**：
- 使用节流（throttle）技术，限制事件处理频率
- 只在宽度变化超过10像素时才触发布局切换
- 缓存窗口宽度，避免重复计算

### 风险3：用户体验变化
**风险**：用户可能不习惯按钮布局的变化
**缓解措施**：
- 在切换时添加视觉提示（如渐变效果）
- 保持按钮的大小和样式不变
- 提供设置选项允许用户固定布局（可选）

## 实现细节

### 关键代码修改点
1. 在 `FormatBuilder.__init__` 中添加窗口宽度监听
2. 创建 `_update_button_layout()` 方法处理布局切换
3. 修改按钮打包逻辑，支持水平和垂直两种模式
4. 添加宽度阈值常量（`RESPONSIVE_THRESHOLD = 1200`）

### 布局切换逻辑
```python
def _update_button_layout(self):
    """根据窗口宽度更新按钮布局"""
    window_width = self.winfo_toplevel().winfo_width()
    
    # 移除现有按钮
    self.up_button.pack_forget()
    self.down_button.pack_forget()
    
    if window_width >= RESPONSIVE_THRESHOLD:
        # 水平排列
        self.up_button.pack(side=tk.LEFT, padx=(0, 5))
        self.down_button.pack(side=tk.LEFT)
    else:
        # 垂直排列
        self.up_button.pack(fill=tk.X, pady=(0, 2))
        self.down_button.pack(fill=tk.X)
```

### 事件处理
```python
def _on_window_configure(self, event):
    """窗口大小变化事件处理"""
    # 节流处理，避免频繁更新
    if hasattr(self, '_configure_after_id'):
        self.after_cancel(self._configure_after_id)
    self._configure_after_id = self.after(100, self._update_button_layout)
```

## 测试策略

1. **单元测试**：测试布局切换逻辑
2. **集成测试**：测试在不同窗口尺寸下的按钮可见性
3. **用户测试**：邀请用户测试响应式布局效果
4. **性能测试**：测试频繁窗口大小变化时的性能表现