# Fix: GUI布局问题 + 撤销重命名逻辑错误

## 问题描述

在测试发票批量重命名工具时发现两个问题：

1. **Excel预览挤掉PDF文件列表**：选择目录后出现文件列表，但选择Excel文件后，Excel预览会把文件列表挤掉，导致PDF文件列表不显示。
2. **撤销重命名失败**：重命名后点击"撤销重命名"按钮，撤销操作失败。

## 根因分析

### 问题1：Excel预览挤掉PDF文件列表

**文件**：`src/invoice_renamer/gui/main_window.py` 第76-84行

当前布局：`excel_frame` 和 `pdf_frame` 都使用 `pack(side=LEFT/RIGHT, fill=BOTH, expand=True)` 并排放置。当Excel加载数据后，Treeview的自然高度随行数增长，挤压PDF列表的空间。

```
当前布局：
┌─────────────────────────────────────────────────────────┐
│  data_frame (pack fill=BOTH, expand=True)               │
│  ┌───────────────────────────┬─────────────────────────┐│
│  │ excel_frame               │ pdf_frame               ││
│  │ (pack LEFT, BOTH, expand) │ (pack RIGHT, BOTH, exp) ││
│  │                           │                         ││
│  │  ┌──────────────────────┐ │  ┌───────────────────┐  ││
│  │  │   Treeview           │ │  │  Listbox          │  ││
│  │  │   (rows grow with    │ │  │  (被挤没了)        │  ││
│  │  │    data content)     │ │  │                   │  ││
│  │  │                      │ │  └───────────────────┘  ││
│  │  └──────────────────────┘ │                         ││
│  └───────────────────────────┴─────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

**修复方案**：将 `data_frame` 的布局从 `pack` 改为 `Grid` 布局，让 Excel 预览和 PDF 文件列表各占50%宽度，并为 Excel 预览设置固定高度约束。使用 `ttk.PanedWindow` 允许用户手动调整两个区域的大小。

### 问题2：撤销重命名逻辑反转

**文件**：`src/invoice_renamer/core/renamer.py` 第155-200行

备份格式：`{original_path}\t{new_filename}`

恢复逻辑（当前错误）：
```python
original_path, current_filename = parts

# ❌ BUG: 重命名后 original_path 已不存在！
if not os.path.exists(original_path):  # 所有文件都会跳过
    continue
```

重命名后：
- `original_path`（如 `D:\dir\原始文件.pdf`）→ 不存在了
- `current_path`（如 `D:\dir\new_name.pdf`）→ 实际文件在这里

恢复时检查 `original_path` 是否存在，但该文件已被重命名，所以所有文件都会被跳过。

**修复方案**：反转存在性检查逻辑：
```python
original_path, current_filename = parts
directory = os.path.dirname(original_path)
current_path = os.path.join(directory, current_filename)

# ✅ 检查重命名后的文件是否存在
if not os.path.exists(current_path):
    continue

# 重命名回原始文件名
os.rename(current_path, original_path)
```

## 实现任务

### Task 1: 修复撤销重命名逻辑
- **文件**：`src/invoice_renamer/core/renamer.py`
- **修改**：`restore_from_backup` 方法中反转存在性检查逻辑

### Task 2: 修复Excel预览布局
- **文件**：`src/invoice_renamer/gui/main_window.py`
- **修改**：`_create_widgets` 方法中 `data_frame` 的布局，使用 `Grid` 或 `PanedWindow`

### Task 3: 修复Excel预览高度约束
- **文件**：`src/invoice_renamer/gui/excel_viewer.py`
- **修改**：为 Treeview 设置最大显示行数或固定高度

## 验证

1. 选择目录 → 文件列表正常显示
2. 选择Excel → Excel预览和PDF文件列表并排显示，互不挤压
3. 重命名文件 → 撤销重命名 → 文件恢复到原始名称
