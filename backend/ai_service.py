
import os
from openai import AsyncOpenAI


async def summarize_news(symbol: str, articles: list) -> str:
    mode = os.getenv("SUMMARY_MODE", "mock").lower()

    if not articles:
        return f"No recent news found for {symbol}."

    if mode == "mock":
        return mock_summary(symbol, articles)

    if mode == "openai":
        return await openai_summary(symbol, articles)

    raise ValueError(f"Unsupported summary mode: {mode}")


def mock_summary(symbol: str, articles: list) -> str:
    headlines = [
        article.get("headline", "")
        for article in articles
        if article.get("headline")
    ]

    return (
        f"Mock summary for {symbol}:\n"
        + "\n".join(f"- {headline}" for headline in headlines)
    )


async def openai_summary(symbol: str, articles: list) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing")

    client = AsyncOpenAI(api_key=api_key, timeout=20.0)

    news_text = ""

    for article in articles:
        news_text += (
            f"Headline: {article.get('headline', '')}\n"
            f"Description: {article.get('summary', '')}\n"
            f"Source: {article.get('source', '')}\n\n"
        )

    response = await client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "You are a financial news summarizer. "
            "Summarize the supplied articles in 3 to 5 sentences. "
            "Explain the important developments for traders. "
            "Use only the supplied news. "
            "Do not invent facts or give investment advice. "
            "If information is insufficient, say so."
        ),
        input=f"Recent news for {symbol}:\n\n{news_text}",
    )

    return response.output_text
