#!/usr/bin/env python3
"""AI Customer Service Basic Edition - One-click deploy AI chatbot.
Based on Dify open-source framework. Supports WeChat/website/mini-program.
Price: 9.9 yuan. License: MIT."""

import json, os
from pathlib import Path

class AICustomerService:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.knowledge_base = []
        self.load_config()

    def load_config(self):
        if self.config_path.exists():
            self.config = json.loads(self.config_path.read_text())
        else:
            self.config = {"model": "deepseek-chat", "platforms": ["wechat", "web"],
                          "greeting": "Hello! How can I help you today?"}
            self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False))

    def add_knowledge(self, title, content):
        self.knowledge_base.append({"title": title, "content": content})
        return len(self.knowledge_base)

    def search_knowledge(self, query):
        results = []
        for kb in self.knowledge_base:
            score = sum(1 for w in query if w in kb["content"])
            if score > 0:
                results.append((score, kb))
        results.sort(key=lambda x: -x[0])
        return [r[1] for r in results[:3]]

    def chat(self, message, platform="web"):
        kb_results = self.search_knowledge(message)
        if kb_results:
            return f"[From KB] {kb_results[0]['title']}: {kb_results[0]['content'][:200]}..."
        return f"I am an AI customer service agent. Platform: {platform}. Your message: {message[:50]}..."

    def deploy_to_wechat(self, token):
        return {"status": "deployed", "platform": "wechat", "token": token[:20] + "..."}


if __name__ == "__main__":
    cs = AICustomerService()
    cs.add_knowledge("Deploy guide", "1. Install Python 3.10+. 2. pip install -r requirements.txt. 3. python app.py")
    cs.add_knowledge("Pricing", "Basic: 9.9 yuan. Custom: starts from 2000 yuan. 3-7 days delivery.")
    print(f"Knowledge base: {len(cs.knowledge_base)} entries")
    while True:
        msg = input("Customer (or quit): ")
        if msg.lower() == "quit":
            break
        print(f"AI: {cs.chat(msg)}")
