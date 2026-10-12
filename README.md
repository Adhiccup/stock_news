# Stock News AI Summarizer

A full-stack application that fetches recent stock news and generates summaries to help users quickly understand important company developments.

Built as a technical assessment for Finanzen.net.

## Tech Stack

- **Frontend:** React, TypeScript, Vite
- **Backend:** Python, FastAPI
- **News Provider:** Finnhub API
- **AI:** OpenAI API
- **Testing:** Pytest

## Features

- Search for stock news using ticker symbols such as AAPL or MSFT
- Fetch recent company news from Finnhub
- Generate AI-powered news summaries
- Display original article headlines and source links
- Switch between mock and real OpenAI summarization
- Handle missing configuration and external API errors

## Requirements

- Python 3.10+
- Node.js and npm
- Finnhub API key
- OpenAI API key for real AI summarization

## Backend Setup

From the project root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure:

```dotenv
FINNHUB_API_KEY=your_finnhub_key
OPENAI_API_KEY=your_openai_key
SUMMARY_MODE=openai
```

For development without OpenAI usage costs, set `SUMMARY_MODE=mock`.

Run:

```bash
fastapi dev main.py
```

The API runs at http://localhost:8000.

API documentation: http://localhost:8000/docs.

## Frontend Setup

Open another terminal and navigate to the frontend folder:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

Enter a stock symbol such as `AAPL` and click **Search**.

## API Endpoint

`GET /stocks/{symbol}`

Example:

```text
GET http://localhost:8000/stocks/AAPL
```

The API returns the stock symbol, summary, news articles, and summary mode.

## Running Tests

Inside the backend folder:

```bash
python -m pytest tests/ -v
```

The initial automated tests cover summary formatting, empty articles, API health, and missing Finnhub configuration.

The testing strategy uses mock data to avoid unnecessary external API calls. Full end-to-end verification requires valid API credentials.

## Design Decisions

**FastAPI:** Chosen for its simplicity, type annotations, and automatically generated API documentation.

**React and TypeScript:** Used to build a simple frontend with typed API responses.

**Separate summary service:** Keeps AI-related code independent from the HTTP endpoint.

**Environment variables:** Keep API credentials outside the source code.

**Mock mode:** Enables local development and testing without paid OpenAI requests.

## Limitations and Future Improvements

- Add caching to reduce repeated API requests.
- Add stronger validation for stock symbols and external API responses.
- Improve automated coverage for Finnhub and OpenAI failures.
- Support additional news providers and stock markets.
- Add request rate limiting and production deployment configuration.

## AI Tools Used

AI assistance was used during development for implementation guidance, code explanations, and documentation. The application should be reviewed, tested, and understood before submission.