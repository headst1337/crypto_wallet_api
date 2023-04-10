import binascii

from typing import Any, Dict

from web3 import Web3
from bip_utils import Bip44, Bip44Changes, Bip44Coins
from erc20_abi import ERC20_ABI


class Account:
    
    @staticmethod
    def get_wallet_data(seed: str = None, private_key: str = None) -> dict[str, str]:
        if private_key: 
            private_key = binascii.unhexlify(private_key)
            bip32_ctx = Bip44.FromPrivateKey(private_key, Bip44Coins.ETHEREUM)
            return {"account_private_key": bip32_ctx.PrivateKey().Raw().ToHex(),
                    "account_public_key": bip32_ctx.PublicKey().RawCompressed().ToHex(),
                    "address": bip32_ctx.PublicKey().ToAddress()}
        
        bip44_mst_ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
        public_master_key = bip44_mst_ctx.PublicKey().ToExtended()
        private_master_key = bip44_mst_ctx.PrivateKey().Raw().ToHex()
        bip44_coin_ctx = bip44_mst_ctx.Purpose().Coin()
        bip44_addr_ctx = bip44_coin_ctx.Account(0).Change(
            Bip44Changes.CHAIN_EXT).AddressIndex(0)
        account_public_key = bip44_addr_ctx.PublicKey().RawCompressed().ToHex()
        account_private_key = bip44_addr_ctx.PrivateKey().Raw().ToHex()
        address = bip44_addr_ctx.PublicKey().ToAddress()
        return {"public_master_key": public_master_key,
                "private_master_key": private_master_key,
                "account_public_key": account_public_key,
                "account_private_key": account_private_key,
                "address": address}
    
    @staticmethod
    def get_balance(rpc: str, address: str) -> Dict[str, Any]:
        web3 = Web3(Web3.HTTPProvider(rpc))
        return {"balance": Web3.fromWei(web3.eth.get_balance(address), 'ether')}
    
    @staticmethod
    def get_token_balance(rpc: str, address: str, contract_address: str) -> Dict[str, Any]:
        web3 = Web3(Web3.HTTPProvider(rpc))
        contract = web3.eth.contract(contract_address, abi=ERC20_ABI)
        balance = contract.functions.balanceOf(address).call()
        return {"balance" : Web3.fromWei(balance, 'ether')}