# -*- coding: utf-8 -*-

import olpcgames
from gi.repository import Gtk

from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbarbox import ToolbarBox
from gettext import gettext as _


class Cuidarme2Activity(olpcgames.PyGameActivity):
    game_name = 'Juego'
    game_title = _('Cuidarme 2')
    game_size = None

    def build_toolbar(self):

        toolbar_box = ToolbarBox()
        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_size_request(0, -1)
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show_all()

        return toolbar_box
