# src/interfaces/cli_agent.py
from src.agent import PsychAgent
from datetime import datetime
import os


class CLIAgent:
    """
    負責 CLI 互動流程（input/print），不動核心邏輯。
    """

    @staticmethod
    def ask(question):
        print(f"\n🤖 諮商師: {question}")
        return input(">> ").strip()

    @staticmethod
    def multiline(question):
        print(f"\n🤖 諮商師: {question}")
        print("(多行輸入，結束請輸入 DONE)")
        buffer = []
        while True:
            line = input(">> ")
            if line.strip().upper() == "DONE":
                break
            if line.strip():
                buffer.append(line)
        return "\n".join(buffer)

    @classmethod
    def run(cls):
        print("=" * 50)
        print("AI 情感諮商室（CLI 版）")
        print("=" * 50)

        user_name = cls.ask("請問怎麼稱呼您？")
        partner_name = cls.ask("對象叫什麼名字？")
        context = cls.multiline("請描述你們近期發生的問題：")
        chat_logs = cls.multiline("請貼上聊天紀錄：")

        agent = PsychAgent(
            user_name=user_name,
            partner_name=partner_name,
            context=context,
            chat_logs=chat_logs
        )

        report = agent.analyze()
        print(report)

        cls.save_report(report, user_name, partner_name)

    @staticmethod
    def save_report(report, user, partner):
        if not os.path.exists("reports"):
            os.makedirs("reports")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"reports/report_{user}_vs_{partner}_{timestamp}.md"

        with open(fname, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\n💾 已存檔：{fname}")
