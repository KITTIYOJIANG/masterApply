# Feishu Robotics Supervisor

这个工作流负责把你的机器人路线固定配方自动推送到飞书：

- 每天 08:00：今日执行卡
- 每天 22:00：晚间交账卡
- 每周日 21:00：周复盘卡

## 1. 飞书里创建机器人

在飞书里新建一个群，例如：

```text
机器人路线监督室
```

添加自定义机器人，复制 webhook URL。

建议机器人安全设置：

- 第一版可以用关键词，例如 `机器人路线`
- 如果开启签名，把密钥保存为 `FEISHU_BOT_SECRET`

## 2. GitHub Actions 方式

在 GitHub 仓库中添加 Secrets：

```text
FEISHU_WEBHOOK_URL
FEISHU_BOT_SECRET
```

其中 `FEISHU_BOT_SECRET` 可选，只有机器人开启签名校验时才需要。

工作流文件：

```text
.github/workflows/feishu-robotics-supervisor.yml
```

GitHub cron 使用 UTC：

- `0 0 * * *` = 北京/上海 08:00
- `0 14 * * *` = 北京/上海 22:00
- `0 13 * * 0` = 北京/上海周日 21:00

你也可以在 Actions 页面手动运行 `workflow_dispatch`，选择：

```text
morning
evening
sunday
```

## 3. 本地测试

预览卡片，不发送：

```powershell
python .\automation\feishu_supervisor.py --mode morning --dry-run
python .\automation\feishu_supervisor.py --mode evening --dry-run
python .\automation\feishu_supervisor.py --mode sunday --dry-run
```

本地发送：

```powershell
$env:FEISHU_WEBHOOK_URL="你的飞书机器人 webhook"
python .\automation\feishu_supervisor.py --mode morning
```

如果开启签名：

```powershell
$env:FEISHU_BOT_SECRET="你的机器人签名密钥"
```

## 4. Windows 本地定时任务

如果你不想依赖 GitHub Actions，可以安装本地计划任务：

```powershell
$env:FEISHU_WEBHOOK_URL="你的飞书机器人 webhook"
powershell -ExecutionPolicy Bypass -File .\automation\install_windows_feishu_tasks.ps1
```

注意：Windows 计划任务可能读不到当前 PowerShell 临时环境变量。更稳的做法是把 `FEISHU_WEBHOOK_URL` 设置成用户级环境变量：

```powershell
[Environment]::SetEnvironmentVariable("FEISHU_WEBHOOK_URL", "你的飞书机器人 webhook", "User")
```

然后重新打开终端。

## 5. 每周进度

脚本读取：

```text
automation/robotics_week_state.json
```

你可以每晚手动更新其中数字，飞书卡片里的进度条会跟着变化。

## 6. 每天自动布置推进任务

早安卡会读取：

```text
automation/robotics_daily_task_plan.json
```

它会根据星期自动给你布置关联推进任务：

```text
周一：定周目标 + 健康检查
周二：实时视觉数据采集
周三：标注 + benchmark
周四：修一个真实问题
周五：项目包装 + 联系
周六：深度项目块
周日：硬指标复盘
```

如果你要改每天任务，只改这个 JSON 文件即可。比如要把周二改成 ROS2 导航，就修改：

```json
"1": {
  "title": "周二：ROS2 导航推进",
  "project": "跑通 Nav2 demo 并记录截图。",
  "study": "学习 TF/URDF 60 分钟。",
  "artifact": "Nav2 运行截图 + 技术记录。"
}
```

后续可以继续升级：

- 从 GitHub commit 数自动更新 `commit_count`
- 从 LeetCode 记录自动更新题数
- 从飞书多维表格读取每日记录
- 晚上没完成时推送更强提醒
