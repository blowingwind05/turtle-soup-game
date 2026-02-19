# 海龟汤 (Situation Puzzle) 项目

这是一个基于 LangChain 实现的“海龟汤”推理游戏。除了内置的经典谜题外，还集成了基于大模型的高质量谜题生成模块。

## 项目结构
- `main.py`: 游戏主入口，负责处理交互逻辑。
- `game_logic.py`: 核心游戏逻辑，包括 LangChain 主持人配置和预设谜题。
- `puzzle_generator.py`: 谜题生成模块，采用“构思-评价-格式化”两阶段法生成本格推理谜题。
- `test_puzzle_generator.py`: 独立测试脚本，用于观察不同大模型的谜题生成效果。
- `.env`: API 密钥和模型配置。

## 运行步骤

1. **配置环境**
   请将 `.env.example` 重命名为 `.env`，然后填入您的 API 配置（支持 ModelScope 等 OpenAI 兼容接口）：
   ```bash
   mv .env.example .env
   ```
   在 `.env` 中修改如下项：
   ```env
   LLM_API_KEY=your_api_key
   LLM_BASE_URL=your_base_url
   LLM_MODEL_NAME=your_model_name
   ```

2. **安装依赖**
   ```bash
   pip install langchain langchain-openai python-dotenv pydantic
   ```

3. **启动游戏**
   运行 `main.py`：
   ```bash
   python main.py
   ```

## 核心功能与特色

### 1. 智能谜题生成 (G)
在主菜单输入 `G`，程序将调用大模型即时创作一个全新的本格推理谜题。
- **两阶段法**：模型先进行“自由构思与自我评价”，确保逻辑自洽、风格鲜明且无超自然元素，最后再提取为 JSON 格式。
- **本格保证**：严格限制解释必须基于现实逻辑，排除鬼魂、外星人等设定。
- **重口味/黑暗元素**：支持创作更具冲击力的社会现实题材。

### 2. 自动化游戏判定
主持人会在玩家猜中真相时自动发送 `[游戏结束]` 信号。程序接收到信号后会热情宣布挑战成功并自动返回主菜单。

### 3. 多模型基准测试
使用 `python test_puzzle_generator.py` 可以观察模型在生成谜题时的“思考过程（草案与自评）”。

## 玩法介绍
1. 游戏给出一段神秘的场景（汤面）。
2. 你需要通过提出“是/否”类问题来推导真相。
3. 输入 `help` 可请求主持人提供微小暗示。
4. 输入 `reveal` 可直接查看汤底。
5. 输入 `exit` 退出游戏。
