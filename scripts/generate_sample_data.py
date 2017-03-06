#!/usr/bin/env python

import os

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection, Item


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    collection = Collection(name="Empty Collection", key='_empty')
    collection.save()

    collection = Collection(name="New Collection", key='_new')
    collection.items2.append(Item(name="Foo").save())
    collection.items2.append(Item(name="Bar").save())
    collection.items2.append(Item(name="A really long name with lots of words.").save())
    collection.items2.append(Item(name="special_character:#").save())
    collection.items2.append(Item(name="special_character:&").save())
    collection.items2.append(Item(name="special_character:'").save())
    collection.save()

    collection = Collection(name="Colors", key='_sample', code='sample',
                            private=True)
    collection.items2.append(Item(name="Red").save())
    collection.items2.append(Item(name="Green").save())
    collection.items2.append(Item(name="Blue").save())
    collection.items2.append(Item(name="Yellow").save())
    collection.save()

    collection = Collection(name="Numbers", key='_numbers', code='numbers')
    collection.items2 = [Item(name=str(n)).save() for n in range(1, 21)]
    collection.save()

    collection = Collection(name="Private Collection",
                            key='_private', private=True)
    collection.items2 = [
        Item(name="Secret One").save(),
        Item(name="Secret Two").save(),
    ]
    collection.save()

    collection = Collection(name="Locked Collection",
                            key='_locked', locked=True)
    collection.items2 = [
        Item(name="Item One").save(),
        Item(name="Item Two").save(),
    ]
    collection.save()


if __name__ == '__main__':
    main()
