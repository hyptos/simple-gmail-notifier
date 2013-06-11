#import gi
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import httplib2
import xml.etree.ElementTree as etree
import webbrowser
import sys

class GmailConnection:
	def __init__(self, username, password):
		self.username = username
		self.password = password
	
	def getNewMails(self, url):
		h = httplib2.Http('.cache')
		h.add_credentials(self.username, self.password)
		resp, content = h.request(url)
		root = etree.fromstring(content)
		fullcount = root.find('{http://purl.org/atom/ns#}fullcount')
		return fullcount.text

	def openbrowser(self, menu_item, menu):
		webbrowser.open('https://mail.google.com/mail/')
		#self.quit()
		Gtk.main_quit()
	
	def notify(self, n):
		ind = appindicator.Indicator.new("example-simple-client", "indicator-messages", appindicator.IndicatorCategory.APPLICATION_STATUS) 
		ind.set_status(appindicator.IndicatorStatus.ACTIVE)
		ind.set_attention_icon("indicator-messages-new")
		
		menu = Gtk.Menu()
		
		s = "Tienes %s correos nuevos" % n
		menu_item = Gtk.MenuItem(s)
		menu.append(menu_item)
		
		menu_item.connect("activate", self.openbrowser, menu)
		menu_item.show()
		
		ind.set_menu(menu)
		Gtk.main()
	def quit(self):
		sys.exit(0)



if __name__ == "__main__":
	g = GmailConnection(gmail, password)
	
	n = g.getNewMails('https://mail.google.com/mail/feed/atom')
	if int(n) > 0:
		g.notify(n)

