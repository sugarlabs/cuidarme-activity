# -*- coding: utf-8 -*-

import olpcgames
import pygame
import gtk

from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton
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

        separator = gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        separator = gtk.SeparatorToolItem()
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