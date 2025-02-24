from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import pandas as pd
import time
import os
# Function to take a screenshot for a given stock symbol
def take_screenshot(symbol, driver, period, pr_period, uind1, uind1_param, uind2, uind2_param, uind3, uind3_param, lind1, lind1_param, lind2, lind2_param, lind3, lind3_param, screenshot_suffix):
    try:
        # Access the website
        url = 'https://main.icharts.in/charts.html'
        driver.get(url)
        
        # Fill in the stock symbol
        symbol_input = driver.find_element(By.ID, 'symbol')
        symbol_input.clear()
        symbol_input.send_keys(symbol)
        
        # Select the period
        period_select = Select(driver.find_element(By.ID, 'period'))
        period_select.select_by_visible_text(period)
        
        # Select the chart size
        chart_size_select = Select(driver.find_element(By.ID, 'chart_size'))
        chart_size_select.select_by_visible_text('Large')
        
        # Select the predefined range
        pr_period_select = Select(driver.find_element(By.ID, 'pr_period'))
        pr_period_select.select_by_visible_text(pr_period)
        
        # Ensure Log Chart and Color Bars options are checked
        log_chart_checkbox = driver.find_element(By.ID, 'log_chart')
        if not log_chart_checkbox.is_selected():
            log_chart_checkbox.click()
        
        color_bars_checkbox = driver.find_element(By.ID, 'color_bars')
        if not color_bars_checkbox.is_selected():
            color_bars_checkbox.click()
        
        # Select the chart type
        chart_type_select = Select(driver.find_element(By.ID, 'chart_type'))
        chart_type_select.select_by_visible_text('CandleStick')
                
        # Set upper indicators
        uind1_select = Select(driver.find_element(By.ID, 'uind1'))
        uind1_select.select_by_visible_text(uind1)
        uind1_param_input = driver.find_element(By.ID, 'uind1_param')
        uind1_param_input.clear()
        uind1_param_input.send_keys(uind1_param)
        
        uind2_select = Select(driver.find_element(By.ID, 'uind2'))
        uind2_select.select_by_visible_text(uind2)
        uind2_param_input = driver.find_element(By.ID, 'uind2_param')
        uind2_param_input.clear()
        uind2_param_input.send_keys(uind2_param)
        
        uind3_select = Select(driver.find_element(By.ID, 'uind3'))
        uind3_select.select_by_visible_text(uind3)
        uind3_param_input = driver.find_element(By.ID, 'uind3_param')
        uind3_param_input.clear()
        uind3_param_input.send_keys(uind3_param)
        
        # Set lower indicators
        lind1_select = Select(driver.find_element(By.ID, 'lind1'))
        lind1_select.select_by_visible_text(lind1)
        lind1_param_input = driver.find_element(By.ID, 'lind1_param')
        lind1_param_input.clear()
        lind1_param_input.send_keys(lind1_param)
        
        lind2_select = Select(driver.find_element(By.ID, 'lind2'))
        lind2_select.select_by_visible_text(lind2)
        lind2_param_input = driver.find_element(By.ID, 'lind2_param')
        lind2_param_input.clear()
        lind2_param_input.send_keys(lind2_param)
        
        lind3_select = Select(driver.find_element(By.ID, 'lind3'))
        lind3_select.select_by_visible_text(lind3)
        lind3_param_input = driver.find_element(By.ID, 'lind3_param')
        lind3_param_input.clear()
        lind3_param_input.send_keys(lind3_param)
        
        # Submit the form to refresh the chart
        refresh_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Refresh Chart"]')
        refresh_button.click()
        print(f"Clicked the refresh button for symbol: {symbol}")
        
        # Wait for the chart to load
        time.sleep(3)
        
        # Scroll to the chart area
        driver.execute_script("window.scrollTo(0, 180);")  # Scroll to Y coordinate 200
        time.sleep(1)  # Wait for the scroll action to complete
        
        # Ensure the output directory exists
        output_dir = 'output/'
        os.makedirs(output_dir, exist_ok=True)
        
        # Take a screenshot of the visible part of the page
        screenshot_path = os.path.join(output_dir, f'{symbol}_chart_{screenshot_suffix}.png')
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as: {screenshot_path}")
        
        # Open the screenshot and crop it
        image = Image.open(screenshot_path)
        left = 190  # Pixels from the left
        top = 0  # Pixels from the top (keep entire height)
        right = image.width - 1000  # Pixels from the right
        bottom = image.height  # Keep entire height
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image_path = os.path.join(output_dir, f'{symbol}_chart_{screenshot_suffix}_c.png')
        cropped_image.save(cropped_image_path)
        print(f"Cropped screenshot saved as: {cropped_image_path}")

        return cropped_image_path

    except Exception as e:
        print(f"Error taking screenshot for symbol {symbol}: {e}")
        return None

# Function to combine images horizontally
def combine_images_horizontally(image_paths, output_path):
    images = [Image.open(path) for path in image_paths if path is not None]
    
    if images:
        total_width = sum(image.width for image in images)
        max_height = max(image.height for image in images)

        combined_image = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for image in images:
            combined_image.paste(image, (x_offset, 0))
            x_offset += image.width

        combined_image.save(output_path)
        print(f"Combined image saved as: {output_path}")
    else:
        print(f"No images to combine for {output_path}")
# Setup Selenium with options
options = Options()
options.headless = True  # Set to True to run in headless mode (without opening a browser window)

# Initialize the WebDriver
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    exit(1)
try:
    # Load Excel file and filter symbols where 'Checkbox' is TRUE
    excel_path = 'data/extracted_data.xlsx'
    df = pd.read_excel(excel_path)

    if 'Symbol' not in df.columns or 'Checkbox' not in df.columns:
        print("Error: Missing required columns in the Excel file.")
        exit(1)

    df = df[df['Checkbox'] == True]  # Filter checked symbols

    if df.empty:
        print("No symbols selected. Exiting.")
        exit(0)
        
    uind_options = [
    "None",
    "Bollinger Bands",
    "Donchain Channel",
    "Envelop (SMA 20 +/- 10%)",
    "Simple Moving Average",
    "Exponential Moving Average",
    "Weighted Moving Average",
    "Triangle Moving Average",
    "Parabolic SAR"
    ]
    
    lind_options = [
    "None", 
    "Accumulation/Distribution", 
    "Aroon Oscillator", 
    "Aroon Up/Down", 
    "Avg Directional Index", 
    "Avg True Range", 
    "Bollinger Band Width", 
    "Chaikin Money Flow", 
    "Chaikin Oscillator", 
    "Chaikin Volatility", 
    "Close Location Value", 
    "Commodity Channel Index", 
    "Detrended Price Osc", 
    "Donchian Channel Width", 
    "Ease of Movement", 
    "Fast Stochastic", 
    "MACD", 
    "Mass Index", 
    "Momentum", 
    "Money Flow Index", 
    "Neg Volume Index", 
    "On Balance Volume", 
    "Performance", 
    "% Price Oscillator", 
    "% Volume Oscillator", 
    "Pos Volume Index", 
    "Price Volume Trend", 
    "Rate of Change", 
    "RSI", 
    "Slow Stochastic", 
    "StochRSI", 
    "TRIX", 
    "Ultimate Oscillator", 
    "Volume", 
    "William's %R"
    ]
    
    for symbol in df['Symbol']:
        weekly_path = take_screenshot(symbol, driver, 'Weekly', '3 Years', uind_options[5], 'Close,20', uind_options[5], 'Close,50', uind_options[5], 'Close,100', lind_options[33], '', lind_options[16], '12,26,9', lind_options[34], '14', '1')
        time.sleep(1)
        nine_month_path = take_screenshot(symbol, driver, 'Daily', '9 Months', uind_options[5], 'Close,20', uind_options[5], 'Close,50', uind_options[2], '20', lind_options[3], '14', lind_options[15], '5,3', lind_options[29], '5,3', '2')
        time.sleep(1)
        six_month_path = take_screenshot(symbol, driver, 'Daily', '6 Months', uind_options[5], 'Close,20', uind_options[5], 'Close,50', uind_options[1], '20,2', lind_options[33], '', lind_options[28], '14', lind_options[32], '7,14,28', '3')
        time.sleep(1)

        combined_image_path = os.path.join('output/combined_stock_charts/', f'{symbol}.png')
        combine_images_horizontally([weekly_path, nine_month_path, six_month_path], combined_image_path)

finally:
    driver.quit()