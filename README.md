# Grok Bot 运行机制调查
本仓库收录脱敏后的静态代码、通用 skills 和调查说明，重点分析用户在 Bot 工作期间继续发送消息、改变任务方向，以及后台任务与子代理的协调机制。

主要阅读入口：

- [运行机制调查](运行机制调查.md)：调查结论、证据与已确认范围。
- [代码证据](evidence.txt)和[摘录索引](excerpts/index.tsv)：定位原始模块与行号。
- [通用 skills](installed-skills/)：routines、channels、box-desktop、code-changes 等配套说明。
- [密钥复查记录](SECRET_SCAN.md)：两处内置 key/认证令牌的脱敏位置。

当前实例使用云端 temporal harness；包内旧本地调度器的优先级代码与共享执行引擎能力，需要结合调查说明中的证据边界理解。

采集日期：2026-10-12（北京时间）。已取得的主程序版本标记：7345aa4。

本包聚焦用户消息介入、后台任务、执行者纠正与停止、父代理唤醒及工具执行支撑。

## 内容

- sources/opt/sand/sand-host/host-main.cjs：静态主程序，包含模块路径、协议、工具定义、提示词和共享执行引擎代码。
- sources/usr/local/bin/：监督启动、桌面启动、桌面分流等脚本。
- sources/workspace/：通用 MCP 启动器和调用客户端。
- excerpts/：相关模块的摘录；每行前面的数字是原始主程序的一基行号。
- installed-skills/：routines、box-desktop、code-changes、channels、no-connector-fallback 的通用说明。
- evidence.txt、evidence-index.json：关键代码证据及定位索引。
- 运行机制调查.md：调查说明；链接改为包内相对路径。
- manifest.json：每个内容文件的大小与 SHA-256。

## 排除项

用户运行状态快照、Bot profile/设置、用户任务及作品、消息与聊天记录、数据库和 WAL、日志、浏览器资料与 cookie、环境变量转储、密钥和凭据文件均未打包。
未包含本地原采集压缩包，以避免重复和混入其他材料。

## 采集与使用范围

静态源码已对两处内置 key/认证令牌进行脱敏，保持原始行号；调查说明移除了当前用户、主机和代理身份信息。包内文件不含采集过程中读取的用户凭据值。密钥复查方法和处理位置见 SECRET_SCAN.md。
补充采集执行服务代码时，跳板机的 2222 转发拒绝连接，因此本包未包含 /exec-daemon/index.js 及该次尝试追加的文件。已成功取得的 8 个静态源码/脚本文件全部包含。
资料供代码调查和阅读；未包含完整依赖、系统镜像或平台服务端源码，也未确认云端本次会话的全部 feature gate。
