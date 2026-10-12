# Grok Bot 运行机制调查

本仓库收录 Grok Bot 的静态代码、通用 skills 和调查说明，重点分析用户在 Bot 工作期间继续发送消息、改变任务方向，以及后台任务与子代理的协调机制。

主要阅读入口：

- [运行机制调查](运行机制调查.md)：调查结论、证据与已确认范围。
- [SSH 补查](SSH补查.md)：消息注入、子代理中断后继续执行、未完成任务提醒的组装代码。
- [扩大范围调查](扩大范围调查.md)：部署查找范围、完整消费链、工具等待释放及策略开启条件。
- [代码证据](evidence.txt)和[摘录索引](excerpts/index.tsv)：定位原始模块与行号。
- [通用 skills](installed-skills/)：routines、channels、box-desktop、code-changes 等配套说明。

当前实例使用云端 temporal harness；包内旧本地调度器的优先级代码与共享执行引擎能力，需要结合调查说明中的证据边界理解。

采集日期：2026-10-12（北京时间）。已取得的主程序版本标记：7345aa4。

## 内容

- sources/opt/sand/sand-host/host-main.cjs：静态主程序，包含模块路径、协议、工具定义、提示词和共享执行引擎代码。
- sources/opt/sand/sand-host/sand-eval-runner.cjs：评估运行程序，包含共享 runner 和子代理控制实现。
- sources/exec-daemon/：工具执行服务及其 JS 分块。
- sources/usr/local/bin/：监督启动、桌面启动、桌面分流等脚本。
- sources/workspace/：通用 MCP 启动器和调用客户端。
- excerpts/：相关模块的摘录；每行前面的数字是原始主程序的一基行号。
- installed-skills/：routines、box-desktop、code-changes、channels、no-connector-fallback 的通用说明。
- evidence.txt、evidence-index.json：关键代码证据及定位索引。
- 运行机制调查.md：调查说明；链接改为包内相对路径。
- manifest.json：每个内容文件的大小与 SHA-256。

## 资料范围

资料包含 43 个静态代码及配套文件和相关模块摘录，供运行机制调查和代码阅读。未包含完整依赖、系统镜像、平台服务端源码；云端调度细节和本次会话的全部 feature gate 尚未确认。
