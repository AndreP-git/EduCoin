"""This is going to be your wallet. Here you can do several things:
- Generate a new address (public and private key). You are going
to use this address (public key) to send or receive any transactions. You can
have as many addresses as you wish, but keep in mind that if you
lose its credential data, you will not be able to retrieve it.

- Send coins to another address
- Retrieve the entire blockchain and check your balance

If this is your first time using this script don't forget to generate
a new address and edit miner config file with it (only if you are
going to mine).

Timestamp in hashed message. When you send your transaction it will be received
by several nodes. If any node mine a block, your transaction will get added to the
blockchain but other nodes still will have it pending. If any node see that your
transaction with same timestamp was added, they should remove it from the
node_pending_transactions list to avoid it get processed more than 1 time.
"""

import requests
import time
import base64
import ecdsa
import json
import tkinter as tk
import sys, os

class Wallet(tk.Frame):

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        
    def create_widgets(self):
        
        self.title = tk.Label(self.master, text="=============================\n" + 
          "Welcome to EduCoin!\n" + 
          f"Currently running: {os.path.basename(sys.argv[0])}\n" + 
          "=============================\n" +
          "Select action:\n")
        self.title["font"] = ("Arial", 24, "bold")
        self.title.pack(pady=10) 
              
        self.generate_button = tk.Button(self.master)
        self.generate_button["text"] = "Generate new wallet"
        self.generate_button["command"] = self.generate_new_wallet
        self.generate_button.pack(pady=10)
        
        self.transfer_button = tk.Button(self.master)
        self.transfer_button["text"] = "Transfer coins"
        self.transfer_button["command"] = self.transfer_coins
        self.transfer_button.pack(pady=10)
        
        self.check_button = tk.Button(self.master)
        self.check_button["text"] = "Check transactions"
        self.check_button["command"] = self.check_transactions
        self.check_button.pack(pady=10)
        
        # self.generate_new_wallet = tk.Entry(self)
        # self.transfer_coins = tk.Entry(self)
        # self.check_transactions = tk.Entry(self)        
    
    def generate_new_wallet(self):
        
        # Generate new window
        self.generate_window = tk.Toplevel(self.master)
        self.generate_window.title("Generate new wallet")
        self.generate_window.geometry("700x500") 
        
        # Disclaimer label    
        self.title = tk.Label(self.generate_window, text="IMPORTANT: save this credentials or you won't be able to recover your wallet\n")
        self.title["font"] = ("Arial", 12, "bold")
        self.title.pack(pady=10)
        
        # Filename entry
        self.filename_text = tk.Label(self.generate_window, text="Write the name of your new address:").pack(pady=10)
        self.filename_entry = tk.Entry(self.generate_window, width=100).pack(pady=10)
        self.filename_button = tk.Button(self.generate_window,
                                         text="Generate",
                                         command=self.generate_ECDSA_keys).pack(pady=10)
        #self.filename_button.bind("ButtonRelease", self.generate_ECDSA_keys)
    
    def transfer_coins(self):
        pass
    
    def check_transactions(self):
        pass
    
    def wallet(self):
        
        response = None
        while response not in ["1", "2", "3", "4"]:
            response = input("""What do you want to do?
            1. Generate new wallet
            2. Transfer coins
            3. Check transactions
            4. Quit\n""")
        if response == "1":
            # Generate new wallet
            print("""=========================================\n
    IMPORTANT: save this credentials or you won't be able to recover your wallet\n
    =========================================\n""")
            self.generate_ECDSA_keys()
        elif response == "2":
            addr_from = input("From: introduce your wallet address (public key)\n")
            private_key = input("Introduce your private key\n")
            addr_to = input("To: introduce destination wallet address\n")
            amount = input("Amount: number stating how much do you want to send\n")
            print("=========================================\n\n")
            print("Is everything correct?\n")
            print(F"From: {addr_from}\nPrivate Key: {private_key}\nTo: {addr_to}\nAmount: {amount}\n")
            response = input("y/n\n")
            if response.lower() == "y":
                self.send_transaction(addr_from, private_key, addr_to, amount)
            elif response.lower() == "n":
                return wallet()  # return to main menu
        elif response == "3":  # Will always occur when response == 3.
            self.check_transactions()
            return wallet()  # return to main menu
        else:
            quit()


    def send_transaction(self, addr_from, private_key, addr_to, amount):
        """Sends your transaction to different nodes. Once any of the nodes manage
        to mine a block, your transaction will be added to the blockchain. Despite
        that, there is a low chance your transaction gets canceled due to other nodes
        having a longer chain. So make sure your transaction is deep into the chain
        before claiming it as approved!
        """
        # For fast debugging REMOVE LATER
        # private_key="181f2448fa4636315032e15bb9cbc3053e10ed062ab0b2680a37cd8cb51f53f2"
        # amount="3000"
        # addr_from="SD5IZAuFixM3PTmkm5ShvLm1tbDNOmVlG7tg6F5r7VHxPNWkNKbzZfa+JdKmfBAIhWs9UKnQLOOL1U+R3WxcsQ=="
        # addr_to="SD5IZAuFixM3PTmkm5ShvLm1tbDNOmVlG7tg6F5r7VHxPNWkNKbzZfa+JdKmfBAIhWs9UKnQLOOL1U+R3WxcsQ=="

        if len(private_key) == 64:
            signature, message = self.sign_ECDSA_msg(private_key)
            url = 'http://localhost:5000/txion'
            payload = {"from": addr_from,
                    "to": addr_to,
                    "amount": amount,
                    "signature": signature.decode(),
                    "message": message}
            headers = {"Content-Type": "application/json"}

            res = requests.post(url, json=payload, headers=headers)
            print(res.text)
        else:
            print("Wrong address or key length! Verify and try again.")


    def check_transactions():
        """Retrieve the entire blockchain. With this you can check your
        wallets balance. If the blockchain is to long, it may take some time to load.
        """
        try:
            res = requests.get('http://localhost:5000/blocks')
            parsed = json.loads(res.text)
            print(json.dumps(parsed, indent=4, sort_keys=True))
        except requests.ConnectionError:
            print('Connection error. Make sure that you have run miner.py in another terminal.')


    def generate_ECDSA_keys(self, event):
        """This function takes care of creating your private and public (your address) keys.
        It's very important you don't lose any of them or those wallets will be lost
        forever. If someone else get access to your private key, you risk losing your coins.

        private_key: str
        public_ley: base64 (to make it shorter)
        """
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)  # this is your sign (private key)
        private_key = sk.to_string().hex()  # convert your private key to hex
        vk = sk.get_verifying_key()  # this is your verification key (public key)
        public_key = vk.to_string().hex()
        # we are going to encode the public key to make it shorter
        public_key = base64.b64encode(bytes.fromhex(public_key))

        filename = "wallet_" + str(time.time()) + ".txt"
        filename = self.filename_entry.get()
        
        #filename = input("Write the name of your new address: ") + ".txt"
        with open(filename, "w") as f:
            f.write(F"Private key: {private_key}\nWallet address / Public key: {public_key.decode()}")
        #print(F"Your new address and private key are now in the file {filename}")
        self.confirm_label = tk.Label(self.generate_window, text="Your new address and private key are now in the file:" + filename).pack(pady=10)

    def sign_ECDSA_msg(private_key):
        """Sign the message to be sent
        private_key: must be hex

        return
        signature: base64 (to make it shorter)
        message: str
        """
        # Get timestamp, round it, make it into a string and encode it to bytes
        message = str(round(time.time()))
        bmessage = message.encode()
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        signature = base64.b64encode(sk.sign(bmessage))
        return signature, message


if __name__ == '__main__':
    print("=============================\n" + 
          "Welcome to EduCoin!\n" + 
          f"Currently running: {os.path.basename(sys.argv[0])}\n" + 
          "=============================\n")
    
    root = tk.Tk()
    root.title("EduCoin")
    root.geometry("700x500")
    wallet = Wallet(master=root)
    wallet.mainloop()
    
    #input("Press ENTER to exit...")
