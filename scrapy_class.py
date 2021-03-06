
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time




class ZillowSpider:
	
	def init_driver(file_path):
		options = Options()
		#options.add_argument("--headless")
		browser = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)	
		browser.wait = WebDriverWait(browser, 10)
		return(browser)

	def _is_empty(self, obj):
		if any([len(obj) == 0, obj == "null"]):
			return(True)
		else:
			return(False)


	def _is_element_displayed(self, browser, elem_text, elem_type):
		if elem_type == "class":
			try:
				out = browser.find_element_by_class_name(elem_text).is_displayed()
			except:
				out = False
		elif elem_type == "css":
			try:
				out = browser.find_element_by_css_selector(elem_text).is_displayed()
			except (NoSuchElementException, TimeoutException):
				out = False
		else:
			raise ValueError("arg 'elem_type' must be either 'class' or 'css'")
		return(out)

	def check_for_captcha(self, browser):
		if self._is_element_displayed(browser, "captcha-container", "class"):
			print("\nCAPTCHA!\n"\
				  "Manually complete the captcha requirements.\n"\
				  "Once that's done, if the program was in the middle of scraping "\
				  "(and is still running), it should resume scraping after ~30 seconds.")
			self._pause_for_captcha(browser)


	def _pause_for_captcha(self, browser):
		while True:
			time.sleep(30)
			if not self._is_element_displayed(browser, "captcha-container", "class"):
				break



	def get_zestimate(self, element_text):
		#print("get_zestimate")
		try:
			#print("get_zestimate_first_try")
			listIndex = element_text.index("Zestimate")
			#print(listIndex)
			#print(listIndex)
			#zestimate = element_text.split()[3]
			zestimate = element_text[listIndex+1]
			if zestimate == "for":
				#print("for")
				element_text = element_text[listIndex+1:]
				#print(listt)

				listIndex = element_text.index("Zestimate")
				#print(listIndex)
				zestimate = element_text[listIndex+1]
				#print(zestimate)

			listIndex = element_text.index("RANGE")
			#zRange = str(element_text.split()[6] + element_text.split()[7] + element_text.split()[8])
			zRange = element_text[listIndex+1] + element_text[listIndex+2] + element_text[listIndex+3]
			return zestimate, zRange
		except:
			#print("get_zestimate_first_except")
			zestimate = "NA"
			zRange = "NA"
			return zestimate, zRange

	def parse_element_text(self, element_text):
		#print("parse_element_text")
		for strIng in element_text:
			if "Built in" in strIng:
				strIng = strIng.replace("Built in",'')
				#print("Built in: " + str)
				builtIn = strIng
			if "Built by" in strIng:
				strIng = strIng.replace("Built by:",'')
				#print("Built by: " + str)
				builtBy = strIng
			if "Community name" in strIng:
				strIng = strIng.replace("Community name:",'')
				#print("Community name: " + str)
				comName = strIng
			if "Parking" in strIng:
				strIng = strIng.replace("Parking:",'')
				#print("Parking: " + str)
				parking = strIng

		return  builtIn, builtBy, comName, parking




	def exception_request(self, browser):
		#print("exception_request")
		#print("Other disign page")
		#####https://www.zillow.com/homes/for_sale//homedetails/295-N-Minnewawa-Ave-Fresno-CA-93727/18759515_zpid/
		#####https://www.zillow.com/homes/for_sale/2094098284_zpid/globalrelevanceex_sort/29.783524,-95.363388,29.650838,-95.474968_rect/12_zm/

		try:
			#print("exception_request_first_try")
			elm = browser.find_element_by_xpath("//*[@class='hdp-fact-moreless-toggle za-track-event']") 
			elm.click()
			elm = browser.find_element_by_xpath("//*[@class='z-moreless-content hdp-fact-moreless-content']")		
			element_text = elm.text.split('\n')
			#print(element_text)

			# ['INTERIOR FEATURES', 
			# 'Bedrooms', 'Beds: 4', 
			# 'Bathrooms', 'Baths: 2 full, 1 half', 
			# 'Heating and Cooling', 'Heating: Forced air', 'Heating: Electric, Gas', 
			# 'Cooling: Central, Refrigeration', 
			# 'Appliances', 'Appliances included: Dishwasher, Dryer, Freezer, Garbage disposal, Microwave, Range / Oven, Refrigerator, Washer', 
			# 'Flooring', 'Floor size: 2,140 sqft', 'Flooring: Carpet, Hardwood, Tile', 'Other Interior Features', 'Fireplace',
			#  'Ceiling Fan', 'Room count: 12', 
			#  'SPACES AND AMENITIES', 
			#  'Spaces', 'Jetted Tub', 'Basketball Court', 
			#  'Amenities', 
			#  'Security System', 
			#  'CONSTRUCTION', 
			#  'Type and Style', 
			#  'Structure type: Other',
			#   'Single Family', 
			#   'Materials', 'Roof type: Shake Shingle', 'Exterior material: Stucco', 
			#   'Dates', 'Last remodel year: 1980', 'Built in 1980', 
			#   'Other Construction Features', 'Stories: 1', 
			#   'EXTERIOR FEATURES', 'Yard', 'Lawn', 'Fenced Yard', 'View Type', 
			#   'View: City', 'Lot', 'Lot: 0.36 acres',
			#    'Other Exterior Features', 
			#    'Parcel #: 46222009', 
			#    'PARKING', 
			#    'Parking: Carport, On street, Attached Garage, 2 spaces, 450 sqft garage', 
			#    'RV Parking',
			#     'UTILITIES', 
			#    'Cable Ready', 
			#    'Sprinkler System', 
			#    'OTHER', 
			#    'Last sold: Jun 2010 for $220,000',
			#     'Price/sqft: $145', 'ACTIVITY ON ZILLOW', 
			#     'Days on Zillow: 132', 'Views in the past 30 days: 3,545',
			#      '59 shoppers saved this home', 'County websiteSee data sources']

			school = "NA"
			parking_details = "NA"
			lastSold = "NA" 
			priceSqft = "NA"


			for strIng in element_text:
				if "Parking:" in strIng:
					strIng = strIng.replace("Parking:",'')
					#print("Parking: " + strIng)
					parking_details = strIng
					#builtIn = strIng
				if "Last sold:" in strIng:
					strIng = strIng.replace("Last sold:",'')
					#print("Last sold: " + strIng)
					#builtIn = strIng
					lastSold = strIng
				if "Price/sqft:" in strIng:
					strIng = strIng.replace("Price/sqft:",'')
					#print("Price/sqft: " + strIng)
					#builtIn = strIng
					priceSqft = strIng
				if "School district:" in strIng:
					strIng = strIng.replace("School district:",'')
					#print("School district: " + strIng)
					#builtIn = strIng
					school = strIng

		except:
			#print("exception_request_first_except")
			self.check_for_captcha(browser)
			school = "NA"
			parking_details = "NA"
			lastSold = "NA"
			priceSqft = "NA"



		try:
			#print("exception_request_second_try")
			elm = browser.find_element_by_id('zestimate-details')
		except:
			#print("exception_request_second_except")
			#print("Other disign page")
			#self.check_for_captcha(browser)
			return "NA" , "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA" 

		try:
			#print("exception_request_third_try")
			elm.click()
			element_text = elm.text.split()
			#print(element_text.split())
			#print(element_text)

			zestimate, zRange = self.get_zestimate(element_text)
			#print(zestimate)
			#print(zRange)


					
			elm = browser.find_element_by_xpath("//*[@class='hdp-facts-expandable-container clear']") 
			element_text = elm.text.split('\n')
			#print(element_text)

			builtIn = element_text[4]
			builtBy = "NA"
			comName = element_text[2]
			parking = element_text[10]

			# print(zestimate)
			# print(zRange)
			# print(builtIn)
			# print(builtBy)
			# print(comName)
			# print(parking)
			# print(school)
			# print(parking_details)
			# print(lastSold)
			# print(priceSqft)
			

			return zestimate , zRange, builtIn, builtBy, comName, parking, school, parking_details, lastSold, priceSqft
		except:
			#print("exception_request_third_except")
			return "NA" , "NA", "NA", "NA", "NA", "NA","NA", "NA", "NA", "NA"


	def main_request(self, browser, elm):
		#print("main_request")
		school = "NA"
		parking_details = "NA"
		lastSold = "NA"
		priceSqft = "NA"
		elm.click()
		#print("main_request_after_elm_click")
		element_text = elm.text.split()
		#print(element_text)
		#print(element_text.split())
		#print(element_text)

		zestimate, zRange = self.get_zestimate(element_text)
		
		#print("main_request_after_get_zestimate")
		#print(zestimate)
		#print(zRange)
		elm = browser.find_element_by_xpath("//*[@class='hdp-facts zsg-content-component']") 
		element_text = elm.text.split('\n')
		#print("main_request_after_find_element_by_xpath")
		builtIn, builtBy, comName, parking = self.parse_element_text(element_text)
		# print(zestimate)
		# print(zRange)
		# print(builtIn)
		# print(builtBy)
		# print(comName)
		# print(parking)
		# print(school)
		# print(parking_details)
		# print(lastSold)
		# print(priceSqft)
		# print("main_request_return")
		return zestimate , zRange, builtIn, builtBy, comName, parking, school, parking_details, lastSold, priceSqft


	def get_one_request(self, browser, url):
		#print("get_one_request")
		zestimate = "NA"
		zRange = "NA"
		builtIn = "NA"
		builtBy = "NA"
		comName = "NA"
		parking = "NA"
		school = "NA"
		parking_details = "NA"
		lastSold = "NA"

		browser.get(url)
		browser.implicitly_wait(1)

		try:
			#print("get_one_request_first_try")
			elm = browser.find_element_by_id('homeValue')
			#elm = browser.find_element_by_id('home-details-module-zone')
		except:
			#print("get_one_request_first_except")
			return self.exception_request(browser)
			
		try:
			#print("get_one_request_second_try")
			return self.main_request(browser, elm)	
		except:
			#print("get_one_request_second_except")
			return "NA" , "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA"











