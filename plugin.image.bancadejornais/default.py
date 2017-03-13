#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2013~2017 enen92 & Leinad4Mind
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs

addon_id = 'plugin.image.bancadejornais'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/icons/'
sitio = 'http://24.sapo.pt/jornais'


def CATEGORIES():
	addDir('[B]Nacional[/B]',sitio+'/nacional/',1, addonfolder + artfolder + 'nacional.png')
	addDir('[B]Desporto[/B]',sitio+'/desporto/',1, addonfolder + artfolder + 'desporto.png')
	addDir('[B]Economia[/B]',sitio+'/economia/',1, addonfolder + artfolder + 'economia.png')
	addDir('[B]Local[/B]',sitio+'/local/',1, addonfolder + artfolder + 'local.png')
	addDir('[B]Lusofonia[/B]',sitio+'/lusofonia/',1, addonfolder + artfolder + 'local.png')
	addDir('[B]Internacional[/B]',sitio+'/internacional/',1, addonfolder + artfolder + 'internacional.png')
	addDir('[B]Revistas[/B]',sitio+'/revistas/',1, addonfolder + artfolder + 'revistas.png')
		
		
		

def jornal_list(url):
	link = abrir_url(url)
	match=re.compile('img data-src="(//thumbs.web.sapo.io/\?epic=.+?)(&.+?)" src=".+?" alt="(.+?)"').findall(link)
	totalitems = len(match)
	for img,thumbnail,titulo in match:
			imagem = urllib.unquote('http:'+img+'&W=1520&H=0&delay_optim=1&tv=1&crop=center')
			thumbs = urllib.unquote('http:'+img+'&W=520&H=0&delay_optim=1&tv=1&crop=center')
			addLink('[B]' + titulo + '[/B]',imagem,thumbs,totalitems)
	xbmc.executebuiltin("Container.SetViewMode(500)")


 
############################################################################################################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

				
def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
				params=sys.argv[2]
				cleanedparams=params.replace('?','')
				if (params[len(params)-1]=='/'):
						params=params[0:len(params)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]
								
		return param




def addLink(name,url,thumbs,number_of_items):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbs)
	liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.jpg')
	liz.setInfo( type='image', infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=number_of_items)
	return ok


def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name })
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
		
			  
params=get_params()
url=None
name=None
mode=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
		print ""
		CATEGORIES()
	   
	   
elif mode==1:
		print ""
		jornal_list(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
