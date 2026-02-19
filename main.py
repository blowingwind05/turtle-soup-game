from game_logic import PUZZLES, GameSession
import sys

def clear_screen():
    print("\033[H\033[J", end="")

def main():
    print("--- 欢迎来到海龟汤 (Situation Puzzle) 游戏 ---")
    print("这是一个通过提问寻求真相的推理游戏。")
    print("-" * 40)
    
    # 获取可用的汤列表
    for p in PUZZLES:
        print(f"[{p['id']}] {p['title']}")
    
    try:
        choice = int(input("\n请选择一个汤品（输入数字 1-3）: "))
        selected_puzzle = next((p for p in PUZZLES if p["id"] == choice), None)
        
        if not selected_puzzle:
            print("选择无效，程序退出。")
            return
            
        print("\n" + "=" * 40)
        print(f"【谜面】：{selected_puzzle['scenario']}")
        print("=" * 40)
        print("\n提示：请问我是/否命题。输入 'exit' 退出程序，输入 'reveal' 直接查看汤底。")
        
        # 初始化游戏会话
        session = GameSession(selected_puzzle)
        
        while True:
            question = input("\n[你的问题] >> ").strip()
            
            if not question:
                continue
                
            if question.lower() == 'exit':
                print("游戏结束，再见！")
                break
                
            if question.lower() == 'reveal':
                print(f"\n【真相】：{selected_puzzle['truth']}")
                print("\n游戏已结束。")
                break
            
            # 使用 LangChain 进行推理
            try:
                print("海龟汤主持人思考中...")
                response = session.ask(question)
                print(f"[主持人回答] << {response}")
                
            except Exception as e:
                print(f"\n[错误] 主持人似乎走神了（API 报错）: {e}")
                print("请检查您的 .env 文件中 API Key 是否正确配置。")
                break
                
    except ValueError:
        print("请输入有效的数字。")
    except KeyboardInterrupt:
        print("\n退出游戏。")

if __name__ == "__main__":
    main()
