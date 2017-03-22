#!/usr/bin/env python
# pylint: disable=import-error,line-too-long

"""
Generate sample data for manual testing.
"""

import os

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection, Item


create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

collection = Collection(name="Empty Collection", key='_empty')
collection.save()

collection = Collection(name="New Collection", key='_new')
collection.add("Foo")
collection.add("Bar")
collection.add("A really long name with lots of words.")
collection.add("special_character:#")
collection.add("special_character:&")
collection.add("special_character:'")
collection.save()

collection = Collection(name="Colors", key='_sample', code='sample',
                        private=True)
collection.add("Red")
collection.add("Green")
collection.add("Blue")
collection.add("Yellow")
collection.save()

collection = Collection(name="Numbers", key='_numbers', code='numbers')
collection.items = [Item(name=str(n)).save() for n in range(1, 21)]
collection.save()

collection = Collection(name="Private Collection",
                        key='_private', private=True)
collection.items = [
    Item(name="Secret One").save(),
    Item(name="Secret Two").save(),
]
collection.save()

collection = Collection(name="Locked Collection",
                        key='_locked', locked=True)
collection.items = [
    Item(name="Item One").save(),
    Item(name="Item Two").save(),
]
collection.save()

collection = Collection(name="Metadata Collection",
                        key='_metadata', code='dogs')
collection.add(
    "Collie",
    description="Medium-sized, fairly lightly built dog, with a pointed snout.",
    image_url="https://upload.wikimedia.org/wikipedia/commons/e/e4/Border_Collie_600.jpg",
    ref_url="https://en.wikipedia.org/wiki/Collie",
)
collection.add(
    "Golden Retriever",
    description="Instinctive love of water, and are easy to train to basic or advanced obedience standards.",
    image_url="https://upload.wikimedia.org/wikipedia/commons/9/93/Golden_Retriever_Carlos_%2810581910556%29.jpg",
    ref_url="https://en.wikipedia.org/wiki/Golden_Retriever",
)
collection.add(
    "Pug",
    description="The Pug is a breed of dog with a wrinkly, short-muzzled face, and curled tail.",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Pug_portrait.jpg/400px-Pug_portrait.jpg",
    ref_url="https://en.wikipedia.org/wiki/Pug",
)
collection.add(
    "Dalmatian",
    description="The Dalmatian is a breed of large dog, noted for its unique black or liver spotted coat and mainly used as a carriage dog in its early days.",
)
collection.add(
    "Shiba Inu",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Shiba_inu_taiki.jpg/1920px-Shiba_inu_taiki.jpg",
)
collection.save()

collection = Collection(name="Single Item Collection")
collection.add("Item One")
collection.save()
