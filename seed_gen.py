import os
import hashlib
#import wallet_ui

class seed:
	
	info = ""
	def __init__(self, gen_info):
		self.info = gen_info

	def hash_message(self, message):
		return str(int(hashlib.sha1(message).hexdigest(), 16)%(10**47))

	def gen_seed_ledger(self, seed_address):
		file_ledger = open("seed_ledger//public.ledger", "a+")
		file_ledger.write(self.hash_message((self.info+seed_address).encode('utf-8'))+'\n')
		file_ledger.close()
		return


def file_exists():
	flag = False
	count = 0
	for file in os.listdir("output//wallet_ui//wallet_back"):
		if(file.endswith('.store')):
			flag = True
			break
		else:
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






def get_test_info():
	test_info = ""
	file_count = 0
	try:
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
		print("Error")
	else:
		file_ledger = open("seed_ledger//public.ledger", "r")
		ledger_records = file_ledger.readlines()
		file_ledger.close()
		if(ledger_records == ''):
			pass
		else:
			#print(type(ledger_records))
			test_info = ledger_records[len(ledger_records)-1]
	return test_info

#print(test_info, len(test_info))

def run_seed_gen(option_user, wallet_address):
	#option_user = input("Enter your option(mining/transaction): ")
	total_seed = 0
	challenge_list = [False, False, False]
	test_info = get_test_info()
	#mining part
	if(option_user == "mining"):
		file_store = open("output//wallet_ui//wallet_back//wallet.key",'r')
		wallet_address_real = file_store.read()
		file_store.close()

		#wallet_address = input("Enter wallet address: ")

		challenge_list = [challenge_ten_nums(wallet_address), challenge_s_in_middle(wallet_address), challenge_sum_nums_prime(wallet_address)]
		if(challenge_list[0] == True and challenge_list[1] == True and challenge_list[2] == True):
			print("Valid address!")
			if(wallet_address_real == wallet_address):
				#print(True)
				if(file_exists() == True):
					seed_store = open("output//wallet_ui//wallet_back//seed_store.store",'r')
					value = seed_store.read()
					total_seed = float(value)
					seed_store.close()
				test_info = test_info + "cpu -->"+wallet_address
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
				print(False)
		else:
			print("Invalid address!")