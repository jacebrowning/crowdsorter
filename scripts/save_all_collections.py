#!/usr/bin/env python

# pylint: disable=import-error

import os

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    for collection in Collection.objects:
        collection.save()


if __name__ == '__main__':
    main()
