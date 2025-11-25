# src/agent.py
import os
from datetime import datetime
from src.llm_client import get_completion
from src.prompts import ANALYSIS_SYSTEM_PROMPT
from src.knowledge import get_concept_guide # 改匯入新的導讀函式

class PsychAgent:
    def __init__(self):
        self.user_name = ""
        self.partner_name = ""
        self.context = ""
        self.chat_logs = ""

    def ask(self, question):
        print(f"\n🤖 諮商師: {question}")
        return input(f">> ").strip()

    def ask_multiline(self, question):
        print(f"\n🤖 諮商師: {question}")
        print("(請輸入內容，輸入完畢後請在新的一行輸入 'DONE' 來送出)")
        buffer = []
        while True:
            line = input(">> ")
            if line.strip().upper() == "DONE":
                break
            if line.strip():
                buffer.append(line)
        return "\n".join(buffer)

    def run_interview(self):
        print("\n" + "="*50)
        print("歡迎來到 AI 情感諮商室 ❤️")
        print("我是你的專屬分析師，在開始分析前，我想先認識你們。")
        print("="*50)

        # 1. 基本資訊
        self.user_name = self.ask("請問怎麼稱呼您？")
        self.partner_name = self.ask(f"嗨 {self.user_name}，請問讓您感到煩惱的對象叫什麼名字？")

        # 2. 主觀描述
        self.context = self.ask_multiline(
            f"好的，{self.user_name}。能不能跟我說說，最近您跟 {self.partner_name} 之間發生了什麼情感問題？\n(您可以盡情抱怨或描述當下的情境)"
        )

        # 3. 客觀對話
        self.chat_logs = self.ask_multiline(
            f"了解... 聽起來確實不容易。為了讓我分析得更準確，\n我可以看一下您跟 {self.partner_name} 的聊天紀錄嗎？\n(請直接複製貼上對話內容)"
        )

        # 4. 開始分析
        print(f"\n(收到。正在統整 {self.user_name} 的描述與聊天紀錄，進行分析中...)\n")
        self.generate_report()

    def generate_report(self):
        # 1. 呼叫 LLM
        final_prompt = ANALYSIS_SYSTEM_PROMPT.format(
            user_name=self.user_name,
            partner_name=self.partner_name,
            context=self.context,
            chat_logs=self.chat_logs
        )
        
        messages = [{"role": "user", "content": final_prompt}]
        llm_analysis = get_completion(messages)

        if llm_analysis:
            # 2. 組合報告： 先放導讀 + 再放 AI 分析
            full_report = get_concept_guide() + "\n" + llm_analysis
            
            # 3. 顯示與存檔
            print(full_report)
            self.save_report(full_report)

    def save_report(self, content):
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/report_{self.user_name}_vs_{self.partner_name}_{timestamp}.md"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n\n💾 完整報告已存檔至: {filename}")
        except Exception as e:
            print(f"存檔失敗: {e}")