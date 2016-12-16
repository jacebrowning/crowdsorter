#!/usr/bin/env python

import os

from crowdsorter.settings import get_config
from crowdsorter.app import create_app
from crowdsorter.models import Collection


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    collection = Collection(name="Empty List", key='_empty')
    collection.save()

    collection = Collection(name="New List", key='_new')
    collection.items.append("Foo")
    collection.items.append("Bar")
    collection.save()

    collection = Collection(name="Colors", key='_sample', code='sample')
    collection.items.append("Red")
    collection.items.append("Green")
    collection.items.append("Blue")
    collection.items.append("Yellow")
    collection.save()


if __name__ == '__main__':
    main()
