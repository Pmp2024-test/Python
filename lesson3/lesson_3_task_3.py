from Address import Address
from Mailing import Mailing


to_address = Address(249360, "Хвастовичи", "Ленина", 17, 1)


to_address = Address(249360, "Хвастовичи", "Ленина", 17, 1)


from_address = Address(249365, "Бояновичи", "Центральная", 2, 2)

track = "AB123456789CD"
cost = 350.75
my_track = Mailing(track, from_address, to_address, cost)

print(my_track)
