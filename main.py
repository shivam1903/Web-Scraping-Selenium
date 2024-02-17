'''
Use Python Selenium to scrape data from the EPFO website. Make sure to use the Chrome driver.
Make sure to verify your requirements.txt file before submitting your code. You can use Python 3.11>= for this coding challenge.

Fill out the sections where TODO is written.
Ideally your code should work simply by running the main.py file.

This is a sample file to get you started. Feel free to add any other functions, classes, etc. as you see fit.
This coding challenge is designed to test your ability to write python code and your familiarity with the Selenium library.
This coding challenge is designed to take 2-4 hours and is representative of the kind of work you will be doing at the company daily.
'''

# Importing the required libraries
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
import pytesseract
import easyocr
import numpy as np



import pandas as pd

DOWNLOAD_DIR = "data/"

def scrape_data(company_name: str):
    '''
    Scrape data from the EPFO website
    '''
    
    # Create Selenium driver
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    # TODO: Add whatever options you might think are helpful
    prefs = {
    "download.default_directory": os.path.abspath(DOWNLOAD_DIR),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
    "safebrowsing.enabled": True}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    # Open the EPFO website
    driver.get('https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome')
    
    # Use time library to visualize the browser else tab will close
    import time
    time.sleep(5)

    # TODO: Fill out the code for the following steps
    # Step 1 - Refer to the sample_output/step_1.png for the screenshot of the page
    # Enter the company name in the search box
    # company_name = "MGH LOGISTICS PVT LTD"
    search_box = driver.find_element(By.ID, "estName")
    search_box.send_keys(company_name)
    
    for i in range(100):
        try:
            
            # Enter the captcha in the captcha box (Hint: You can use Google lens, Python OCR libraries like pytesseract, etc.)
            captcha_element = driver.find_element(By.ID, "capImg")
            img_screenshot = captcha_element.screenshot_as_png
            captcha_image = Image.open(BytesIO(img_screenshot))
            captcha_image.save("captcha.png")

            ## PyTesseract
            # image = cv2.imread('captcha.png')
            # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # gray = cv2.medianBlur(gray, 3)
            # filename = "{}.png".format("temp")
            # cv2.imwrite(filename, gray)
            # captcha_text = pytesseract.image_to_string(Image.open(filename))

            ## EasyOCR
            captcha_image_gray = captcha_image.convert('L')
            captcha_image_np = np.array(captcha_image_gray)
            reader = easyocr.Reader(['en'])  # You can specify language(s) as needed
            captcha_text = reader.readtext(captcha_image_np)
            captcha_text = ' '.join([result[1] for result in captcha_text])
            captcha_text = captcha_text.upper()
            print(captcha_text)
            captcha_arr = captcha_text.split(' ')
            new_cap_txt = ""
            for txt in captcha_arr:
                new_cap_txt = new_cap_txt + txt

            print(new_cap_txt)
            captcha_box = driver.find_element(By.ID, "captcha")
            captcha_box.send_keys(new_cap_txt)

            search_button = driver.find_element(By.ID, "searchEmployer")
            search_button.click()
            time.sleep(2)
            if "Please enter valid captcha" in driver.page_source:
                print("Invalid captcha. Retrying...")
                time.sleep(2)
                continue
            break
        except:
            print("Stale Element Reference Exception occurred. Retrying...")

    # TODO: Fill out the code for the following steps
    # Step 2 - Refer to the sample_output/step_2.png for the screenshot of the page
    # Click on the "View Details" button - you should see an output similar to sample_output/step_2.png
    link = driver.find_element(By.XPATH, "//a[@title='Click to view establishment details.']")
    link.click()
    time.sleep(4)
    # Click on the "View Payment Details" button that is displayed in sample_output/step_2.png - this opens a new tab
    link2 = driver.find_element(By.XPATH, "//a[@title='Click to view payment details.']")
    link2.click()
    time.sleep(4)

    # TODO: Fill out the code for the following steps
    # Step 3 - Refer to the sample_output/step_3.png for the screenshot of the page - this is the new tab that opens up in Step 2
    # Click on the "Excel" button - this downloads an excel file in the Downloads folder
    driver.switch_to.window(driver.window_handles[-1])
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dt-button.buttons-excel.buttons-html5")))
    button.click()
    # This should be the final output of the function and should save the excel file in the data folder
    # It should look something like data/Payment Details.xlsx as used in the test_scrape_data() function
    time.sleep(5)



def test_scrape_data():
    '''
    Test the scraped data
    '''
    # Convert xlsx file to csv due to some issues with pandas
    from xlsx2csv import Xlsx2csv
    Xlsx2csv("data/Payment Details.xlsx", outputencoding="utf-8").convert("payment_details.csv")

    df = pd.read_csv("payment_details.csv")

    assert set(df.columns) == set(['TRRN', 'Date Of Credit', 'Amount', 'Wage Month', 'No. of Employee', 'ECR'])
    assert df['TRRN'].loc[0] == 3171702000767
    assert df['Date Of Credit'].loc[0] == '03-FEB-2017 14:35:15'
    assert df['Amount'].loc[0] == 334901
    assert df['Wage Month'].loc[0] == 'DEC-16'
    assert df['No. of Employee'].loc[0] == 83
    assert df['ECR'].loc[0] == 'YES'
    print("All tests passed!")

def main():
    print("Hello World!")

    scrape_data("MGH LOGISTICS PVT LTD")

    # TODO: Uncomment the following tests whenever scraping is completed.
    test_scrape_data()
    # TODO: Feel free to add any edge cases which you might think are helpful


if __name__ == "__main__":
    main()