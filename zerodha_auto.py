from selenium import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import time
import cv2
import numpy as np
import pyautogui
import os
from dotenv import load_dotenv

# loading env variables
load_dotenv()

# Zerodha
buyPixel = [218, 148, 75]
sellPixel = [115, 251, 253]

buy_flag = 1
sell_flag = 0

def open_zerodha():
	driver.get('https://kite.zerodha.com/chart/web/tvc/NFO-FUT/BANKNIFTY21AUGFUT/12783874?theme=dark')

def login():
	alert = driver.switch_to.alert
	alert.accept()

	userId = driver.find_element_by_xpath("//input[@id='userid']")
	userId.send_keys(os.getenv("USER_ID"))

	password = driver.find_element_by_xpath("//input[@id='password']")
	password.send_keys(os.getenv("PASSWORD"))

	loginBtn = driver.find_element_by_xpath("//button[@class='button-orange wide']")
	loginBtn.click()

	time.sleep(1)

	pin = driver.find_element_by_xpath("//input[@id='pin']")
	pin.send_keys(os.getenv("PIN"))

	continueBtn = driver.find_element_by_xpath("//button[@class='button-orange wide']")
	continueBtn.click()

#Does not require you to login using QR CODE
options = Options()
options.headless = False
options.add_argument('--user-data-dir=/Users/pushpitbhardwaj/Library/Application Support/Google/Chrome/Default')
options.add_argument('--profile-directory=Default')

driver = webdriver.Chrome(executable_path='/Users/pushpitbhardwaj/Desktop/h4CK3R/dev/zerodha_auto/chromedriver', options=options)

open_zerodha()
time.sleep(2)

login()
print('Logged In...')

time.sleep(2)

requiredLi = driver.find_element_by_xpath('//li[@data-balloon="3"]')
requiredLi.click()

chosenIndex = driver.find_element_by_xpath('//span[@class="nice-name" and text()="BANKNIFTY AUG 35500 CE"]')
chosenIndex.click()

time.sleep(3)

# Load chart
pyautogui.click(x=335, y=280)
time.sleep(3)

# loadChartLayoutArrow = driver.find_element_by_xpath('//div[@class="arrow-2pXEy7ej-"]')
# loadChartLayoutArrow.click()
pyautogui.click(x=1285, y=230)
time.sleep(2)

# loadChartLayout = driver.find_element_by_xpath('//div[@class="js-save-load-menu-item-load-chart item-2xPVYue0-"]')
# loadChartLayout.click()

pyautogui.click(x=1285, y=315)
time.sleep(1)

# chooseSupertrend = driver.find_element_by_xpath('//div[@class="js-table-row tv-load-chart-dialog-table__row tv-load-chart-dialog-table__row--item tv-load-chart-dialog-table__row--item-without-favs"]')
# chooseSupertrend.click()

pyautogui.click(x=900, y=475)
time.sleep(1)

# closeLoadChartLayout = driver.find_element_by_xpath('//div[@class="tv-dialog__close js-dialog__close"]')
# closeLoadChartLayout.click()

pyautogui.click(x=1205, y=315)
time.sleep(1)

buyPrice = 0 
sellPrice = 0

while True:
	# take a screenshot
	img = pyautogui.screenshot(region=(2200, 450, 150, 1150))

	# convert these pixels to a proper numpy array to work with OpenCV
	frame = np.array(img)

	# convert colors from BGR to RGB
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	
	for pixelValues in frame:
		for pixelValue in pixelValues:
			pixelValueList = pixelValue.tolist()
			
			if pixelValueList[0] == buyPixel[2] and pixelValueList[1] == buyPixel[1] and pixelValueList[2] == buyPixel[0] and buy_flag:
				print("\n\nBuy!!!!")
				lastPrice = driver.find_element_by_xpath('//span[@class="last-price"]')
				buyPrice = float(lastPrice.text)
				print("25 *", buyPrice, "=", 25*buyPrice)
				# pyautogui.click(x=205, y=280)
				buy_flag = 0
				sell_flag = 1
			elif pixelValueList[0] == sellPixel[2] and pixelValueList[1] == sellPixel[1] and pixelValueList[2] == sellPixel[0] and sell_flag:
				print("\n\n---------------- Sell ----------------")
				lastPrice = driver.find_element_by_xpath('//span[@class="last-price"]')
				sellPrice = float(lastPrice.text)
				print("25 *", sellPrice, "=", 25*sellPrice)
				print("\nGain =", 25*(buyPrice - sellPrice))
				buy_flag = 1
				sell_flag = 0

	cv2.imshow("Screen", frame)

	# if the user clicks q, it exits
	if cv2.waitKey(5) == ord("q"):
		break

# make sure everything is closed when exited
cv2.destroyAllWindows()