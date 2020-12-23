#-*-coding: utf-8-*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from json import loads, dumps
from codecs import open


class Freelancer:
	def __init__(self, config="stored_data.json", arg_data="!"):
		self.config_file = config
		self.data = self.load_data(config)
		if arg_data != "!" and type(arg_data) == type({}): #If there is preloaded data, 
			for data in arg_data:
				if data in self.data:
					self.data[data] = arg_data[data] 
			self.save_data(config)

		options = Options()
		#options.add_argument('--headless')
		options.add_argument('--disable-gpu') 
		options.add_argument("--log-level=3");
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = webdriver.Chrome(chrome_options=options)


	def load_data(self, file):
		try:
			with open(file, "r", encoding="utf-8") as f:
				return loads(f.read())
		except:
			data = {
				"user": "",
				"password": "",
				"Project": {
					"skills": [],
					"rating": [0, 5],
					"payment": [10, 100]
				},
				"Contest": {
					"skills": [],
					"rating": [0, 5],
					"payment": [10, 100],
				}
			}
			self.save_data(file, d=data)
			return data

	def save_data(self, file, d="!"):
		if d != "!":
			data = d
		else:
			data = self.data

		with open(file, "w", encoding="utf-8") as f:
			f.write(dumps(data, indent=4))

	def login(self):
		self.driver.get("https://www.freelancer.com/login")
		self.driver.find_element_by_xpath("/html/body/app-root/app-logged-out-shell/app-login-page/fl-container/fl-bit/app-login/app-credentials-form/form/fl-input[1]/fl-bit/fl-bit/input").send_keys(self.data["user"])
		self.driver.find_element_by_xpath("/html/body/app-root/app-logged-out-shell/app-login-page/fl-container/fl-bit/app-login/app-credentials-form/form/fl-input[2]/fl-bit/fl-bit/input").send_keys(self.data["password"])
		self.driver.find_element_by_xpath("/html/body/app-root/app-logged-out-shell/app-login-page/fl-container/fl-bit/app-login/app-credentials-form/form/app-login-signup-button/fl-button/button").click()
		