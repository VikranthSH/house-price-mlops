# 🏠 Bangalore House Price Prediction - MLOps Project

A complete MLOps project for predicting house prices in Bangalore using Machine Learning, FastAPI, Streamlit, and Docker.

## 📋 Project Structure

```
house-price-mlops/
│
├── Dockerfile                          # Docker config for FastAPI
├── Dockerfile.streamlit                # Docker config for Streamlit
├── docker-compose.yml                  # Multi-container orchestration
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
│
├── model.pkl                           # Trained model
├── feature_columns.pkl                 # Feature columns
├── unique_locations.pkl                # Available locations
│
├── data/
│   └── raw/
│       └── Bengaluru_House_Data.csv   # Dataset
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py          # Data preprocessing pipeline
│   ├── model.py                       # Model training & prediction
│   └── train.py                       # Training script
│
├── api/
│   ├── __init__.py
│   └── app.py                         # FastAPI application
│
└── streamlit_app.py                   # Streamlit UI
```

## 🚀 Quick Start with Docker

### Prerequisites
- Docker installed ([Download Docker](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (comes with Docker Desktop)

### Step 1: Train the Model (If not already trained)

```bash
# Install dependencies locally (optional, for training)
pip install -r requirements.txt

# Train the model
python src/train.py data/raw/Bengaluru_House_Data.csv
```

This will generate:
- `model.pkl`
- `feature_columns.pkl`
- `unique_locations.pkl`

### Step 2: Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

### Step 3: Access the Applications

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs
- **FastAPI Health Check**: http://localhost:8000/health

### Stop the Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🔧 Manual Docker Commands (Alternative)

### Build Images

```bash
# Build FastAPI image
docker build -t house-price-api .

# Build Streamlit image
docker build -f Dockerfile.streamlit -t house-price-streamlit .
```

### Run Containers

```bash
# Create network
docker network create app-network

# Run FastAPI
docker run -d --name house-price-api \
  -p 8000:8000 \
  -v $(pwd)/model.pkl:/app/model.pkl \
  -v $(pwd)/feature_columns.pkl:/app/feature_columns.pkl \
  -v $(pwd)/unique_locations.pkl:/app/unique_locations.pkl \
  --network app-network \
  house-price-api

# Run Streamlit
docker run -d --name house-price-streamlit \
  -p 8501:8501 \
  -e API_URL=http://house-price-api:8000 \
  --network app-network \
  house-price-streamlit
```

## 📡 API Endpoints

### GET `/`
Root endpoint with API information

### GET `/health`
Health check endpoint

### GET `/locations`
Get list of available locations

### POST `/predict`
Predict house price

**Request Body:**
```json
{
  "location": "Whitefield",
  "sqft": 1500,
  "bath": 2,
  "bhk": 3
}
```

**Response:**
```json
{
  "predicted_price": 85.5,
  "location": "Whitefield",
  "sqft": 1500,
  "bath": 2,
  "bhk": 3
}
```

## 🧪 Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Get locations
curl http://localhost:8000/locations

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Whitefield",
    "sqft": 1500,
    "bath": 2,
    "bhk": 3
  }'
```

### Using Python

```python
import requests

# Make prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "location": "Whitefield",
        "sqft": 1500,
        "bath": 2,
        "bhk": 3
    }
)

print(response.json())
```

## 🔍 Troubleshooting

### Port Already in Use

If ports 8000 or 8501 are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change host port
```

### Model Files Not Found

Ensure you have trained the model and the following files exist:
- `model.pkl`
- `feature_columns.pkl`
- `unique_locations.pkl`

### Container Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs streamlit

# Follow logs
docker-compose logs -f
```

### Rebuild Containers

```bash
# Force rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

## 🛠️ Development

### Local Development (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI
cd api
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Run Streamlit (in another terminal)
streamlit run streamlit_app.py
```

### Add New Locations

Retrain the model with updated data to include new locations.

## 📊 Model Information

- **Algorithm**: Linear Regression
- **Features**: Square feet, bathrooms, BHK, location (one-hot encoded)
- **Target**: House price in lakhs
- **Framework**: scikit-learn
- **Tracking**: MLflow

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is for educational purposes.

## 👥 Contact

For questions or issues, please open an issue in the repository.

---