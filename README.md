# Pump.fun Token Scraper

![Pump Fun Logo](https://pump.fun/_next/image?url=%2Flogo.png&w=32&q=75)

This tool extracts in-depth data about cryptocurrency tokens from Pump.fun, a platform dedicated to Solana-based assets.
It provides valuable insights into tokens, including their market caps, trading patterns, social media links, and more.

## Key Features
- Scrapes information for 1,000 tokens in a single operation.
- Includes price information from Pool
- Extensive filtering to save you money on responses:
  - **Sort By**: Last Trade, Creation Time, Last Reply, or Market Cap
  - **Sort Order**: Ascending or Descending
  - **NSFW Content**: Option to include or exclude
  - **Market Cap**: Option to load only coins above certain market cap
  - **Is Graduated**: Option to load only coins that are complete and are in raydium.
  - And more...
- All token details returned automatically from pump.fun are returned
  - **Basic Data**: Token name, symbol, and mint address
  - **Market Data**: Market cap, reserves, and trading figures
  - **Social Media**: Links to Twitter, Telegram, and website
  - **Full Metadata**: Descriptions, images, and additional details
  - **Price Info**: For tokens that are graduated, you can get the price information!!!

## Key Use Cases
- **Market Intelligence**: Analyze token performance, investor sentiment, and broader market trends.  
- **Emerging Token Discovery**: Spot new tokens early by tracking creation timestamps and initial trading activity.  
- **Data-Driven Trading**: Leverage historical market data to refine and backtest trading strategies.  
- **Valuation Monitoring**: Track market capitalization shifts to uncover promising projects and investment opportunities.  
- **Social Sentiment Analysis**: Assess community engagement by analyzing reply counts, discussions, and platform interactions.  
- **Project Verification**: Conduct due diligence with in-depth token metadata and real-time project updates.  
- **Competitive Benchmarking**: Compare token performance and market positioning against competitors.  
- **Community Engagement Insights**: Measure and interpret social activity across multiple channels to gauge adoption and interest.  


## Input Configuration
- **sort (String)**: Choose how to sort the results by: `last_trade_timestamp`, `created_timestamp`, `last_reply`, or `market_cap` (default: `created_timestamp`).
- **order (String)**: Set the sorting order: `ASC` or `DESC` (default: `DESC`).
- **includeNsfw (Boolean)**: Decide if NSFW tokens should be included (default: `false`).

### Example Input
```json
{
  "order_by": "created_timestamp",
  "order_by_direction": "ASC",
  "is_nsfw": true
}
