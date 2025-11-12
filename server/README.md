# SmartBuy Server (Backend)

## Tech
- Node.js
- Express.js

## Run
npm install
npm start

## API
GET /best-products?query=mobile

## Logic (MVP)
1. Accept product query
2. Fetch mock product list
3. Rank using formula:
   finalScore = (rating * 0.5) + (reviewScore * 0.5)
4. Return top 3

## Future
- DB integration
- ETL pipeline for product ingestion
- NLP based sentiment scoring
- Vision based damage detection
