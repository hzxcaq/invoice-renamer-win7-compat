## ADDED Requirements

### Requirement: 多版本并行打包
系统 SHALL 支持同时打包Windows 7和Windows 10/11版本。

#### Scenario: 并行打包两个版本
- **WHEN** 触发打包流程
- **THEN** 系统 SHALL 同时启动两个打包任务
- **AND** 一个任务使用Python 3.7打包Windows 7版本
- **AND** 另一个任务使用Python 3.11打包Windows 10/11版本

### Requirement: 版本区分明确
系统 SHALL 确保两个版本有明确的区分。

#### Scenario: 文件名区分
- **WHEN** 打包完成
- **THEN** Windows 7版本 SHALL 命名为`发票批量重命名工具_Win7.exe`
- **AND** Windows 10/11版本 SHALL 命名为`发票批量重命名工具_Win10.exe`

### Requirement: 统一发布
系统 SHALL 将两个版本统一发布到同一个GitHub Release。

#### Scenario: 统一发布到Release
- **WHEN** 两个版本都打包完成
- **THEN** 系统 SHALL 将两个exe文件上传到同一个GitHub Release
- **AND** Release页面 SHALL 明确标注两个版本的兼容性

### Requirement: 用户选择指导
系统 SHALL 为用户提供清晰的版本选择指导。

#### Scenario: 版本选择说明
- **WHEN** 用户访问GitHub Release页面
- **THEN** SHALL 看到明确的版本说明
- **AND** SHALL 能根据自己的Windows版本选择合适的下载文件

### Requirement: 功能一致性
系统 SHALL 确保两个版本的功能完全一致。

#### Scenario: 功能测试通过
- **WHEN** 两个版本都打包完成
- **THEN** 两个版本 SHALL 通过相同的功能测试
- **AND** 用户体验 SHALL 保持一致