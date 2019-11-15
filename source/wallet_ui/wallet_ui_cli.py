import random, os
import pyperclip
import base64


def store_alphanum(alph_text):
	store_file = open("wallet_back//wallet.key",'w')
	store_file.write(alph_text)
	store_file.close()
	return

def receive_alphanum():
	store_file = open("wallet_back//wallet.key",'r')
	content = store_file.read()
	store_file.close()
	return content


def file_exists():
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


def challenge_generic_address():
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

def gen_address():
	random_alphanum = ""
	challenge_list = [False,False,False]
	os.chdir('wallet_ui')
	try:
		os.mkdir("wallet_back")
	except Exception as e:
		#print("Already exists")
		pass
	#print(self.file_exists())
	if(file_exists() == True):
		#print("Here's True")
		random_alphanum = receive_alphanum()
	else:
		#print("Here's break")
		while(True):
			random_alphanum = challenge_generic_address()
			challenge_list[0] = challenge_ten_nums(random_alphanum)
			challenge_list[1] = challenge_s_in_middle(random_alphanum)
			challenge_list[2] = challenge_sum_nums_prime(random_alphanum)
			if(challenge_list[0] == True and challenge_list[1] == True and challenge_list[2] == True):
				break


		store_alphanum(random_alphanum)
		random_alphanum = receive_alphanum()
	#cypPrivate.disabled = False
	#return random_alphanum
	print("Address: ", random_alphanum)

def gen_value():
	seed_val = "0.0000000"
	try:
		os.chdir("..")
		path = os.getcwd()
		#print(path)
		seed_store = open(path+"//public_ledger//public.ledger",'r')
		value = seed_store.readlines()
		#total_seed = float(value)
		value_last = value[len(value)-1]
		last_val = get_orig_msg(value_last)
		#print(last_val)
		#last_val = get_orig_msg(last_val)
		#first_part = last_val[0:last_val.index('|')]
		total_seed = last_val[last_val.index('@')+1:last_val.index('|')]
		seed_val = total_seed
		seed_store.close()
	except Exception as e:
		print("Create seeds!")
	#return seed_val
	print("Amount: ", seed_val)

flag = 0
while(True):
	if(flag == 0):
		gen_value()
		gen_address()
		flag = 1

