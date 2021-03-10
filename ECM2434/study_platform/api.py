import logging
import re
import uuid
import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required

from .models import *


logging.basicConfig(format='[%(asctime)s] - %(levelname)s: %(message)s',
                    level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


def reraise(exc_type, exc_value, exc_traceback=None):
    """
    Raise an exception, used to add information/message to a raised error
    """
    if exc_value is None:
        exc_value = exc_type()
    if exc_value.__traceback__ is not exc_traceback:
        raise exc_value.with_traceback(exc_traceback)
    raise exc_value


def id_style_check(i):
    """
    check the style of id

    :param i: a string of id. The id should be a 32-bit long string(Hexadecimal) or 36-bit long contain '-'
    :type i: str

    :return: a boolean value representing whether the ID is valid or not
    :rtype: bool
    """
    return len(re.findall("[0-9a-fA-F]", i.replace('-', ""))) == 32


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


@login_required
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


@login_required
def add_tags_to_Card(card, *tags):
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


@login_required
def remove_tags_from_Card(card, *tags):
    """
    Remove tag(s) from a card, **will not** raise an exception if tag(s) not exist

    :param card: an instance of Card or a string represent Card ID
    :type card: Card | str

    :param tags: String(s) of tags
    :type tags: str

    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one ID
    """

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


def get_rank(target):
    """
    get the corresponding rank title of a user according his/her score

    :param target: Can use User or Profile instance as input, also allow integers
    :type target: User | Profile | int

    :return: will return a string represent
    :rtype: str

    :exception TypeError: raises when the input is not any of the above three classes
    :exception FileNotFoundError: raises when rank.json not exists
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one instance
    """

    def rank(score):
        try:
            with open("groupH/rank.json") as f:
                rank_dict = json.load(f)
            for con in rank_dict:
                if rank_dict[con]['LowerLimit'] < score <= rank_dict[con]['UpperLimit']:
                    return rank_dict[con]['title']
        except FileNotFoundError as e:
            msg = "Important file(s) is missing, please double confirm the file(s) path and restart the server!\n" \
                  "  - rank.json"
            logging.critical(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))

    if isinstance(target, User):
        try:
            return rank(Profile.objects.get(user=User).score)
        except ObjectDoesNotExist as e:
            msg = "0 records found in table:Profile with User-{}".format(target.username)
            logging.info(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
        except MultipleObjectsReturned as e:
            msg = "Multiple record found in table:Profile with User-{}".format(target.username)
            logging.warning(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
    elif isinstance(target, Profile):
        return rank(Profile.score)
    elif isinstance(target, int):
        return rank(target)
    else:
        msg = "Invalid input-{}".format(target)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)


def get_profile(user):
    """
    Get the profile of a user
    :param user: an instance of User
    :type user: User

    :return: The profile of the user
    :rtype: Profile

    :exception TypeError: raises when the input is not any of the above three classes
    :exception ObjectDoesNotExist: raises when no record found
    :exception MultipleObjectsReturned: raises when multiple records returned on one instance
    """
    if isinstance(user, User):
        try:
            profile = Profile.objects.get(user=user)
            return profile
        except ObjectDoesNotExist as e:
            msg = "0 records found in table:Profile with User-{}".format(user.username)
            logging.info(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
        except MultipleObjectsReturned as e:
            msg = "Multiple record found in table:Profile with User-{}".format(user.username)
            logging.warning(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
    else:
        msg = "Invalid input-{}".format(user)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)


def gold_modify(amount, user, description):
    # todo: 完善documentation
    """
    modify the gold amount in a user profile

    :param amount: amount of gold to be modified
    :type amount: int

    :param user: target user
    :type user: User

    :param description: reason of modification
    :type description: str

    :return: the updated profile
    :rtype: Profile
    """
    if not isinstance(amount, int):
        msg = "Invalid input-{}".format(amount)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)
    elif not isinstance(description, str):
        msg = "Invalid input-{}".format(description)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)
    elif not isinstance(user, User):
        msg = "Invalid input-{}".format(user)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)
    else:
        try:
            profile = Profile.objects.get(user)
            profile.gold_modify(amount)
            return profile
        except ObjectDoesNotExist as e:
            msg = "0 records found in table:Profile with User-{}".format(user.username)
            logging.info(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
        except MultipleObjectsReturned as e:
            msg = "Multiple record found in table:Profile with User-{}".format(user.username)
            logging.warning(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))


def get_all_item(target):
    # todo: 完善documentation
    """

    :param target:
    :type target:
    :return:
    :rtype:
    """
    if isinstance(target, User):
        try:
            profile = Profile.objects.get(user=target)
            return list(profile.resources.all())
        except ObjectDoesNotExist as e:
            msg = "0 records found in table:Profile with User-{}".format(target)
            logging.info(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
        except MultipleObjectsReturned as e:
            msg = "Multiple record found in table:Profile with User-{}".format(target)
            logging.warning(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
    else:
        msg = "Invalid input-{}".format(target)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)


def modify_item(item, target, amount=1):
    # todo: 完善documentation
    if not isinstance(item, Item):
        msg = "Invalid input-{}".format(item)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)

    if isinstance(target, User):
        try:
            target = Profile.objects.get(user=target)
        except ObjectDoesNotExist as e:
            msg = "0 records found in table:Profile with User-{}".format(target.username)
            logging.info(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))
        except MultipleObjectsReturned as e:
            msg = "Multiple record found in table:Profile with User-{}".format(target.username)
            logging.warning(msg)
            reraise(type(e), type(e)("[ERROR] " + msg))

    if isinstance(target, Profile):
        if item in list(target.resources.all()):
            rec = User_item.objects.get(item=item, profile=target)
            if amount > 0:
                rec.amount += amount
                rec.save()
            elif amount == 0:
                msg = "amount cannot be 0"
                logging.info(msg)
                raise TypeError(msg)
            elif amount < 0:
                if rec.amount > abs(amount):
                    rec.amount += amount
                    rec.save()
                elif rec.amount == abs(amount):
                    rec.delete()
                else:
                    raise IndexError("Negative item amount generated")
        else:
            User_item.objects.create(item=item, profile=target)

    else:
        msg = "Invalid input-{}".format(item)
        logging.info(msg)
        raise TypeError("[ERROR] " + msg)
