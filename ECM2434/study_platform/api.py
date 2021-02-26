from groupH.models import Collection, Card, Comment, Poster, Option


def id_style_check(i):
    """
    check the style of id

    :param i: a string of id. The id should be a 32-bit long string(Hexadecimal) or 36-bit long contain '-'
    :type i: str

    :return: a boolean value representing whether the ID is valid or not
    :rtype: bool
    """
    if len(i.strip('-')) != 32:
        return False
    else:
        return True


def get_all_cards(collection):
    """
    Get a list of all cards in a specified collection

    :param collection: a Collection instance, or a 32/36-bit length string represent collection id
    :type collection: Collection | str

    :return: a list of card instances in the collection
    :rtype: list[Card]

    :exception IndexError: raises when no records found
    :exception TypeError: raises when the input is not a valid id or collection instance
    """

    if isinstance(collection, Collection):
        return list(collection.coll_cards.all())
    elif isinstance(collection, str):
        if id_style_check(collection):
            try:
                cards = Collection.objects.filter(coll_id=collection)[0].coll_cards.all()
                return list(cards)
            except IndexError:
                return IndexError("[ERROR] Unable to find the corresponding record")
        else:
            raise TypeError("[ERROR] Invalid ID Length")
    else:
        raise TypeError("[ERROR] Invalid Input")


def get_options(card):
    """
    Get all options of a specified card.

    :param card: a Card instance, or a 32/36-bit length string represent card id
    :type card: Card | str

    :return: a list of options, a TypeError or an IndexError
    :rtype: list[Option]

    :exception IndexError: raises when no records found
    :exception TypeError: raises when the input is not a valid id or collection instance
    """

    if isinstance(card, Card):
        options = card.option_set.all()
        return list(options)
    elif isinstance(card, str):
        if id_style_check(card):
            try:
                options = Card.objects.filter(card_id=card)[0].option_set.all()
                return list(options)
            except IndexError:
                return IndexError("[ERROR] Unable to find the corresponding record")
        else:
            raise TypeError("[ERROR] Invalid ID Length")
    else:
        raise TypeError("[ERROR] Invalid Input")


def get_options_list(card_list):
    """
    get all options in a list of card

    :return: a list of option list
    :rtype: list[list[Option]]

    :exception IndexError: raises when no records found
    :exception TypeError: raises when the input is not a valid id or collection instance
    """
    result = []
    for c in card_list:
        result.append(get_options(c))
    return result


def add_card2coll(card, collection):
    """
    Insert a card to collection

    :param card: a Card instance, or a 32/36-bit length string represent card id
    :type card: Card | str

    :param collection: a Collection instance, or a 32/36-bit length string represent collection id
    :type collection: Collection | str

    :return: a Collection instance
    :rtype: Collection

    :exception IndexError: raises when no records found
    :exception TypeError: raises when the input is not a valid id or collection instance
    """

    if isinstance(card, Card):
        card = card.card_id
    elif isinstance(card, str):
        if not id_style_check(card):
            raise TypeError("[ERROR] Invalid ID Length")
    try:
        c = Card.objects.filter(card_id=card)[0]
    except IndexError:
        raise IndexError("[ERROR] Unable to find the corresponding record")

    if isinstance(collection, Collection):
        collection = collection.coll_id
    elif isinstance(collection, str):
        if not id_style_check(collection):
            raise TypeError("[ERROR] Invalid ID Length")
    try:
        s = Collection.objects.filter(coll_id=collection)[0]
    except IndexError:
        raise IndexError("[ERROR] Unable to find the corresponding record")

    s.coll_cards.add(c)
    return s


def get_next_comt(father_id):
    """
    :param father_id: a 32/36-bit length id represented an instance of father_type
    :type father_id: str | Card | Poster | Comment

    :return: a comment fowled by the father_id
    :rtype: Comment
    """

    if isinstance(father_id, Card):
        father_id = Card.card_id
    elif isinstance(father_id, Comment):
        father_id = Comment.comt_id
    elif isinstance(father_id, Poster):
        father_id = Poster.post_id
    elif isinstance(father_id, str):
        if not id_style_check(father_id):
            raise TypeError("[ERROR] Invalid ID Length")

    try:
        result = Comment.objects.filter(comt_father_id=father_id)[0]
        return result
    except IndexError:
        raise IndexError("[ERROR] Unable to find the corresponding record")


def get_all_comt(father_id, amount=0):
    """
    get comments by a enter a ID.

    amount:
        - amount > 0: returns the specified number of comments
        - amount = 0: returns all comments
        - amount < 0: raises a ValueError

    ------------

    :param father_id: a 32/36-bit length id represented an instance of father_type
    :type father_id: str

    :param amount: an integer representing the number of records to be searched. The default is 0.
    :type amount: int

    :return: a list of comment instances
    :rtype: list[Comment]

    :exception TypeError: raises when the input is not a valid id
    :exception ValueError: raises when the input is negative
    :exception IndexError: raises when no record founds
    """

    def amount_check(n):
        if isinstance(n, int):
            if n < 0:
                raise ValueError("[ERROR] Invalid number")
        else:
            raise TypeError("[ERROR] Invalid input type")

    if isinstance(father_id, Card):
        father_id = Card.card_id
    elif isinstance(father_id, Comment):
        father_id = Comment.comt_id
    elif isinstance(father_id, Poster):
        father_id = Poster.post_id
    elif isinstance(father_id, str):
        if not id_style_check(father_id):
            raise TypeError("[ERROR] Invalid ID Length")
    amount_check(amount)

    result = []

    if amount == 0:
        while True:
            try:
                r = get_next_comt(father_id)
                result.append(r)
                father_id = r.comt_id
            except IndexError:
                return result
    elif amount > 0:
        for i in range(amount):
            try:
                r = get_next_comt(father_id)
                result.append(r)
                father_id = r.comt_id
            except IndexError:
                return result
        return result
