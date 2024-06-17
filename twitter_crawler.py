import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the browser
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
wait = WebDriverWait(driver, 10)

# Starting URL
start_url = "https://twitter.com/search?q=%23Winter"

# Crawl 6 hashtag pages
for i in range(6):
    # Load the current URL
    driver.get(start_url)
    
    #Sleep so I can log in
    time.sleep(30)

    # Wait for the tweets to load
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/hashtag/']")))
    
    # Find hashtag links on the page
    hashtags = driver.find_elements_by_css_selector("a[href*='/hashtag/']")
    
    # Select a random hashtag and get its URL
    random_hashtag = random.choice(hashtags)
    start_url = random_hashtag.get_attribute("href")
    
    # Print the visited page number and URL
    print(f"Visited Page {i + 1}: {start_url}")

# Close the browser
driver.quit()
