#-*-coding: utf-8-*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from json import loads, dumps
from codecs import open
from time import sleep


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
		self.actions = ActionChains(self.driver)
		self.logged_in = False


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
		cu = self.driver.current_url
		self.driver.find_element_by_xpath("/html/body/app-root/app-logged-out-shell/app-login-page/fl-container/fl-bit/app-login/app-credentials-form/form/app-login-signup-button/fl-button/button").click()
		for i in range(10):
			sleep(1)
			if self.driver.current_url != cu:
				self.logged_in = True
				return 0

		self.logged_in = False


	def search_job(self, ptype="Project", clean_skills = True):
		if ptype == "Project":
			self.driver.get("https://www.freelancer.com/search/projects")
		elif ptype == "Contest":
			self.driver.get("https://www.freelancer.com/search/contests")

		else:
			return -1
		
		self.driver.implicitly_wait(10)
		continue_but = self.driver.find_element_by_xpath("/html/body/div[2]/main/section/fl-search/div/div[2]/div/div[2]/ul/li[9]/a")
		clear = self.driver.find_element_by_xpath("//*[@id='main']/section/fl-search/div/div[1]/form/ol[2]/fl-projects-filter/li/ul/li[2]/div[2]/button")
		if clean_skills:
			self.actions.move_to_element(clear).perform()
			clear.click()
			skill_box = self.driver.find_element_by_xpath("/html/body/div[2]/main/section/fl-search/div/div[1]/form/ol[2]/fl-projects-filter/li/ul/li[2]/div[1]/fl-tag-input/div/input")
			for skill in self.data[ptype]["skills"]:
				skill_box.send_keys(skill)
				skill_box.send_keys(Keys.ENTER)
			print("Skills set")