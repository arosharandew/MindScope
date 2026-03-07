# 🧠 MindScope: Dementia Risk Prediction Using Non-Medical Features

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MindScope is a **machine learning system designed to predict dementia risk using non-medical features**, including demographics, lifestyle habits, and social engagement factors.

The goal is to create a **non-invasive and interpretable screening tool** that can assist in early risk identification in community settings or serve as a preliminary assessment before formal clinical evaluation.

The project uses data from the **National Alzheimer’s Coordinating Center (NACC)** and applies advanced **feature engineering, hyperparameter optimization, and model calibration** to achieve extremely high predictive performance (**ROC-AUC > 0.998**).

The final trained model is packaged for **easy deployment** and includes a simple prediction interface.

---

# 🔍 Project Overview

Dementia is typically diagnosed using clinical evaluations and medical imaging. However, many early indicators can be detected through **behavioral, lifestyle, and demographic data**.

MindScope explores whether **non-medical variables alone** can be used to accurately predict dementia risk.

The system includes:

- Data preprocessing and feature engineering
- Baseline model benchmarking
- Hyperparameter tuning
- Model calibration
- Feature importance analysis
- Deployment-ready prediction interface

---

# ✨ Features

### Data Processing
- Cleans and preprocesses raw **NACC dataset**
- Handles missing values
- Generates interaction and polynomial features

### Feature Engineering
Creates advanced predictors including:

- Healthy lifestyle score
- Social engagement index
- Age and education groups
- Target encoding for high-cardinality categorical variables

### Fast Baseline Modeling

Trains and evaluates multiple machine learning models:

- Logistic Regression
- Random Forest
- XGBoost
- LightGBM
- Linear SVM
- K-Nearest Neighbors

### Hyperparameter Optimization

Uses multiple tuning strategies:

- **Optuna**
- **GridSearchCV**
- **RandomizedSearchCV**

### Model Interpretation

Provides explainability tools such as:

- Feature importance plots
- SHAP-ready outputs
- Performance visualizations

### Deployment Ready

Includes a packaged model and a **DementiaRiskPredictor class** for easy integration into applications.

### Comprehensive Documentation

All outputs including **model reports, evaluation metrics, and visualizations** are stored in the `results/` directory.

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/arosharandew/MindScope-Dementia-Risk-Prediction-System.git
cd MindScope-Dementia-Risk-Prediction-System
```

### Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate environment:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

If you do not have a requirements file, install core packages manually:

```bash
pip install pandas numpy scikit-learn xgboost lightgbm optuna matplotlib seaborn jupyter joblib
```

---

# 🚀 Usage

## 1️⃣ Data Preparation

Place your **raw NACC dataset (CSV format)** in:

```
data/raw/
```

The expected format follows the **NACC Uniform Data Set (UDS)** structure.

---

## 2️⃣ Run the Machine Learning Pipeline

Execute the notebooks sequentially:

```
notebooks/01_data_loading.ipynb
notebooks/02_feature_engineering.ipynb
notebooks/03_baseline_modeling.ipynb
notebooks/04_hyperparameter_tuning.ipynb
notebooks/05_final_model_evaluation.ipynb
```

Outputs including models, reports, and visualizations are automatically saved in:

```
results/
```

---

## 3️⃣ Make Predictions

Use the `DementiaRiskPredictor` class to generate predictions.

```python
import joblib
from src.predictor import DementiaRiskPredictor

# Load trained model
predictor = DementiaRiskPredictor("results/models/final_deployment_model.pkl")

sample = {
    'NACCAGE': 75,
    'EDUC': 16,
    'INDEPEND': 2,
    'SHOPPING': 3,
    'BILLS': 3
}

result = predictor.predict_risk(sample)
print(result)
```

Example output:

```
{
 'probabilities': array([0.12]),
 'predictions': array([0]),
 'risk_levels': ['Low Risk']
}
```

---

# 📊 Results

The final model (**LightGBM with Platt scaling**) achieved exceptional performance.

| Metric | Score | 95% Confidence Interval |
|------|------|------|
| Accuracy | 0.9870 | 0.9859 – 0.9883 |
| Precision | 0.9811 | 0.9786 – 0.9837 |
| Recall | 0.9748 | 0.9719 – 0.9780 |
| F1 Score | 0.9780 | 0.9760 – 0.9801 |
| ROC-AUC | 0.9989 | 0.9988 – 0.9990 |

These results show that **non-medical features alone can effectively predict dementia risk**.

---

# 📈 Feature Importance (Top Predictors)

| Feature | Importance |
|------|------|
| NACCID_encoded | 856 |
| NACCFDYS | 748 |
| NACCDAYS | 595 |
| NACCVNUM | 245 |
| NACCAVST | 173 |
| NACCADC | 128 |
| SHOPPING | 128 |
| BILLS | 119 |
| VISITYR | 112 |
| BIRTHYR | 108 |

Detailed feature importance plots are stored in:

```
results/visuals/feature_importance/
```

---

# 📁 Project Structure

```
MindScope-Dementia-Risk-Prediction-System/

├── data/
│   ├── raw/               # Original NACC dataset
│   ├── processed/         # Cleaned datasets
│   └── external/          # External reference data
│
├── notebooks/             # Machine learning pipeline notebooks
│
├── src/                   # Python modules
│   ├── data_loader.py
│   ├── feature_engineering.py
│   └── predictor.py
│
├── results/
│   ├── models/            # Saved models
│   ├── reports/           # Model cards and evaluation reports
│   └── visuals/           # Generated charts and plots
│
├── config/
│   └── paths.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🤝 Contributing

Contributions are welcome.

Steps to contribute:

1. Fork the repository
2. Create a branch

```
git checkout -b feature/YourFeature
```

3. Commit changes

```
git commit -m "Add new feature"
```

4. Push to your branch

```
git push origin feature/YourFeature
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# 📬 Contact

**Author:** Arosha Randew  

GitHub: https://github.com/arosharandew  

Project Repository:

https://github.com/arosharandew/MindScope-Dementia-Risk-Prediction-System

---

⚠️ **Disclaimer**

This tool is intended for **research and educational purposes only**.  
It is **not a medical device** and should **not replace professional clinical diagnosis**.

