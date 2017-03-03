#!/usr/bin/env python

import os

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection, Item


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    for collection in Collection.objects:
        if not collection.items2:
            print(f"Migrating {collection}...")

            for name in collection.items:
                item = Item(name=name)
                item.save()
                collection.items2.append(item)

            collection.save()

            print(collection.items2)


if __name__ == '__main__':
    main()
