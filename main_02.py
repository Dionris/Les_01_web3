# для второй части импортируем
from decimal import Decimal

'''
Token:
    address
    balance
'''

tokens_dict = {
    'ETH': {
        'address': '0x0000000000000000000000000000',
        'balance': 100000000000000
    },
    'USDC': {
        'address': '0xdE57E424baebCbE9e29873F1d89C68750D33b5E8',
        'balance': 100000
    }
}

# смотрим баланс через дикт
print(tokens_dict['ETH']['balance'])


# Перепишим в класс чтобы было удобнее
class Token:
    def __init__(self, name: str, address: str, balance: int):
        name = name.upper()
        self.name = name
        self.address = address
        self.balance = balance

    # для - print(Tokens.ETH)
    def __str__(self):
        return f'name: {self.name} | address: {self.address} | balance: {self.balance}'

    # def __repr__(self):
    #     return f'Token(name= "{self.name}", address= "{self.address}", balance= {self.balance})'


class Tokens:
    ETH = Token(name='ETH', address='0x0000000000000000000000000000', balance='100000000000000')
    USDC = Token(name='USDC', address='0xdE57E424baebCbE9e29873F1d89C68750D33b5E8', balance='100000')


print(Tokens.USDC.balance)  # так проще

# можно еще так
print(Tokens.ETH)

print('part 2')


# 2 часть импортируем Decimal в самом начале кода
# для работы с числами
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


eth_balance = TokenAmount(  # можно deimals и wei не указывать, так как они указаны в коде
    amount=10,
    decimals=18,
    wei=False
)

# чек баланса
print(eth_balance)
print(eth_balance.Ether)
print(eth_balance.Wei)

# если wei=True (ETH в wei)
balance = TokenAmount(
    amount=12452453,
    decimals=6,
    wei=True
)
print(balance.Ether)
print(balance.Wei)

# 3 вариант если даем инфу в долларах то получаем в ETH
balance_dollars = TokenAmount(
    amount=0.1,
    decimals=6,
    wei=False
)

print(balance_dollars.Ether)
print(balance_dollars.Wei)
