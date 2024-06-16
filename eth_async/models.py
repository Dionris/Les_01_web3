from decimal import Decimal
from dataclasses import dataclass

from web3 import Web3
import requests

from . import exceptions


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: int | float | str | Decimal, decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = int(amount)
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals

    def __str__(self):  # позволяет всё выводить
        return f'{self.Ether}'


@dataclass  # dataclass автоматичкски добавляет метод repr объектам
class DefaultABIs:
    Token = [
        {
            # constant - меняет структуру блокчейна или не меняет True - read , False - write
            'constant': True,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [],  # что должна принимать
            "name": "name",  # название функции
            "outputs": [{'name': '', 'type': 'string'}],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "view",
            "type": "function"
        },
        {
            'constant': True,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [],  # что должна принимать
            "name": "symbol",  # название функции
            "outputs": [{'name': '', 'type': 'string'}],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "view",
            "type": "function"
        },
        {
            'constant': True,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [],  # что должна принимать
            "name": "totalSupply",  # название функции
            "outputs": [{'name': '', 'type': 'uint256'}],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "view",
            "type": "function"
        },
        {
            'constant': True,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [],  # что должна принимать
            "name": "decimals",  # название функции
            "outputs": [{'name': '', 'type': 'uint256'}],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "view",
            "type": "function"
        },
        {
            'constant': True,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [{'name': 'account ', 'type': 'address'}],  # что должна принимать
            "name": "balanceOf",  # название функции
            "outputs": [{'name': '', 'type': 'uint256'}],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "view",
            "type": "function"
        },
        {
            'constant': True,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [{'name': 'owner ', 'type': 'address'}, {'name': 'spender ', 'type': 'address'}],
            "name": "allowance",  # название функции
            "outputs": [{'name': 'remaining', 'type': 'uint256'}],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "view",
            "type": "function"
        },
        {
            'constant': False,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [{'name': 'spender ', 'type': 'address'}, {'name': 'value ', 'type': 'uint256'}],
            "name": "approve",  # название функции
            "outputs": [],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            'constant': False,  # ее можно убрать она устаревшая костанта а аналог ей "stateMutability":"view"
            'inputs': [{'name': 'to ', 'type': 'address'}, {'name': 'value ', 'type': 'address'}],
            "name": "transfer",  # название функции
            "outputs": [],  # типы параметров
            'payable': False,  # ничкго не платит
            "stateMutability": "nonpayable",
            "type": "function"
        },
    ]


class Network:  # аналог класу Token из main2, сдесь будем указывать инфу о нашей сети
    def __init__(
            self,
            name: str,
            rpc: str,
            chain_id: int | None = None,
            tx_type: int = 0,
            coin_symbol: str | None = None,
            explorer: str | None = None
    ) -> None:
        self.name: str = name.lower()
        self.rpc: str = rpc
        self.chain_id: int | None = chain_id
        self.tx_type: int = tx_type
        self.coin_symbol: str | None = coin_symbol
        self.explorer: str | None = explorer

        if not self.chain_id:
            try:
                self.chain_id = Web3(provider=Web3.HTTPProvider(self.rpc)).eth.chain_id
            except Exception as err:
                raise exceptions.WrongChainID(f'Can not get chain id: {err}')

        if not self.coin_symbol:
            try:
                response = requests.get('https://chainid.network/chsin.json').json()
                for network in response:
                    if network['chainId'] == self.chain_id:
                        self.coin_symbol = network['nativeCurrency']['symbol']
                        break
            except Exception as err:
                raise exceptions.WrongCoinSymbol(f'Can not get coin symbol: {err}')

        if not self.coin_symbol:
            self.coin_symbol = self.coin_symbol.upper()


class Networks:
    # Mainnets
    Etheteum = Network(
        name='ethereum',
        rpc='https://rpc.ankr.com/eth/',
        chain_id=1,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://etherscan.io/',
    )

    Arbitrum = Network(
        name='arbitrum',
        rpc='https://rpc.ankr.com/arbitrum/',
        chain_id=42161,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://arbiscan.io/',
    )

    ArbitrumNova = Network(
        name='Arbitrum_nova',
        rpc='https://nova.arbitrum.io/rpc/',
        chain_id=42170,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://nova.arbiscan.io/',
    )

    Optimism = Network(
        name='optimism',
        rpc='https://rpc.ankr.com/optimism/',
        chain_id=10,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://optimism.etherscan.io/',
    )

    BSC = Network(
        name='bsc',
        rpc='https://rpc.ankr.com/bsc/',
        chain_id=56,
        tx_type=2,
        coin_symbol='BNB',
        explorer='https://bscscan.com/',
    )

    Polygon = Network(
        name='polygon',
        rpc='https://rpc.ankr.com/polygon/',
        chain_id=137,
        tx_type=2,
        coin_symbol='MATIC',
        explorer='https://polyginscan.com/',
    )

    Avalanche = Network(
        name='avalanche',
        rpc='https://rpc.ankr.com/avalanche/',
        chain_id=43114,
        tx_type=2,
        coin_symbol='AVAX',
        explorer='https://showtrace.io/',
    )

    Moonbeam = Network(
        name='moonbeam',
        rpc='https://rpc.api.mooonbeam.network/',
        chain_id=1284,
        tx_type=2,
        coin_symbol='GLMR',
        explorer='https://moonscan.io/',
    )

    # todo: сделать самостоятель
    Fantom = ...

    # todo: сделать самостоятель
    Celo = ...

    # todo: сделать самостоятель
    Gnosis = ...

    # todo: сделать самостоятель
    HECO = ...

    # Testnets
    Goerli = Network(
        name='goerli',
        rpc='https://rpc.ankr.com/eth_goerli/',
        chain_id=5,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://goerli.etherscan.io/',
    )

    # todo: сделать самостоятель
    Sepolia = ...
