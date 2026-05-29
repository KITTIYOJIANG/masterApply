from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "automation" / "robotics_supervisor_config.json"
STATE_PATH = ROOT / "automation" / "robotics_week_state.json"
TASK_PLAN_PATH = ROOT / "automation" / "robotics_daily_task_plan.json"
SHANGHAI = ZoneInfo("Asia/Shanghai")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return load_json(path)


def progress_bar(current: float, target: float, width: int = 10) -> str:
    if target <= 0:
        return "□" * width
    filled = max(0, min(width, int(round(width * current / target))))
    return "■" * filled + "□" * (width - filled)


def format_progress(config: dict, state: dict) -> str:
    targets = config["weekly_targets"]
    rows = [
        ("学习", state.get("study_hours", 0), targets["study_hours"], "h"),
        ("项目", state.get("project_hours", 0), targets["project_hours"], "h"),
        ("LeetCode", state.get("leetcode_count", 0), targets["leetcode_count"], "题"),
        ("英文", state.get("english_hours", 0), targets["english_hours"], "h"),
        ("联系", state.get("contact_count", 0), targets["contact_count"], "个")
    ]
    lines = []
    for name, current, target, unit in rows:
        lines.append(f"**{name}**  {progress_bar(float(current), float(target))}  {current}/{target} {unit}")
    return "\n".join(lines)


def format_evening_template() -> str:
    return "\n".join(
        [
            "**学习**：__ 分钟 / 内容：",
            "**项目**：__ 分钟 / 仓库或文件：",
            "**LeetCode**：__ 题 / 题号：",
            "**英文**：__ 分钟 / 内容：",
            "**联系**：__ 个 / 对象：",
            "**可展示成果**：",
            "**明天第一步**：",
        ]
    )


def format_sunday_template() -> str:
    return "\n".join(
        [
            "**本周最大成果**：",
            "**本周最大卡点**：",
            "**下周第一项目**：",
            "**下周第一步**：",
        ]
    )


def pick_daily_task(task_plan: dict, now: dt.datetime) -> dict:
    if not task_plan:
        return {}
    weekday = str(now.weekday())
    return task_plan.get("weekday_tasks", {}).get(weekday, task_plan.get("fallback_task", {}))


def format_daily_assignment(task_plan: dict, now: dt.datetime) -> str:
    task = pick_daily_task(task_plan, now)
    if not task:
        return ""

    rules = "\n".join(f"- {rule}" for rule in task_plan.get("rules", []))
    content = f"""**今日关联推进任务：{task.get("title", "默认推进任务")}**

**项目推进**：{task.get("project", "")}
**学习推进**：{task.get("study", "")}
**今日证据**：{task.get("artifact", "")}
"""
    if task_plan.get("project_theme"):
        content += f"\n**本阶段主题**：{task_plan['project_theme']}"
    if rules:
        content += f"\n\n**执行规则**\n{rules}"
    return content


def card_div(text: str) -> dict:
    return {"tag": "div", "text": {"tag": "lark_md", "content": text}}


def card_hr() -> dict:
    return {"tag": "hr"}


def build_morning_card(config: dict, state: dict, now: dt.datetime, task_plan: dict | None = None) -> dict:
    tasks = config["today_default_tasks"]
    content = f"""**机器人路线｜今天不是靠心情启动，是靠系统启动。**

定位：{config["identity"]}
主线：{config["main_line"]}
当前项目：{config["active_project"]}

**今日必须交付：**
1. 学习：{tasks["study"]}
2. 项目：{tasks["project"]}
3. LeetCode：{tasks["leetcode"]}
4. 英文：{tasks["english"]}
5. 联系：{tasks["contact"]}
6. 成果：{tasks["artifact"]}
"""
    progress = format_progress(config, state)
    rules = "\n".join(f"- {rule}" for rule in config["focus_rules"])
    assignment = format_daily_assignment(task_plan or {}, now)
    elements = [
        card_div(content),
        card_hr(),
    ]
    if assignment:
        elements.extend([card_div(assignment), card_hr()])
    elements.extend(
        [
            card_div("**本周进度条**\n" + progress),
            card_div("**今天的规矩**\n" + rules),
            card_div("晚上 22:10 会追问你交账。别让未来的自己来擦屁股。")
        ]
    )
    return make_card(
        title=f"早安执行卡｜{now:%Y-%m-%d}",
        template="blue",
        elements=elements,
    )


def build_evening_card(config: dict, state: dict, now: dt.datetime) -> dict:
    progress = format_progress(config, state)
    content = """**机器人路线｜交账时间到了。**

请在飞书/追踪表里填 7 行事实：

最低标准：今天必须有一个可展示证据，比如 commit、截图、benchmark 输出、技术记录、投递记录。"""
    return make_card(
        title=f"晚间交账卡｜{now:%Y-%m-%d}",
        template="orange",
        elements=[
            card_div(content),
            card_div(format_evening_template()),
            card_hr(),
            card_div("**当前周进度**\n" + progress),
            card_div(f"项目状态：{state.get('project_progress', '待更新')}")
        ],
    )


def build_sunday_card(config: dict, state: dict, now: dt.datetime) -> dict:
    metrics = "\n".join(f"- {item}：" for item in config["weekly_review_metrics"])
    progress = format_progress(config, state)
    content = f"""**机器人路线｜周日复盘，只看硬指标。**

{metrics}

请补充：
"""
    return make_card(
        title=f"周日复盘卡｜{now:%Y-%m-%d}",
        template="purple",
        elements=[
            card_div(content),
            card_div(format_sunday_template()),
            card_hr(),
            card_div("**本周进度条**\n" + progress),
            card_div("如果这一周没有可展示成果，下周第一优先级必须砍掉娱乐和泛泛刷课。")
        ],
    )


def make_card(title: str, template: str, elements: list[dict]) -> dict:
    return {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": template,
                "title": {"tag": "plain_text", "content": title}
            },
            "elements": elements,
        },
    }


def sign_payload(payload: dict, secret: str) -> dict:
    timestamp = str(int(time.time()))
    string_to_sign = f"{timestamp}\n{secret}"
    sign = base64.b64encode(
        hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    ).decode("utf-8")
    payload["timestamp"] = timestamp
    payload["sign"] = sign
    return payload


def post_to_feishu(webhook_url: str, payload: dict) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            text = response.read().decode("utf-8")
            print(text)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu webhook failed: HTTP {exc.code}: {body}") from exc


def infer_mode(now: dt.datetime) -> str:
    if now.weekday() == 6 and 20 <= now.hour <= 22:
        return "sunday"
    if now.hour < 12:
        return "morning"
    return "evening"


def build_payload(mode: str, config: dict, state: dict, now: dt.datetime, task_plan: dict | None = None) -> dict:
    if mode == "morning":
        return build_morning_card(config, state, now, task_plan=task_plan)
    if mode == "evening":
        return build_evening_card(config, state, now)
    if mode == "sunday":
        return build_sunday_card(config, state, now)
    raise ValueError(f"Unknown mode: {mode}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Push robotics execution cards to a Feishu custom bot.")
    parser.add_argument("--mode", choices=["morning", "evening", "sunday", "auto"], default="auto")
    parser.add_argument("--config", default=str(CONFIG_PATH))
    parser.add_argument("--state", default=str(STATE_PATH))
    parser.add_argument("--task-plan", default=str(TASK_PLAN_PATH))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    now = dt.datetime.now(SHANGHAI)
    mode = infer_mode(now) if args.mode == "auto" else args.mode
    config = load_json(Path(args.config))
    state = load_json(Path(args.state))
    task_plan = load_optional_json(Path(args.task_plan))
    payload = build_payload(mode, config, state, now, task_plan=task_plan)

    secret = os.getenv("FEISHU_BOT_SECRET", "").strip()
    if secret:
        payload = sign_payload(payload, secret)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    webhook_url = os.getenv("FEISHU_WEBHOOK_URL", "").strip()
    if not webhook_url:
        print("FEISHU_WEBHOOK_URL is not set. Use --dry-run to preview the card.", file=sys.stderr)
        return 2

    post_to_feishu(webhook_url, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
