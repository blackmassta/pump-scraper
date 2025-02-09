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
  "mint": "hXiY1MPjbuuWCeg5AYUgAawqsmJkm7i9rw4W8vKpump",
  "name": "Bearly AI",
  "symbol": "Bearly",
  "description": "Research app for reading and writing with access to leading AI models in an easy-to-use UI",
  "creator": "34sNEPBxrThLYbU3GozAqeLMwYPfnrnu2736rbfnNs5p",
  "market_cap": 22.209999999999997,
  "usd_market_cap": 4539.057699999999,
  "created_timestamp": "2025-02-09 07:41:48.258000+00:00",
  "image_uri": "https://ipfs.io/ipfs/QmUUXScn33dJeLGCpiGHp5u3Cqr88wHBewsD9hzB6EtaAr",
  "metadata_uri": "https://ipfs.io/ipfs/QmQa4u6TCnaSKzeaftWPmPVofvfDv4QmFPSSXZzGwDQf9k",
  "twitter": "https://x.com/bearlyai/status/1888416487452627438",
  "telegram": null,
  "bonding_curve": "5hu5MRiYLYMnYXQXUm5vsTd32s4A9mHyuPWznKryD8vD",
  "associated_bonding_curve": "2S3QBZwusTP2Li7r2vuHxBfEuPhJRsAgPvkahtP48RAm",
  "raydium_pool": "7Vux5xC9XZJ89gxRD2bUESjjtY4iRzihnEruVVG1Liag",
  "complete": true,
  "virtual_sol_reserves": 115005359342,
  "virtual_token_reserves": 279900000000000,
  "hidden": null,
  "total_supply": 1000000000000000,
  "website": null,
  "show_name": true,
  "last_trade_timestamp": "2025-02-09 07:50:05+00:00",
  "king_of_the_hill_timestamp": "2025-02-09 07:42:51+00:00",
  "reply_count": 11,
  "last_reply": "2025-02-09 07:57:16+00:00",
  "nsfw": false,
  "market_id": "8x8rXFE6AgbvsmMG81gUKADGj6CXJ4YeveXegeABD9Em",
  "inverted": true,
  "is_currently_live": false,
  "username": null,
  "profile_image": null,
  "pool": {
    "pool_name": "Bearly / SOL",
    "price": 4.29485225223411e-06,
    "price_change_5m": -97.66,
    "price_change_15m": -96.5,
    "price_change_30m": -96.5,
    "price_change_1h": -96.5,
    "price_change_6h": -96.5,
    "price_change_24h": -96.5
  },
  "scraped_date": "2025-02-09 08:03:56.839560+00:00"
}
```