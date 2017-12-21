import random

BRANDS = ["OM", "CocaCola", "Sprite", "Dorna", "Sprite"]
CAPACITY = [0.5, 1, 1.5, 2, 5, 6]
DESTINATION = ["Chisina", "Cahul", "Cojusna", "Balti", "Tiraspol", "Cernauti"]
PRICE = [6, 8, 10, 13, 15, 20, 24]




bottle = {
    "id" : 12,
    "brand": "OM",
    "capacity": 1.5,
    "destitation": "Cahul",
    "price": 10,
}


class RandomDataGenerator:
    def __init__(self):
        self._amount = self.__generateRandomAmount()
        self.index_array = random.sample(range(1, 1000), self._amount)

    def __generateRandomAmount(self):
        return random.randint(3, 7)

    def __generateRandomBottle(self, index):
        _id = self.index_array[index]
        index_brand = random.randint(0, 4)
        brand = BRANDS[index_brand]
        index_capacity = random.randint(0, 5)
        capacity = CAPACITY[index_capacity]
        index_destination = random.randint(0, 5)
        destination = DESTINATION[index_destination]
        price = PRICE[index_capacity]
        # print(_id, brand, capacity, destination, price)
        return {
            "_id": _id,
            "brand": brand,
            "capacity": capacity,
            "destitation": destination,
            "price": price,
        }

    def get_data(self):
        bottles = []
        for index in range(0, self._amount):
            new_bottle = self.__generateRandomBottle(index)
            bottles.append(new_bottle)
        return bottles


