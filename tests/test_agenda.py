# from mydevoirs import __version__
# from mydevoirs.widgets import ItemWidget, Clock, JourItems, JourWidget, BaseGrid
from mydevoirs.agenda import (
    AgendaItemWidget,
    JourWidget,
    Agenda,
    CarouselWidget,
    JourItems,
    BaseGrid,
)

# from pony.orm import db_session, delete
from .fixtures import *

# from mydevoirs.constants import MATIERES
# import datetime
from unittest.mock import patch, MagicMock
from kivy.uix.widget import Widget

# import pytest
# from kivy.config import ConfigParser

from kivy.uix.dropdown import DropDown

# from mydevoirs.matiere_dropdown import MatiereOption


class AgendaItemWidgetTestCase(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()

        with db_session:
            self.JOUR = db.Jour(date=datetime.date.today())
            self.MAT = db.Matiere["Grammaire"]
            self.FIRST = db.Item(content="un", matiere=self.MAT, jour=self.JOUR)
            self.SECOND = db.Item(
                content="deux", matiere=self.MAT, jour=self.JOUR, done=True
            )

    def test_widget_init(self):

        item = AgendaItemWidget(**self.FIRST.to_dict())
        assert item.entry == self.FIRST.id  # super.__init__ called
        assert hasattr(item, "_jour_widget")

    def test_on_done(self):

        # check super call
        with patch("mydevoirs.agenda.ItemWidget.on_done") as e:
            print(e)
            item = AgendaItemWidget(**self.FIRST.to_dict())
            item.loaded_flag = False
            item.on_done()
            assert e.called

        # reste
        item = AgendaItemWidget(**self.FIRST.to_dict())
        item._jour_widget = MagicMock()
        item.on_done()
        assert item.jour_widget.update_progression.called

    def test_jour_widget(self):
        item_today()
        jw = JourWidget(datetime.date.today())
        item = jw.jouritem.children[0]

        # base behaviour
        assert item.jour_widget == jw

        # test cache
        with patch.object(item, "walk_reverse") as m:
            assert item.jour_widget == jw
            assert not m.called


class JourItemsTestCase(MyDevoirsTestCase):
    def setUp(self):

        super().setUp()

        self.a = item_today()
        self.b = item_today()
        self.c = item_today()

        self.jouritems = JourItems(self.a.jour.date)

        self.render(self.jouritems)

    def test_load(self):

        assert len(self.jouritems.children) == 3
        assert self.jouritems.children[0].entry == self.c.id


class JourWidgetTestCase(MyDevoirsTestCase):
    def setUp(self):

        super().setUp()

        self.a = item_today()
        self.b = item_today()
        self.c = item_today()

    def test_nice_date(self):
        jour = JourWidget(datetime.date(2019, 11, 12))
        assert jour.ids.titre_jour.text == "mardi 12 novembre 2019"

    def test_add(self):
        jour = JourWidget(self.a.jour.date)
        self.render(jour)
        assert len(jour.jouritem.children) == 3

        get_touch(jour.ids.add_button).click()
        self.render(jour)

        assert len(jour.jouritem.children) == 4
        print(self.Window.children)
        assert any(isinstance(x, DropDown) for x in self.Window.children)
        with db_session:
            assert db.Item[jour.jouritem.children[0].entry]


class TestBaseGrid(MyDevoirsTestCase):
    def test_get_week_days(self):
        with patch.object(
            BaseGrid,
            "get_days_to_show",
            return_value=[False, True, False, True, False, True, False],
        ):
            b = BaseGrid(day=datetime.date(2019, 11, 12))
            for d, z in zip(
                b.children,
                [
                    datetime.date(2019, 11, 16),
                    datetime.date(2019, 11, 14),
                    datetime.date(2019, 11, 12),
                ],
            ):

                assert d.date == z
