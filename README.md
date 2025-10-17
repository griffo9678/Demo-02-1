# UK Real Estate Analyzer

A visual dashboard built with **Streamlit** to explore property investment risk across UK cities.

## 📊 Features
- Upload or use sample property CSVs
- View **rental yield**, **vacancy rate**, and **appreciation** per property
- See **city-level averages** and **risk distributions**
- Interactive **charts** and **gauge indicator**
- Download filtered data as CSV

## 🧮 Risk Formula
RiskScore = (VacancyRate × 100) − RentalYield − (Appreciation% ÷ 2)

- **Low Risk:** RiskScore ≤ 0  
- **Medium Risk:** 0 < RiskScore ≤ 10  
- **High Risk:** RiskScore > 10  

## 🚀 Run Locally

1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```bash
   streamlit run UK_Real_Estate_Analyzer.py
   ```

## 📁 Sample Data Columns
```
PropertyID, Location, PurchasePrice, CurrentValue, AnnualRent, VacancyRate, address, price, bedrooms
```

## 🏙️ Example Output
- Interactive scatterplots of rent yield vs vacancy rate  
- Bar charts comparing purchase price vs current value  
- Pie chart showing risk band proportions  
- City summary table with averages

---

💡 *Developed for testing property risk models and visualization workflows.*
