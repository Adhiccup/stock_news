
import pytest
from ai_service import mock_summary, summarize_news


def test_mock_summary():
    articles = [
        {"headline": "Apple announces a new product"},
        {"headline": "Apple reports higher revenue"},
    ]

    result = mock_summary("AAPL", articles)

    assert "Apple announces a new product" in result
    assert "Apple reports higher revenue" in result


@pytest.mark.asyncio
async def test_no_articles():
    result = await summarize_news("AAPL", [])

    assert result == "No recent news found for AAPL."
