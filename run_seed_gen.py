import seed_gen
import time

option_user = input("Enter your option(mining/transaction): ")
wallet_address = input("Enter wallet address: ")

while(True):
	time.sleep(10)
	seed_gen.run_seed_gen(option_user, wallet_address)

#os.system('seed_gen.py option_user wallet_address')