#!/usr/bin/env python

import os

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection, Item, Wins, Loss


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    for collection in Collection.objects:
        if not (collection.items2 or collection.votes2):
            print(f"Migrating {collection}...")

            items = {}

            for name in collection.items:
                item = Item(name=name)
                item.save()
                collection.items2.append(item)
                items[item.name] = item

            for wins in collection.votes:

                collection.votes2.wins = Wins(winner=items[wins.winner])

                for loss in wins.against:
                    loss = Loss(loser=items[loss.loser], count=loss.count)
                    collection.votes2.wins.against.append(loss)

            collection.save()

            print(collection.items2)
            print(collection.votes2)


        items = {}
        for item in collection.items2:
            items[item.name] = item

        for wins in collection.votes:
            for loss in wins.against:
                print(loss.count)

                for wins2 in collection.votes2:
                    for loss2 in wins2.against:

                        if wins.winner == wins2.winner.name and \
                                loss.loser == loss2.loser.name and loss.count:
                            loss2.count = loss.count
                            print("Updated loss count")
                            collection.save()
                            break

if __name__ == '__main__':
    main()
