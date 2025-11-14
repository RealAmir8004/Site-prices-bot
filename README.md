# Site-prices-bot — Online Shop Price Update Helper

A desktop application that helps e-commerce site admins intelligently update product prices & quantities across [Torob](https://torob.com) using pricing analysis.

## Overview

The application imports product data (Excel/CSV), filters and groups items into a `DataList`, then scrapes Torob for competitor prices. It computes suggested prices to improve buy-box priority while preserving profit margins and applying charm-pricing (for example, 87.99). Admins review suggestions in the PyQt5 UI, can accept or override prices, adjust quantities based on inventory and recent wholesale costs, and export the final changes to an XLSX file.

## Features

- **Competitive Price Scraping**: Automatically scrapes [Torob](https://torob.com) to gather competitor prices
- **Smart Price Calculation**: Computes optimal prices for each product that:
  - Maximize buy-box positioning based on Torob's priority algorithm
  - Preserve profit margins using configurable charm-price formatting (e.g., 87.99)
  - Account for badged/trusted sellers vs. standard sellers
- **Data Integration**: Processes product data from multiple sources (Excel, CSV, Asan7 accounting systems)
- **Interactive UI**: Review suggested prices, override with custom prices, adjust quantities based on real inventory
- **Batch Operations**: Update multiple products at once with progress tracking
- **Persistent Storage**: SQLite database for snapshot persistence between runs

## Tech Stack

- **Frontend**: PyQt5 (Desktop GUI)
- **Backend**: Python3 , pandas (data processing)
- **Web Scraping**: BeautifulSoup, undetected-chromedriver, requests
- **Database**: SQLite
- **Dependencies**: sortedcontainers, googlesearch


## Planned features (Roadmap)

- Add a PrestaShop/WordPress integration module to push price/quantity updates directly to PrestaShop stores.
- Improve marketplace support beyond Torob and add more robust URL-resolution fallbacks.
- Incrementally refine the price-optimization algorithm and UI for faster manual review.

## Demo

A pre-built demo executable is available to let reviewers explore the application without installing dependencies.  
*(Demo mode does not send real scrape requests because it has no real XLSX input file.)*

1. Visit the demo release:  
   https://github.com/RealAmir8004/Site-prices-bot/releases/tag/structure-demo
2. Download `v0.1.App.Structure.Overview.zip` and extract it anywhere.
3. Run `main.exe` — no installation required.

**Note:**  
If the console window freezes for a few seconds at startup, simply press **Enter** to continue.


## How It Works

1. **Data Import**: Loads product data from `input xlsx/`
2. **Filtering**: Automatically filters products by:
   - Active status
   - Available quantity > 0
   - Accounting system inventory
3. **Web Scraping**: For each product, scrapes [Torob](https://torob.com) to find:
   - Top competitor prices
   - Badged/trusted seller badges
   - Historical price changes
4. **Price Optimization**: Applies priority algorithm similar to Torob's buy-box logic:
   - Balances price aggressiveness with trust badges
   - Formats prices in charm ranges (e.g., 87.99 instead of 88.00)
   - Accounts for 5% trust badge premium
5. **Manual Review**: Admin reviews suggestions in UI and can:
   - Accept suggested price
   - Set custom price
   - Adjust inventory quantity
6. **Export**: Saves all changes back to `output xlsx/` with formatted pricing

## Input/Output

**Input Folders**:
- `input xlsx/` — Product database export (required)
- `input torob/` — CSV mapping product names to Torob URLs (optional, falls back to Google search)
- `input asan7/` — Asan7 accounting system inventory data (optional)

**Output**:
- `output xlsx/` — Updated product prices & quantities
- `storage/` — SQLite database snapshots and logs

## Key Implementation Details

- **Background Worker**: Batch updates run on separate thread with progress dialog
- **Custom Logging**: Four log levels (DEBUG, INFO, IMPORTANT, BACKGROUND) with separate file outputs
- **Dynamic Sorting**: Products are sorted by Torob buy-box algorithm (see `Site.__lt__` in [scraping.py](scraping.py))
- **Charm Pricing**: Intelligent price formatting to maintain competitiveness (e.g., reduce by 1000 rials from 10,000 multiple)


## Author
**Amiryazdan Ghiasy** — Creator & Maintainer of this project

GitHub: [@RealAmir8004](https://github.com/RealAmir8004)


## License

This project is proprietary and all rights are reserved.

The source code in this repository is provided for **review and portfolio purposes only**.  
No part of this project may be copied, modified, reused, or distributed in any form without explicit written permission from the author.

© 2025 Amiryazdan Ghiasy — All Rights Reserved
