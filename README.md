# 发票批量重命名工具

一款简单易用的发票批量重命名工具，支持Windows 7及更高版本。

## 项目结构

```
invoice-renamer/
├── .github/workflows/            # GitHub Actions工作流
│   ├── build-win7.yml           # Windows 7版本打包工作流
│   └── build-multi.yml          # 多版本打包工作流
├── src/                          # 源代码目录
│   └── invoice_renamer/          # 主程序包
│       ├── main.py               # 主程序入口
│       ├── gui/                  # 图形界面模块
│       │   ├── main_window.py    # 主窗口
│       │   ├── file_selector.py  # 文件选择器
│       │   ├── excel_viewer.py   # Excel预览器
│       │   ├── format_builder.py # 格式构建器
│       │   └── preview_table.py  # 预览表格
│       ├── core/                 # 核心逻辑
│       │   ├── excel_reader.py   # Excel读取
│       │   ├── file_matcher.py   # 文件匹配
│       │   ├── renamer.py        # 重命名逻辑
│       │   └── utils.py          # 工具函数
│       └── tests/                # 测试模块
│           ├── test_excel_reader.py
│           ├── test_file_matcher.py
│           └── test_renamer.py
├── dist/                         # 打包输出目录
│   ├── 发票批量重命名工具_Win7.exe   # Windows 7兼容版本
│   └── 发票批量重命名工具_Win10.exe  # Windows 10/11版本
├── build/                        # 打包临时文件
├── openspec/                     # OpenSpec变更管理
├── design.md                     # 设计文档
├── plan.md                       # 实施计划
├── final_report.html             # 项目完成报告（HTML格式）
├── build_exe.py                  # 打包脚本
├── create_test_data.py           # 测试数据创建脚本
├── test_gui.py                   # GUI测试脚本
├── test_full_flow.py             # 完整流程测试脚本
├── 发票批量重命名工具.spec        # PyInstaller配置文件（Windows 10/11）
└── 发票批量重命名工具_v2.spec     # PyInstaller配置文件（Windows 7）
```

## 功能特点

1. **灵活格式定义**：可以根据Excel表格中的列自由组合重命名格式
2. **智能匹配**：自动从文件名中提取发票号码，与Excel数据匹配
3. **实时预览**：在重命名前可以预览效果
4. **安全操作**：提供备份和撤销功能
5. **简单易用**：图形界面，点击按钮即可操作

## 系统要求

- Windows 7 或更高版本
- Python 3.8 或更高版本（如果从源码运行）

## 安装使用

### 方法一：直接运行exe文件（推荐）

#### 下载说明

本项目提供两个版本的可执行文件，适用于不同的Windows系统：

| 版本 | 文件名 | 兼容系统 | 说明 |
|------|--------|----------|------|
| Windows 7 版本 | `发票批量重命名工具_Win7.exe` | Windows 7 SP1 及更高版本 | 使用 Python 3.7 打包，无需额外补丁 |
| Windows 10/11 版本 | `发票批量重命名工具_Win10.exe` | Windows 10 及更高版本 | 使用 Python 3.11 打包，推荐在现代系统使用 |

#### 下载步骤

1. 访问 [GitHub Releases](https://github.com/your-username/invoice-renamer/releases) 页面
2. 根据您的Windows版本选择合适的文件下载
3. 双击运行下载的exe文件
4. 按照界面提示操作

#### 版本选择指南

- **Windows 7 用户**：请选择 `发票批量重命名工具_Win7.exe`
- **Windows 10/11 用户**：推荐使用 `发票批量重命名工具_Win10.exe`（也兼容Windows 7）
- **不确定系统版本**：可以选择 `发票批量重命名工具_Win7.exe`（兼容性更广）

### 方法二：从源码运行

1. 进入 `src/invoice_renamer/` 目录
2. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行主程序：
   ```bash
   python main.py
   ```

## 使用说明

### 步骤1：选择目录
点击"选择目录"按钮，选择包含发票PDF文件的文件夹。

### 步骤2：选择Excel文件（可选）
如果有Excel表格，点击"选择Excel"按钮选择文件。Excel表格应包含发票信息，如发票号码、金额、公司名称等。

### 步骤3：定义重命名格式
1. 在"可用列"列表中选择要使用的列
2. 点击"添加"按钮将列添加到"已选列"列表
3. 使用"上移"/"下移"按钮调整列的顺序
4. 选择分隔符（下划线、短横线、空格等）
5. 查看"格式预览"确认格式

### 步骤4：预览重命名结果
点击"预览重命名"按钮，查看原始文件名和新文件名的对应关系。

### 步骤5：执行重命名
确认无误后，点击"开始重命名"按钮执行批量重命名。

### 撤销操作
如果需要撤销重命名，点击"撤销重命名"按钮。

## 文件匹配规则

### 有Excel表格时
1. 优先从PDF文件名中提取发票号码
   - 支持"DZFP"格式：DZFP12345678.pdf → 12345678
   - 支持其他格式：invoice_12345678.pdf → 12345678
2. 将提取的发票号码与Excel中的"发票号码"列匹配
3. 匹配成功则建立对应关系

### 没有Excel表格时
程序会列出所有PDF文件，用户可以定义基于原始文件名的重命名格式。

## 测试说明

### 运行测试
```bash
# 进入源代码目录
cd src/invoice_renamer

# 运行所有测试
python -m pytest tests/ -v
```

### 使用真实数据测试
项目包含真实测试数据，位于 `D:\Document\ai\4月` 目录：
- 包含242条发票记录的Excel文件
- 32个PDF发票文件
- 匹配率：100%

```bash
# 运行真实数据测试
python test_real_data.py
```

### 创建测试数据
```bash
# 创建测试Excel和PDF文件
python create_test_data.py
```

### 测试GUI
```bash
# 测试GUI是否正常启动
python test_gui.py
```

### 完整流程测试
```bash
# 测试完整业务流程
python test_full_flow.py
```

## 打包说明

### 自动打包（推荐）

本项目使用GitHub Actions进行自动化打包，支持同时打包Windows 7和Windows 10/11版本。

#### 触发打包

1. **推送版本标签**：
   ```bash
   # 创建标签
   git tag v1.0.0
   
   # 推送标签
   git push origin v1.0.0
   ```

2. **手动触发**：
   - 访问GitHub仓库的Actions页面
   - 选择"Build Multi-Version Release"工作流
   - 点击"Run workflow"按钮

#### 打包流程

GitHub Actions会自动：
1. 使用Python 3.7打包Windows 7兼容版本
2. 使用Python 3.11打包Windows 10/11版本
3. 创建GitHub Release并上传两个版本的exe文件

### 手动打包

#### 本地打包Windows 10/11版本
```bash
# 运行打包脚本
python build_exe.py
```

#### 本地打包Windows 7版本
```bash
# 创建Python 3.7虚拟环境
conda create -n win7_env python=3.7
conda activate win7_env

# 安装依赖
pip install -r src/invoice_renamer/requirements.txt
pip install pyinstaller

# 打包
pyinstaller --onefile --windowed --name="发票批量重命名工具_Win7" src/invoice_renamer/main.py
```

## 注意事项

1. **文件名安全**：程序会自动移除文件名中的非法字符（\ / : * ? " < > |）
2. **重名处理**：如果重命名后有重名文件，程序会自动添加序号避免覆盖
3. **备份文件**：重命名前会自动创建备份文件，位于目录下的`.backup`文件夹中
4. **中文支持**：完全支持中文文件名

## 常见问题

### Q: 程序无法运行怎么办？
A: 请确保您的系统是Windows 7或更高版本。如果是在Windows 7上运行，请下载`发票批量重命名工具_Win7.exe`版本。

### Q: Windows 7上运行提示缺少DLL文件怎么办？
A: 请下载`发票批量重命名工具_Win7.exe`版本，该版本使用Python 3.7打包，完全兼容Windows 7，无需额外补丁。

### Q: Excel文件无法读取怎么办？
A: 请确保Excel文件是.xlsx格式，并且第一行是表头。

### Q: 发票号码匹配不上怎么办？
A: 程序会尝试多种方式匹配，如果仍然无法匹配，可能会按文件顺序匹配。

### Q: 重命名后可以撤销吗？
A: 可以。点击"撤销重命名"按钮即可恢复原始文件名。

### Q: 如何获取最新版本？
A: 访问[GitHub Releases](https://github.com/your-username/invoice-renamer/releases)页面，根据您的Windows版本选择合适的文件下载。

### Q: 两个版本有什么区别？
A: 功能完全一致，只是打包环境不同。Windows 7版本使用Python 3.7打包，兼容性更广；Windows 10/11版本使用Python 3.11打包，性能可能更好。

## 版本历史

### v1.0.0 (2026-05-30)
- 初始版本
- 支持Excel数据读取和格式定义
- 支持文件智能匹配
- 支持实时预览和批量重命名
- 支持备份和撤销功能