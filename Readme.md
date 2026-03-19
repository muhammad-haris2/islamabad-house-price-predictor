# 🏠 Islamabad House Price Predictor

A production-style machine learning web application that predicts residential property prices across Islamabad's housing societies using real market data.

Built with **scikit-learn**, **FastAPI**, and **Streamlit** — following a clean 3-layer architecture that separates ML, API, and UI concerns.

---

## 📸 Screenshots

> Add screenshots of your app here after deployment

---

## 🚀 Features

- 🏘️ Predicts prices for **172 Islamabad locations** (DHA, Bahria Town, G-sectors, F-sectors and more)
- 🤖 **82.2% R² accuracy** using Gradient Boosting Regressor
- ⚡ **FastAPI backend** with auto-generated Swagger docs at `/docs`
- 🖥️ **Streamlit frontend** with clean dark UI
- 📊 Full price breakdown — total price + per Marla rate
- 🔄 Easy data swap — update training data without changing any other file

---

## 🗂️ Project Structure

```
islamabad-house-price-predictor/
│
├── ml/                         # ML layer
│   ├── preprocess.py           # Data cleaning pipeline
│   ├── train.py                # Model training + artifact export
│   └── artifacts/              # Saved model files
│       ├── model.pkl
│       ├── label_encoders.pkl
│       ├── feature_names.pkl
│       └── training_stats.json
│
├── api/                        # FastAPI layer
│   ├── main.py                 # App entry point
│   ├── routes.py               # /predict, /health, /info endpoints
│   ├── schemas.py              # Pydantic request/response models
│   └── config.py               # Paths and settings
│
├── app/                        # Streamlit layer
│   ├── streamlit_app.py        # Main UI entry point
│   └── components/
│       ├── sidebar.py          # Location list sidebar
│       ├── input_form.py       # Property input form
│       └── prediction_card.py  # Result display
│
├── data/
│   ├── raw/                    # Original dataset (not pushed to GitHub)
│   └── processed/
│       └── clean_data.csv      # Cleaned dataset
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://https://github.com/muhammad-haris2/islamabad-house-price-predictor.git
cd islamabad-house-price-predictor
```

### 2. Create a virtual environment
```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# Mac/Linux
source myenv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add the dataset
Download the Pakistan housing dataset from Kaggle and place it at:
```
data/raw/islamabad_housing.csv
```

### 5. Run the preprocessing pipeline
```bash
python ml/preprocess.py
```

### 6. Train the model
```bash
python ml/train.py
```

---

## ▶️ Running the App

You need **two terminals** running simultaneously.

**Terminal 1 — Start the FastAPI backend:**
```bash
python -m api.main
```
API will be available at: `http://localhost:8000`
Swagger docs at: `http://localhost:8000/docs`

**Terminal 2 — Start the Streamlit frontend:**
```bash
streamlit run app/streamlit_app.py
```
App will open at: `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | `/`        | Root — API info                    |
| GET    | `/health`  | Health check + model loaded status |
| GET    | `/info`    | Model stats + valid input options  |
| POST   | `/predict` | Predict house price                |

### Example prediction request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "property_type": "House",
    "location": "DHA Defence",
    "area_marla": 10,
    "bedrooms": 4,
    "bathrooms": 3
  }'
```

### Example response

```json
{
  "predicted_price_pkr": 51043722.24,
  "predicted_price_label": "PKR 5.10 Crore",
  "price_per_marla_pkr": 5104372.22,
  "price_per_marla_label": "PKR 51.04 Lakh",
  "input_summary": {
    "property_type": "House",
    "location": "DHA Defence",
    "area_marla": 10.0,
    "bedrooms": 4,
    "bathrooms": 3
  },
  "model_r2": 0.8217
}
```

---

## 🧠 ML Details

| Detail            | Value                         |
|-------------------|-------------------------------|
| Model             | GradientBoostingRegressor     |
| Training rows     | 2,527                         |
| Test R² Score     | 0.8217 (82.2%)                |
| Cross-val R²      | 0.8262 ± 0.05                 |
| Top feature       | area_marla (68.7% importance) |
| Encoding          | LabelEncoder for categoricals |

---

## 🔄 Updating the Data

One of the key design goals of this project is that **data is completely decoupled from code**.

To update with fresh Zameen.com data:
1. Replace `data/raw/islamabad_housing.csv` with new data (same column format)
2. Re-run `python ml/preprocess.py`
3. Re-run `python ml/train.py`
4. Restart the API — done. No other files need to change.

---

## 🛠️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| ML        | scikit-learn, pandas, numpy       |
| API       | FastAPI, Uvicorn, Pydantic        |
| Frontend  | Streamlit                         |
| Packaging | joblib                            |

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-linkedin)
- Location: Islamabad, Pakistan 🇵🇰

---

## 📄 License

MIT License — feel free to use, modify, and share.