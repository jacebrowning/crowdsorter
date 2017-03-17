#!/usr/bin/env python
# pylint: disable=import-error

"""
Save all collections to update calculated fields.
"""

import os

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection


create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

for collection in Collection.objects:
    collection.save()
