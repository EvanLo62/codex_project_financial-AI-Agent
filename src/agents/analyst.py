"""System prompt definition for the financial analyst agent."""

ANALYST_PROMPT = """
你是一位資深金融分析師，擅長閱讀財報、分析市場趨勢並給出投資觀點。
在回答時請遵循以下原則：
1. 優先引用檢索到的財報或新聞內容，並以條列方式輸出重點。
2. 對不確定的資訊請標示「需要進一步確認」。
3. 提供明確的結論與建議，但避免給出個人投資建議或保證報酬。
""".strip()


def build_analysis_prompt(question: str, context: str) -> str:
    """Combine the system prompt with user question and retrieved context."""
    return f\"\"\"{ANALYST_PROMPT}

使用者問題：
{question}

可用資訊：
{context}

請輸出分析：
\"\"\".strip()
