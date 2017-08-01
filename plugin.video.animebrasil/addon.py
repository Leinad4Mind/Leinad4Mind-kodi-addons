#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# By AddonBrasil & Leinad4Mind
#########################################################################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, HTMLParser, sys

from xbmcgui import ListItem
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup


addon_id    = 'plugin.video.animebrasil'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
setting     = selfAddon.getSetting
artfolder   = addonfolder + '/resources/img/'
fanart      = addonfolder + '/fanart.jpg'
base        = 'uggcf://navghor.vasb'
base        = base.decode('rot13')

def menuPrincipal():
		if setting('genero-disable') == 'false':      addDir2('Gêneros'    , base + '/genero'            , 10, artfolder + 'categorias.jpg')
		if setting('lancamentos-disable') == 'false': addDir2('Lançamentos', base + '/animes-lancamentos', 20, artfolder + 'recentes.jpg')
		if setting('legendados-disable') == 'false':  addDir2('Legendados' , base + '/anime'             , 30, artfolder + 'comentados.jpg')
		if setting('dublados-disable') == 'false':    addDir2('Dublados'   , base + '/animes-dublado'    , 30, artfolder + 'populares.jpg')
		if setting('tokusatsu-disable') == 'false':   addDir2('Tokusatsu'  , base + '/tokusatsu'         , 30, artfolder + 'destaque.jpg')
		addDir2('Pesquisa'   , base                        , 99, artfolder + 'pesquisa.jpg')
		xbmc.executebuiltin('Container.SetViewMode(51)')

def getGeneros(url):
		link = openURL(url)

		soup    = BeautifulSoup(link)
		generos = soup.find("div", { "class" : "row" }).findAll('a')
		totG    = len(generos)

		for genero in generos:
				titG  = genero.text.encode('utf-8', 'ignore').replace('<span class="badge"></span>','')
				urlG  = base + genero["href"]
				imgG  = artfolder + 'categorias.jpg'

				addDir(titG, urlG, 11, imgG, True, totG)
		
def getAnimesGen(url):
		link  = openURL(url)
		link  = unicode(link, 'latin', 'ignore')
		link  = link.encode('ascii', 'ignore')

		urlsA = re.findall('<h2 class="go"><a class="internalUrl" href="(.*?)" title="(.*?)" rel="bookmark" itemprop="name">', link)
		imgsA = re.findall('<img class="img-responsive" alt=".*?" title=".*?" src="(.*?)" itemprop="image">', link)

		totA  = len(imgsA)

		try :
				primeira = re.findall('href="(.*?)">Primeiro</a></li>', link)[0]
				anterior = re.findall('href="(.*?)">Voltar</a></li>', link)[0]
				proxima = re.findall('href="(.*?)">Avanar</a></li>', link)[0]
				pa = re.findall('([0-9]+?)$', anterior)[0]
				pd = re.findall('([0-9]+?)$', primeira)[0]
				pp = re.findall('([0-9]+?)$', proxima)[0]
				if (pp != '2'): addDir('. Primeira Página', base + primeira, 11, artfolder + 'pagantr.jpg')
				if (pp != '2'): addDir('<< Página Anterior '+pa, base + anterior, 11, artfolder + 'pagantr.jpg')
		except :
				pass

		for i in range(totA):
				titA = urlsA[i][1].encode('ascii', 'ignore')
				urlA = base + urlsA[i][0]
				imgA = base + imgsA[i]

				addDir(titA, urlA, 31, imgA, True, totA, '')

		try :
				ultima = re.findall('href="(.*?)">ltimo</a></li>', link)[0]
				pu = re.findall('([0-9]+?)$', ultima)[0]
				if (pu != '1'): addDir('Página Seguinte '+pp+' >>', base + proxima, 11, artfolder + 'proxpag.jpg')
				if (pu != '1'): addDir('Última Página '+pu+' >>', base + ultima, 11, artfolder + 'proxpag.jpg')
		except :
				pass
		xbmc.executebuiltin('Container.SetViewMode(500)')

def getLancamentos(url):
		link = openURL(url)

		soup = BeautifulSoup(link)
		episodios = soup.findAll("div", {"class" : "well well-sm"})


		totE = len(episodios)

		try :
				anterior = re.findall('href="(.*?)">Voltar</a></li>', link)[0]
				primeira = re.findall('href="(.*?)">Primeiro</a></li>', link)[0]
				proxima = re.findall('href="(.*?)">Avançar</a></li>', link)[0]
				pa = re.findall('([0-9]+?)$', anterior)[0]
				pd = re.findall('([0-9]+?)$', primeira)[0]
				pp = re.findall('([0-9]+?)$', proxima)[0]
				if (pp != '2'): addDir('. Primeira Página', base + primeira, 20, artfolder + 'pagantr.jpg')
				if (pp != '2'): addDir('<< Página Anterior '+pa, base + anterior, 20, artfolder + 'pagantr.jpg')
		except :
				pass

		for episodio in episodios:
				try :
						titE = episodio.a.img["title"].encode('utf-8', 'ignore')
						urlE = base + episodio.a["href"]
						if episodio.a.img.has_key("src"): imgE = base + episodio.a.img["src"]
						else: imgE = base + episodio.a.img["data-cfsrc"]
						addDir(titE, urlE, 100, imgE, False, totE, '')
				except :
						pass
		try :
				ultima = re.findall('href="(.*?)">Último</a></li>', link)[0]
				pu = re.findall('([0-9]+?)$', ultima)[0]
				if (pu != '1'): addDir('Página Seguinte '+pp+' >>', base + proxima, 20, artfolder + 'proxpag.jpg')
				if (pu != '1'): addDir('Última Página '+pu+' >>', base + ultima, 20, artfolder + 'proxpag.jpg')
		except :
				pass
		xbmc.executebuiltin('Container.SetViewMode(51)')

def getLegendados(url):
		link  = openURL(url)
		link  = unicode(link, 'latin', 'ignore')
		link  = link.encode('ascii', 'ignore')

		urlsA = re.findall('<h2 class="go"><a class="internalUrl" href="(.*?)" title="(.*?)" rel="bookmark" itemprop="name">', link)
		imgsA = re.findall('<img class="img-responsive" alt=".*?" title=".*?" src="(.*?)" itemprop="image">', link)

		totA  = len(imgsA)

		try :
				anterior = re.findall('href="(.*?)">Voltar</a></li>', link)[0]
				primeira = re.findall('href="(.*?)">Primeiro</a></li>', link)[0]
				proxima = re.findall('href="(.*?)">Avanar</a></li>', link)[0]
				pa = re.findall('([0-9]+?)$', anterior)[0]
				pd = re.findall('([0-9]+?)$', primeira)[0]
				pp = re.findall('([0-9]+?)$', proxima)[0]
				if (pp != '2'): addDir('. Primeira Página', base + primeira, 30, artfolder + 'pagantr.jpg')
				if (pp != '2'): addDir('<< Página Anterior '+pa, base + anterior, 30, artfolder + 'pagantr.jpg')
		except :
				pass

		for i in range(totA):
				titA = urlsA[i][1].encode('ascii', 'ignore')
				urlA = base + urlsA[i][0]
				imgA = imgsA[i]
		
				addDir(titA, urlA, 31, imgA, True, totA, '')
		
		try :
				ultima = re.findall('href="(.*?)">ltimo</a></li>', link)[0]
				pu = re.findall('([0-9]+?)$', ultima)[0]
				if (pu != '1'): addDir('Página Seguinte '+pp+' >>', base + proxima, 30, artfolder + 'proxpag.jpg')
				if (pu != '1'): addDir('Última Página '+pu+' >>', base + ultima, 30, artfolder + 'proxpag.jpg')
		except :
				pass
		xbmc.executebuiltin('Container.SetViewMode(500)')

def getEpsLegendados(url):
		link = openURL(url)
		soup = BeautifulSoup(link, convertEntities=BeautifulSoup.HTML_ENTITIES)
		eps  = soup.findAll("div", { "class" : "well well-sm" }) 

		plotE = re.findall('<span itemprop="description">\s*(.*?)</span>', link, re.DOTALL|re.MULTILINE)[0]
		plotE = unicode(BeautifulStoneSoup(plotE,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )).encode('utf-8')
		plotE = BeautifulSoup(plotE.replace("<br>"," ")).text

		totE = len(eps)

		try :
				anterior = re.findall('href="(.*?)">Voltar</a></li>', link)[0]
				primeira = re.findall('href="(.*?)">Primeiro</a></li>', link)[0]
				proxima = re.findall('href="(.*?)">Avançar</a></li>', link)[0]
				pa = re.findall('([0-9]+?)$', anterior)[0]
				pd = re.findall('([0-9]+?)$', primeira)[0]
				pp = re.findall('([0-9]+?)$', proxima)[0]
				if (pp != '2'): addDir('. Primeira Página', base + primeira, 31, artfolder + 'pagantr.jpg')
				if (pp != '2'): addDir('<< Página Anterior '+pa, base + anterior, 31, artfolder + 'pagantr.jpg')
		except :
				pass

		for ep in eps:
				try :
						titE = ep.img["title"].encode('ascii', 'ignore')
						urlE = base + ep.a["href"]
						if ep.a.img.has_key("src"): imgE = ep.a.img["src"]
						else: imgE = ep.a.img["data-cfsrc"]
						addDir(titE, urlE, 100, imgE, False, totE, plotE)
				except:
						pass
				
		try :
				ultima = re.findall('href="(.*?)">Último</a></li>', link)[0]
				pu = re.findall('([0-9]+?)$', ultima)[0]
				if (pu != '1'): addDir('Página Seguinte '+pp+' >>', base + proxima, 31, artfolder + 'proxpag.jpg')
				if (pu != '1'): addDir('Última Página '+pu+' >>', base + ultima, 31, artfolder + 'proxpag.jpg')
		except :
				pass

def doPlay(url, name, iconimage):
		pagina = openURL(url)
		video = re.compile('src=\"(.*?insertVideo.*?)&nocache=[A-Za-z0-9]*\"').findall(pagina)
		video = str(video).replace("'","").replace("[","").replace("]","")
		xbmc.log(video)
		link = openURL(video)
		xbmc.log(link)
		urls = re.compile("source: '(.*?)',").findall(link)
		xbmc.log(str(urls))
		
		if not urls : return

		index = 0

		if len(urls) > 1 :
				if setting('qualidade-enable') == 'true': index=1
		
				if index == -1 : return
		
		urlVideo = urls[index]
		
		playlist = xbmc.PlayList(1)

		playlist.clear()

		listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		listitem.setProperty('IsPlayable', 'true')

		playlist.add(urlVideo,listitem)
		xbmcPlayer = xbmc.Player()
		xbmcPlayer.play(playlist)

def doPesquisa():
		keyb = xbmc.Keyboard('', 'Pesquisar...')
		keyb.doModal()

		if (keyb.isConfirmed()):
			search = keyb.getText()
			busca = urllib.quote(search)
			url = base + '/busca/?search_query=%s&tipo=desc' % busca
	
			getLancamentos(url)

###################################################################################

def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', iconimage)
		liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		return ok

def addDir2(name,url,mode,iconimage,pasta=True,total=1,plot=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', fanart)
		liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		return ok
	
def openURL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'UCWEB/2.0 (iPad; U; CPU OS 7_1 like Mac OS X; en; iPad3,6) U2/1.0.0 UCBrowser/9.3.1.344')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

###################################################################################

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

params    = get_params()
url       = None
name      = None
mode      = None
iconimage = None

try    : url=urllib.unquote_plus(params["url"])
except : pass

try    : name=urllib.unquote_plus(params["name"])
except : pass

try    : mode=int(params["mode"])
except : pass

try    : iconimage=urllib.unquote_plus(params["iconimage"])
except : pass

if   mode == None : menuPrincipal()
elif mode == 10   : getGeneros(url)
elif mode == 11   : getAnimesGen(url)
elif mode == 20   : getLancamentos(url)
elif mode == 30   : getLegendados(url)
elif mode == 31   : getEpsLegendados(url)
elif mode == 99   : doPesquisa()
elif mode == 100  : doPlay(url, name, iconimage)

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
xbmcplugin.endOfDirectory(int(sys.argv[1]))