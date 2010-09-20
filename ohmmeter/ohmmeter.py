#!/usr/bin/env python

import gtk
import datetime

class OhmMeter(gtk.StatusIcon):
    def __init__(self, *args, **kwargs):
        gtk.StatusIcon.__init__(self, *args, **kwargs)
        self.set_from_stock(gtk.STOCK_FIND)
        self.set_tooltip('Fetching')
        self._init_menu()

    def _init_menu(self):
        menu = gtk.Menu()
        refresh_item = gtk.MenuItem(label="Refresh")
        refresh_item.connect("activate", self.cb_refresh)
        refresh_item.show()

        quit_item = gtk.MenuItem(label="Quit")
        quit_item.connect('activate', self.cb_quit)
        quit_item.show()

        menu.append(refresh_item)
        menu.append(quit_item)

        self.connect('popup-menu', self.cb_popup, menu)


    def cb_popup(self, tray, button, atime, menu):
        menu.popup(None, None, None, button, atime, None)


    def cb_quit(self, *args, **kwargs):
        gtk.main_quit()

    def cb_refresh(self, *args, **kwargs):
        self.set_tooltip("Wooohooo %s" % datetime.datetime.utcnow())

def main():
    ohmmeter = OhmMeter()
    gtk.main()

if __name__ == '__main__':
    main()
