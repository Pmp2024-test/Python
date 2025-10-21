from smartphone import Smartphone

catalog =[
    Smartphone("Infinix", "NOTE 30 Pro", "+79805112233"),
    Smartphone("Infinix", "NOTE 30", "+79805112234"),
    Smartphone("Infinix", "NOTE 40 Pro", "+79805112235"),
    Smartphone("Infinix", "NOTE 30", "+79805112236"),
    Smartphone("Infinix", "NOTE 50 Pro", "+79805112237")
    ]
   
for smartphone in catalog:
    print(f"{smartphone.phone_brand} - {smartphone.phone_model} - {smartphone.subscription_number}")