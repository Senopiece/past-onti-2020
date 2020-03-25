class EthContractBridge:
    user_account = None

    def __init__(self, ABI, contract_addr, user_account=None):
        """
        Мост к уже существующему контракту. (Для деплоя см EthAccountBridge.deploy_contract())

        Методы автоматически определяются как call или buildTransaction из ABI
        > методы определенные как call возвращают результат функции
        > методы определенные как bT возвращают рецепт отправленной транзакции,
          затем результат исполнения метода

        Обращение к эвентам через contract.events как в документации из web3,
        подробнее - https://web3py.readthedocs.io/en/stable/contracts.html#web3.contract.ContractEvents


        Args:
            ABI (dict): преобразованный в dict ABI контракта или путь к жсон файлу
            contract_addr (str): адресс контракта
            user_account (EthAccountBridge): аккаунт,
                который будет оплачивать выполнение bT функций, но и call функции проводятся от его имени

        Note:
            > Тк методы контракта вызываются напрямую из атрибутов класса,
               не переопределяйте заготовленные атрибуты типо:
               user_account, events..., в противном случае будет вызвано исключение

            > В аргументах к bT методам зарезервированно поле value, не называть в функции аргумент value!!!!
               value автомотически использыется как сумма перевода баланса на контракт
        """
        if isinstance(ABI, str):
            if ABI.endswith('.json'):
                ABI = parce_json(ABI)

        if contract == None:
            contract = user_account.w3.eth.contract(ABI=ABI, address=contract_addr)

        # setup events
        self.events = contract.events

        # setup contract methods
        for elem in kwargs['abi']:
            if 'name' in elem:
                # choose call or buildTransaction
                if elem['stateMutability'] == 'view':
                    def funct(name):
                        def func(*args, **kwargs):
                            return getattr(contract.functions, name)(*args, **kwargs).call()
                        return func

                elif elem['stateMutability'] == 'nonpayable' or \
                        elem['stateMutability'] == 'pure' or \
                        elem['stateMutability'] == 'payable':
                    def funct(name):
                        def func(*args, **kwargs, value = 0):
                            result = getattr(contract.functions, name)(*args, **kwargs).call()
                            txr = user_account.send_tx({
                                'to': contract.address,
                                'value': value,
                                'data': contract.encodeABI(fn_name=name, args=args, kwargs=kwargs)
                            })
                            return txr, result
                        return func

                # contract sould not contain some attributes that preinstalled in this class
                if not hasattr(self, elem['name']):
                    setattr(self, elem['name'], funct(elem['name']))
                else:
                    raise AttributeError("Contract sould not contain "+elem['name']+" attribute")
