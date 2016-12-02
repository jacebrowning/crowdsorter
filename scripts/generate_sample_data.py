#!/usr/bin/env python

import os

from crowdsorter.settings import get_config
from crowdsorter.app import create_app
from crowdsorter.models import Collection


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    collection = Collection(name="Sample List")
    collection.save()


if __name__ == '__main__':
    main()
