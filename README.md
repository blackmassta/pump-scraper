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
  "has_king_of_the_hill": false,
  "include_pricing": true,
  "is_graduated": false,
  "is_mkt_cap_usd": false,
  "is_nsfw": true,
  "limit": 1000,
  "offset": 0,
  "order_by": "created_timestamp",
  "order_by_direction": "DESC"
}
```

### Sample Output
```json
{
  "mint": "DGufurYCFCufY7FZcHP7nezirNkBPQ1hTYCvkomTpump",
  "name": "Lacy Live On Twitch",
  "symbol": "LLOT",
  "description": "Lacy Live On Twitch",
  "creator": "CTs3M6RBTV9rWvbT7THQS9bZ48kZM25BFhHD9vTeX4eb",
  "market_cap": 20.29,
  "usd_market_cap": 4164.3196,
  "created_timestamp": "2025-02-09 05:47:24.583000+00:00",
  "image_uri": "https://ipfs.io/ipfs/QmSG4RJ6RJKmcw2ZELdwZXtYcxGfmnGsm73kcP3yXcvNJr",
  "metadata_uri": "https://ipfs.io/ipfs/QmTH3UMMSVamtwW7ExgUvHXefCHRhxGWcKofaQNc3f6BjR",
  "twitter": null,
  "telegram": null,
  "bonding_curve": "5ggQAZNh6Y2xxoBfY5umP5HWc2kSz2SXx74GzoFHdeUu",
  "associated_bonding_curve": "7zxxogqTRcs5qKFpaRpT4vNnmE6s1YW9hQfp7T6ubk2s",
  "raydium_pool": "5F8NinrzdMz5GxC4gmMBNyp7TX6ptLVhSLkE8yxnrAmo",
  "complete": true,
  "virtual_sol_reserves": 110539815753,
  "virtual_token_reserves": 291207288400374,
  "hidden": null,
  "total_supply": 1000000000000000,
  "website": "https://twitch.am/",
  "show_name": true,
  "last_trade_timestamp": "2025-02-09 05:52:02+00:00",
  "king_of_the_hill_timestamp": "2025-02-09 05:48:50+00:00",
  "reply_count": 18,
  "last_reply": "2025-02-09 05:53:57+00:00",
  "nsfw": false,
  "market_id": "7nhUH44iyTbz2FWthEQLeyqtA9CgZKBAtbR8QR6jVYs2",
  "inverted": true,
  "is_currently_live": false,
  "username": null,
  "profile_image": null,
  "pool": {
    "pool_name": "LLOT / SOL",
    "price": 0.0000041654936770611,
    "price_change_24h": -94.49
  },
  "scraped_date": "2025-02-09 06:28:23.553993+00:00"
}
```