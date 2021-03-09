import logging
import re
import uuid

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Collection, Card, Comment, Blog, Option, User

# from study_platform.models import Collection, Card, Comment, Blog, Option


logging.basicConfig(format='[%(asctime)s] - %(levelname)s: %(message)s',
                    level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


# Done
def reraise(exc_type, exc_value, exc_traceback=None):
    """
    Raise an exception, used to add information/message to a raised error
    """
    if exc_value is None:
        exc_value = exc_type()
    if exc_value.__traceback__ is not exc_traceback:
        raise exc_value.with_traceback(exc_traceback)
    raise exc_value


# Done
def id_style_check(i):
    """
    check the style of id
    :param i: a string of id. The id should be a 32-bit long string(Hexadecimal) or 36-bit long contain '-'
    :type i: str
    :return: a boolean value representing whether the ID is valid or not
    :rtype: bool
    """
    return len(re.findall("[0-9a-fA-F]", i.replace('-', ""))) == 32


# Done
def get_all_cards(collection):
    """
    Get a list of all cards in a specified collection
    :param collection: a Collection instance, or a 32/36-bit length string represent collection id
    :type collection: Collection | UUID | str
    :return: a list of card instances in the collection, will return an empty list if no cards found
    :rtype: list[Card]
    :exception TypeError: raises when the input is not a valid id or collection instance
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one ID
    """
    if isinstance(collection, str):
        if id_style_check(collection):
            collection = uuid.UUID(collection)
        else:
            msg = "Invalid ID, ID-{}".format(collection)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)

    if isinstance(collection, Collection):
        result = list(collection.coll_cards.all())
        return result
    elif isinstance(collection, uuid.UUID):
        try:
            result = list(Collection.objects.get(coll_id=collection).coll_cards.all())
            return result
        except ObjectDoesNotExist as e:
            msg = "0 record found in table:Collection with ID-{}".format(collection)
            logging.info(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
        except MultipleObjectsReturned as e:
            msg = "Multiple records found in table:Collection with ID-{}".format(collection)
            logging.warning(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
    else:
        logging.info("Invalid Input")
        raise TypeError("[ERROR] Invalid Input")


# Done
def get_options(card):
    """
    Get all options of a specified card.
    :param card: a Card instance, or a 32/36-bit length string represent card id
    :type card: Card | str | UUID
    :return: a list of options, will return an empty list if no options found
    :rtype: list[Option]
    :exception TypeError: raises when the input is not a valid id or collection instance
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one ID
    """

    if isinstance(card, str):
        if id_style_check(card):
            card = uuid.UUID(card)
        else:
            msg = "Invalid ID, ID-{}".format(card)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)

    if isinstance(card, Card):
        options = card.option_set.all()
        return list(options)
    elif isinstance(card, uuid.UUID):
        try:
            options = Card.objects.get(card_id=card)[0].option_set.all()
            return list(options)
        except ObjectDoesNotExist as e:
            msg = "0 record found in table:Card with ID-{}".format(card)
            logging.info(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
        except MultipleObjectsReturned as e:
            msg = "Multiple record found in table:Card with ID-{}".format(card)
            logging.warning(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
    else:
        raise TypeError("[ERROR] Invalid Input")


# Done
def get_options_list(card_list):
    """
    get all options in a list of card
    :return: a list of option list
    :rtype: list[list[Option]]
    :exception TypeError: raises when the input is not a valid id or collection instance
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one ID
    """
    result = []
    for c in card_list:
        result.append(get_options(c))
    return result


# Done
def add_card2coll(card, collection):
    """
    Insert a card to collection
    :param card: a Card instance, or a 32/36-bit length string represent card id
    :type card: Card | str
    :param collection: a Collection instance, or a 32/36-bit length string represent collection id
    :type collection: Collection | str
    :return: a Collection instance
    :rtype: Collection
    :exception TypeError: raises when the input is not a valid id or collection instance
    :exception ObjectDoesNotExist: raises when no records found
    :exception MultipleObjectsReturned: raises when several records found with a same ID
    """
    if isinstance(card, Card):
        card = card.card_id
    elif isinstance(card, str):
        if id_style_check(card):
            card = uuid.UUID(card)
        else:
            msg = "Invalid ID, ID-{}".format(card)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)

    if isinstance(collection, Collection):
        collection = collection.coll_id
    elif isinstance(collection, str):
        if id_style_check(card):
            collection = uuid.UUID(collection)
        else:
            msg = "Invalid ID, ID-{}".format(collection)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)

    s = Collection()
    c = Card()

    try:
        s = Collection.objects.get(coll_id=collection)
    except ObjectDoesNotExist as e:
        msg = "0 records found in table:Collection with ID-{}".format(collection)
        logging.info(msg)
        reraise(type(e), type(e)("[ERROR] " + msg))
    except MultipleObjectsReturned as e:
        msg = "Multiple record found in table:Collection with ID-{}".format(collection)
        logging.warning(msg)
        reraise(type(e), type(e)("[ERROR] " + msg))

    try:
        c = Card.objects.get(card_id=card)
    except ObjectDoesNotExist as e:
        msg = "0 records found in table:Card with ID-{}".format(card)
        logging.info(msg)
        reraise(type(e), type(e)("[ERROR] " + msg))
    except MultipleObjectsReturned as e:
        msg = "Multiple record found in table:Card with ID-{}".format(card)
        logging.warning(msg)
        reraise(type(e), type(e)("[ERROR] " + msg))

    s.coll_cards.add(c)
    return s


# Done
def get_next_comt(father_id):
    """
    :param father_id: a 32/36-bit length id represented an instance of father_type
    :type father_id: str | Card | Blog | Comment
    :return: a comment followed by the father_id
    :rtype: Comment
    :exception TypeError: raises when the input is not a valid id or collection instance
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one ID
    """

    if isinstance(father_id, Card):
        father_id = Card.card_id
    elif isinstance(father_id, Comment):
        father_id = Comment.comt_id
    elif isinstance(father_id, Blog):
        father_id = Blog.blog_id
    elif isinstance(father_id, str):
        if id_style_check(father_id):
            father_id = uuid.UUID(father_id)
        else:
            msg = "Invalid ID, ID-{}".format(father_id)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)

    try:
        result = Comment.objects.get(comt_father_id=father_id)
        return result
    except ObjectDoesNotExist as e:
        msg = "0 records found in table:Comment with ID-{}".format(father_id)
        logging.info(msg)
        reraise(type(e), type(e)("[ERROR] " + msg))
    except MultipleObjectsReturned as e:
        msg = "Multiple record found in table:Comment with ID-{}".format(father_id)
        logging.warning(msg)
        reraise(type(e), type(e)("[ERROR] " + msg))


# Done
def get_all_comt(father_id, amount=0):
    """
    get comments by a enter a ID.
    amount:
        - amount > 0: returns the specified number of comments
        - amount = 0: returns all comments
        - amount < 0: raises a ValueError
    ------------
    :param father_id: a 32/36-bit length id represented an instance of father_type
    :type father_id: str | Card | Comment | Blog
    :param amount: an integer representing the number of records to be searched. The default is 0.
    :type amount: int
    :return: a list of comment instances
    :rtype: list[Comment]
    :exception ValueError: raises when the input is negative
    :exception TypeError: raises when the input is not a valid id or collection instance
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one ID
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
    elif isinstance(father_id, Blog):
        father_id = Blog.blog_id
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
            except ObjectDoesNotExist:
                return result
    elif amount > 0:
        for i in range(amount):
            try:
                r = get_next_comt(father_id)
                result.append(r)
                father_id = r.comt_id
            except ObjectDoesNotExist:
                return result
        return result


def get_card_by_tag(*tags):
    """
    Return a list of cards contains all tags
    :param tags: one or more tags
    :type tags: str | Tag
    :return: a list of cards, can be empty
    :rtype: list[Card]
    """

    result = list(Card.objects.filter(card_tags__name__in=tags).distinct())
    return result


def get_coll_by_tag(*tags):
    return list(Collection.objects.filter(coll_tags__name__in=tags).distinct())


def add_tags_to_card(card, *tags):
    """
    add one or more tag to a specified card
    :param card: a ID string or Card instance
    :type card: str | Card
    :param tags: one or more string or Tag instance
    :type tags: str | Tag
    :return: The updated Card
    :rtype: Card
    :exception TypeError: raises when the input is not a valid id or collection instance
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one ID
    """
    if isinstance(card, Card):
        card.card_tags.add(tags)
    elif isinstance(card, str):
        if id_style_check(card):
            card = uuid.UUID(card)
            try:
                c = Card.objects.get(card_id=card)
                c.card_tags.add(tags)
                return c
            except ObjectDoesNotExist as e:
                msg = "0 records found in table:Card with ID-{}".format(card)
                logging.info(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
            except MultipleObjectsReturned as e:
                msg = "Multiple record found in table:Card with ID-{}".format(card)
                logging.warning(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
        else:
            msg = "Invalid ID, ID-{}".format(card)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)


def remove_tags_from_card(card, *tags):
    if isinstance(card, Card):
        card.card_tags.remove(tags)
    elif isinstance(card, str):
        if id_style_check(card):
            card = uuid.UUID(card)
            try:
                c = Card.objects.get(card_id=card)
                c.card_tags.remove(tags)
                return c
            except ObjectDoesNotExist as e:
                msg = "0 records found in table:Card with ID-{}".format(card)
                logging.info(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
            except MultipleObjectsReturned as e:
                msg = "Multiple record found in table:Card with ID-{}".format(card)
                logging.warning(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
        else:
            msg = "Invalid ID, ID-{}".format(card)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)


def add_tags_to_coll(coll, *tags):
    if isinstance(coll, Collection):
        coll.coll_tags.add(tags)
    elif isinstance(coll, str):
        if id_style_check(coll):
            coll = uuid.UUID(coll)
            try:
                c = Card.objects.get(card_id=coll)
                c.card_tags.add(tags)
                return c
            except ObjectDoesNotExist as e:
                msg = "0 records found in table:Card with ID-{}".format(coll)
                logging.info(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
            except MultipleObjectsReturned as e:
                msg = "Multiple record found in table:Card with ID-{}".format(coll)
                logging.warning(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
        else:
            msg = "Invalid ID, ID-{}".format(coll)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)


def remove_tags_from_coll(coll, *tags):
    if isinstance(coll, Collection):
        coll.coll_tags.remove(tags)
    elif isinstance(coll, str):
        if id_style_check(coll):
            coll = uuid.UUID(coll)
            try:
                c = Collection.objects.get(coll_id=coll)
                c.card_tags.remove(tags)
                return c
            except ObjectDoesNotExist as e:
                msg = "0 records found in table:Card with ID-{}".format(coll)
                logging.info(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
            except MultipleObjectsReturned as e:
                msg = "Multiple record found in table:Card with ID-{}".format(coll)
                logging.warning(msg)
                reraise(type(e), type(e)("[ERROR] " + msg))
        else:
            msg = "Invalid ID, ID-{}".format(coll)
            logging.info(msg)
            raise TypeError("[ERROR] " + msg)
