# Web-Scraping-Selenium
This repo contains my practice code for working with Selenium to implement Web Scraping. Also involves having Captcha identification

repo link: https://github.com/shivam1903/Web-Scraping-Selenium

For the mentioned tasks, I have used chrome webdriver.

## Step 1 - Company Name
I start by entering the company name in the search box. I identify the search box using its ID.
Once the name is entered, we move to the captcha.

## Step 2 - Captcha
Captcha was the tricky part. For this part I tried user pytesseract initially, and then I used easyOCR. Both of them did not give perfect results. I realized OCR will not always give perfect answers for Captcha. I could have created a ML model to deal with this. But for simplicity, I initiated a for loop which keeps checking the Captcha, until a correct Captcha is received (or 100 times, whichever comes first).
For this, I first took a screenshot of the Captch element, and then process it using EasyOCR. The derived text is not always in the perfect form, thus after some tests, I found the characters are usually space separated, lowercase or in jumbled order. I added some processing to solve the space separated and lowercase problem. Once that is done, I input it in the field and check if it is correct.

## Step 3 - Opening Links
Using the find element path, I navigate through the different links. Once completed, it finally opens a new tab. From where we get the "Excel" button to download the relevant file.

## Step 4 - Downloading Payment Details
I click on the "Excel" button using the element_to_be_clicked function. Once clicked, it will start downloading, but as the downloading takes some time, I have added a sleep option. This will make sure the download is successfull. One can increase the sleep time according to the network.

Note - The captcha screenshot is stored as captcha.png. We can use these images to train a model and increase the perfection instead of using EasyOCR.
