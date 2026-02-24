import os
import markdown
from enum import Enum
from datetime import datetime
from src.llm_client import get_completion
from src.prompts import ANALYSIS_SYSTEM_PROMPT
from src.knowledge import get_concept_guide

class State(Enum):
    INIT = 1
    PROCESS_CHUNK = 2
    AGGREGATE = 3
    DONE = 4
    
class PsychAgent:
    """
    核心 domain：給定 user_name / partner_name / context / chat_logs
    → 透過 FSM 與 Chunking 處理長文本，回傳完整分析報告
    """

    def __init__(self, user_name="", partner_name="", context="", chat_logs=""):
        self.user_name = user_name
        self.partner_name = partner_name
        self.context = context
        self.chat_logs = chat_logs
        
        # FSM 狀態與記憶體上下文 (Context)
        self.state = State.INIT
        self.chunks = []
        self.partial_results = []
        self.current_chunk_idx = 0

    def chunk_chat_logs(self, max_lines=50):
        """將長篇聊天紀錄切分為多個 Chunk"""
        lines = self.chat_logs.split('\n')
        chunks = []
        for i in range(0, len(lines), max_lines):
            chunk = "\n".join(lines[i:i + max_lines])
            if chunk.strip():
                chunks.append(chunk)
        return chunks if chunks else ["(無對話紀錄)"]

    def process_single_chunk(self, chunk_data):
        """處理單一 Chunk，請 LLM 提取局部特徵"""
        prompt = (
            f"你是一個情感分析助手。請分析以下聊天紀錄片段，"
            f"簡短列出是否有出現指責、逃避、焦慮等衝突行為？\n\n"
            f"{chunk_data}\n\n(請以條列式簡短回答)"
        )
        messages = [{"role": "user", "content": prompt}]
        return get_completion(messages)

    def build_final_prompt(self, aggregated_insights):
        """組合最終的 Prompt，將各 Chunk 提取的局部特徵整合進去"""
        # 將 Chunk 分析結果合併到背景描述中，增強 LLM 的判斷依據
        enhanced_context = f"{self.context}\n\n[系統萃取的對話局部特徵]:\n{aggregated_insights}"
        
        return ANALYSIS_SYSTEM_PROMPT.format(
            user_name=self.user_name,
            partner_name=self.partner_name,
            context=enhanced_context,
            chat_logs=self.chat_logs 
        )

    def analyze(self):
        """FSM 狀態機主迴圈 (Event Loop)"""
        self.state = State.INIT
        final_report = ""

        while self.state != State.DONE:
            
            if self.state == State.INIT:
                # 狀態：初始化與分塊
                self.chunks = self.chunk_chat_logs(max_lines=50) # 預設每 50 行一個 chunk
                self.current_chunk_idx = 0
                self.partial_results = []
                self.state = State.PROCESS_CHUNK  # 轉移狀態
                
            elif self.state == State.PROCESS_CHUNK:
                # 狀態：處理各個 Chunk
                if self.current_chunk_idx < len(self.chunks):
                    chunk_data = self.chunks[self.current_chunk_idx]
                    partial_insight = self.process_single_chunk(chunk_data)
                    
                    if partial_insight:
                        self.partial_results.append(f"片段 {self.current_chunk_idx + 1}: {partial_insight}")
                    
                    self.current_chunk_idx += 1
                else:
                    # 所有 Chunk 處理完畢，進入彙整
                    self.state = State.AGGREGATE

            elif self.state == State.AGGREGATE:
                # 狀態：全局彙整並生成最終報告
                aggregated_insights = "\n".join(self.partial_results)
                prompt = self.build_final_prompt(aggregated_insights)
                
                messages = [{"role": "user", "content": prompt}]
                llm_output = get_completion(messages)

                if not llm_output:
                    final_report = "（分析失敗：模型無回應）"
                else:
                    # 靜動態字串拼接
                    final_report = get_concept_guide() + "\n" + llm_output

                self.state = State.DONE  # 結束狀態機

        return final_report
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
