#!/usr/bin/env python3.12

import json
import asyncio
import os


async def main():
    histories = json.loads(os.getenv("GPTSCRIPT_CONTEXT", "{}"))
    chat = ["<USER_MESSAGES>"]

    completion = histories.get("completion", {})

    i = 1

    for message in completion.get("messages", []):
        role = message.get("role", "")
        text = " ".join(
            [part["text"] for part in message.get("content", []) if "text" in part]
        )
        if role == "user" and len(text) > 0 and not text.startswith("Call "):
            chat.append(f"[User Message #{i}] {text}")
            i += 1

    chat.append("</USER_MESSAGES>")
    print("\n".join(chat))


asyncio.run(main())
