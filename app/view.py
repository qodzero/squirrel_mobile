import math
import random
import re

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.garden.iconfonts import icon
from kivy.garden.magnet import Magnet
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import (ColorProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import rgba

from app.storage import Database
from customs.customs import MaterialWidget
from vendor.graph import BarPlot, LinePlot, MeshLinePlot, SmoothLinePlot


class Card(Magnet):
    card_id = NumericProperty()
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

    def on_balance(self, inst, value):
        self.ids.balance.text = str(value)

class Container(MaterialWidget):
    primary = ColorProperty()
    empty = NumericProperty(1)
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

class NewDeposit(Container):
    def __init__(self, **kw):
        super().__init__(**kw)

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

class ExpenseChip(Container):
    expense_id = NumericProperty()
    icon = StringProperty()
    name = StringProperty()
    card = StringProperty()
    amount = StringProperty()
    def __init__(self, **kw):
        super().__init__(**kw)

class FlatToggle(ToggleButton):
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_state(self, inst, value):
        if value == 'normal':
            self.color = rgba('#ffffff')
        else:
            self.color = App.get_running_app().root.success

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
        self.db = Database()

        Clock.schedule_once(self.init_view, .1)
        # Clock.schedule_once(lambda x: self.change_theme('light'), 5)
        # Clock.schedule_once(self.draw_card, 2)


    def init_view(self, dtx):

        self.primary = rgba("#2C323C")
        self.back = rgba("#282C34")
        self.danger = rgba('#ff003f')
        self.secondary = rgba('#ffffff')
        self.tertiary = rgba('#212232')
        self.success = rgba('#05a95c')

        self.card_colors = [
            rgba("#ff621b"),
            rgba("#ff5722"),
            rgba("#c51162"),
            rgba("#f50057"),
            rgba("#ff31432b")]
        # self.primary = rgba("#242c3f")
        # expenses - (card, card_num, expense, cost, paid, recurring, day_paid)
        self.expenses = self.db.get_expenses()
        self.all_expenses = dict()
        self.sample = (0,'sample card | 0123', 'mastercard', '01/94', '2048.00')

        self.cards = [list(x) for x in self.db.get_cards()]
        if len(self.cards) < 1:
            self.cards.append(self.sample)

        self.total_balance = round(sum([float(x[4]) for x in self.cards]), 3)
        bal, c = str(self.total_balance).rsplit('.',1)
        bal = '%s[size=%s]%s[/size]'%(bal,int(sp(10)), c)
        self.ids.total_bal.text = bal

        for e in self.cards:
            key = e[1].upper()
            self.all_expenses[key] = list()

        for e in self.expenses:
            key = ' | '.join([e[1].upper(), e[2]])

            self.all_expenses[key].append(e)

        data = [float(x[4]) for x in self.expenses]
        graph = Graph()
        if len(data) > 2:
            graph.draw_bar(data)

            self.ids.graph_wrapper.add_widget(graph)
        self.data_error(data, graph)

        tcard = self.cards[0][1].upper()
        card_total = sum([float(x[4]) for x in self.all_expenses[tcard.upper()] if x[8] == 'True'])

        if card_total < 1:
            card_total = '0.00'

        total, cents = str(card_total).rsplit('.')
        cents = '[size=%s].%s[/size]'%(int(sp(12)), cents)
        self.ids.card_expense_total.text = ''.join(['$ ', total, cents])

        for ex in self.all_expenses[tcard]:
            ec = ExpenseChip()
            ec.icon = icon('zmdi-store')
            ec.card = ' | '.join([ex[1], ex[2]])
            ec.name = ex[3]
            ec.amount = ex[4]
            ec.size_hint_y = None
            ec.height = sp(42)
            ec.ids.amount.color = rgba('#00ff00') if ex[8] == 'False' else self.danger

            self.ids.cards_expenses.add_widget(ec)
        self.data_error(self.all_expenses[tcard], self.ids.cards_expenses)

        for ex in self.expenses:
            ec = ExpenseChip()
            ec.icon = icon('zmdi-store') if ex[8] == 'True' else icon('zmdi-balance')
            ec.card = ' | '.join([ex[1], ex[2]])
            ec.name = ex[3]
            ec.amount = ex[4]
            ec.size_hint_y = None
            ec.height = sp(42)
            ec.ids.amount.color = rgba('#00ff00') if ex[8] == 'False' else self.danger

            self.ids.overview_history.add_widget(ec)
        self.data_error(self.all_expenses[tcard], self.ids.overview_history)

        for card in self.cards:
            _card, num = card[1].rsplit(' | ',1)
            c = Card()
            c.card_id = card[0]
            c.name = _card.upper()
            c.vendor = card[2]
            c.num = num
            c.exp = card[3]

            sc = Card()
            sc.card_id = card[0]
            sc.name = _card
            sc.vendor = card[2]
            sc.num = num
            sc.exp = card[3]

            balance = card[4] if '.' in card[4] else '.'.join([card[4], '00'])

            bal, cents = balance.rsplit('.',1)

            balance = '%s[size=%s].%s[/size]'%(bal, int(sp(14)), cents)
            c.balance = balance
            sc.balance = balance

            self.ids.cards_wrapper.add_widget(c)
            self.ids.stats_cards.add_widget(sc)
        self.data_error(self.cards, self.ids.stats_cards)
        self.data_error(self.cards, self.ids.cards_wrapper)
            # ToDo - Allow rotation
            # if Window.width < Window.height or len(self.ids.cards_wrapper.children) > 0: #landscape mode
            #     break
            # else:
            #     self.ids.cards_wrapper.spacing = sp(15)

        #init tabs
        self.ids.default_tab.state = 'down'

        tcard = self.cards[0][1].upper()
        self.update_stats(self.all_expenses[tcard])

        # Add Recurring expenses
        # expenses - (card, card_num, expense, cost, paid, recurring, date_paid)
        recurring = [x for x in self.all_expenses[tcard] if x[6] == 'True']
        # print(ipoints)

        for r in recurring:
            ep = ExpenseProgress()
            ep.max = float(r[4])
            ep.value = float(r[5])
            ep.name = r[3].lower()
            ep.size_hint_y = None
            ep.height = sp(18)

            self.ids.recurring_wrapper.add_widget(ep)
        self.data_error(recurring, self.ids.recurring_wrapper)

    def data_error(self, expenses, w):
        lbl = Label(text='no data to show', shorten=True)
        lbl.shorten_from='right'
        lbl.color=rgba('#ffffff42')
        lbl.text_size = lbl.size
        lbl.valign = 'middle'
        lbl.halign = 'center'

        if len(expenses) == 0:

            print(w)
            w.add_widget(lbl)

    def update_stats(self, expenses):
        ipoints = self.get_points(expenses)
        try:
            ymax = max(ipoints, key=lambda x: x[1])[1]
            # xmax = max(ipoints, key=lambda x: x[0])
        except ValueError:
            ymax = 100

        self.ids.stats_graph.y_ticks_major = math.ceil(ymax/9)
        self.ids.stats_graph.ymax = ymax

        self.plot = LinePlot(color=self.danger)
        self.plot.line_width = 1.4
        self.plot.points = ipoints
        self.ids.stats_graph.add_plot(self.plot)

    def get_points(self, expenses):
        points = [(int(x[7].split('/',1)[0]), float(x[4])) for x in expenses]
        points.insert(0, (0,0))
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

        return ipoints

    def view_stats(self, carousel, next=0):
        try:
            if next == 0:
                cname = carousel.next_slide.name
                cnum = carousel.next_slide.num
                carousel.load_next()
            elif next == 1:
                cname = carousel.previous_slide.name
                cnum = carousel.previous_slide.num
                carousel.load_previous()
            else:
                cname = carousel.current_slide.name
                cnum = carousel.current_slide.num

            tcard = ' | '.join([cname, cnum])

            # sample - ('paypal prepaid', '2519', 'GoDaddy', '3.65', '3.65', 'True', '27')
            self.ids.stats_graph.remove_plot(self.plot)
            self.update_stats(self.all_expenses[tcard.upper()])

            self.ids.recurring_wrapper.clear_widgets()
            recurring = [x for x in self.all_expenses[tcard.upper()] if x[6] == 'True']
            # print(ipoints)

            for r in recurring:
                ep = ExpenseProgress()
                ep.max = float(r[4])
                ep.value = float(r[5])
                ep.name = r[3].lower()
                ep.size_hint_y = None
                ep.height = sp(18)

                self.ids.recurring_wrapper.add_widget(ep)

            self.data_error(recurring, self.ids.recurring_wrapper)

        except AttributeError:
            pass
            # self.graph.remove_plot(self.plot)

    def view_expenses(self, carousel, next=0):
        try:
            if next == 0:
                cname = carousel.next_slide.name
                cnum = carousel.next_slide.num
                carousel.load_next()
            elif next == 1:
                cname = carousel.previous_slide.name
                cnum = carousel.previous_slide.num
                carousel.load_previous()
            else:
                cname = carousel.current_slide.name
                cnum = carousel.current_slide.num

            tcard = ' | '.join([cname, cnum])
            card_total = sum([float(x[5]) for x in self.all_expenses[tcard.upper()] if x[8] == 'True'])

            card_total = round(card_total,2)
            if card_total == 0:
                card_total = '0.00'

            total, cents = str(card_total).rsplit('.')
            cents = '[size=%s].%s[/size]'%(int(sp(12)), cents)
            self.ids.card_expense_total.text = ''.join(['$ ', total, cents])

            self.ids.cards_expenses.clear_widgets()
            for ex in self.all_expenses[tcard.upper()]:
                ec = ExpenseChip()
                ec.icon = icon('zmdi-store')
                ec.card = ' | '.join([ex[1], ex[2]])
                ec.name = ex[3]
                ec.amount = ex[5]
                ec.size_hint_y = None
                ec.height = sp(42)
                ec.ids.amount.color = rgba('#00ff00') if ex[8] == 'False' else self.danger

                self.ids.cards_expenses.add_widget(ec)
        except AttributeError:
            pass

    def add_new(self, modal, add='card'):
        modal.dismiss()

        fv = ModalView(size_hint=[.8, .5], padding=sp(10))

        if add == 'card':
            nc = NewCard()
            nc.ids.submit.bind(on_release=lambda x: self.new_card(fv, nc))

            fv.add_widget(nc)
        elif add == 'deposit':
            nd = NewDeposit()
            nd.ids.submit.bind(on_release=lambda x: self.new_deposit(fv, nd))

            fv.add_widget(nd)
        else:
            ne = NewExpense()
            ne.ids.submit.bind(on_release=lambda x: self.new_expense(fv, ne))
            fv.add_widget(ne)

        fv.open()

    def new_card(self, modal, obj):
        modal.dismiss()

        name = obj.ids.name.text.upper()
        num = obj.ids.num.text
        vendor = obj.ids.vendor.text
        exp = obj.ids.date.text
        balance = obj.ids.balance.text

        if len(name) > 3 and len(num) == 4 and vendor is not 'card vendor' and len(exp) > 3 and len(balance) > 1:

            balance = balance if '.' in balance else '.'.join([balance, '00'])

            _balance = balance
            bal, cents = balance.rsplit('.',1)

            balance = '%s[size=%s].%s[/size]'%(bal, int(sp(14)), cents)

            m, y = exp.rsplit('/',1)
            y = y[2:]
            exp = '/'.join([m,y])

            # ToDo: Add Card To DB
            # ('sample card', 'mastercard', '0123', '01/94', '2048.00')
            key = ' | '.join([name.upper(), num])
            new_card = [key, vendor, exp, _balance]
            cid = self.db.add_card(new_card)

            if not cid == -1:
                new_card.insert(0, cid)
                self.cards.append(new_card)
                self.all_expenses[key] = list()

                card = Card()
                card.card_id = cid
                card.balance = balance
                card.name = name
                card.exp = exp
                card.vendor = vendor
                card.num = num

                scard = Card()
                scard.card_id = cid
                scard.balance = balance
                scard.name = name
                scard.exp = exp
                scard.vendor = vendor
                scard.num = num

                cw = self.ids.cards_wrapper
                sc = self.ids.stats_cards
                cw.add_widget(card)
                sc.add_widget(scard)

                for c in cw.slides:
                    if c.card_id == 0:
                        cw.remove_widget(c)

                for c in sc.slides:
                    if c.card_id == 0:
                        sc.remove_widget(c)

                self.total_balance = round(sum([float(x[4]) for x in self.cards]), 3)
                bal, c = str(self.total_balance).rsplit('.',1)
                bal = '%s[size=%s]%s[/size]'%(bal,int(sp(10)), c)
                self.ids.total_bal.text = bal



    def new_deposit(self, modal, obj):
        modal.dismiss()

        amount = obj.ids.amount.text
        name = obj.ids.name.text
        card = obj.ids.card.text
        date = obj.ids.date.text

        if len(amount) > 0 and len(name) > 2 and card is not 'Deposit Card':

            amount = amount if '.' in amount else '.'.join([amount, '00'])

            bal, cents = amount.rsplit('.',1)
            # expenses - (card, card_num, expense, cost, paid, recurring, day_paid)
            c, n = card.rsplit(' | ',1)
            new_expense = [c, n, name, amount, amount, 'False', date, 'False']

            eid = self.db.add_expense(new_expense)

            if not eid == -1:
                for c in self.cards:
                    if c[1] == card:
                        prev_bal = c[4]

                        _balance = round(float(prev_bal) + float(amount), 3)
                        c[4] = str(round(_balance,3))
                        break

                for c in self.ids.cards_wrapper.slides:
                    name = ' | '.join([c.name, c.num])
                    if name == card:
                        _b,_c = str(_balance).rsplit('.',1)
                        _bal = "%s[size=%s].%s[/size]"%(_b,int(sp(10)),_c)

                        c.balance = _bal
                        self.db.update_card((_balance, c.card_id))

                new_expense.insert(0, eid)
                self.expenses.append(new_expense)
                self.all_expenses[card].append(new_expense)
                amount = '%s[size=%s].%s[/size]'%(bal, int(sp(14)), cents)

                self.total_balance = round(sum([float(x[4]) for x in self.cards]), 3)
                bal, c = str(self.total_balance).rsplit('.',1)
                bal = '%s[size=%s]%s[/size]'%(bal,int(sp(10)), c)
                self.ids.total_bal.text = bal

                ec = ExpenseChip()
                ec.icon = icon('zmdi-balance')
                ec.card = card
                ec.name = name
                ec.amount = amount
                ec.size_hint_y = None
                ec.height = sp(42)
                ec.ids.amount.color = rgba('#00ff00')

                idx = len(self.ids.overview_history.children)
                self.ids.overview_history.add_widget(ec, idx)

                self.view_stats(self.ids.stats_cards, -1)
                self.view_expenses(self.ids.cards_wrapper, -1)

    def new_expense(self, modal, obj):
        modal.dismiss()

        name = obj.ids.name.text
        cost = obj.ids.cost.text
        day = obj.ids.day.text
        card = obj.ids.card.text
        recurring = obj.ids.recurring.state
        paid = obj.ids.paid.state

        if len(cost) > 0 and len(name) > 2 and card is not 'Expense Card':
            cost = cost if '.' in cost else '.'.join([cost, '00'])
            _cost = cost

            bal, cents = cost.rsplit('.',1)

            cost = '%s[size=%s].%s[/size]'%(bal, int(sp(14)), cents)

            # expenses - (card, card_num, expense, cost, paid, recurring, day_paid)
            c, n = card.rsplit(' | ',1)
            if recurring == 'down':
                sub = 'True'
            else:
                sub = 'False'

            new_expense = [c, n, name, _cost, _cost, sub, day, 'True']

            eid = self.db.add_expense(new_expense)

            if eid is not -1:
                for c in self.cards:
                    if c[1] == card:
                        prev_bal = c[4]
                        _balance = round(float(prev_bal) - float(_cost), 3)
                        c[4] = str(round(_balance,3))
                        break

                for c in self.ids.cards_wrapper.slides:
                    name = ' | '.join([c.name, c.num])
                    if name == card:
                        _b,_c = str(_balance).rsplit('.',1)
                        _bal = "%s[size=%s].%s[/size]"%(_b,int(sp(10)),_c)

                        c.balance = _bal
                        self.db.update_card((_balance, c.card_id))

                new_expense.insert(0, eid)
                self.expenses.append(new_expense)
                self.all_expenses[card.upper()].append(new_expense)

                self.total_balance = round(sum([float(x[4]) for x in self.cards]), 3)
                bal, c = str(self.total_balance).rsplit('.',1)
                bal = '%s[size=%s]%s[/size]'%(bal,int(sp(10)), c)
                self.ids.total_bal.text = bal

                if recurring == 'down':
                    ep = ExpenseProgress()
                    ep.size_hint_y = None
                    ep.height = sp(18)

                    ep.name = name
                    ep.max = float(_cost)
                    if paid == 'down':
                        ep.value = float(_cost)
                    else:
                        ep.value = 0

                    self.ids.recurring_wrapper.add_widget(ep)

                ec = ExpenseChip()
                ec.icon = icon('zmdi-store')
                ec.card = card
                ec.name = name
                ec.amount = cost
                ec.size_hint_y = None
                ec.height = sp(42)

                idx = len(self.ids.overview_history.children)
                self.ids.overview_history.add_widget(ec, idx)

                self.view_stats(self.ids.stats_cards, -1)
                self.view_expenses(self.ids.cards_wrapper, -1)

    def add_expense(self):
        fv = ModalView(size_hint=[.6, .3], padding=sp(10))
        btn_card = Button(text='Add New Card', background_color=rgba('#2073B5'), background_normal='')
        btn_card.bind(on_release=lambda x: self.add_new(fv, 'card'))

        btn_expense = Button(text='Add New Expense', background_color=rgba('#2073B5'), background_normal='')
        btn_expense.bind(on_release=lambda x: self.add_new(fv, 'expense'))

        btn_deposit = Button(text='Add New Deposit', background_color=rgba('#2073B5'), background_normal='')
        btn_deposit.bind(on_release=lambda x: self.add_new(fv, 'deposit'))
        ctn = Container(orientation='vertical')
        ctn.spacing = sp(15)
        ctn.elevation = 4
        ctn.add_widget(btn_card)
        ctn.add_widget(btn_expense)
        ctn.add_widget(btn_deposit)

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
