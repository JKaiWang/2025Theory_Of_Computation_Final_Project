import os
import markdown
from datetime import datetime
from src.llm_client import get_completion
from src.prompts import ANALYSIS_SYSTEM_PROMPT
from src.knowledge import get_concept_guide

class PsychAgent:
    """
    核心 domain：給定 user_name / partner_name / context / chat_logs
    → 回傳完整分析報告（字串）
    不包含 I/O、不包含 input()、不包含 print()
    """

    def __init__(self, user_name="", partner_name="", context="", chat_logs=""):
        self.user_name = user_name
        self.partner_name = partner_name
        self.context = context
        self.chat_logs = chat_logs

    def build_prompt(self):
        """組合完整 Prompt"""
        return ANALYSIS_SYSTEM_PROMPT.format(
            user_name=self.user_name,
            partner_name=self.partner_name,
            context=self.context,
            chat_logs=self.chat_logs
        )

    def analyze(self):
        """執行 LLM，在前面加上心理學導讀"""
        prompt = self.build_prompt()
        messages = [{"role": "user", "content": prompt}]
        llm_output = get_completion(messages)

        if not llm_output:
            return "（分析失敗：模型無回應）"

        return get_concept_guide() + "\n" + llm_output
class ChatAgent:
    def __init__(self):
        self.history = [
            {"role": "system", "content": "你是一位溫和、專業的情感諮詢聊天機器人。"},
            {"role": "assistant", "content": "您好 😊 請問今天想聊什麼呢？"}
        ]
    def reply(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        response = get_completion(self.history)

        if not response:
            response = "抱歉，我剛剛有點分心了，可以再說一次嗎？"

        self.history.append({"role": "assistant", "content": response})
        return response