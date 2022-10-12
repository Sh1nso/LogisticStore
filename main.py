from abc import ABC, abstractmethod


class Storage(ABC):
    items: dict
    capacity: int

    @abstractmethod
    def add(self, title, amount):
        pass

    @abstractmethod
    def remove(self, title, amount):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self, capacity=100):
        self.items: dict[str:int] = dict()
        self.capacity: int = capacity

    def add(self, title: str, amount: int):
        if self.get_free_space() > amount:
            self.items[title] = self.items.get(title, 0) + amount
        else:
            self.items[title] = self.items[title] + self.get_free_space()

    def remove(self, title, amount):
        if self.items.get(title, 0) - amount > 0:
            self.items[title] -= amount
            return True
        return False

    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items)


class Shop(Storage):
    def __init__(self, capacity=20):
        self.items: dict[str:int] = dict()
        self.capacity: int = capacity

    def add(self, title, amount):
        if self.get_free_space() >= amount or self.get_unique_items_count() < 5:
            self.items[title] = self.items.get(title, 0) + amount
            return True
        elif self.get_free_space() == 0:
            pass
        else:
            self.items[title] += self.get_free_space()

    def remove(self, title, amount):
        if self.items[title] - amount > 0:
            self.items[title] -= amount
            return True
        return False

    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items)


class Request:
    from_come: str
    to = None
    amount: int
    product: str

    def __init__(self, user_str: str, items=None):
        user_input = user_str.lower()
        if user_input.split()[0] == "курьер":
            self.from_come = user_input.split()[5]
            self.amount = int(user_input.split()[2])
            self.product = user_input.split()[3]
        if user_input.split()[0] == "доставить":
            self.from_come = user_input.split()[4]
            self.to = user_input.split()[6]
            self.amount = int(user_input.split()[1])
            self.product = user_input.split()[2]
        self.items = items


def main():
    store = Store()
    store.add('бананы', 20)
    store.add('люди', 10)
    store.add('коты', 15)

    shop = Shop()
    shop.add('бананы', 7)
    shop.add('коты', 10)

    user_input = input('Укажите путь доставки \n')

    user_req = Request(user_input)
    if user_req.to is not None:
        if store.remove(user_req.product, user_req.amount) and shop.add(user_req.product, user_req.amount):
            print(f"Нужное количество есть на {user_req.from_come}\n"
                  f"Курьер забрал {user_req.amount} {user_req.product} со {user_req.from_come}\n"
                  f"Курьер везет {user_req.amount} {user_req.product} со {user_req.from_come} в {user_req.to}\n"
                  f"Курьер доставил {user_req.amount} {user_req.product} в {user_req.to}\n"
                  f"*****\n"
                  f"На складе храниться {store.get_unique_items_count()} товаров\n")
            for item in store.get_items().items():
                print(*item)
            print(f"*****\n"
                  f"В магазине храниться {shop.get_unique_items_count()} товаров\n")
            for item in shop.get_items().items():
                print(*item)


if __name__ == "__main__":
    main()
