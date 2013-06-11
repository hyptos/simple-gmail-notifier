#import gi
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import httplib2
import xml.etree.ElementTree as etree
import webbrowser

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

	def openbrowser(self):
		webbrowser.open('https://mail.google.com/mail/')
	
	def notify(self, n):
		ind = appindicator.Indicator.new("example-simple-client", "indicator-messages", appindicator.IndicatorCategory.APPLICATION_STATUS) 
		ind.set_status(appindicator.IndicatorStatus.ACTIVE)
		ind.set_attention_icon("indicator-messages-new")
		
		menu = Gtk.Menu()
		
		s = "Tienes %s correos nuevos" % n
		menu_item = Gtk.MenuItem(s)
		menu.append(menu_item)
		
		#menu_item.connect("activate", self.openbrowser(), s)
		menu_item.show()
		
		ind.set_menu(menu)
		Gtk.main()



if __name__ == "__main__":
	g = GmailConnection('lukas.zorich@gmail.com', 'udechile')
	
	n = g.getNewMails('https://mail.google.com/mail/feed/atom')
	if int(n) > 0:
		g.notify(n)

