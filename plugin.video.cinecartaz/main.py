#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos email: MafaStudios@gmail.com
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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,json

addon_id = 'plugin.video.cinecartaz'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = os.path.join(addonfolder,'resources','img')
fanart = os.path.join(addonfolder,'fanart.png')
mainURL = 'http://cinecartaz.publico.pt'

def CATEGORIES():
	addDir('Filmes em Destaque',mainURL,1,'')
	addDir('Estreias',mainURL+'/Estreias',5,'')
	addDir('Brevemente',mainURL+'/Brevemente',5,'')	
	addDir('Trailers',mainURL+'/Trailers',1,'')

def list_trailers(url):
	trailers = open_url(url)
	section = re.compile('<ul class="blocklist posterlist">(.+?)</ul>', re.DOTALL).findall(trailers)
	for s in section:
		trailer = re.compile('<a href="(.+?)" title="(.+?)" class=".+?">\s+<img src="(.+?)" width="\d+" height="\d+" alt=".+?" />', re.DOTALL).findall(s)
		counttrailers = len(trailer)
		for url,title,thumb in trailer:
			thumb = thumb.replace('&amp;w=140&amp;h=190&amp;act=cropResize','')
			addDir(title,mainURL+url.replace('/Filme/','/Trailer/'),3,thumb,False,counttrailers,searchmovie(mainURL+url.replace('/Trailer/','/Filme/'),thumb))
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin('Container.SetViewMode(500)')

def list_estreias(url):
	estreias = open_url(url)
	section = re.compile('<h2 class="boxtitle first"><span>(.+?)</span></h2>', re.DOTALL).findall(estreias)
	for s in section:
		addDir(s,url,6,'',True,1)
	#xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	#if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin('Container.SetViewMode(500)')

def list_estreias2(name,url):
	estreias = open_url(url)
	searchstring = '<h2 class="boxtitle first"><span>%s</span></h2>(.+?)</ul>' % name
	section = re.compile(searchstring, re.DOTALL).findall(estreias)
	for s in section:
		trailer = re.compile('<a href="(.+?)" title="(.+?)" class=".+?">\s+<img src="(.+?)" width="\d+" height="\d+" alt=".+?" />', re.DOTALL).findall(s)
		counttrailers = len(trailer)
		for url,title,thumb in trailer:
			thumb = thumb.replace('&amp;w=140&amp;h=190&amp;act=cropResize','')		
			addDir(title,mainURL+url.replace('/Filme/','/Trailer/'),3,thumb,False,counttrailers,searchmovie(mainURL+url,thumb))
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin('Container.SetViewMode(500)')
	
def play_trailer(url):
	trailerpage = open_url(url)
	trailer = re.compile('dfpVideoFile = "(.+?)";', re.DOTALL).findall(trailerpage)
	try: 
		url = trailer[0]
		play(url)	
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok("Cinecartaz", "Sem trailer disponível")	

def play(url):
	listitem = xbmcgui.ListItem()
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		pass

def searchmovie(url,thumb):
	listgenre = []
	listcast = []
	listcastr = []	
	genre = ''
	title = ''
	plot = ''
	year = ''
	tagline = ''
	director = ''
	writer = ''
	credits = ''
	poster = thumb
	fanart = ''
	temptitle = ''
	originaltitle = ''
	duration = ''
	page = open_url(url)
	genr = re.compile('<dt>G&eacute;nero:</dt><dd>(.+?)</dd>', re.DOTALL).findall(page)
	mpa = re.compile('<dt>Classifica&ccedil;&atilde;o:</dt><dd>(.+?)</dd>', re.DOTALL).findall(page)
	titl = re.compile('<div class="box">\s+<h2>(.+?)</h2>', re.DOTALL).findall(page)
	originaltitl = re.compile('<dt>Título original:</dt><dd>(.+?)</dd>', re.DOTALL).findall(page)
	directo = re.compile('<dt>De:</dt><dd><a target="_blank" href=".+?">(.+?)</a></dd>', re.DOTALL).findall(page)
	try: 
		anotherdata = re.compile('<dt>Outros dados:</dt><dd>(.+?), (.+?), .+?, (.+?) min.</dd>', re.DOTALL).findall(page)[0]
		duration = int(anotherdata[2])*60
		year = anotherdata[1]
	except: pass
	try: v = re.compile('total de (\d{1,9}) votos', re.DOTALL).findall(page)[0]
	except: v = ''
	try: c = re.compile('name="newrate"value="(\d)"title="\w+"checked', re.DOTALL).findall(page.replace('&','').replace(';','').replace(' ',''))[0]
	except: c = ''
	try:
		castarea = re.compile('dt>Com:</dt><dd>(.+?)</dd>', re.DOTALL).findall(page)[0]
		cast = re.compile('<a target="_blank" href=".+?">(.+?)</a>', re.DOTALL).findall(castarea)
		for a in cast: listcast.append(a)
	except: pass
	try: plot = re.compile('<meta name="description" content="(.+?)" />', re.DOTALL).findall(page)[0]
	except: pass
	try: genre = genr[0]
	except: genre = ''
	try: mpaa = mpa[0]
	except: mpaa = ''
	try: originaltitle = originaltitl[0]
	except: originaltitle = ''
	try: title = titl[0]
	except: title = ''
	try: director = directo[0]
	except: director = ''
	try:
		if 'static.publico.pt' in thumb:
				jsonpage = open_url('http://www.omdbapi.com/?plot=short&r=json&t='+urllib.quote_plus(originaltitle))
				jdef = json.loads(jsonpage)
				thumb = jdef['Poster']
	except: pass
	info = {
			"genre": genre,
			"mpaa": mpaa,
			"originaltitle": originaltitle,	
			"title": title,
			"director": director,
			"cast": listcast,
			"plot": plot,
			"duration": duration,
			"year": year,
			"votes": v,
			"rating": float(c)*2,
			"poster": thumb
			}
	return info
	
def open_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,plot='',fromSection=None):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta=True,total=1,info=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	if info <> '':
		if 'static.publico.pt' in iconimage: 
			try: iconimage= re.compile("'poster': u'(.+?)',", re.DOTALL).findall(str(info))[0]
			except: pass
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	if info <> '': liz.setInfo( type="Video", infoLabels=info )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: list_trailers(url)
elif mode==3: play_trailer(url)
elif mode==4: play(url)
elif mode==5: list_estreias(url)
elif mode==6: list_estreias2(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
