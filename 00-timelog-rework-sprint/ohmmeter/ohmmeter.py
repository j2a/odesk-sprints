#!/usr/bin/env python

import gtk
import gobject
import datetime
import odesk
import climeter
import ConfigParser

def get_odesk_client():
    cfg = ConfigParser.ConfigParser()
    cfg.read(['creds.ini'])
    creds = (
        cfg.get('odesk-auth', 'public-key'),
        cfg.get('odesk-auth', 'secret-key'),
        cfg.get('odesk-auth', 'token'))
    client = odesk.Client(*creds)
    return client


class OhmMeter(gtk.StatusIcon):
    def __init__(self, *args, **kwargs):
        gtk.StatusIcon.__init__(self, *args, **kwargs)
        self.set_from_stock(gtk.STOCK_FIND)
        self.set_tooltip('Fetching')
        self._init_menu()
        self.cb_refresh()
        gobject.timeout_add_seconds(10*60, self.cb_refresh)

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
        if not getattr(self, 'odesk_client', None):
            self.odesk_client = get_odesk_client()
        meter = climeter.by_workdiary(self.odesk_client)
        tooltip = "Your workload for today: %s\n" % meter.pop('overall')
        for team in sorted(meter):
            if meter[team]:
                tooltip += "\nTeam %s: %s" %(team, meter[team])
        self.set_tooltip(tooltip)
        # Should return false to loop with timeout
        return False

def main():
    ohmmeter = OhmMeter()
    gtk.main()

if __name__ == '__main__':
    main()
