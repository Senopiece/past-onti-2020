# ether-bridge
 Simple bridge to ethereum (around web3) for fastest coding.


Quik start:
===

### What I can import?
```
from ether_bridge import EthSession
from ether_bridge import tools
from ether_bridge import exceptions
```
Web3 exceptions watch [here](https://github.com/ethereum/web3.py/blob/master/web3/exceptions.py)

### Example:
```
from ether_bridge import EthSession

session = EthSession('https://sokol.poa.network')

acc = session.Account(priv_key)

txr, contract = acc.deploy_contract('contract/abi.json', 'contract/bytecode.json')

print(txr['contractAddress'])

result1 = contract.some_call_method()
txr, result2 = contract.some_bT_method()
```

### Note that transaction receipt follows this structure:
```
{
    'blockHash': '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd',
    'blockNumber': 46147,
    'contractAddress': None,
    'cumulativeGasUsed': 21000,
    'from': '0xA1E4380A3B1f749673E270229993eE55F35663b4',
    'gasUsed': 21000,
    'logs': [],
    'root': '96a8e009d2b88b1483e6941e6812e32263b05683fac202abc622a3e31aed1957',
    'to': '0x5DF9B87991262F6BA471F09758CDE1c0FC1De734',
    'transactionHash': '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060',
    'transactionIndex': 0,
}
```

For more information, just read the docs that are inserted in the code...

Useful links
===

Solitity [docs](https://github.com/ethereum/wiki/wiki/%5BRussian%5D-%D0%A0%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE-%D0%BF%D0%BE-Solidity#cheatsheet)

Web3 contract events [docs](https://web3py.readthedocs.io/en/stable/contracts.html#web3.contract.ContractEvents) 
