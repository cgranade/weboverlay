#!/usr/bin/python

##
# simplestatus.py: shows a simple status icon in the tray.
##
# (c) 2010 Christopher E. Granade (cgranade@gmail.com).
# Licensed under GPL v3.
##
# WARNING: This is still a proof of concept. Do not use it
#     without improving it first, unless you plan on filing bug
#     reports.
##

import pygtk
pygtk.require('2.0')
import gtk

class SimpleStatus(object):
    def __init__(self, stock_name=None, tooltip=None):
    
        self.status_icon = gtk.StatusIcon()
        if stock_name:
            self.status_icon.set_from_stock("gtk-apply")
        
        self.status_icon.connect("activate", self.on_activate)
        self.status_icon.connect("popup-menu", self.on_status_popup)
        
        if tooltip:
            self.status_icon.set_tooltip(tooltip)
        
    def get_status_icon(self):
        return self.status_icon
        
    def get_menu(self):
        return None
        
    def on_activate(self, widget, data=None):
        pass
        
    def on_status_popup(self, icon, button, activate_time, user_data=None):
        if self.get_menu():
            self.popup_menu.popup(None, None, None, button, activate_time, None)
         
    def make_menu_item(self, formenu, activate_cb, label=None, icon=None, accel_key=None, accel_grp=None):
        if icon:
            agr = accel_grp or self.agr
            item = gtk.ImageMenuItem(icon, agr)
            k, m = gtk.accelerator_parse(accel_key)
            item.add_accelerator("activate", agr, k, m, gtk.ACCEL_VISIBLE)
        elif label:
            item = gtk.MenuItem(label)
        else:
            # TODO: throw error
            return
        item.connect("activate", activate_cb)
        formenu.append(item)
        item.show()
        return item
        
