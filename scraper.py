from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
from dotenv import load_dotenv
import os
from openAI import jsonifyDataAI

load_dotenv()

def scrape_data() :
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the login page
        logger.info("Opening login page...")
        driver.get(os.getenv("TARGET_URL"))

        # Switch to the iframe
        logger.info("Switching to iframe...")
        iframe = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)

        # Wait for the username field to be present
        logger.info("Waiting for username field...")
        wait = WebDriverWait(driver, 2)
        username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='LOGIN_ID']")))

        # Enter your username
        logger.info("Entering username...")
        username.send_keys(os.getenv("EMAIL"))

        # Wait for the "Next" button to be clickable and click it
        logger.info("Waiting for 'Next' button...")
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "nextbtn")))
        logger.info("Clicking 'Next' button...")
        next_button.click()

        # Wait for some time before waiting for the password field
        time.sleep(5)  # Adjust the sleep time as needed

        # Wait for the password field to appear
        logger.info("Waiting for password field...")
        password = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='PASSWORD']")))

        # Enter your password
        logger.info("Entering password...")
        password.send_keys(os.getenv("PASSWORD"))

        # Find the login button and click it
        logger.info("Clicking login button...")
        login_button = next_button
        login_button.click()

        time.sleep(20)

        # Switch back to the main content
        driver.switch_to.default_content()

        # Wait for the attendance page to load by checking for the element with ID 'My_Attendance'
        logger.info("Waiting for attendance page to load...")
        wait.until(EC.presence_of_element_located((By.ID, "My_Attendance")))

        # Now you are logged in, navigate to the page you want to scrape
        logger.info("Navigating to target page...")
        driver.get(os.getenv("AttendancePG_URL"))

        time.sleep(15)
        # Perform your scraping tasks
        logger.info("Performing scraping tasks...")
        content = driver.find_element(By.CLASS_NAME, "mainDiv").text

        # signing out after getting the data
        logger.info("Signing out...")
        popUp = driver.find_element(By.XPATH, f"//div[@id='{"zc-account-settings"}']//a")
        popUp.click()
        
        signout = wait.until(EC.presence_of_element_located((By.ID, "portalLogout")))
        signout.click()
        # time.sleep(5)
        # driver.save_screenshost(f"signoutcreen.png")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        driver.save_screenshot(f"error_screenshot{timestamp}.png")
        logger.info(f"Screenshot saved as error_screenshot{timestamp}.png")
        # with open("page_source.html", "w", encoding="utf-8") as f:
        #     f.write(driver.page_source)
        # logger.info("Page source saved as page_source.html")

    finally:        
        # Close the browser
        logger.info("Closing the browser...")
        driver.quit()
        output = jsonifyDataAI(content)
        return output


# print(scrape_data())