# Reviews Sentiment Analysis Service

Flask service for collecting reviews with automatic sentiment analysis.

## Quick Start

```bash
pip install flask
python app.py
```

## API Endpoints

### POST /reviews
Creates a new review with sentiment analysis.

**Request:**
```json
{
    "text": "Your review text"
}
```

**Response:**
```json
{
    "id": 1,
    "text": "Your review text",
    "sentiment": "positive",
    "created_at": "2025-07-17T10:30:00"
}
```

### GET /reviews
Returns all reviews or filters by sentiment.

**Parameters:**
- `sentiment` (optional): `positive`, `negative`, `neutral`

## Usage Examples

```bash
# Create review
curl -X POST http://localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text": "Great service, love it!"}'

# Get all reviews
curl http://localhost:5000/reviews

# Filter by sentiment
curl http://localhost:5000/reviews?sentiment=negative
```