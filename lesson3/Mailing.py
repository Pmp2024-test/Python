from Address import Address


class Mailing:
    def __init__(self, track:str, from_address: Address, to_address: Address, cost:float):
        self.track = track
        self.from_address = from_address
        self.to_address = to_address
        self.cost = cost
        

    def __str__(self):
        return f"Отправление {self.track} из {self.from_address} в {self.to_address}."
        f"Стоимость {self.cost} рублей."