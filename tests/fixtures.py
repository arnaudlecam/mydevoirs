from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from pony.orm import db_session, delete
from mydevoirs.database.database import db, db_init
import datetime
import os
from kivy.lang import Builder


def test_setup():
    os.environ["MYDEVOIRS_BASE_DIR"] = os.getcwd()
    Builder.load_file("mydevoirs/mydevoirs.kv")

class Touche(UnitTestTouch):
    def click(self):
        self.touch_down()
        self.touch_up()


def get_touch(item):
    return Touche(
        item.pos[0] + item.size[0] / 2,
        item.pos[1] + item.size[1] / 2,
    )

def matiere_francais():
    with db_session:
        return db.Matiere['Français']

def jour_today():
    with db_session:
        return db.Jour.get(date=datetime.date.today()) or db.Jour(date=datetime.date.today())

def item_today():
    with  db_session:
        i = db.Item(content="item today",matiere =  matiere_francais(), jour = jour_today())
        return i




class MyDevoirsTestCase(GraphicUnitTest):
    def setUp(self):
        super().setUp()


        with db_session:
            for entity in db.entities.values():
                    if  entity.__name__ != "Matiere":
                        delete(e for e in entity)