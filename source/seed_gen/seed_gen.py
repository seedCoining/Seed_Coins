import os
import hashlib
import base64
import datetime
from datetime import date
import time
#import wallet_ui

class seed:
	
	info = ""
	def __init__(self, gen_info):
		self.info = gen_info

	def hash_message(self, message):
		return str(int(hashlib.sha1(message).hexdigest(), 16)%(10**47))

	def encode_info(self, seed_info):
		bytes_formed = str.encode(seed_info)
		msg_encoded = base64.b64encode(bytes_formed)
		msg_encoded_dec = msg_encoded.decode()
		#return str(msg_encoded)
		return msg_encoded_dec

	def gen_seed_ledger(self, seed_info, path):
		file_ledger = open(path+"//public_ledger//public.ledger", "a+")
		encoded_record = self.encode_info(seed_info)
		file_ledger.write(encoded_record+'\n')
		#file_ledger.write(self.hash_message((self.info+seed_address).encode('utf-8'))+'\n')
		file_ledger.close()
		return


def file_exists(path):
	flag = False
	count = 0
	try:
		#os.chdir("..")
		os.mkdir("public_ledger")
	except:
		pass
	#path = os.getcwd()
	for file in os.listdir(path+"//public_ledger"):
		if(file.endswith('.ledger')):
			flag = True
			#print("Here2")
			break
		else:
			#print("Here3")
			count += 1
			if(count == 1):
				break
	return flag


def challenge_ten_nums(wallet_address):
	count = 0
	decision = False
	for index in wallet_address:
		if(ord(index)>=48 and ord(index)<=57):
			count += 1
	if(count == 15):
		decision = True
	return decision


def challenge_s_in_middle(wallet_address):
	rec_point = int(len(wallet_address)/2)
	decision = False
	if(wallet_address[rec_point] == 's'):
		decision = True
	return decision


def challenge_sum_nums_prime(wallet_address):
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


def get_orig_msg(test_info):
	test_info_enc = str.encode(test_info)
	test_info_byte = base64.b64decode(test_info_enc)
	test_info_str = test_info_byte.decode()
	return test_info_str

def get_test_info(path):
	test_info = ""
	#file_count = 0
	'''try:
		os.mkdir("seed_ledger")
	except:
		pass
	for file in os.listdir("seed_ledger"):
		if(file.endswith(".ledger")):
			file_count += 1
		if(file_count > 1):
			break
	if(file_count == 0):
		pass
	elif(file_count>1):
		print("Error")'''
	if(file_exists(path) == False):
		test_info = "Genesis"
		#print("here")
	else:
		file_ledger = open("public_ledger//public.ledger", "r")
		ledger_records = file_ledger.readlines()
		file_ledger.close()
		'''if(ledger_records == ''):
			pass
		else:'''
			#print(type(ledger_records))
		test_info = ledger_records[len(ledger_records)-1]
		test_info = get_orig_msg(test_info)
		#print(test_info)
		test_info = test_info[0:test_info.index(':')]
		#print(test_info)
	return test_info

#print(test_info, len(test_info))

def run_seed_gen(option_user, wallet_address, path):
	#option_user = input("Enter your option(mining/transaction): ")
	total_seed = 0
	challenge_list = [False, False, False]
	#os.chdir("..")
	#path = os.getcwd()
	test_info = get_test_info(path) 
	#mining part
	if(option_user == "mining"):
		'''try:
			os.chdir("..")
			#os.mkdir(wallet_back)
		except:
			pass'''
		#path = os.getcwd()
		file_store = open(path+"//wallet_ui//wallet_back//wallet.key",'r')
		wallet_address_real = file_store.read()
		file_store.close()

		#wallet_address = input("Enter wallet address: ")

		challenge_list = [challenge_ten_nums(wallet_address), challenge_s_in_middle(wallet_address), challenge_sum_nums_prime(wallet_address)]
		if(challenge_list[0] == True and challenge_list[1] == True and challenge_list[2] == True):
			#print("Valid address! "+ wallet_address)

			if(wallet_address_real == wallet_address):
				#print(True)
				if(file_exists(path) == True):
					#print(True)
					public_ledger = open(path+"//public_ledger//public.ledger",'r')
					value = public_ledger.readlines()
					value_len = len(value)
					last_val = value[value_len-1]
					#total_seed = float(value)
					#print(last_val)
					last_val = get_orig_msg(last_val)
					#first_part = last_val[0:last_val.index('|')]
					total_seed = float(last_val[last_val.index('@')+1:last_val.index('|')])
					#print(last_val[last_val.index('@'):len(last_val)])
					total_seed += 1.0000000/value_len
					formatted_total = '{:.7f}'.format(total_seed)
					public_ledger.close()
					test_info_final = test_info+"@"+formatted_total+"|-->"+wallet_address
					#now = datetime.now()
					#date_str = now.strftime("%d/%m/%Y %H:%M:%S")
					#print("Information created ", date_str)
					new_seed = seed(test_info_final)
					new_seed.gen_seed_ledger(str(new_seed)+":"+test_info_final, path)
					print("Block created")
				else:
					#public_ledger = open("public_ledger",'a+')
					#print(False)
					formatted_total = '{:.7f}'.format(total_seed)
					test_info_final = test_info+"@"+formatted_total+"|-->"+wallet_address
					new_seed = seed(test_info_final)
					new_seed.gen_seed_ledger(str(new_seed)+":"+test_info_final, path)
					print("Block created Gen")


				'''test_info = test_info + "cpu -->"+wallet_address
				new_seed = seed(test_info)
				new_seed.gen_seed_ledger(str(new_seed))
				#wallet_ui.wallet_ui().run()
				seed_store = open("output//wallet_ui//wallet_back//seed_store.store",'w')
				
				file_ledger = open("seed_ledger//public.ledger", "r")
				block_list = file_ledger.readlines()
				file_ledger.close()

				#for index in block_list:
				#	print(index)
				total_seed = total_seed + 1.0000000/len(block_list)
				formatted_total = '{:.7f}'.format(total_seed)
				seed_store.write(str(formatted_total))
				seed_store.close()

				#print(str(new_seed))

			else:
				print("Not a local address! "+wallet_address)
		else:
			print("Invalid address!")'''


option_user = input("Enter your option(mining/transaction): ")
wallet_address = input("Enter wallet address: ")
flag = 0
while(True):
	time.sleep(10)
	if(flag!=1):
		os.chdir("..")
		path = os.getcwd()
		flag = 1
	run_seed_gen(option_user, wallet_address, path)
#1gazrzan6e34tk6v0wllzdy2snxkcq1j02obc83me6qhd52s