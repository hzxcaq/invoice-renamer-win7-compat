## ADDED Requirements

### Requirement: GitHub Actions自动化打包
系统 SHALL 使用GitHub Actions工作流自动打包Windows 7兼容的可执行文件。

#### Scenario: 自动触发打包
- **WHEN** 开发者推送版本标签（如v1.0.0）到GitHub仓库
- **THEN** GitHub Actions SHALL 自动触发Windows 7版本的打包流程

### Requirement: Python 3.7环境打包
系统 SHALL 使用Python 3.7环境进行Windows 7版本的打包。

#### Scenario: 正确设置Python环境
- **WHEN** GitHub Actions工作流开始运行
- **THEN** 系统 SHALL 安装并配置Python 3.7环境
- **AND** 所有依赖 SHALL 在Python 3.7环境中正确安装

### Requirement: 生成兼容的可执行文件
系统 SHALL 生成在Windows 7上可直接运行的可执行文件。

#### Scenario: 生成Windows 7兼容版本
- **WHEN** 打包流程完成
- **THEN** 系统 SHALL 生成名为`发票批量重命名工具_Win7.exe`的可执行文件
- **AND** 该文件 SHALL 在Windows 7 SP1上无需额外补丁即可运行

### Requirement: 自动发布到GitHub Releases
系统 SHALL 自动将生成的可执行文件发布到GitHub Releases。

#### Scenario: 创建发布版本
- **WHEN** 打包流程成功完成
- **THEN** 系统 SHALL 创建一个新的GitHub Release
- **AND** Release标签 SHALL 与推送的标签一致
- **AND** 生成的exe文件 SHALL 作为Release附件上传

### Requirement: 打包流程文档化
系统 SHALL 提供清晰的打包流程文档。

#### Scenario: 文档完整性
- **WHEN** 用户查看项目文档
- **THEN** SHALL 找到Windows 7版本的打包说明
- **AND** SHALL 找到如何触发打包流程的说明