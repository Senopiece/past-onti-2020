from eth_account import Account
from web3 import Web3
from json import load

# TODO: добавить обёртки на другие тулзы

def priv_key_to_address(priv_key):
    prefix = '' if priv_key.startswith('0x') else '0x'
    return Account.privateKeyToAccount(prefix + priv_key).address
# TODO: из публичного ключа в адресс

def to_checksum_address(addr):
    return Web3.toChecksumAddress(addr)

def estimate_gas(tx):
    return Web3.eth.estimateGas(tx)

def to_hex(data):
    return Web3.toHex(data)

def to_wei(val, nominal):
    return Web3.toWei(val, nominal)

def parce_json(file_path):
    with open(file_path) as f:
        content = load(f)
    return content
