from game_logic import PUZZLES, GameSession
from puzzle_generator import generate_puzzle
import sys

def clear_screen():
    print("\033[H\033[J", end="")

def main():
    print("--- 欢迎来到海龟汤 (Situation Puzzle) 游戏 ---")
    print("这是一个通过提问寻求真相的推理游戏。")
    print("-" * 40)
    
    # 获取可用的汤列表
    for p in PUZZLES:
        title = p.get('title', '未命名汤品')
        print(f"[{p['id']}] {title}")
    print(f"[G] 随机生成一个新谜题 (大模型发散思维)")
    
    try:
        user_input = input("\n请选择一个汤品（输入数字 1-3 或 G）: ").strip().upper()
        
        if user_input == 'G':
            print("\n正在通过大模型发散思维生成新谜题，请稍候...")
            selected_puzzle = generate_puzzle()
            if not selected_puzzle:
                print("谜题生成失败，请检查网络或 API 配置。")
                return
        else:
            choice = int(user_input)
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
                response, finished = session.ask(question)
                print(f"[主持人回答] << {response}")
                
                if finished:
                    print("\n" + "*" * 40)
                    print("检测到游戏结束信号：恭喜你成功解开了谜题！")
                    print("*" * 40)
                    break
                
            except Exception as e:
                print(f"\n[错误] 主持人似乎走神了（API 报错）: {e}")
                print("请检查您的 .env 文件中 API Key 是否正确配置。")
                break
                
    except ValueError:
        print("请输入有效的指令（数字或 G）。")
    except KeyboardInterrupt:
        print("\n退出游戏。")

if __name__ == "__main__":
    main()
