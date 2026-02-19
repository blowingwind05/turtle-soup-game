from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import os
from dotenv import load_dotenv

load_dotenv()

# 海龟汤谜题定义 (Scenario 是题目, Truth 是答案)
PUZZLES = [
    {
        "id": 1,
        "title": "海龟汤 (Classic)",
        "scenario": "一男子走进一家餐厅，点了一碗海龟汤。喝了一口后，他失声痛哭，走出餐厅自杀了。",
        "truth": "该男子曾和家人遭遇海难。在荒岛上，快饿死时，他的父亲骗他说煮了海龟肉给他喝。实际上是父亲牺牲了自己的肉。男子在餐厅喝到真正的海龟汤，发现味道完全不同，意识到当年吃的是父亲的肉。"
    },
    {
        "id": 2,
        "title": "半根火柴",
        "scenario": "一个人死在沙漠里，手里攥着半根火柴。周围没有其他任何痕迹。",
        "truth": "他和其他游客乘热气球飞行。气球漏气，必须减轻重量。大家脱光衣服扔掉，仍不够重。最后抽签，谁抽到短的火柴就跳下去。他不幸抽到了，只能跳下气球。结果他死后气球飞走了。"
    },
    {
        "id": 3,
        "title": "点燃蜡烛",
        "scenario": "一个盲人点了一根蜡烛，不久就把火弄灭了，他知道自己死定了。",
        "truth": "他在潜艇里，电力中断了。他是唯一的幸存者且看不见。他点燃蜡烛想确定是否有氧气。蜡烛灭了，说明氧气耗尽了。"
    }
]

def get_game_chain(scenario, truth):
    """
    创建一个 LangChain 以作为海龟汤主持人。
    """
    # 显式使用环境变量中的配置，或者直接通过参数传入
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", # 现代 LangChain 中使用 model 替代 model_name
        temperature=0.2,       # 适度低温，保持逻辑严密
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

    system_prompt = f"""你是一名专业的‘海龟汤’（情境猜谜）主持人。
汤面（题目）：{scenario}
汤底（真相）：{truth}

你的任务是：
1. 玩家会针对故事背景提问，你的回答只能是：'是'、'不是'、'与此无关'。
2. 如果玩家非常接近真相或逻辑陷入死胡同，你可以提供极其微小的暗示（hint），但不要直接泄露真相。
3. 如果玩家猜中了核心真相，你应该热情地宣布挑战成功，并完整复述汤底（真相）。
4. 始终保持神秘、冷静且客观的风格。

重要：严禁在玩家猜到之前透露汤底的任何细节。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm
    return chain

class GameSession:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.chain = get_game_chain(puzzle["scenario"], puzzle["truth"])
        self.history = ChatMessageHistory()
        
    def ask(self, question):
        # 封装 LangChain 运行逻辑
        response = self.chain.invoke({
            "input": question,
            "history": self.history.messages
        })
        
        # 添加到历史记录
        self.history.add_user_message(question)
        self.history.add_ai_message(response.content)
        
        return response.content
