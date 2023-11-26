from hexbytes import HexBytes
from web3 import Web3
from eth_account import Account

from erc20_abi import ERC20_ABI


class Transaction:

    @staticmethod
    def send_transaction(rpc: str, address_to: str, amount: float, private_key: str) -> dict[str, str]:
        web3 = Web3(Web3.HTTPProvider(rpc))
        account = Account.from_key(private_key)

        gas_estimate = web3.eth.estimate_gas({
            'to': address_to,
            'value': web3.to_wei(amount, 'ether'), 
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': web3.eth.chain_id
        })

        transaction = {
            'to': address_to,
            'value': web3.to_wei(amount, 'ether'), 
            'gas': gas_estimate,
            'gasPrice':  web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': web3.eth.chain_id
        }
        signed_transaction = account.sign_transaction(transaction)
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
        return {'hash': transaction_receipt['transactionHash'].hex()}
    
    @staticmethod
    def send_token_transaction(
        rpc: str, 
        address_to: str, 
        amount: float, 
        private_key: str, 
        contract_address: str
    ) -> dict[str, str]:
        web3 = Web3(Web3.HTTPProvider(rpc))
        account = Account.from_key(private_key)
        contract = web3.eth.contract(contract_address, abi=ERC20_ABI)

        amount = amount * 10 ** contract.functions.decimals().call()
        data = contract.functions.transfer(address_to, int(amount)).buildTransaction({'from': account.address})
        gas_estimate = contract.functions.transfer(address_to, int(amount)).estimate_gas({'from': account.address})

        transaction = {
            'to': contract_address,
            'gas': gas_estimate,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': web3.eth.chainId,
            'data': data
        }
        signed_transaction = account.sign_transaction(transaction)
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
        return {'hash': transaction_receipt['transactionHash'].hex()}
    
    @staticmethod
    def get_transaction_receipt(rpc: str, transaction_hash: str) -> dict[str, str]:
        web3 = Web3(Web3.HTTPProvider(rpc))
        transaction_receipt_info = web3.eth.get_transaction_receipt(transaction_hash)
        transaction_info = web3.eth.get_transaction(transaction_hash)
        token_logs = transaction_receipt_info.get("logs")
        is_token_transaction = bool(token_logs)
        transaction_receipt = {}
        if is_token_transaction:
            token_contract = token_logs[0].get("address")
            chainId = transaction_info.get("chainId")
            if chainId == 137:
                token_value = transaction_info.get("value")
            else:
                token_value = int.from_bytes(bytes(token_logs[0].get("data")), byteorder='big')
            if chainId != 1: 
                receiver = token_logs[0].get("topics")[2]
            else:
                receiver = token_logs[0].get("topics")[0]
            receiver = "0x" + HexBytes.hex(receiver)[26:74]
            token_contract_str = str(token_contract)
            token_value_str = str(Web3.from_wei(token_value, 'ether'))
            transaction_receipt = {
                "from": transaction_receipt_info.get("from"),
                "to": receiver,
                "gasUsed": transaction_receipt_info.get("gasUsed"),
                "status": transaction_receipt_info.get("status"),
                "value": "null",
                "tokenContract": token_contract_str,
                "tokenValue": token_value_str
            }
        else:
            native_value_str = str(Web3.from_wei(transaction_info.get("value"), 'ether'))
            transaction_receipt = {
                "from": transaction_receipt_info.get("from"),
                "to": transaction_receipt_info.get("to"),
                "gasUsed": transaction_receipt_info.get("gasUsed"),
                "status": transaction_receipt_info.get("status"),
                "value": native_value_str,
                "tokenContract": "null",
                "tokenValue": "null"
            }
        return transaction_receipt
