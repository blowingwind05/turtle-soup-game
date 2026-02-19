from puzzle_generator import generate_puzzle
import time

import time

def run_test(models):
    print(f"--- 谜题生成效果测试 ---")
    
    for model in models:
        print(f"\n{'='*40}")
        print(f"当前测试模型: {model}")
        print(f"{'='*40}")
        
        start_eval = time.time()
        try:
            # generate_puzzle 内部会打印阶段 1 的原始输出
            puzzle = generate_puzzle(model_name=model)
            
            if puzzle:
                print(f"\n[生成成功] 最终耗时: {time.time() - start_eval:.2f}s")
                print("-" * 20)
                print(f"汤面: {puzzle.get('scenario')}")
                print(f"汤底: {puzzle.get('truth')}")
                print("-" * 20)
            else:
                print(f"模型 {model} 未能生成有效 JSON。")
        except Exception as e:
            print(f"模型 {model} 运行出错: {e}")
            
    print("\n--- 测试完成 ---")

if __name__ == "__main__":

    benchmark_models = [
        "deepseek-ai/DeepSeek-V3.2"
    ]
    run_test(benchmark_models)
