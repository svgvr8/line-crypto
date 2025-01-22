"""
Wallet handler for LINE Bot integration
"""
import os
import logging
from typing import Optional, Dict
from eth_account import Account
import secrets

logger = logging.getLogger(__name__)

class WalletHandler:
    def __init__(self):
        # In production, this should use a secure database
        self.wallets = {}

    def create_wallet(self, user_id: str) -> Dict:
        """Create a new Ethereum wallet"""
        try:
            if user_id in self.wallets:
                return {
                    "status": "error",
                    "message": "Wallet already exists for this user"
                }

            # Generate a new private key
            private_key = "0x" + secrets.token_hex(32)
            account = Account.from_key(private_key)

            # Store wallet info (in production, use secure database)
            self.wallets[user_id] = {
                "address": account.address,
                "private_key": private_key
            }

            return {
                "status": "success",
                "address": account.address,
                "private_key": private_key
            }
        except Exception as e:
            logger.error(f"Error creating wallet: {str(e)}")
            return {
                "status": "error",
                "message": "Failed to create wallet"
            }

    def get_wallet(self, user_id: str) -> Optional[Dict]:
        """Get wallet information"""
        try:
            wallet = self.wallets.get(user_id)
            if wallet:
                return {
                    "status": "success",
                    "address": wallet["address"]
                }
            return None
        except Exception as e:
            logger.error(f"Error getting wallet info: {str(e)}")
            return None