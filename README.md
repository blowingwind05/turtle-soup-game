# 海龟汤 (Situation Puzzle) LangChain 项目

这是一个基于 LangChain 实现的“海龟汤”推理游戏。

## 项目结构
- `main.py`: 游戏主入口，负责处理交互逻辑。
- `game_logic.py`: 核心 LangChain 逻辑，包括谜题定义和 LLM Chain 配置。
- `.env`: API 密钥和环境配置。

## 运行步骤

1. **配置环境**
   在根目录下找到 `.env` 文件，填入您的 OpenAI API Key。
   ```env
   OPENAI_API_KEY=sk-xxxx...
   ```

2. **安装依赖**
   通过以下命令安装所需的 Python 包：
   ```bash
   pip install langchain langchain-openai python-dotenv
   ```

3. **启动游戏**
   运行 `main.py`：
   ```bash
   python main.py
   ```

## 玩法介绍
1. 游戏会给出一个神秘的场景（汤面）。
2. 你需要通过不断提问（通常是只能回答“是”或“否”的问题）来推导故事背后的真相（汤底）。
3. 主持人（AI）会根据真相协助你：
   - 如果你的猜测接近真相，主持人会给出肯定的答复。
   - 如果你的问题与此无关，主主持人会告诉你。
   - 猜中核心点后，主持人会完整揭晓谜底。

## 支持指令
- 输入 `exit`: 退出程序
- 输入 `reveal`: 直接揭晓当前汤底
