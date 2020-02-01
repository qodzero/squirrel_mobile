import math
import random
import re

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.garden.magnet import Magnet
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import (ColorProperty, ListProperty, NumericProperty,StringProperty, ObjectProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import rgba

from vendor.graph import BarPlot, LinePlot, MeshLinePlot, SmoothLinePlot
from customs.customs import MaterialWidget

class Card(Magnet):
    back = ColorProperty([0,0,1,1])
    name = StringProperty()
    vendor = StringProperty()
    num = StringProperty()
    exp = StringProperty()
    balance = StringProperty()
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_vendor(self, inst, val):
        if val == 'mastercard':
            master = MasterCard()
            self.ids.logo.add_widget(master)
        elif val == 'visa':
            lbl = Label(text='VISA')
            lbl.font_name = 'app/assets/fonts/Roboto-BlackItalic.ttf'
            self.ids.logo.add_widget(lbl)


class Container(MaterialWidget):
    primary = ColorProperty()
    def __init__(self, **kw):
        super().__init__(**kw)
        self.primary = rgba("#2C323C")


    def draw_back(self, dtx):
        with self.canvas.before:
            Color(rgba=App.get_running_app().root.primary)
            Rectangle(pos=self.pos, size=self.size)

class FlatView(ModalView):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.background_color = [0,0,0,0]
        self.background_normal = ''

class Graph(Magnet):
    def __init__(self, **kw):
        super().__init__(**kw)

    def draw_bar(self, data: list):
        norm = self.normalise(data)

        for i, d in enumerate(norm):
            bar = Bar()
            bar.background_color = [0,1,0,1]
            bar.text = str(data[i])
            bar.size_hint_y = d
            # bar.color = [0,0,0,0]

            self.ids.graph.add_widget(bar)

    def normalise(self, x: list):
        """Given a list of values, normalise The
        values to a range of 0 - 1

        Parameters
        ----------
        x : list
            A list of values to normalise

        Returns
        -------
        list
            A normalised list

        """
        norm = list()
        for xi in x:
            zi = (xi-min(x)) / (max(x) - min(x))
            norm.append(zi)

        return norm

class OutlineInput(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)

class DateInput(OutlineInput):
    def __init__(self, **kw):
        super().__init__(**kw)

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        _text = ''.join([self.text, substring])
        if len(_text) > 5:
            return
        pat = self.pat
        s = re.sub(pat, '', substring)

        if len(self.text) >= 2:
            x = self.text[:2]
            y = self.text[2:]

            if int(x) > 12 or int(x) < 1:
                x = '12'
            self.text = '/'.join([x, y])
        self.text = self.text.replace('//','/')

        return super().insert_text(s, from_undo=from_undo)


class CardInput(OutlineInput):
    def __init__(self, **kw):
        super().__init__(**kw)

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        _text = ''.join([self.text, substring])
        if len(_text) > 4:
            return
        pat = self.pat
        s = re.sub(pat, '', substring)

        return super().insert_text(s, from_undo=from_undo)

class NewCard(Container):
    def __init__(self, **kw):
        super().__init__(**kw)

class NewExpense(Container):
    def __init__(self, **kw):
        super().__init__(**kw)

class Bar(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.color = [0,0,0,0]

class ExpenseProgress(BoxLayout):
    max = NumericProperty()
    name = StringProperty()
    value = NumericProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

class MasterCard(Label):
    def __init__(self, **kw):
        super().__init__(**kw)


class FloatingButton(FloatLayout):
    callback = ObjectProperty()
    def __init__(self, **kw):
        super().__init__(**kw)

    def trigger_release(self):
        self.callback()

class FlatToggle(ToggleButton):
    def __init__(self, **kw):
        super().__init__(**kw)
    #     Clock.schedule_once(self.init_view, .2)
    #
    # def init_view(self, dtx):
    #     self.bind(color=self.change_color)
    #
    # def change_color(self, inst, value):
    #     self.color = App.get_running_app().root.secondary

    def on_state(self, inst, value):
        if value == 'normal':
            self.color = rgba('#ffffff')
            # with self.canvas.before:
            #     Color(rgba=rgba('#212232'))
            #     RoundedRectangle(
            #         pos=[self.pos[0], self.size[1]-2],
            #         size=[self.size[0], 2],
            #         radius=[2])
        else:
            self.color = App.get_running_app().root.success
            # with self.canvas.before:
            #     Color(rgba=rgba('#ffffff9f'))
            #     RoundedRectangle(
            #         pos=[self.pos[0], self.size[1]-2],
            #         size=[self.size[0], 2],
            #         radius=[2])

class MainWindow(BoxLayout):
    primary = ColorProperty()
    card_colors = ListProperty()
    back = ColorProperty()
    success = ColorProperty()
    danger = ColorProperty()
    secondary = ColorProperty()
    tertiary = ColorProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

        Clock.schedule_once(self.init_view, .1)
        # Clock.schedule_once(lambda x: self.change_theme('light'), 5)
        # Clock.schedule_once(self.draw_card, 2)

    def init_view(self, dtx):
        self.card_colors = [
            rgba("#ff621b"),
            rgba("#ff5722"),
            rgba("#c51162"),
            rgba("#f50057"),
            rgba("#ff31432b")]
        # self.primary = rgba("#242c3f")
        self.cards = [('payoneer', 'mastercard', '6296', '05/22', '2096.12'), ('FNB Botswana', 'visa', '5697', '09/22', '920')]

        # expenses - (card, card_num, expense, cost, paid, recurring, day_paid)
        self.expenses = [
        ('payoneer', '6296', 'Rent', '150.00', '150.00', 'True', '7'),
        ('payoneer', '6296', 'DigitalOcean Credit', '5.00', '0.00', 'True','10'),
        ('payoneer', '6296', 'Gold Pass', '5.65', '5.65', 'True', '11'),
        ('payoneer', '6296', 'namecheap', '32.56', '12.72', 'True', '15'),
        ('payoneer', '6296', 'Adidas ZX750', '118.00', '118.00', 'False', '4'),
        ('payoneer', '6296', 'Xiaomi Smart Band', '9.99', '9.99', 'False', '10'),
        ('payoneer', '6296', 'Internet', '20.00', '15.00', 'True', '7')
        ]

        self.primary = rgba("#2C323C")
        self.back = rgba("#282C34")
        self.danger = rgba('#ff003f')
        self.secondary = rgba('#ffffff')
        self.tertiary = rgba('#212232')
        self.success = rgba('#05a95c')

        data = [10,40,50,20,45,68,12,9,45]
        graph = Graph()
        graph.draw_bar(data)

        self.ids.graph_wrapper.add_widget(graph)

        for card in self.cards:
            c = Card()
            c.name = card[0].upper()
            c.vendor = card[1]
            c.num = card[2]
            c.exp = card[3]

            sc = Card()
            sc.name = card[0].upper()
            sc.vendor = card[1]
            sc.num = card[2]
            sc.exp = card[3]

            balance = card[4] if '.' in card[4] else '.'.join([card[4], '00'])

            bal, cents = balance.rsplit('.',1)

            balance = '%s[size=%s].%s[/size]'%(bal, int(sp(14)), cents)
            c.balance = balance
            sc.balance = balance

            self.ids.cards_wrapper.add_widget(c)
            self.ids.stats_cards.add_widget(sc)

            # ToDo - Allow rotation
            # if Window.width < Window.height or len(self.ids.cards_wrapper.children) > 0: #landscape mode
            #     break
            # else:
            #     self.ids.cards_wrapper.spacing = sp(15)

        #init tabs
        self.ids.default_tab.state = 'down'

        # Add Recurring expenses
        # expenses - (card, card_num, expense, cost, paid, recurring, date_paid)
        recurring = [x for x in self.expenses if x[5] == 'True']
        points = [(int(x[6]), float(x[4])) for x in self.expenses]
        points = sorted(points, key=lambda x: x[0])

        ipoints = points
        dups = list()
        for x, p in enumerate(points):
            for y, i in enumerate(points):
                if x == y:
                    continue
                else:
                    if p[0] == i[0]:
                        dups.append((p,i))
                        ipoints.remove(p)
                        ipoints.remove(i)

        for d in dups:
            val = d[0][1] + d[1][1]
            ipoints.append((d[0][0], val))

        ipoints = sorted(ipoints, key=lambda x: x[0])
        ymax = max(ipoints, key=lambda x: x[1])[1]
        xmax = max(ipoints, key=lambda x: x[0])

        self.ids.stats_graph.y_ticks_major = math.ceil(ymax/9)
        self.ids.stats_graph.ymax = ymax

        plot = LinePlot(color=self.danger)
        plot.line_width = 2
        plot.points = ipoints
        self.ids.stats_graph.add_plot(plot)
        # print(ipoints)

        for r in recurring:
            ep = ExpenseProgress()
            ep.max = float(r[3])
            ep.value = float(r[4])
            ep.name = r[2].lower()
            ep.size_hint_y = None
            ep.height = sp(18)

            self.ids.recurring_wrapper.add_widget(ep)

    def add_new(self, modal, add='card'):
        modal.dismiss()

        fv = ModalView(size_hint=[.8, .5], padding=sp(10))

        if add == 'card':
            nc = NewCard()
            nc.ids.submit.bind(on_release=lambda x: self.new_card(fv, nc))

            fv.add_widget(nc)
        else:
            ne = NewExpense()
            ne.ids.submit.bind(on_release=lambda x: self.new_expense(fv, ne))
            fv.add_widget(ne)

        fv.open()

    def new_card(self, modal, obj):
        modal.dismiss()

    def new_expense(self, modal, obj):
        modal.dismiss()

    def add_expense(self):
        print('Photoshp')
        fv = ModalView(size_hint=[.6, .2], padding=sp(10))
        btn_card = Button(text='Add New Card', background_color=rgba('#2073B5'), background_normal='')
        btn_card.bind(on_release=lambda x: self.add_new(fv, 'card'))
        btn_expense = Button(text='Add New Expense', background_color=rgba('#2073B5'), background_normal='')
        btn_expense.bind(on_release=lambda x: self.add_new(fv, 'expense'))

        ctn = Container(orientation='vertical')
        ctn.spacing = sp(15)
        ctn.elevation = 4
        ctn.add_widget(btn_card)
        ctn.add_widget(btn_expense)

        fv.add_widget(ctn)
        fv.open()


    def draw_card(self, dtx):
        c = self.ids.cards_wrapper.children[0]
        with c.canvas.before:
            pos_x = range(int(c.pos[0]), int(c.size[0]))
            pos_y = range(int(c.pos[1]), int(c.size[1]))

            size_x = range(int(sp(10)), int(c.size[0]))
            size_y = range(int(sp(10)), int(c.size[1]))

            Color(rgba=rgba('#ffffff10'))
            Ellipse(
                pos=[random.choice(pos_x), random.choice(pos_y)],
                size=[random.choice(size_x), random.choice(size_y)]
            )

    def on_back(self, *args):
        with self.canvas.before:
            Color(rgba=self.back)
            Rectangle(
                pos=self.pos,
                size=self.size
                )


    def change_theme(self, theme='dark'):
        if theme == 'dark':
            self.back = rgba("#262d4f")
            self.primary = rgba("#242c3f")
            self.secondary = rgba('#ffffff')
            self.tertiary = rgba('#212232')
            self.success = rgba('#05a95c')
        else:
            self.primary = rgba("#ffffff")
            self.secondary = rgba('#242c3f')
            self.tertiary = rgba('#f4f4f4')
            self.success = rgba('#05a95cb4')
