## Why

当前 Excel 读取模块只读取第一个 sheet（`发票基础信息`），但该 sheet 缺少"货物或应税劳务名称"等商品用途信息。实际发票 Excel 文件包含三个 sheet：

| Sheet | 行数 | 特点 |
|-------|------|------|
| 发票基础信息 | 132行 | 发票号码唯一，有金额/销方等基础信息，**无商品名称** |
| 信息汇总表 | 242行(132唯一) | **有"货物或应税劳务名称"**，但一张发票可能对应多条明细 |
| 建筑服务 | 3行 | 有建筑服务发生地、建筑项目名称等独有列 |

用户需要在重命名时使用商品名称（如"镀锌管"）、建筑信息等字段，当前方案无法支持。

## What Changes

- **ExcelReader** 新增多 sheet 读取和合并方法：以发票基础信息为底，按发票号码 LEFT JOIN 信息汇总表（取金额最大的那条明细的商品名称，去掉分类前缀），LEFT JOIN 建筑服务（取独有列）
- **FormatBuilder** 从扁平 Listbox 改造为树状选择器（ttk.Treeview），按 sheet 分组展示列，方便快速查找和选择
- **MainWindow** 适配新的 ExcelReader 接口，传递分组信息给 FormatBuilder
- **ExcelViewer** 预览合并后的数据

## Capabilities

### New Capabilities
- `multi-sheet-merge`: 读取 Excel 所有 sheet，按发票号码智能合并为一行一条发票的扁平数据
- `goods-name-extraction`: 从"货物或应税劳务名称"中提取商品名（去掉 `*分类*` 前缀），取金额最大的明细
- `tree-column-selector`: 格式构建器使用树状结构按 sheet 分组展示可选列

### Modified Capabilities
- `excel-reading`: ExcelReader 从单 sheet 读取扩展为多 sheet 合并读取

## Impact

- **代码影响**: 修改 `excel_reader.py`、`format_builder.py`、`main_window.py`
- **依赖影响**: 无新依赖（openpyxl 已支持多 sheet 读取）
- **兼容性**: 单 sheet 的旧 Excel 文件仍然兼容（退化为原有行为）
- **GUI 影响**: 格式构建器从 Listbox 改为 Treeview，交互方式变化
