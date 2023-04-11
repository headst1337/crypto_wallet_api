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