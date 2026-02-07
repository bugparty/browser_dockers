# 浏览器容器稳定性测试

这个 GitHub Actions 工作流会自动测试浏览器容器的稳定性，确保它不会意外崩溃或重启。

## 概述

该工作流对 Chrome 浏览器容器执行 5 分钟的稳定性测试，以验证：
- 容器成功启动
- 测试期间不会重启
- 健康检查持续通过
- Chrome DevTools Protocol 端点保持响应

## 触发条件

工作流在以下情况下触发：
- **拉取请求（Pull Request）** 修改了：
  - `Dockerfile.chrome`
  - `entrypoint.sh`
  - `compose.local.yml`
  - `.github/workflows/browser-stability-test.yml`
- **推送到 main/master 分支** 修改了相同的文件
- **手动触发** 通过 `workflow_dispatch`

## 测试流程

### 测试平台
- `linux/amd64` (在 ubuntu-latest 上运行)
- `linux/arm64` (在 ubuntu-24.04-arm 上运行)

### 测试步骤

1. **设置环境**: 初始化环境并为 `appuser` 目录设置正确的权限
2. **构建镜像**: 从 `Dockerfile.chrome` 构建 Chrome 浏览器 Docker 镜像
3. **启动容器**: 使用 docker-compose 启动浏览器容器
4. **监控运行**: 在 5 分钟内执行 10 次健康检查（每 30 秒一次）：
   - 验证容器正在运行
   - 检查重启次数未增加
   - 测试健康端点（`http://127.0.0.1:9223/json/version`）
5. **生成报告**: 生成详细的测试摘要

### 成功标准

测试通过条件：
- 全部 10 次健康检查通过（100% 成功率）
- 容器重启次数保持为 0
- 容器始终保持"running"状态
- 健康端点每次检查都有响应

## 测试结果

结果显示在 GitHub Actions 摘要中，包括：
- 测试平台（linux/amd64 或 linux/arm64）
- 通过/失败状态
- 执行的检查总数
- 通过/失败的检查数量
- 详细日志（失败时）

## 健康检查详情

健康检查验证：
- 容器状态为"running"
- 重启次数未增加
- Chrome DevTools Protocol 端点 `http://127.0.0.1:9223/json/version` 成功响应

## 故障排除

如果测试失败：
1. 检查 GitHub Actions 日志获取详细错误信息
2. 查看"Container Logs"部分以查看浏览器输出
3. 常见问题：
   - 挂载卷的权限问题
   - 运行器的资源限制
   - 网络连接问题
   - Chrome/Chromium 启动失败

## 超时设置

整个工作流有 15 分钟的超时限制以防止任务挂起。5 分钟的测试本身应该会更快完成，额外的时间用于构建和设置。
