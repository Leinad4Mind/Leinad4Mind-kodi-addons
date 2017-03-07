# -*- coding: utf-8 -*-

""" OKGoals
    2015~2017 fightnight/Leinad4Mind
"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,os,re,sys, urllib, urllib2,htmlentitydefs,requests,HTMLParser

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
art=os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'resources','art')
MainURL = 'http://www.okgoals.com/'
TugaURL = 'http://www.goalsoftheworld.tk/goals-in-Portugal.html'
h = HTMLParser.HTMLParser()

def menu_principal():
      addDir(traducao(30010),MainURL,2,os.path.join(art,'ulgolos.png'),1)
      addDir(traducao(30011),TugaURL,7,os.path.join(art,'ligapt.png'),1)
      addDir(traducao(30012),MainURL,3,os.path.join(art,'ugolosl2.png'),1)
      addDir(traducao(30001),MainURL,4,os.path.join(art,'semana.png'),1)
      addDir(traducao(30013),MainURL + 'seasons-archive.php',5,os.path.join(art,'epoca.png'),1)
      addDir(traducao(30002),MainURL,6,os.path.join(art,'lupa.png'),1)
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def ligaportuguesa(url):
      conteudos= re.compile("""class='linkgoal sapo' id='(.+?)'><h1.+?><img.+?src='.+?'.+?><span.+?>(.+?)\((.+?):(.+?)\)\s*-\s*(.+?)\s*([0-9]*)\s*vs\s*([0-9]*)\s*(.+?)</span></h1>""").findall(abrir_url(url))
      from random import randint
      for endereco,data,hora1,hora2,equipa1,resultado1,resultado2,equipa2 in conteudos:
            if len(resultado1)==0 : resultado1=str('#')
            if len(resultado2)==0 : resultado2=str('#')
            addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange](%sh%s)[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hora1,hora2,clean(equipa1.encode('ascii','xmlcharrefreplace')),resultado1,resultado2,clean(equipa2.encode('ascii','xmlcharrefreplace'))),'http://www.goalsoftheworld.tk/getcontent.php?rand=%s&id_results=%s' % (str(randint(1, 100)),endereco),1,os.path.join(art,'pt.png'),len(conteudos),pasta=False)
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def listadeligas(url):
      ligas=re.compile("""<li class='active'><a href='(.+?)' class="menulinks">.+?alt="(.+?)" src="http://www.okgoals.com/images/(.+?)"> (.+?)</span>""").findall(abrir_url(url))
      for endereco,liga,thumb,country in ligas:
            liga=liga.replace('EPL','Premiere League')
            addDir('%s (%s)' % (liga.capitalize().title(),country.capitalize().title()),MainURL + endereco,2,os.path.join(art,thumb),len(ligas))
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def epocasanteriores(url):
      anteriores=re.compile('<a href="([^"]+?)">([^"]+?)</a><BR />').findall(abrir_url(url).replace('amp;',''))
      for endereco,titulo in anteriores:
            addDir(titulo,MainURL + endereco,8,os.path.join(art,'proxima.png'),len(anteriores))
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def request(url,special=False):
      link=abrir_url(url).replace('&nbsp;','')
      if special:
            listagolos=re.compile('<div id=".+?"><a href="(.+?)"><img.+?src="images/(.+?)\..+?" />\s+?([0-9]{4}\.[0-9]{2}\.[0-9]{2})\s*(\([0-9]{2}h[0-9]{2}\))\s*-\s*([A-Za-z ]+?)\s*([0-9]*)\s*-\s*([0-9]*)\s*(.+?)</a></div>').findall(link)
            for endereco,thumb,data,hora,equipa1,resultado1,resultado2,equipa2 in listagolos:
                  addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange]%s[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hora,equipa1,resultado1,resultado2,equipa2),MainURL + endereco,1,os.path.join(art,'%s.png' % (thumb)),len(listagolos),pasta=False)
      else:
            listagolos=re.compile('<div id=".+?"><a href="(.+?)"><img.+?src="images/(.+?)\..+?" />\s+?([0-9]{4}\.[0-9]{2}\.[0-9]{2})\s*(\([0-9]{2}h[0-9]{2}\))\s*-\s*([A-Za-z ]+?)\s*([0-9]*)\s*-\s*([0-9]*)\s*(.+?)</a></div>').findall(link)
            for endereco,thumb,data,hora,equipa1,resultado1,resultado2,equipa2 in listagolos:
                  addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange]%s[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hora,equipa1,resultado1,resultado2,equipa2),MainURL + endereco,1,os.path.join(art,'%s.png' % (thumb)),len(listagolos),pasta=False)

      if re.search('page-start', link):
            try:
                  try:enderecopagina=re.compile('</b> <a href="(.+?)">').findall(link)[0]
                  except: enderecopagina=re.compile('</b><a href="(.+?)">').findall(link)[0]
                  valorpagina=int(re.compile('page-start_from_(.+?)_archive.+?.html').findall(enderecopagina)[0])
                  pagina=int((valorpagina/30)+1)
                  if special==True: mode=8
                  else: mode=2
                  addDir('[COLOR blue][B]%s %s >[/COLOR][/B]' % (traducao(30003),pagina),MainURL + enderecopagina,mode,os.path.join(art,'proxima.png'),1)
            except: pass

      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def captura(name,url):
      link=abrir_url(url)
      linkoriginal = link
      if re.search('okgoals',url):
            goals=True
            '''
            link=link.replace('<div style="float:left;"><iframe','').replace('"contentjogos">','"contentjogos"></iframe>')
            ij=link.find('"contentjogos">')
            link=link[ij:]
            '''
      else: goals=False
      goals=True
      titles=[]; ligacao=[]
      aliezref=int(0)
      aliez=re.compile('<iframe.+?src="http://emb.aliez.tv/(.+?)"').findall(link)
      if aliez:
            for codigo in aliez:
                  aliezref=int(aliezref + 1)
                  if len(aliez)==1: aliez2=str('')
                  else: aliez2=' #' + str(aliezref)
                  titles.append('Aliez' + aliez2)
                  ligacao.append('http://emb.aliez.tv/' + codigo)
      dailymotionref=int(0)
      dailymotion=re.compile('src="http://www.dailymotion.com/embed/video/(.+?)"',re.DOTALL|re.M).findall(link)
      if not dailymotion: dailymotion = re.compile('src="http://www.dailymotion.com/embed/video/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)
     
      if dailymotion:
            for codigo in dailymotion:
                  golo=findgolo(link,codigo)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Dailymotion' + golo)
                  ligacao.append('http://www.dailymotion.com/video/' + codigo)
      fbvideoref=int(0)
      fbvideo=re.compile('src="http://www.facebook.com/video/embed.+?video_id=(.+?)"',re.DOTALL|re.M).findall(link)
      if fbvideo:
           for codigo in fbvideo:
                 golo=findgolo(link,codigo)
                 if golo: golo=' (%s)' % (golo)
                 titles.append('Facebook' + golo)
                 ligacao.append("http://www.facebook.com/video/embed?video_id=" + codigo)
      kiwiref=int(0)
      kiwi=re.compile('src="http://v.kiwi.kz/v2/(.+?)/"',re.DOTALL|re.M).findall(link)
      if kiwi:
            for codigo in kiwi:
                  golo=findgolo(link,codigo)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Kiwi'+ golo)
                  ligacao.append(codigo)
      #Falta
      longtailref=int(0)
      longtail=re.compile('flashvars=".+?".+?src="http://player.longtailvideo.com/player5.2.swf"').findall(link)
      if longtail:
            for codigo in longtail:
                  longtailref=int(longtailref+1)
                  if len(longtail)==1: longtail2=str('')
                  else: longtail2=' #' + str(longtailref)
                  titles.append('Longtail' + longtail2 + ' (' + traducao(30004) + ')')
                  ligacao.append(0)
      metauaref=int(0)
      metaua=re.compile('src="http://video.meta.ua/players/video/3.2.19k/Player.swf.+?fileID=(.+?)&').findall(link)
      if metaua:
            for codigo in metaua:
                  metauaref=int(metauaref+1)
                  if len(metaua)==1: metaua2=str('')
                  else: metaua2=' #' + str(metauaref)
                  titles.append('Meta.ua' + metaua2 + ' (' + traducao(30004) + ')')
                  ligacao.append(0)
      playwire=re.compile('data-publisher-id="(.+?)" data-video-id="(.+?)"').findall(link)
      if not playwire: playwire=re.compile('http://config.playwire.com/videos/(.+?)/(.+?)/').findall(link)
      if playwire:
          for publisher,codigo in playwire:
                  if publisher=='v2': publisher='configopener'
                  golo=findgolo(link,codigo)
                  if golo: golo=' (%s)' % (golo)
                  if "media only" in golo:golo=''
                  
                  titles.append('Playwire' + golo)
                  ligacao.append('http://cdn.playwire.com/v2/%s/config/%s.json' % (publisher,codigo))
            
      playwire_v2=re.compile('//config.playwire.com/(.+?)/videos/v2/(.+?).json').findall(link)
      if playwire_v2:
          for publisher,codigo in playwire_v2:
                  golo=findgolo(link,codigo)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Playwire' + golo)
                  ligacao.append('http://config.playwire.com/%s/videos/v2/%s.json' % (publisher,codigo))
                  
      rutuberef=int(0)
      rutube=re.compile('src=".+?rutube.ru/video/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if not rutube: rutube=re.compile('value="http://video.rutube.ru/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)  
      if not rutube: rutube=re.compile('src="http://rutube.ru/video/embed/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)
      if rutube:
            for codigo in rutube:
                  golo=findgolo(link,codigo)
                  if golo: golo=' (%s)' % (golo)
                  titles.append("Rutube" + golo)
                  ligacao.append(codigo)
      saporef=int(0)
      sapo=re.compile('src=".+?videos.sapo.pt/playhtml.+?file=(.+?)/1&"',re.DOTALL|re.M).findall(link)
      if not sapo: sapo=re.compile('src=".+?videos.sapo.pt/playhtml.+?file=(.+?)/1"',re.DOTALL|re.M).findall(link)
      if sapo:
            for endereco in sapo:
                  if goals==True:
                        golo=findgolo(link,endereco)
                        if golo: golo=' (%s)' % (golo)
                  else:
                        saporef=int(saporef + 1)
                        if len(sapo)==1: golo=str('')
                        else: golo=' #' + str(saporef)
                  titles.append('Videos Sapo' + golo)
                  ligacao.append(endereco)
      videaref=int(0)
      videa=re.compile('src="http://videa.hu/(.+?)"',re.DOTALL|re.M).findall(link)
      if videa:
            for codigo in videa:
                  golo=findgolo(link,codigo)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Videa' + golo)
                  ligacao.append('http://videa.hu/' + codigo)
      vkref=int(0)
      vk=re.compile('src="http://vk.com/(.+?)"',re.DOTALL|re.M).findall(link)
      if vk:
          for codigo in vk:
                golo=findgolo(link,codigo)
                if golo: golo=' (%s)' % (golo)
                titles.append('VK' + golo)
                ligacao.append('http://vk.com/' + codigo)
      youtuberef=int(0)
      youtube=re.compile('src="http://www.youtube.com/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if not youtube: youtube=re.compile('src="//www.youtube.com/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if youtube:
        for codigo in youtube:     
              golo=findgolo(link,codigo)
              if golo: golo=' (%s)' % (golo)
              titles.append('Youtube' + golo)
              ligacao.append(codigo)
      print ligacao
      if len(ligacao)==0:
            xbmcgui.Dialog().ok(traducao(30000), traducao(30005))
            index=-1
      elif len(ligacao)==1: index=0
      else: index = xbmcgui.Dialog().select(traducao(30006), titles)
      if index > -1:
             linkescolha=ligacao[index]
             servidor=titles[index]
             if linkescolha:
                   if re.search('Rutube',servidor):
                         link=abrir_url('http://rutube.ru/api/play/options/' + linkescolha)
                         try:streamurl=re.compile('"m3u8": "(.+?)"').findall(link)[0]
                         except:streamurl=re.compile('"default": "(.+?)"').findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Aliez',servidor):
                         linkescolha=linkescolha.replace('amp;','')
                         link=abrir_url(linkescolha)
                         streamurl=re.compile("file.+?'(.+?)'").findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Playwire',servidor):
                         if re.search('configopener',linkescolha):
                               videoid=''.join(linkescolha.split('/')[-1:]).replace('.json','')
                               streamurl=redirect('http://config.playwire.com/videos/v2/%s/player.json'%videoid).replace('player.json','manifest.f4m')
                         else:
                               link=abrir_url(linkescolha)
                               try:streamurl=re.compile('"src":"(.+?)"').findall(link)[0]
                               except:streamurl=re.compile('"f4m":"(.+?)"').findall(link)[0]
                         if re.search('.f4m',streamurl):
                               titles=[]
                               ligacao=[]
                               f4m=abrir_url(streamurl)
                               baseurl=re.compile('<baseURL>(.+?)</baseURL>').findall(f4m)[0]
                               videos=re.compile('url="(.+?)".+?height="(.+?)"').findall(f4m)
                               for urlname,quality in videos:
                                     titles.append(quality + 'p')
                                     ligacao.append(urlname)
                               if len(ligacao)==1:index=0
                               else: index = xbmcgui.Dialog().select("Qualidade", titles)
                               if index > -1: streamurl='%s/%s' % (baseurl,ligacao[index])
                               else: return
                         streamurl=streamurl.replace('rtmp://streaming.playwire.com/','http://cdn.playwire.com/').replace('mp4:','')
                         comecarvideo(name,streamurl)
                   elif re.search('VK',servidor):
                         linkescolha=linkescolha.replace('amp;','')
                         link=abrir_url(linkescolha)
                         link=link.replace('\\','')
                         if re.search('No videos found.',link): xbmcgui.Dialog().ok(traducao(30000),traducao(30007))
                         else:
                               titles=[]
                               ligacao=[]
                               try:
                                     streamurl=re.compile('"url1080":"(.+?)"').findall(link)[0]
                                     titles.append("1080p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url720":"(.+?)"').findall(link)[0]
                                     titles.append("720p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url480":"(.+?)"').findall(link)[0]
                                     titles.append("480p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url360":"(.+?)"').findall(link)[0]
                                     titles.append("360p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url240":"(.+?)"').findall(link)[0]
                                     titles.append("240p")
                                     ligacao.append(streamurl)
                               except: pass
                               if len(ligacao)==1:index=0
                               else: index = xbmcgui.Dialog().select(traducao(30014), titles)
                               if index > -1:
                                     linkescolha=ligacao[index]
                                     comecarvideo(name,linkescolha)
                   elif re.search('Sapo',servidor): comecarvideo(name,linkescolha)
                   elif re.search('Facebook',servidor):
                         link=abrir_url(linkescolha)
                         params = re.compile('"params","([\w\%\-\.\\\]+)').findall(link)[0]
                         html = urllib.unquote(params.replace('\u0025', '%')).decode('utf-8')
                         html = html.replace('\\', '')
                         streamurl = re.compile('(?:hd_src|sd_src)\":\"([\w\-\.\_\/\&\=\:\?]+)').findall(html)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Kiwi',servidor):
                         link=urllib.unquote(abrir_url('http://v.kiwi.kz/v2/'+linkescolha))
                         streamurl=re.compile('&url=(.+?)&poster').findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('videa',linkescolha):
                         referencia=re.compile('flvplayer.swf.+?v=(.+?)"').findall(linkescolha)[0]
                         link=abrir_url('http://videa.hu/flvplayer_get_video_xml.php?v='+ referencia)
                         streamurl=re.compile('<version quality="standard" video_url="(.+?)"').findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Youtube',servidor):
                         streamurl='plugin://plugin.video.youtube/?action=play_video&videoid='+codigo
                         comecarvideo(name,streamurl)
                         
                   elif re.search('dailymotion',linkescolha):
                         import urlresolver
                         sources=[]
                         hosted_media = urlresolver.HostedMediaFile(url=linkescolha)
                         sources.append(hosted_media)
                         source = urlresolver.choose_source(sources)
                         if source:
                                     linkescolha=source.resolve()
                                     if linkescolha==False:
                                           xbmcgui.Dialog().ok(traducao(30000),traducao(30007))
                                           return
                                     else: comecarvideo(name,linkescolha)

def comecarvideo(titulo,url):
      playlist = xbmc.PlayList(1)
      playlist.clear()
      listitem = xbmcgui.ListItem(titulo, iconImage="DefaultVideo.png", thumbnailImage=thumb)
      listitem.setInfo("Video", {"Title":titulo})
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      playlist.add(url, listitem)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
      xbmcPlayer = xbmc.Player()
      xbmcPlayer.play(playlist)

def addDir(name,url,mode,iconimage,total,pasta=True):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      #liz.setProperty('fanart_image', os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'fanart.jpg'))
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
      return ok

def pesquisa():
      pesquisa=xbmcgui.Dialog().input(traducao(30008),autoclose=60000)
      if pesquisa:
            xbmcgui.Dialog().ok(traducao(30000),traducao(30009),traducao(30015))
            link=abrir_url( MainURL + 'search.php?dosearch=yes&search_in_archives=yes&title=' + urllib.quote(pesquisa))
            jogos=re.compile('<div style="font-family:Arial, Helvetica, sans-serif; font-size:12px;"><a href="/(.+?)">([0-9]{4}\.[0-9]{2}\.[0-9]{2})\s*(\([0-9]{2}h[0-9]{2}\))\s*-\s*([A-Za-z ]+?)\s*([0-9]*)\s*-\s*([0-9]*)\s*([A-Za-z ]+?)</a></div>').findall(link)
            for endereco,data,hora,equipa1,resultado1,resultado2,equipa2 in jogos:
                  addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange]%s[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hora,equipa1,resultado1,resultado2,equipa2),MainURL + endereco,1,os.path.join(art,'proxima.png'),len(jogos),pasta=False)
            if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")
      else: sys.exit(0)
                        
def abrir_url(url):
      link=requests.get(url, headers={'User-Agent':user_agent},verify=False).text
      return link

def redirect(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      gurl=response.geturl()
      return gurl

def clean(text):
      command={'&#193;':'A','&#194;':'A','&#195;':'A','&#199;':'C','&#201;':'E','&#202;':'E','&#205;':'I','&#211;':'O','&#212;':'O','&#213;':'O','&#217;':'U','&#218;':'U','&#224;':'a','&#225;':'a','&#226;':'a','&#227;':'a','&#231;':'c','&#232;':'e','&#233;':'e','&#234;':'e','&#237;':'i','&#243;':'o','&#244;':'o','&#245;':'o','&#249;':'u','&#250;':'u'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

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

def findgolo(link, codigo):
      text=link[:link.find(codigo)]
      golo=text[max([text.rfind('</iframe>'),text.rfind('</script>'),text.rfind('</a>')]):max([text.rfind('<iframe'),text.rfind('<script')])]
      golo=re.sub('<[^<]+?>', '', golo.replace('\n','').replace('&#39;',"'"))
      return golo

def descape(content):
      content = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), content)
      return content.encode('utf-8')

def traducao(text):
      return xbmcaddon.Addon().getLocalizedString(text).encode('utf-8')

params=get_params()
url=None
name=None
mode=None
thumb=None
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: thumb=urllib.unquote_plus(params["thumb"])
except: pass

if mode==None or url==None or len(url)<1: menu_principal()
elif mode==1: captura(name,url)
elif mode==2: request(url)
elif mode==3: listadeligas(url)
elif mode==4: request(MainURL + re.compile('<a href="([^"]+?)">previous weeks archive').findall(abrir_url(url))[0].replace('amp;',''))
elif mode==5: epocasanteriores(url)
elif mode==6: pesquisa()
elif mode==7: ligaportuguesa(url)
elif mode==8: request(url,special=True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
