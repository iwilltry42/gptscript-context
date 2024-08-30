#!/usr/bin/env python3.12

import json
import asyncio
import os


async def main():
    histories_str = os.getenv("GPTSCRIPT_CONTEXT", "")

    if not histories_str:
        print("<USER_MESSAGES></USER_MESSAGES>")
        return

    histories = json.loads(histories_str)

    limit = int(os.getenv("LIMIT", "50"))

    chat = ["<USER_MESSAGES>"]
    msgs = []

    completion = histories.get("completion", {})

    i = 1

    for message in completion.get("messages", []):
        role = message.get("role", "")
        text = " ".join(
            [part["text"] for part in message.get("content", []) if "text" in part]
        )
        if role == "user" and len(text) > 0 and not text.startswith("Call "):
            msgs.append(f"[User Message #{i}] {text}")
            i += 1

    if limit > len(msgs):
        limit = len(msgs)

    if limit == 0:
        for msg in msgs:
            chat.append(msg)
    else:
        for msg in msgs[-limit:]:
            chat.append(msg)

    chat.append("</USER_MESSAGES>")
    print("\n".join(chat))


asyncio.run(main())
