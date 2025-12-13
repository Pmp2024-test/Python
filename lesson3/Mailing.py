from Address import Address


class Mailing:
    def __init__(self, track: str, from_address: Address, to_address, cost):
        self.track = track
        self.from_address = from_address
        self.to_address = to_address
        self.cost = cost

    def __str__(self):
        return f"Отправление {self.track} из {self.from_address}"
        f"в {self.to_address}, Стоимость {self.cost} рублей."
