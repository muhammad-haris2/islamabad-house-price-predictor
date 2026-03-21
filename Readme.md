# 🏠 Islamabad House Price Predictor

A production-style machine learning web application that predicts residential property prices across Islamabad's housing societies using real 2025 market data scraped from Zameen.com.

Built with **scikit-learn**, **FastAPI**, and **Streamlit** — following a clean 3-layer architecture that separates ML, API, and UI concerns.

---

## 📸 Screenshots

<img width="1919" height="824" alt="image" src="https://github.com/user-attachments/assets/15a2bda2-cb48-4f0a-a9ba-94f86eddc159" />
<img width="1918" height="820" alt="image" src="https://github.com/user-attachments/assets/724077b3-78a6-4b68-9030-50e16736c9a6" />
<img width="1919" height="832" alt="image" src="https://github.com/user-attachments/assets/37ec8bd8-163b-41f7-a0e2-2a68972fa84e" />
<img width="1919" height="814" alt="image" src="https://github.com/user-attachments/assets/424fa3d2-f67a-4749-a6c4-5a218ef9cc8b" />
<img width="1919" height="829" alt="image" src="https://github.com/user-attachments/assets/b451de28-77f1-45e6-9186-e94fdc99e57b" />
<img width="1919" height="827" alt="image" src="https://github.com/user-attachments/assets/f02db82e-eef8-4d93-a740-e5dee73a624d" />




---

## 🚀 Features

- 🏘️ Predicts prices for **219 Islamabad locations** (DHA, Bahria Town, MPCHS, G-13, F-7, F-8, B-17 and more)
- 🤖 **87.4% R² accuracy** using Gradient Boosting Regressor
- 📡 **Fresh 2025 data** scraped directly from Zameen.com using Selenium
- ⚡ **FastAPI backend** with auto-generated Swagger docs at `/docs`
- 🖥️ **Streamlit frontend** with a clean dark UI
- 📊 Full price breakdown — total price + per Marla rate
- 🔄 Easy data refresh — update training data without changing any other file

---

## 🗂️ Project Structure

```
islamabad-house-price-predictor/
│
├── ml/                         # ML layer
│   ├── preprocess.py           # Data cleaning pipeline
│   ├── train.py                # Model training and artifact export
│   └── artifacts/              # Saved model files (generated locally)
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
│   ├── raw/                    # Raw scraped data (not pushed to GitHub)
│   └── processed/              # Cleaned dataset (generated locally)
│
├── zameen_scraper.py           # Selenium scraper for fresh Zameen.com data
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/muhammad-haris2/islamabad-house-price-predictor.git
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

---

## 📦 Getting the Data

You have two options:

**Option A — Scrape fresh data from Zameen.com (recommended)**
```bash
pip install selenium webdriver-manager
python zameen_scraper.py
```
This collects ~1,000 fresh Islamabad house listings directly from Zameen.com and saves them to `data/raw/islamabad_fresh.csv`.

**Option B — Use an existing dataset**

Download any Pakistan housing dataset from Kaggle, place it in `data/raw/`, and update the `RAW_PATH` in `ml/preprocess.py`.

---

## ▶️ Running the Pipeline

### Step 1 — Preprocess the data
```bash
python ml/preprocess.py
```

### Step 2 — Train the model
```bash
python ml/train.py
```

---

## 🖥️ Running the App

You need **two terminals** running simultaneously.

**Terminal 1 — FastAPI backend:**
```bash
python -m api.main
```
- API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

**Terminal 2 — Streamlit frontend:**
```bash
streamlit run app/streamlit_app.py
```
- App: `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | `/`        | API info                           |
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
  "predicted_price_pkr": 95000000.0,
  "predicted_price_label": "PKR 9.50 Crore",
  "price_per_marla_pkr": 9500000.0,
  "price_per_marla_label": "PKR 95.00 Lakh",
  "input_summary": {
    "property_type": "House",
    "location": "DHA Defence",
    "area_marla": 10.0,
    "bedrooms": 4,
    "bathrooms": 3
  },
  "model_r2": 0.8738
}
```

---

## 🧠 ML Details

| Detail            | Value                         |
|-------------------|-------------------------------|
| Model             | GradientBoostingRegressor     |
| Training rows     | 949                           |
| Test R² Score     | 0.8738 (87.4%)                |
| Cross-val R²      | 0.8333 ± 0.077                |
| Top feature       | area_marla (63% importance)   |
| Locations         | 219 unique Islamabad areas    |
| Price range       | PKR 62 Lakh — PKR 5.5 Crore  |
| Median price      | PKR 48.5 Lakh                 |
| Data source       | Zameen.com (scraped 2025)     |
| Encoding          | LabelEncoder for categoricals |

---

## 🔄 Refreshing the Data

One of the key design goals of this project is that **data is completely decoupled from code**.

To update with fresh Zameen.com data:
```bash
# 1. Scrape fresh listings
python zameen_scraper.py

# 2. Clean the data
python ml/preprocess.py

# 3. Retrain the model
python ml/train.py

# 4. Restart the API
python -m api.main
```

Zero changes needed to the API or Streamlit code.

---

## 🛠️ Tech Stack

| Layer    | Technology                       |
|----------|----------------------------------|
| Scraping | Selenium, webdriver-manager      |
| ML       | scikit-learn, pandas, numpy      |
| API      | FastAPI, Uvicorn, Pydantic       |
| Frontend | Streamlit                        |
| Packaging| joblib                           |

---

## 👨‍💻 Author

**Muhammad Haris**
- GitHub: [@muhammad-haris2](https://github.com/muhammad-haris2)
- LinkedIn: [@Muhammad-Haris](https://www.linkedin.com/in/muhammad-haris-455166294/)
- Location: Islamabad, Pakistan 🇵🇰

---

## 📄 License

MIT License — feel free to use, modify, and share.
