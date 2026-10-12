
import { useState } from "react";
import "./App.css";

type Article = {
  headline: string;
  url: string;
  source: string;
};

type StockResponse = {
  symbol: string;
  summary: string;
  articles: Article[];
  mode: string;
};

function App() {
  const [symbol, setSymbol] = useState("AAPL");
  const [data, setData] = useState<StockResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function searchStock() {
    const stockSymbol = symbol.trim().toUpperCase();

    if (!stockSymbol) return;

    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await fetch(
        `http://localhost:8000/stocks/${encodeURIComponent(stockSymbol)}`
      );

      if (!response.ok) {
        throw new Error("Could not fetch stock news");
      }

      const result: StockResponse = await response.json();
      setData(result);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <h1>Stock News AI</h1>
      <p>Get a quick summary of the latest stock news.</p>

      <div className="search">
        <input
          value={symbol}
          onChange={(event) => setSymbol(event.target.value)}
          placeholder="Enter stock symbol"
        />
        <button onClick={searchStock} disabled={loading}>
          {loading ? "Loading..." : "Search"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {data && (
        <section className="results">
          <h2>{data.symbol} News Summary</h2>

          <p className="summary">{data.summary}</p>

          <small>
            Mode: {data.mode === "mock" ? "Mock AI" : "AI"}
          </small>

          <h3>News Sources</h3>

          {data.articles.length === 0 ? (
            <p>No recent articles found.</p>
          ) : (
            <ul>
              {data.articles.map((article, index) => (
                <li key={`${article.url}-${index}`}>
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {article.headline}
                  </a>
                  <p>{article.source}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </main>
  );
}

export default App;
