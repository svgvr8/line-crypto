"""
Wallet handler for EVM-compatible blockchains
"""
from eth_account import Account
import secrets
import json
import os

class WalletHandler:
    def __init__(self):
        self.wallets_dir = "wallets"
        if not os.path.exists(self.wallets_dir):
            os.makedirs(self.wallets_dir)

    def create_wallet(self, user_id):
        """Create a new wallet for a user"""
        # Generate a new private key
        private_key = "0x" + secrets.token_hex(32)
        account = Account.from_key(private_key)
        
        wallet_info = {
            "address": account.address,
            "private_key": private_key,
        }
        
        # Save wallet info (in production, use secure storage)
        wallet_file = os.path.join(self.wallets_dir, f"{user_id}.json")
        with open(wallet_file, "w") as f:
            json.dump(wallet_info, f)
            
        return wallet_info

    def get_wallet(self, user_id):
        """Get wallet information for a user"""
        wallet_file = os.path.join(self.wallets_dir, f"{user_id}.json")
        if os.path.exists(wallet_file):
            with open(wallet_file, "r") as f:
                return json.load(f)
        return None
