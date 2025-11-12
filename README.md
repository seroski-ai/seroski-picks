# SmartBuy MVP – AI Product Selection

## Problem
Users waste time comparing products manually. We rank products using AI, ratings, reviews and deliver the best choice instantly.

## Solution
- AI based review sentiment
- Aggregate ratings & feedback
- Future: image damage detection, extension support

## Architecture
Frontend → Node API → Ranker → Top results

## Tech Stack (MVP)
Frontend: React (Vite)
Backend: Node + Express

## Run Project
### Start Backend
cd server
npm install
npm start

### Start Frontend
cd client
npm install
npm run dev

## API Endpoint
GET /best-products?query=<product>

## Future Scope
- AI image damage detection
- Browser extension for Amazon/Flipkart overlay
- ETL pipeline for bulk product ingestion
- Vector search for ranking
- Recommendation personalization

