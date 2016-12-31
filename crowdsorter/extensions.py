from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from flask_menu import Menu
from flask_sendgrid import SendGrid

db = MongoEngine()

bootstrap = Bootstrap()
menu = Menu()

sendgrid = SendGrid()
