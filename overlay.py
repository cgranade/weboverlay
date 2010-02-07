#!/usr/bin/python

##
# overlay.py: small daemon for showing web pages in an overlay
##
# (c) 2010 Christopher E. Granade (cgranade@gmail.com).
# Licensed under GPL v3.
##
# This file is a part of the weboverlay project.
# http://github.com/cgranade/weboverlay
##
# WARNING: This is still a proof of concept. Do not use it
#     without improving it first, unless you plan on filing bug
#     reports.
##

import pygtk
pygtk.require('2.0')
import gtk

import webkit
import yaml

from simplestatus import SimpleStatus

class OverlayConfiguration(object):
    def __init__(self, name="Unnamed Web Overlay", url=None, user_agent=None, size=(100,100)):
        self.name = name
        self.url = url
        self.user_agent = user_agent
        self.size = size
        
    def get_name(self):
        return self.name
        
    def get_initial_url(self):
        return self.url
        
    def get_user_agent(self):
        return self.user_agent
        
    def get_size(self):
        return self.size

def load_configurations():
    yaml_doc = """
    - name: Google Tasks
      url: https://mail.google.com/tasks/ig
      size: [ 300, 500 ]
    """
       
    return map(lambda d: OverlayConfiguration(**d), yaml.safe_load(yaml_doc))

class OverlayWindow(object):
    visible = False

    def __init__(self, conf):
        
        self.conf = conf
        
        # Initialize and configure the window.
        self.window = gtk.Window()
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)
        self.window.set_decorated(False)
        #self.window.set_keep_above(True)
        self.window.set_default_size(*(self.conf.get_size()))
        
        # Make a browser.
        self.browser = webkit.WebView()
        try:
            self.browser.get_settings().set_property('user-agent', self.conf.get_user_agent())
        except TypeError:
            print "[DEBUG] Could not set user agent string. Consider upgrading pywebkitgtk to version 1.1.11 or later."
        
        # Pack the browser in a scollbox.
        scroller = gtk.ScrolledWindow()
        scroller.add(self.browser)
        
        # Pack the browser in a box.
        box = gtk.VBox(homogeneous=False, spacing=0)
        box.add(scroller)
        box.pack_start(scroller, expand=True, fill=True, padding=0)
        self.window.add(box)
        
        # Show everything but the window itself.
        box.show()
        scroller.show()
        self.browser.show()
        
        # Connect events.
        self.window.connect('focus-out-event', self.on_lost_focus)
        
        # Open a default page.
        self.browser.open(self.conf.get_initial_url())
        
    def toggle_show(self, x=0, y=0):
        if not self.visible:
            self.visible = True
            self.window.move(x,y)
            self.window.show()
            self.window.present()
        else: self.hide()
        
    def on_lost_focus(self, widget, event, data=None):
        self.hide()
        
    def hide(self):
        self.visible = False
        self.window.hide()

class OverlayStatus(SimpleStatus):
    def __init__(self, for_overlay, tooltip=None):
        SimpleStatus.__init__(self, stock_name="gtk-apply", tooltip=tooltip)
        self.overlay = for_overlay
        self.popup_menu = self.make_menu()
        
    def show_overlay(self):
        screen, mouse_x, mouse_y, mask = self.get_status_icon().get_screen().get_display().get_pointer()
        self.overlay.toggle_show(mouse_x, mouse_y)
        
    def make_menu(self):
        menu = gtk.Menu()
        
        self.agr = gtk.AccelGroup()
        
        #pref_item = self.make_menu_item(menu, self.on_pref_item_activate, accel_key="P", icon=gtk.STOCK_PREFERENCES)
        quit_item = self.make_menu_item(menu, self.on_quit, accel_key="Q", icon=gtk.STOCK_QUIT)
        
        return menu
        
    def get_menu(self):
        return self.popup_menu
                
    def on_activate(self, widget, data=None):
        # Overrides base class.
        self.show_overlay()
            
    def on_quit(self, widget, data=None):
        gtk.main_quit()
        
class Main(object):
    def __init__(self):        
        self.conf_list = load_configurations()
        self.overlay_statuses = list()
    
        for conf in self.conf_list:
            print conf
            overlay = OverlayWindow(conf)
            self.overlay_statuses.append(OverlayStatus(overlay, tooltip=conf.get_name()))
        
    def on_show_overlay(self, widget, data=None):
        screen, mouse_x, mouse_y, mask = self.status_icon.get_status_icon().get_screen().get_display().get_pointer()
        self.overlay.toggle_show(mouse_x, mouse_y)
        
    def main(self):
        gtk.main()

# This code amuses me... providing several ways of running the module.

def main():
    mainMain = Main()
    mainMain.main()

if __name__ == "__main__":
    main()
    
