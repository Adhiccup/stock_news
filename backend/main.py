
import os
from datetime import date, timedelta
from fastapi.middleware.cors import CORSMiddleware

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from ai_service import summarize_news


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")




@app.get("/")
def home():
    return {"message": "Stock News API is running!"}


@app.get("/stocks/{symbol}")
async def get_stock_news(symbol: str):
    if not FINNHUB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Finnhub API key is missing"
        )

    today = date.today()
    start_date = today - timedelta(days=7)

    url = "https://finnhub.io/api/v1/company-news"

    params = {
        "symbol": symbol.upper(),
        "from": start_date.isoformat(),
        "to": today.isoformat(),
        "token": FINNHUB_API_KEY,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            articles = response.json()

    except (httpx.HTTPError, ValueError):
        raise HTTPException(
            status_code=502,
            detail="Could not fetch stock news"
        )

    
    
    selected_articles = articles[:5]

    try:
        summary = await summarize_news(
            symbol.upper(),
            selected_articles
        )
    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI summarization failed"
        )

    return {
        "symbol": symbol.upper(),
        "summary": summary,
        "articles": selected_articles,
        "mode": os.getenv("SUMMARY_MODE", "mock").lower()
    }


