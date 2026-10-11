# SSH 补查：运行中改向与子代理继续执行

补查日期：2026-10-12。SSH 已恢复连接，本次取得 20 个额外静态文件：评估运行程序 `sand-eval-runner.cjs`，以及执行服务 `index.js`、分块文件、启动器、包信息和对应版权说明。

## 结论

继续检查本机代码确实取得了更完整的运行机制实现。新增评估程序包含共享 harness 的本地 runner、steer 收件队列、后台子代理控制和提醒组装代码。它补强了机制证据，但尚不能直接证明线上 Temporal Worker 对每条消息采用相同策略。

## 运行中的消息注入

[`SandSteerInbox`](excerpts/eval-564631-turn-steer.ts.txt) 在 `beginRun()` 后接收消息，将其包装成 `userMessageAction` 放进数组，并通知已注册的监听器。`pop()` 使用 `shift()`，在这条实现中按收件顺序读取。

`enqueue()` 返回 `{kind: "steered", deliveredAtStepBoundary: Promise}`；无活动运行时返回 `no-live-run`。`receiver()` 暴露 `hasPendingUserInjections` 和 `onUserInjectionAdmitted`，并通过 [`conversationActionReceiver`](excerpts/eval-566183-turn-run-shell.ts.txt) 传给执行器。消费失败可以将已取出的消息放回队首；运行结束会停止接收并将尚未交付的消息标为失败。调用方是否再入队，需要另查调用链。

这些代码支持“运行期间可以接收新消息并在步骤边界处理”。步骤边界交付不等同于每个正在执行的外部工具都能立即终止。

## 父代理纠正后台子代理

[`createSubagentRuntime`](excerpts/eval-526093-subagent-runtime.ts.txt) 的 `steerSubagent()` 验证子代理仍在运行后：

1. 将纠正消息存入 `pendingSubagentSteers`。
2. 调用同一子代理 runner 的 `interrupt()`。
3. 当前运行结算时，读取纠正消息，复用同一个 runner 调用 `runSandAgentTurn()`。

[`formatSteerPrompt`](excerpts/eval-504520-steer-prompt.txt) 明确要求从当前任务位置继续，不要重新开始。

因此这条实现允许中断当前运行并在原会话中继续任务。“不丢上下文”不能概括成“从不打断当前 turn”。它与上面的步骤边界注入是两条不同路径。

纠正消息以子代理 ID 为键保存在 Map 中；同一子代理在结算前收到多次 `set()` 会覆盖前一个待处理值。这是此本地实现的行为，不能推广为云端所有用户消息都会覆盖。

## 未完成任务提醒的实际组装

[`createTurnRunShell.interrupt()`](excerpts/eval-566183-turn-run-shell.ts.txt) 在已经派发的活动运行被 supersede 时设置 `unfinishedTasksReminderPending`。下一次非 action-only 运行将该标记或显式选项传给 `assembleTurnAction()`。

[`userMessageReminders()` 与 prompt glue](excerpts/eval-523378-user-message-reminders.txt) 根据 `unfinishedTasks` 添加 `UNFINISHED_TASKS_REMINDER`；组装时还检查 `allowsSystemReminder(host, "unfinishedTasks")`。这说明提醒存在有条件的实际注入路径，但不是每次中断、每个 harness 都无条件添加。

## 云端 Worker 的查找范围

本次检查了主程序、评估程序、执行服务及其顶层 JS 分块，并查看相关依赖目录和运行进程的执行文件/脚本路径。

这些文件中未找到 `@temporalio/worker`、`@temporalio/workflow`、`@temporalio/client`、`NativeConnection`、`defineSignal(`、`proxyActivities(`、`workflowBundle` 或 `taskQueue:`。被检查的顶层 node_modules 中也未看到 `@temporalio`。运行中的相关 Node 进程对应 host、工具执行、桌面和同步服务。

这些结果支持“已检查的本机运行程序不是一份完整的 Temporal Worker 部署”的判断。关键词未命中和进程枚举不能证明整台机器绝不存在其他语言、改名、动态获取或尚未检查的实现。尚未取得线上 Workflow 的消息选择、队列、取消传播和跨任务调度代码。

## 对原调查的补充

原报告中“云端 worker 的实际调度源码不在本次取得的文件中”仍成立。应补充：已找到更完整的共享 runner 实现；本机代码具有继续调查价值，线上 Workflow/Worker 调度仍需更多证据核实。

本次仅查看静态代码和进程信息，没有启动评估程序或发送测试消息。
