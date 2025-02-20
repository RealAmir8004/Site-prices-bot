class Price:
    def __init__(self, price: int, badged: bool):
        self.price = price
        self.badged = badged

    

    def price_reduce(self) -> 'Price': # range gheymat jens haro check kon !!!!!!!!!!!!!!!!!!!!!
        mod = self.price % 10_000

        match self.price:
            case price if price <= 50_000 & mod>=6 :  
                reducation = -5_000
            case price if price <= 500_000 :    
                reducation = 0
            case price if price <= 1_000_000:
                reducation = 10_000
            case price if price <= 5_000_000:
                reducation = 20_000
            case price if price <= 10_000_000:
                reducation = 30_000
            case price if price <= 15_000_000:
                reducation = 40_000
            case _:
                reducation = 50_000

        new_price = self.price - (mod + 1) * 1_000 - reducation
        return Price(new_price, self.badged)


    def __lt__(self, other: 'Price') -> bool:
        return self.price < other.price
    


def calc(sparkPrice: int, prices: list[Price]) -> list[Price]:
    prices.sort() # dar vaghe sort nabayad bokonim chon torob sort shode mide 

    suggestion: list[Price] = []

    for price in prices[:4]:
        suggestion.append(price.price_reduce())

    return suggestion



# main
prices = [
    Price(9_000_000, False),
    Price(2_000_000, False),
    Price(3_000_000, False),
    Price(5_000_000, True),
    Price(4_000_000, False),
    Price(13_000_000, False),
    Price(6_000_000, True),
    Price(10_000_000, False),
    Price(8_000_000, True),
    Price(7_000_000, False),
    Price(11_000_000, False),
    Price(12_000_000, True),
    Price(14_000_000, False),
    Price(1_000_000, False),
    Price(15_000_000, False),
]

sparkPrice = 1_000_000
suggestion = calc(sparkPrice, prices)

from colorama import Fore, Back, Style


for i , price in enumerate(prices):
    if price.badged:
        print(Fore.RED + f"Price {i + 1}: {price.price} ")
    else:
        print(Fore.WHITE + f"Price {i + 1}: {price.price} ")
        
print("\n")

for i, price in enumerate(suggestion):
    if price.badged:
        print(Fore.RED + f"suggested Price {i + 1}: {price.price} ")
    else:
        print(Fore.WHITE + f"suggested Price {i + 1}: {price.price} ")


