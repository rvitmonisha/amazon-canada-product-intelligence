import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [url, setUrl] = useState("");
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [insights, setInsights] = useState(null);
  const [insightsLoading, setInsightsLoading] = useState(false);

  const [compareMode, setCompareMode] = useState(false);
  const [compareUrl, setCompareUrl] = useState("");
  const [compareProduct, setCompareProduct] = useState(null);
  const [compareLoading, setCompareLoading] = useState(false);
  const [comparison, setComparison] = useState(null);

  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    const savedHistory = localStorage.getItem(
      "amazon-product-history"
    );

    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (error) {
        console.error("Unable to load history:", error);
        setHistory([]);
      }
    }
  }, []);

  const saveToHistory = (scrapedProduct) => {
    const historyItem = {
      id: Date.now(),
      title: scrapedProduct.title,
      price: scrapedProduct.price,
      currency: scrapedProduct.currency || "CAD",
      rating: scrapedProduct.rating,
      reviews: scrapedProduct.reviews,
      url: scrapedProduct.url,
      analyzedAt: new Date().toLocaleString(),
    };

    setHistory((previousHistory) => {
      const updatedHistory = [
        historyItem,
        ...previousHistory,
      ].slice(0, 20);

      localStorage.setItem(
        "amazon-product-history",
        JSON.stringify(updatedHistory)
      );

      return updatedHistory;
    });
  };

  const clearHistory = () => {
    localStorage.removeItem("amazon-product-history");
    setHistory([]);
  };

  const analyzeProduct = async () => {
    if (!url.trim()) {
      setError("Please enter an Amazon.ca product URL.");
      return;
    }

    setLoading(true);
    setError("");
    setProduct(null);
    setInsights(null);

    try {
      const response = await fetch(
        `${API_URL}/products/scrape`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: url.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to fetch product information."
        );
      }

      const scrapedProduct = data.product || data;

      setProduct(scrapedProduct);

      saveToHistory(scrapedProduct);
    } catch (err) {
      console.error("Product fetch error:", err);
      setError(
        err.message || "Failed to fetch product."
      );
      setProduct(null);
    } finally {
      setLoading(false);
    }
  };

  const generateInsights = async () => {
    if (!product) {
      setError(
        "Please analyze a product before generating AI insights."
      );
      return;
    }

    setInsightsLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/products/insights`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(product),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to generate product insights."
        );
      }

      setInsights(data);
    } catch (err) {
      console.error("AI insight error:", err);
      setError(
        err.message ||
          "Failed to generate AI insights."
      );
    } finally {
      setInsightsLoading(false);
    }
  };

  const analyzeCompareProduct = async () => {
    if (!compareUrl.trim()) {
      setError(
        "Please enter another Amazon.ca product URL."
      );
      return;
    }

    setCompareLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/products/scrape`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: compareUrl.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to fetch comparison product."
        );
      }

      const scrapedProduct = data.product || data;

      setCompareProduct(scrapedProduct);
    } catch (err) {
      console.error(
        "Comparison product error:",
        err
      );

      setError(
        err.message ||
          "Failed to fetch comparison product."
      );
    } finally {
      setCompareLoading(false);
    }
  };

  const compareProducts = async () => {
    if (!product || !compareProduct) {
      setError(
        "Analyze two products before comparing."
      );
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/products/compare`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify([
            product,
            compareProduct,
          ]),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to compare products."
        );
      }

      setComparison(data);
    } catch (err) {
      console.error("Comparison error:", err);

      setError(
        err.message ||
          "Failed to compare products."
      );
    }
  };

  return (
    <div className="app">

      <nav className="navbar">
        <div className="brand">
          <div className="brand-icon">A</div>

          <div>
            <h2>Amazon Intelligence</h2>
            <span>Canada Product Analytics</span>
          </div>
        </div>

        <div className="nav-status">
          <span className="status-dot"></span>
          API Connected
        </div>
      </nav>

      <main className="dashboard">

        <section className="hero-section">

          <div className="eyebrow">
            PRODUCT INTELLIGENCE PLATFORM
          </div>

          <h1>
            Analyze Amazon Canada Products
          </h1>

          <p>
            Enter an Amazon.ca product URL to
            analyze pricing, ratings, reviews,
            and product performance.
          </p>

          <div className="search-box">

            <input
              type="url"
              placeholder="Paste Amazon.ca product URL..."
              value={url}
              onChange={(e) =>
                setUrl(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  analyzeProduct();
                }
              }}
            />

            <button
              onClick={analyzeProduct}
              disabled={loading}
            >
              {loading
                ? "Fetching..."
                : "Analyze Product"}
            </button>

          </div>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

        </section>

        <section className="stats-grid">

          <div className="stat-card">
            <span>Current Price</span>

            <strong>
              {product &&
              product.price !== null
                ? `$${product.price}`
                : "—"}
            </strong>

            <small>CAD</small>
          </div>

          <div className="stat-card">
            <span>Rating</span>

            <strong>
              {product &&
              product.rating !== null
                ? `${product.rating} / 5`
                : "—"}
            </strong>

            <small>Customer rating</small>
          </div>

          <div className="stat-card">
            <span>Reviews</span>

            <strong>
              {product
                ? product.reviews ?? 0
                : "—"}
            </strong>

            <small>Customer reviews</small>
          </div>

          <div className="stat-card">
            <span>Analysis</span>

            <strong
              className={
                product ? "active" : ""
              }
            >
              {loading
                ? "Fetching"
                : product
                ? "Complete"
                : "Ready"}
            </strong>

            <small>
              Amazon.ca product data
            </small>
          </div>

        </section>

        <section className="content-grid">

          <div className="panel">

            <div className="panel-header">

              <div>
                <div className="panel-label">
                  PRODUCT ANALYSIS
                </div>

                <h2>
                  Product Overview
                </h2>
              </div>

              <span className="badge">
                {product
                  ? "Analyzed"
                  : "Ready"}
              </span>

            </div>

            <div className="product-placeholder">

              <div className="product-image">
                Product
              </div>

              <div className="product-info">

                <h3>
                  {product
                    ? product.title
                    : "Amazon Canada Product"}
                </h3>

                <p>
                  {product
                    ? "Product information successfully fetched from Amazon.ca."
                    : "Product information will appear here after analyzing an Amazon.ca product URL."}
                </p>

                <div className="product-details">

                  <div>
                    <span>PRICE</span>

                    <strong>
                      {product &&
                      product.price !== null
                        ? `$${product.price}`
                        : "—"}
                    </strong>
                  </div>

                  <div>
                    <span>RATING</span>

                    <strong>
                      {product &&
                      product.rating !== null
                        ? `${product.rating} / 5`
                        : "—"}
                    </strong>
                  </div>

                  <div>
                    <span>REVIEWS</span>

                    <strong>
                      {product
                        ? product.reviews ?? 0
                        : "—"}
                    </strong>
                  </div>

                </div>

              </div>

            </div>

          </div>

          <div className="panel">

            <div className="panel-header">

              <div>
                <div className="panel-label">
                  AI ANALYSIS
                </div>

                <h2>
                  Product Insights
                </h2>
              </div>

              <span className="ai-badge">
                AI
              </span>

            </div>

            {!insights && (
              <div className="insight-empty">

                <p>
                  Analyze a product and generate
                  intelligent product insights.
                </p>

                <button
                  className="primary-action"
                  onClick={generateInsights}
                  disabled={
                    !product ||
                    insightsLoading
                  }
                >
                  {insightsLoading
                    ? "Generating..."
                    : "Generate AI Insights"}
                </button>

              </div>
            )}

            {insights && (
              <div className="ai-results">

                <div className="result-item">
                  <span>
                    PRICE ASSESSMENT
                  </span>

                  <strong>
                    {insights.price_assessment}
                  </strong>
                </div>

                <div className="result-item">
                  <span>
                    RATING ASSESSMENT
                  </span>

                  <strong>
                    {insights.rating_assessment}
                  </strong>
                </div>

                <div className="result-item">
                  <span>
                    REVIEW ASSESSMENT
                  </span>

                  <strong>
                    {insights.review_assessment ||
                      "Review data analyzed"}
                  </strong>
                </div>

                <div className="result-item">
                  <span>
                    RECOMMENDATION
                  </span>

                  <strong>
                    {insights.recommendation}
                  </strong>
                </div>

              </div>
            )}

          </div>

        </section>

        <section className="bottom-grid">

          <div className="panel">

            <div className="panel-header">

              <div>
                <div className="panel-label">
                  PRICE TRACKING
                </div>

                <h2>
                  Price History
                </h2>
              </div>

              <span className="badge">
                {history.length} Records
              </span>

            </div>

            {!showHistory ? (
              <div className="chart-placeholder">

                <div className="chart-line"></div>

                <span>
                  {history.length > 0
                    ? `${history.length} product price records available.`
                    : "No price history available yet."}
                </span>

                <button
                  className="primary-action"
                  onClick={() =>
                    setShowHistory(true)
                  }
                >
                  View Price History
                </button>

              </div>
            ) : (
              <div className="history-section">

                {history.length === 0 ? (
                  <p>
                    No price history available.
                    Analyze a product to create
                    your first record.
                  </p>
                ) : (
                  <>
                    <div className="history-header">

                      <strong>
                        Recent Analysis History
                      </strong>

                      <button
                        className="clear-button"
                        onClick={clearHistory}
                      >
                        Clear History
                      </button>

                    </div>

                    <div className="history-list">

                      {history.map((item) => (
                        <div
                          className="history-item"
                          key={item.id}
                        >

                          <div className="history-product">

                            <strong>
                              {item.title}
                            </strong>

                            <small>
                              {item.analyzedAt}
                            </small>

                          </div>

                          <div className="history-price">
                            <strong>
                              $
                              {item.price}
                            </strong>

                            <small>
                              {item.currency}
                            </small>
                          </div>

                          <div className="history-rating">
                            {item.rating
                              ? `${item.rating} / 5`
                              : "N/A"}
                          </div>

                        </div>
                      ))}

                    </div>
                  </>
                )}

                <button
                  className="secondary-action"
                  onClick={() =>
                    setShowHistory(false)
                  }
                >
                  Hide History
                </button>

              </div>
            )}

          </div>

          <div className="panel">

            <div className="panel-header">

              <div>
                <div className="panel-label">
                  QUICK ACTIONS
                </div>

                <h2>
                  Product Tools
                </h2>
              </div>

            </div>

            <div className="actions">

              <button
                onClick={() =>
                  setShowHistory(true)
                }
              >
                View Price History
              </button>

              <button
                onClick={() => {
                  setCompareMode(true);
                  setComparison(null);
                }}
              >
                Compare Products
              </button>

              <button
                onClick={generateInsights}
                disabled={
                  !product ||
                  insightsLoading
                }
              >
                {insightsLoading
                  ? "Generating..."
                  : "Generate AI Insights"}
              </button>

            </div>

          </div>

        </section>

        {compareMode && (
          <section className="panel comparison-panel">

            <div className="panel-header">

              <div>
                <div className="panel-label">
                  PRODUCT COMPARISON
                </div>

                <h2>
                  Compare Products
                </h2>
              </div>

              <button
                className="close-button"
                onClick={() =>
                  setCompareMode(false)
                }
              >
                Close
              </button>

            </div>

            <div className="comparison-input">

              <input
                type="url"
                placeholder="Enter second Amazon.ca product URL..."
                value={compareUrl}
                onChange={(e) =>
                  setCompareUrl(e.target.value)
                }
              />

              <button
                onClick={analyzeCompareProduct}
                disabled={compareLoading}
              >
                {compareLoading
                  ? "Fetching..."
                  : "Fetch Product"}
              </button>

            </div>

            {compareProduct && (
              <div className="comparison-product">

                <h3>
                  {compareProduct.title}
                </h3>

                <p>
                  Price: $
                  {compareProduct.price}
                </p>

                <p>
                  Rating:{" "}
                  {compareProduct.rating}
                  / 5
                </p>

                <p>
                  Reviews:{" "}
                  {compareProduct.reviews}
                </p>

                <button
                  className="primary-action"
                  onClick={compareProducts}
                >
                  Compare Products
                </button>

              </div>
            )}

            {comparison && (
              <div className="comparison-result">

                <h3>
                  Comparison Result
                </h3>

                <div className="comparison-card">

                  <span>
                    LOWEST PRICE
                  </span>

                  <strong>
                    {
                      comparison
                        .lowest_price_product
                        ?.title
                    }
                  </strong>

                  <p>
                    $
                    {
                      comparison
                        .lowest_price_product
                        ?.price
                    }{" "}
                    CAD
                  </p>

                </div>

                <div className="comparison-card">

                  <span>
                    HIGHEST RATED
                  </span>

                  <strong>
                    {
                      comparison
                        .highest_rated_product
                        ?.title
                    }
                  </strong>

                  <p>
                    Rating:{" "}
                    {
                      comparison
                        .highest_rated_product
                        ?.rating
                    }{" "}
                    / 5
                  </p>

                </div>

              </div>
            )}

          </section>
        )}

      </main>

      <footer>

        <span>
          Amazon Canada Product Intelligence
        </span>

        <span>
          Powered by FastAPI + React
        </span>

      </footer>

    </div>
  );
}

export default App;