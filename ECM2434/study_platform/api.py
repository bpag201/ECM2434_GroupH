from groupH.models import Collection, Card, Comment, Poster, Option


def get_all_cards(collection):
    """
    Get a list of all cards in a specified collection
    :param collection: a Collection instance, or a 32/36-bit length string represent collection id
    :return: a list of cards, a TypeError or an IndexError
    """
    if isinstance(collection, Collection):
        return list(collection.coll_cards.all())
    elif isinstance(collection, str):
        if len(collection.strip('-')) == 32:
            try:
                cards = Collection.objects.filter(coll_id=collection)[0].coll_cards.all()
                return list(cards)
            except IndexError:
                return IndexError("[ERROR] Unable to find the corresponding record")
        else:
            raise TypeError("[ERROR] Invalid ID Length")
    else:
        raise TypeError("[ERROR] Invalid Input")


def get_options_list(card_list):
    result = []
    for c in card_list:
        result.append(get_options(c))
    return result


def get_options(card):
    """
    Get all options of a specified card.
    :param card: a Card instance, or a 32/36-bit length string represent card id
    :return: a list of options, a TypeError or an IndexError
    """
    if isinstance(card, Card):
        options = card.option_set.all()
        return list(options)
    elif isinstance(card, str):
        if len(card.strip('-')) == 32:
            try:
                options = Card.objects.filter(card_id=card)[0].option_set.all()
                return list(options)
            except IndexError:
                return IndexError("[ERROR] Unable to find the corresponding record")
        else:
            raise TypeError("[ERROR] Invalid ID Length")
    else:
        raise TypeError("[ERROR] Invalid Input")


def add_card2coll(card, collection):
    """
    Insert a card to collection
    :param card: a Card instance, or a 32/36-bit length string represent card id
    :param collection: a Collection instance, or a 32/36-bit length string represent collection id
    :return: a Collection instance
    """
    if isinstance(card, Card):
        card = card.card_id
    elif isinstance(card, str):
        if len(card.strip('-')) != 32:
            raise TypeError("[ERROR] Invalid ID Length")
    try:
        c = Card.objects.filter(card_id=card)[0]
    except IndexError:
        raise IndexError("[ERROR] Unable to find the corresponding record")

    if isinstance(collection, Collection):
        collection = collection.coll_id
    elif isinstance(collection, str):
        if len(collection.strip('-')) != 32:
            raise TypeError("[ERROR] Invalid ID Length")
    try:
        s = Collection.objects.filter(coll_id=collection)[0]
    except IndexError:
        raise IndexError("[ERROR] Unable to find the corresponding record")

    s.coll_cards.add(c)
    return s
