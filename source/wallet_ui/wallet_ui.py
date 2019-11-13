import kivy
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.lang import Builder
import random, os
import pyperclip
import base64


Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', False)
Config.write()


class Root(FloatLayout):
	pass

class wallet_ui(App):

	address_text = ""

	def build(self):
		kv_builder = Builder.load_string("""
Root:
	Label:
		text: "Amount:"
		x: -70 
		y: 115

	TextInput:
		id: amount
		x: 225
		y: 250
		size_hint: 0.3, 0.10
		multiline: False
		disabled: True
		text: app.gen_value(amount)

	Label:
		text: "Address:"
		x: -205
		y: 44

	TextInput:
		id: cypPrivate
		x: 75
		y: 180
		size_hint: 0.85, 0.10
		multiline: False
		disabled: True
		text: app.gen_address(cypPrivate)
		readonly: True
		allow_copy: True
		copydata: self.text

	""")
		return kv_builder

	def store_alphanum(self, alph_text):
		store_file = open("wallet_back//wallet.key",'w')
		store_file.write(alph_text)
		store_file.close()
		return

	def receive_alphanum(self):
		store_file = open("wallet_back//wallet.key",'r')
		content = store_file.read()
		store_file.close()
		return content


	def file_exists(self):
		flag = False
		count = 0
		for file in os.listdir("wallet_back"):
			if(file.endswith('.key')):
				flag = True
				break
			else:
				count += 1
				if(count == 3):
					break
		return flag


	def challenge_generic_address(self):
		random_alphanum = ""
		while(True):
			if(len(random_alphanum) == 48):
				break
			ascii_num = random.randint(48,122)
			if(ascii_num>=58 and ascii_num<=96):
				pass
			else:
				random_alphanum += chr(ascii_num)
		return random_alphanum


	def challenge_ten_nums(self, wallet_address):
		count = 0
		decision = False
		for index in wallet_address:
			if(ord(index)>=48 and ord(index)<=57):
				count += 1
		if(count == 15):
			decision = True
		return decision


	def challenge_s_in_middle(self, wallet_address):
		rec_point = int(len(wallet_address)/2)
		decision = False
		if(wallet_address[rec_point] == 's'):
			decision = True
		return decision


	def challenge_sum_nums_prime(self, wallet_address):
		decision = False
		prime_total = 0
		div_flag = 0
		count = 0
		for index in wallet_address:
			if(ord(index)>=48 and ord(index)<=57):
				prime_total += int(index)
		for index in range(1,prime_total):
			if(prime_total%index == 0):
				count += 1
		if(count == 2):
			decision = True

		return decision
		

	def get_orig_msg(self, test_info):
		test_info_enc = str.encode(test_info)
		test_info_byte = base64.b64decode(test_info_enc)
		test_info_str = test_info_byte.decode()
		return test_info_str

	def gen_address(self, cypPrivate):
		random_alphanum = ""
		challenge_list = [False,False,False]
		try:
			os.mkdir("wallet_back")
		except Exception as e:
			#print("Already exists")
			pass
		#print(self.file_exists())
		if(self.file_exists() == True):
			#print("Here's True")
			random_alphanum = self.receive_alphanum()
		else:
			#print("Here's break")
			while(True):
				random_alphanum = self.challenge_generic_address()
				challenge_list[0] = self.challenge_ten_nums(random_alphanum)
				challenge_list[1] = self.challenge_s_in_middle(random_alphanum)
				challenge_list[2] = self.challenge_sum_nums_prime(random_alphanum)
				if(challenge_list[0] == True and challenge_list[1] == True and challenge_list[2] == True):
					break


			self.store_alphanum(random_alphanum)
			random_alphanum = self.receive_alphanum()
		cypPrivate.disabled = False
		return random_alphanum

	def gen_value(self, amount):
		seed_val = "0.0000000"
		try:
			os.chdir("..")
			path = os.getcwd()
			#print(path)
			seed_store = open(path+"//public_ledger//public.ledger",'r')
			value = seed_store.readlines()
			#total_seed = float(value)
			value_last = value[len(value)-1]
			last_val = self.get_orig_msg(value_last)
			#print(last_val)
			#last_val = get_orig_msg(last_val)
			#first_part = last_val[0:last_val.index('|')]
			total_seed = last_val[last_val.index('@')+1:last_val.index('|')]
			seed_val = total_seed
			seed_store.close()
		except Exception as e:
			print("Create seeds!")
		return seed_val

	
wallet_ui().run()