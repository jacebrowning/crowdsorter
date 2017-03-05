#!/usr/bin/env python

import os

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    for collection in Collection.objects:
        print(f"Migrating {collection}...")
        collection.items = collection.items2
        collection.votes = collection.votes2
        collection.save()


if __name__ == '__main__':
    main()
