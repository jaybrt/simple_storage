from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as f:
    simple_storage_file = f.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.6.0",
    )

with open("compiled_code.json", "w") as f:
    json.dump(compiled_sol, f)

#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/09ab9d53f1254bada930ec5e674fd144"))
chainid = 4
my_address = "0xcd665ac920702948461f20be1D4dfCB98d69e168"
private_key = os.getenv("PRIVATE_KEY")

#create contract with web3
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

#get nonce
nonce = w3.eth.getTransactionCount(my_address)

#build transaction
transaction = SimpleStorage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price, "chainId": chainid, "from": my_address, "nonce": nonce})

#sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#send signed txn
print('Deploying contract...')
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

#get contract address and abi in order to work with it
simple_storage = w3.eth.contract(address = txn_receipt.contractAddress, abi=abi)

print(simple_storage.functions.retrieve().call())

#send a transaciton to store a number in the contract

store_txn = simple_storage.functions.store(3).buildTransaction({
    "gasPrice": w3.eth.gas_price, "chainId": chainid, "from": my_address, "nonce": nonce+1
})
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key=private_key)
print('Sending favorite number...')
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)
print('Stored number:')
print(simple_storage.functions.retrieve().call())