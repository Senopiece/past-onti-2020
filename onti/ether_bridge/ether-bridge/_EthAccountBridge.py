from ether_bridge._EthContractBridge import EthContractBridge
from ether_bridge.tools import priv_key_to_address
from web3 import exceptions

class EthAccountBridge:
    w3 = None
    address = None
    priv_key = None
    gas_price = None

    # TODO: добавить больше функций

    def __init__(self, w3, priv_key):
        self.w3 = w3
        self.address = priv_key_to_address(priv_key)
        self.priv_key = priv_key

    def get_tx_count(self):
        return self.w3.eth.getTransactionCount(addr)

    def get_balance(self):
        return self.w3.eth.getBalance(address)

    def send_tx(self, tx):
        """
        Args:
           tx (dict):
             (required) 'value'    (int): сумма перевода
             (required) 'to'       (str): чексумма адреса получателя
             (optional) 'data'   (bytes): дата транзакции, возможно код контракта
             (optional) 'gasPrice' (int): если указано, то используется это значение,
                                          иначе проверяется self.gas_price,
                                          если его не существует, то используется eth.gasPrice
        Return:
           txr (dict): рецепт транзакции
        Note:
           Если на аккаунте не хватит баланса на совершение оплаты, вместо txr будет возвращён None.
        """
        tx['nonce'] = self.w3.eth.getTransactionCount(self.address)
        tx['gas'] = self.w3.eth.estimateGas(tx)
        tx['from'] = self.w3.toChecksumAddress(self.address)

        if not('gasPrice' in tx):
            if self.gas_price == None:
                tx['gasPrice'] = self.w3.eth.gasPrice
            else:
                tx['gasPrice'] = self.gas_price

        try:
            signed = self.w3.eth.account.signTransaction(tx, private_key=self.priv_key)
            tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
            tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            return tx_receipt
        except Exception as ex:
            if str(ex).find('Insufficient funds') != -1:
                return None
            else:
                raise ex

    def deploy_contract(self, ABI, bytecode, *contract_constructor_args, **contract_constructor_kwargs):
        """
        Args:
            ABI (dict/string): преобразованный в dict ABI контракта или путь к жсон файлу
            bytecode (string): скомпилированный байткод контракта в строке или путь к жсон файлу, возьмётся поле object
            И дополнительно можно докинуть аргументы для контруктора контракта.

        Return:
            (tx_receipt, EthContractBridge)
            > tx_receipt - рецепт транзакции в которой задеплоился контракт
            > Экземпляр EthContractBridge, уже подключенный к задеплоеному контракту
        """
        if isinstance(ABI, str):
            if ABI.endswith('.json'):
                ABI = parce_json(ABI)

        if isinstance(byetcode, str):
            if byetcode.endswith('.json'):
                byetcode = parce_json(byetcode)['object']

        tx = self.w3.eth.contract(ABI=ABI, bytecode=bytecode).constructor(*contract_constructor_args, **contract_constructor_kwargs).buildTransaction({
            'gasPrice': gas_price if self.gas_price != None else self.w3.eth.gasPrice,
            'nonce': self.w3.eth.getTransactionCount(self.address)
        })
        tx_receipt = self.send_tx(tx)
        return tx_receipt, EthContractBridge(user_account=self, ABI=ABI, contract_addr=tx_receipt['contractAddress'])

    def Contract(self, ABI, address):
        """
        Args:
            ABI (dict): преобразованный в dict ABI контракта или путь к жсон файлу
            address (string): адресс контракта

        Return:
            contract (EthContractBridge): мост к контракту
        """
        return EthContractBridge(user_account=self, ABI=ABI, contract_addr=address)
