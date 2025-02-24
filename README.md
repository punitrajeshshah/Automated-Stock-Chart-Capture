# 📈 Automated Stock Chart Capture  

## 📌 Project Overview  
This project automates **stock chart retrieval from icharts.in** using **Selenium**. It captures, processes, and merges stock charts across different timeframes, applying **technical indicators** for better analysis.  

## 🚀 Features  
- ✅ **Automates web scraping** of stock charts from `icharts.in`.  
- ✅ **Reads stock symbols from an Excel file** and processes selected stocks.  
- ✅ **Captures screenshots** of stock performance over multiple timeframes (Weekly, 9M, 6M).  
- ✅ **Applies technical indicators** like EMA, RSI, MACD, Bollinger Bands.  
- ✅ **Combines stock chart images** into a single visual for easy comparison.  

## 📂 Repository Structure  
Automated-Stock-Chart-Capture/     
│── README.md # Project Overview          
│── LICENSE # Default GitHub License          
│── .gitignore # Default GitHub .gitignore         
│         
├── data/         
│ ├── extracted_data.xlsx # Excel file containing stock symbols and Check Box     
│ ├── extracted_data.csv # CSV file containing stock symbols        
│   
├── scripts/         
│ ├── RUN_Charts.py # Main Python script for automation    
│ ├── RUN_Charts.ipynb # Jupiter notebook of the script    
│   
├── output/         
│ ├── combined_stock_charts/ # Folder for merged stock chart images     


## 🛠️ How to Use  
### **1️⃣ Install Dependencies**  
```bash
pip install selenium pandas openpyxl pillow

```
### 2️⃣ Set Up Selenium WebDriver
The script automatically installs ChromeDriver using `webdriver-manager`.
No manual setup is required! Just make sure you have Google Chrome installed on your system.

### 3️⃣ Run the Script
```bash
python scripts/RUN_Charts.py

```
- The script will open icharts.in, navigate through stock charts, and capture screenshots.
- It will save the combined stock chart images in the `output/combined_stock_charts/` folder.

## 📊 Technical Indicators Used
The script applies technical analysis indicators to stock charts:

- 📈 Upper Indicators: EMA (20, 50, 100), Bollinger Bands
- 📉 Lower Indicators: MACD, RSI, Stochastic Oscillator
  
These indicators help analyze market trends and price movements effectively.

## 🔍 Future Enhancements
🚀 Planned Improvements:
- Cloud storage integration – Save stock images online automatically.
- Real-time alerts – Identify significant stock pattern changes.
- Improved UI/UX – Make the tool more interactive.
