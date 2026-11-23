import os
import sys
import time
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

OUTPUT_DIR = r"d:\Purnashish\automated-web-security-scanner\demo-video"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Capture Real Website Frames via Selenium
# ---------------------------------------------------------------------------
def capture_real_ui_frames():
    print("Starting local Flask server...")
    server_proc = subprocess.Popen([sys.executable, "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        print("Capturing live UI frames at 1920x1080...")
        driver.get("http://127.0.0.1:5000/")
        time.sleep(2)
        
        # Frame 1: Initial Hero & Dashboard
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "raw_frame_01_hero.png"))
        print("Captured Frame 1: Hero")
        
        # Frame 2: Entering Target URL
        inp = driver.find_element(By.ID, "target-url")
        btn = driver.find_element(By.ID, "scan-button")
        inp.clear()
        inp.send_keys("https://example.com")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "raw_frame_02_input.png"))
        print("Captured Frame 2: Input URL")
        
        # Frame 3: Scanning in progress (temporarily set label to simulate instant scanning snapshot)
        driver.execute_script("document.getElementById('button-label').textContent = 'Scanning…'; document.getElementById('scan-button').disabled = true;")
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "raw_frame_03_scanning.png"))
        print("Captured Frame 3: Scanning state")
        
        # Click scan and wait for real results
        driver.execute_script("document.getElementById('scan-form').dispatchEvent(new Event('submit'));")
        WebDriverWait(driver, 25).until(
            lambda d: not d.find_element(By.ID, "results").get_attribute("hidden")
        )
        time.sleep(1)
        
        # Frame 4: Results top (Summary metric cards & HTTP pill)
        driver.execute_script("window.scrollTo(0, 380);")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "raw_frame_04_results_top.png"))
        print("Captured Frame 4: Results Top")
        
        # Frame 5: Detailed findings (HTTPS, CSP, HSTS)
        driver.execute_script("window.scrollTo(0, 680);")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "raw_frame_05_findings_mid.png"))
        print("Captured Frame 5: Findings Middle")
        
        # Frame 6: Cookies & CORS findings
        driver.execute_script("window.scrollTo(0, 1100);")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "raw_frame_06_findings_bottom.png"))
        print("Captured Frame 6: Findings Bottom")
        
        # Frame 7: Feature Cards Grid (HTTPS, Cookie Checks, CORS Review)
        driver.execute_script("window.scrollTo(0, 1750);")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "raw_frame_07_features.png"))
        print("Captured Frame 7: Feature Cards")
        
    finally:
        driver.quit()
        server_proc.terminate()
        server_proc.wait()
        print("Selenium capture completed.")

if __name__ == "__main__":
    capture_real_ui_frames()
