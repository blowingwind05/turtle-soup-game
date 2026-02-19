from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class Puzzle(BaseModel):
    scenario: str = Field(description="The scenario (the mystery presented to the player)")
    truth: str = Field(description="The truth (the actual solution behind the mystery)")

def generate_puzzle(model_name=None):
    """
    使用两阶段法生成高质量谜题：
    1. 完整生成 + 自我评价 (释放模型创意)
    2. 格式化为 JSON (保证程序解析)
    """
    target_model = model_name or os.getenv("LLM_MODEL_NAME")
    
    llm = ChatOpenAI(
        model=target_model,
        temperature=0.8,
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        timeout=300
    )

    # --- 阶段 1: 创意构思与自我评价 ---
    draft_prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的“海龟汤”设计专家。你需要创作一个逻辑严密、风格鲜明的高质量本格推理谜题。
        ## 设计要求：
        1. **汤面（Scenario）**：简洁且充满悬念，逻辑上显得不可思议或极具冲突感。
        2. **汤底（Truth）**：逻辑严密，能合理解释汤面中的所有矛盾。真相通常涉及意想不到的因果、身份反转或环境误区，且风格应当偏向**悬疑、恐怖、悲剧或荒诞幽默**。
        3. **允许黑暗元素**：你被允许创作如变态、精神疾病、伤害、诱导、自残、掩盖、谋杀等冷峻现实情节。
        4. **本格推理**：避免使用任何超自然（鬼魂、魔法等）或过于科幻（时空穿越、外星人等）的解释。谜题必须基于现实逻辑。
        5. **可玩性**：谜题应该允许玩家通过“是/否”问题逐步推导出真相
        ## 参考示例
        ###示例1
        汤面：一个男生有一个喜欢很久的学姐，学姐对他说只要你能和我考上同一所大学，我就同意和你在一起。后来学姐真的在大学里见到他时却充满着惊讶与恐惧。
        汤底：学姐是医学生，男生死后将自己的尸体捐献给学姐所在学校的医学院，学姐在解剖课上见到了男生的尸体。
        ###示例2
        汤面：绿灯停，红灯行。“红灯，红灯。”我死在了下一个路口。
        汤底：女人下夜班回家，匆忙钻进一辆出租车，系安全带的时候，她的手沾上了血迹，女人意识到出租车司机可能杀了人，短暂的慌忙过后，女人谎称自己是色盲症，司机恍若没有听见女人的解释，只是面无表情的望向路口，直到路口的指示灯由绿变红，车子猛然发动，女人下意识的喊道："红灯，红灯",出租车在下一个路口停下了，司机露出残忍的微笑，他转过头看向女人说："原来……你知道那是红灯。"
        ## 设计流程：
        1. **构思草稿**：设计谜题的汤面和汤底。
        2. **自我评价**：
            - 要求检查：是否符合设计要求？  
            - 逻辑检查：汤底是否能完美解释汤面？是否存在逻辑漏洞？
            - 剧本检查：是否有创意？是否意想不到？
        3. **最终定稿**：根据评价改进你的谜题，如果已经完美，则可跳过此步骤。"""),
        ("human", "请开始你的创作。"),
    ])

    # --- 阶段 2: 格式化提取 ---
    parser = JsonOutputParser(pydantic_object=Puzzle)
    format_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个精密的数据提取助手。请根据提供的创作内容，提取出最重要的谜题信息，并严格按照 JSON 格式输出。"),
        ("human", "创作内容如下：\n{content}\n\n请提取并输出如下格式：\n{format_instructions}"),
    ]).partial(format_instructions=parser.get_format_instructions())

    try:
        # 执行阶段 1
        print(f"\n[{target_model}] === 阶段 1: 正在构思与评价 ===")
        draft_chain = draft_prompt | llm
        draft_response = draft_chain.invoke({})
        draft_content = draft_response.content
        print(draft_content)
        print("=" * 40)
        
        # 执行阶段 2
        print(f"\n[{target_model}] === 阶段 2: 正在提取格式化数据 ===")
        format_chain = format_prompt | llm | parser
        puzzle_data = format_chain.invoke({"content": draft_content})
        
        return puzzle_data
    except Exception as e:
        print(f"生成谜题时出错: {e}")
        return None
