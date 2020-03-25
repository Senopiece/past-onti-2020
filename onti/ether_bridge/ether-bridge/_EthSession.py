from web3 import Web3, HTTPProvider, WebsocketProvider, IPCProvider
from ether_bridge._EthAccountBridge import EthAccountBridge

class EthSession:
    web3 = None

    # TODO: больше функционала!!!

    def __init__(self, provider_url):
        if provider_url.startswith('http'):
            self.web3 = Web3(HTTPProvider(provider_url))
        elif provider_url.startswith('ws'):
            self.web3 = Web3(WebsocketProvider(provider_url))
        elif provider_url.endswith('ipc'):
            self.web3 = Web3(IPCProvider(provider_url))
        else:
            raise RuntimeError('Undefined protocol')

    def Account(self, priv_key):
        return EthAccountBridge(self.web3, priv_key)

    def get_balance(self, addr):
        return self.web3.eth.getBalance(addr)

    def get_tx(self, hash):
        return self.web3.eth.getTransaction(hash)

    def get_tx_count(self, addr):
        return self.web3.eth.getTransactionCount(addr)
