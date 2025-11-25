# main.py
from src.agent import PsychAgent

if __name__ == "__main__":
    # 建立一個諮商師實例
    agent = PsychAgent()
    
    # 開始訪談
    try:
        agent.run_interview()
    except KeyboardInterrupt:
        print("\n\n(諮商已中斷)")