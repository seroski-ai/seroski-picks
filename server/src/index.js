import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

// Mock product data (temporary MVP storage)
const products = [
  {
    title: "Boat 450 Pro headphones",
    price: 1999,
    rating: 4.6,
    sentiment_score: 0.91,
    image_quality: 0.95,
  },
  {
    title: "Noise 550 Wireless",
    price: 1799,
    rating: 4.3,
    sentiment_score: 0.87,
    image_quality: 0.93,
  },
  {
    title: "XYZ Bass Boost",
    price: 1499,
    rating: 4.2,
    sentiment_score: 0.80,
    image_quality: 0.6,
  }
];

// Ranking Logic
products.forEach(p => {
  p.final_score = (p.rating * 0.4) + (p.sentiment_score * 0.4) + (p.image_quality * 0.2);
  p.verdict = p.image_quality > 0.7 ? "✅ No major issues" : "⚠ Possible build/image issues";
});

// API: Return top 3 ranked products
app.get("/best-products", (req, res) => {
  const ranked = [...products].sort((a, b) => b.final_score - a.final_score).slice(0, 3);
  res.json(ranked);
});

app.listen(3000, () => console.log("Backend running on http://localhost:3000"));
