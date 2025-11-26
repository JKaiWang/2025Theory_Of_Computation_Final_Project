# src/interfaces/web_agent.py
from src.agent import PsychAgent


class WebAgent:
    """
    Web API 用，不用 DONE，不用多段 input。
    一次接收完整欄位，回傳完整報告字串。
    """

    @staticmethod
    def generate_report(user_name, partner_name, context, chat_logs):
        agent = PsychAgent(
            user_name=user_name,
            partner_name=partner_name,
            context=context,
            chat_logs=chat_logs
        )

        return agent.analyze()
