## Why

当前使用Python 3.11 + PyInstaller打包的exe文件在Windows 7上无法运行，提示缺少`api-ms-win-core-path-l1-1-0.dll`。这是因为Python 3.11不再原生支持Windows 7，而项目设计要求兼容Windows 7及更高版本。需要建立一个自动化打包流程，确保为Windows 7用户提供兼容的可执行文件。

## What Changes

- 添加GitHub Actions工作流，使用Python 3.7环境自动打包Windows 7兼容版本
- 创建专用的PyInstaller配置文件，针对Windows 7优化
- 更新项目文档，说明不同Windows版本的下载和使用方式
- 保持现有Windows 10/11版本的打包流程不变

## Capabilities

### New Capabilities
- `win7-build-automation`: 自动化Windows 7兼容版本的打包和发布流程
- `multi-version-distribution`: 支持同时发布Windows 7和Windows 10/11版本

### Modified Capabilities
<!-- 无现有能力需要修改 -->

## Impact

- **代码影响**: 添加`.github/workflows/`目录下的工作流文件
- **依赖影响**: 无新依赖，但需要确保项目依赖兼容Python 3.7
- **系统影响**: 需要GitHub仓库启用Actions功能
- **用户体验**: Windows 7用户可以直接下载兼容版本，无需手动安装补丁