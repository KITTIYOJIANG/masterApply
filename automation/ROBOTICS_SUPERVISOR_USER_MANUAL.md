# 机器人路线自动监督系统使用手册

## 1. 系统用途

这个系统不是普通提醒事项，而是你的外部监督器。

它每天通过飞书群自动推送任务卡片，强制你围绕这条主线行动：

> 会 AI/代码的机器人与无人系统算法工程师，主攻规划控制、机器人系统、视觉/学习。

当前项目主线：

> 五子棋机器人：真实棋盘视觉 + AI 决策 + 机械臂接口。

## 2. 自动推送时间

GitHub Actions 会自动运行：

| 时间 | 卡片 | 目的 |
| --- | --- | --- |
| 每天 08:10 | 早安执行卡 | 布置今日任务 |
| 每天 22:10 | 晚间交账卡 | 逼你复盘和交付 |
| 每周日 21:10 | 周日复盘卡 | 看硬指标，定下周方向 |

时间按北京时间 / 上海时间理解。

## 3. 每天早上怎么做

收到早安执行卡后，不要重新规划，不要纠结方向。

你只需要在飞书群里回复：

```text
今日计划
学习：
项目：
LeetCode：
英文：
联系：
可展示成果：
```

示例：

```text
今日计划
学习：OpenCV HSV 阈值 60 分钟
项目：采集五子棋 live benchmark 8 张图
LeetCode：1 道 BFS
英文：读 robotics vision README 20 分钟
联系：整理北航灵巧手实验室问题清单
可展示成果：live_benchmark_20260528 数据目录 + label.txt
```

## 4. 白天最低执行标准

每天最低动作：

- 学习 60 分钟
- 项目 90 分钟
- LeetCode 1 题
- 英文 20 分钟
- 联系导师/公司 0-1 个
- 留下 1 个可展示成果

优先级：

1. 项目推进
2. 可展示成果
3. C++ / ROS2 / 控制 / 视觉基础
4. LeetCode 和英文
5. 联系导师/公司

## 5. 什么算可展示成果

至少满足一个：

- Git commit
- benchmark 输出
- 实验截图
- demo 视频
- 技术报告
- README 更新
- 联系导师/公司记录
- 项目问题分析文档

不要把“看了视频”“想了方向”“收藏了资料”当成果。

## 6. 每天晚上怎么交账

收到晚间交账卡后，在飞书群里回复：

```text
今日交账
学习：__ 分钟 / 内容：
项目：__ 分钟 / 仓库或文件：
LeetCode：__ 题 / 题号：
英文：__ 分钟 / 内容：
联系：__ 个 / 对象：
可展示成果：
明天第一步：
```

如果当天失败，也必须交账：

```text
今日交账
学习：0 分钟 / 内容：未完成
项目：0 分钟 / 仓库或文件：未完成
LeetCode：0 题
英文：0 分钟
联系：0 个
可展示成果：无
未完成原因：
补救动作：
明天第一步：
```

失败可以接受，失联不接受。

## 7. 周日怎么复盘

周日 21:10 收到复盘卡后，只看 5 个硬指标：

```text
周复盘
代码提交次数：
项目进度：
题目数：
联系数：
可展示成果：
本周最大成果：
本周最大卡点：
下周第一项目：
下周第一步：
```

如果一周没有可展示成果，下周必须砍掉泛泛刷课和娱乐时间，优先补项目证据。

## 8. 每天任务是怎么自动分配的

系统会按星期布置关联推进任务：

| 星期 | 自动任务主题 |
| --- | --- |
| 周一 | 定周目标 + 健康检查 |
| 周二 | 实时视觉数据采集 |
| 周三 | 标注 + benchmark |
| 周四 | 修一个真实问题 |
| 周五 | 项目包装 + 联系 |
| 周六 | 深度项目块 |
| 周日 | 硬指标复盘 |

任务配置文件：

```text
automation/robotics_daily_task_plan.json
```

如果你想改每天布置什么任务，只改这个文件。

## 9. 进度条从哪里来

飞书卡片里的进度条读取：

```text
automation/robotics_week_state.json
```

字段：

```json
{
  "study_hours": 0,
  "project_hours": 0,
  "leetcode_count": 0,
  "english_hours": 0,
  "contact_count": 0,
  "commit_count": 0,
  "artifact": "待更新",
  "project_progress": "待更新"
}
```

你可以每晚手动更新它。后续也可以升级为自动统计。

## 10. 手动测试推送

在本地测试早安卡：

```powershell
cd F:\Work\Portfolio\masterApply
python .\automation\feishu_supervisor.py --mode morning
```

测试晚间卡：

```powershell
python .\automation\feishu_supervisor.py --mode evening
```

测试周日卡：

```powershell
python .\automation\feishu_supervisor.py --mode sunday
```

只预览不发送：

```powershell
python .\automation\feishu_supervisor.py --mode morning --dry-run
```

## 11. GitHub Actions 手动运行

进入 GitHub 仓库：

```text
KITTIYOJIANG/masterApply
```

点击：

```text
Actions -> Feishu Robotics Supervisor -> Run workflow
```

选择：

```text
morning
evening
sunday
```

然后运行。

## 12. 常见问题

### GitHub Actions 成功但飞书没收到

检查 GitHub Secret：

```text
FEISHU_WEBHOOK_URL
```

是否填错。

### 报 Key Words Not Found

飞书机器人关键词校验没通过。

机器人关键词建议设为：

```text
机器人路线
```

脚本卡片正文已经包含这个词。

### 飞书卡片格式很丑

运行最新版脚本。现在进度条已经改成：

```text
学习  □□□□□□□□□□  0/15 h
```

不是代码块。

### 想改提醒时间

修改：

```text
.github/workflows/feishu-robotics-supervisor.yml
```

注意 GitHub Actions cron 使用 UTC。

当前设置：

```text
10 0 * * *    北京时间 08:10
10 14 * * *   北京时间 22:10
10 13 * * 0   北京时间周日 21:10
```

## 13. 使用原则

每天只有一个核心问题：

> 今天有没有让“机器人算法候选人”这个身份更可信？

如果答案是否定的，晚上交账必须写补救动作。

## 14. 当前下一步

当前项目下一步：

```text
五子棋机器人实时摄像头泛化验证
```

推荐命令：

```powershell
cd D:\Projects\gomoku_project

python tools/live_vision_monitor.py `
  --camera-id 0 `
  --corners "72,18;513,28;508,461;74,468" `
  --capture-dir calibration_tools/live_benchmark_20260528
```

拍摄新数据后：

1. 填 `label.txt`
2. 跑 `benchmark_vision.py`
3. 记录结果
4. 如果有问题，修一个最关键问题并 commit
