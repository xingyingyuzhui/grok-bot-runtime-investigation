# 密钥复查与脱敏记录

检查日期：2026-10-12。范围：本目录全部内容文件及对应 ZIP。

已清除 `sources/opt/sand/sand-host/host-main.cjs` 两处内置值：

- 原始第 529556 行：`STATSIG_CLIENT_KEY`，客户端 key，替换为 `REDACTED_STATSIG_CLIENT_KEY`。
- 原始第 647542 行：`DEFAULT_AUTH_TOKEN`，默认认证令牌，替换为 `REDACTED_DEFAULT_AUTH_TOKEN`。

两处替换均保留代码结构及行号。ZIP、原采集目录中的对应源码和 runtime-source.tar.gz 已同步脱敏；清单 SHA-256 已重新计算。未保留包含原值的备份。

检查包括：私钥 PEM 标记、常见 API/云服务 token 格式、JWT、URL 内嵌账号密码、认证头、凭据字段字面量、认证默认值及高熵字符串。

未发现上述模式的其他实际凭据。OAuth client ID、环境变量名称、凭据文件路径、协议字段及编码字符表属于代码定义，保留。未读取远端当前凭据，未验证凭据有效性。此记录反映静态扫描结果。


本次 SSH 补查新增 20 个静态文件，经过私钥、常见服务 token、JWT、凭据字段字面量、认证头和高熵字符串复查，未发现额外需要清除的凭据值。

认证 URL 检查命中了执行服务中 5 处模板表达式，均由运行时变量构造，没有保存账号密码或 token 字面值；代码原样保留。
