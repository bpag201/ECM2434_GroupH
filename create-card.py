from PIL import Image


def create_card(card_name, accessory_name):
    """Assembles the card"""

    card = Image.open(card_name)
    accessory = Image.open(accessory_name)
    final_card = Image.new("RGBA", (1335, 1984))
    final_card.paste(card, (0, 0), card)
    final_card.paste(accessory, (0, 0), accessory)
    final_card.save("final_card.png")
    final_card.show()
    return final_card


create_card('D:\GIMP 2.10.22\Card Back\Card Back.png', 'D:\GIMP 2.10.22\Accessories\Moustache png\Brown moustache.png')
