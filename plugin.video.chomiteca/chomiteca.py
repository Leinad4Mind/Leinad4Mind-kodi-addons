# -*- coding: utf-8 -*-

""" Chomiteca
    2015-2019 fightnight/Mafarricos/Leinad4Mind"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,xbmcvfs,HTMLParser
from t0mm0.common.net import Net
from resources.lib import internalPlayer

try: import json
except: import simplejson as json
h = HTMLParser.HTMLParser()
net=Net()

####################################################### CONSTANTES #####################################################
addon_id = 'plugin.video.chomiteca'
nameURL = 'Chomikuj'
MainURL = 'https://chomikuj.pl/'
art = '/resources/art/'
covers = '/resources/covers/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'iconpq.png'
traducaoma= selfAddon.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
cookies = os.path.join(pastaperfil, "cookies.lwp")
username_ck = urllib.quote(selfAddon.getSetting('chomikuj-username'))
servidor_ut = urllib.quote(selfAddon.getSetting('servidor-cover'))
moviesFolder = xbmc.translatePath(selfAddon.getSetting('libraryfolder'))
tvshowFolder = xbmc.translatePath(selfAddon.getSetting('tvshowlibraryfolder'))
musicvideoFolder = xbmc.translatePath(selfAddon.getSetting('musicvideolibraryfolder'))
foldertype = int(selfAddon.getSetting('folder-type'))
usernameURL = urllib.quote(selfAddon.getSetting('chomikuj-username'))

#################################################### LOGIN CHOMITECA #####################################################
def login(defora=False):
    print "Sem cookie. A iniciar login"
    username,password,site,label,color = appendValues()
    for x in range(0, len(username)):
        try:
            print username[x]
            link=abrir_url(site[x])
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(link)[0]
            form_d = {'RedirectUrl':'','Redirect':'True','FileId':0,'Login':username[x],'Password':password[x],'RememberMe':'true','__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': site[x], 'X-Requested-With': 'XMLHttpRequest', 'Referer': site[x],'User-Agent':user_agent}
            endlogin=site[x] + 'action/login/login'
            try: logintest= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: logintest='Erro'
        except:
            link='Erro'
            logintest='Erro'
        if  re.search('Logowanie',logintest):
            mensagemok(label[x],traducao(40002))
            entrarnovamente(1)
            selfAddon.setSetting(label[x]+'-check',"false")
        elif re.search('Chomik o takiej nazwie nie istnieje',logintest):
            mensagemok(label[x],traducao(40003))
            entrarnovamente(1)
            selfAddon.setSetting(label[x]+'-check',"false")
        elif re.search('"LoggedIn":true',logintest):
            net.save_cookies(cookies)
            selfAddon.setSetting(label[x]+'-check',"true")
        elif re.search('Erro',logintest) or link=='Erro':
            opcao= xbmcgui.Dialog().yesno(label[x], traducao(40005), "", "",traducao(40006), 'OK')
            selfAddon.setSetting(label[x]+'-check',"false")
        else: return selfAddon.setSetting(label[x]+'-check',"true")

################################################### MENUS PLUGIN ######################################################
def menu_principal(ligacao):
    if ligacao==1:
        addDir(traducao(40007),MainURL,1,wtpath + art + 'topcol.png',1,True)
        addDir(traducao(40008),MainURL,2,wtpath + art + 'recents.png',2,True)
        if ReturnStatus(nameURL.lower()): addDir(traducao(40009)+nameURL,MainURL + usernameURL,3,wtpath + art + 'my.png',2,True)
        if ReturnStatus(nameURL.lower()): addDir(traducao(40010)+nameURL,'pastas',5,wtpath + art + 'goto.png',2,True)
        addDir(traducao(40037),MainURL,9,wtpath + art + 'friends.png',2,True)
        addDir(traducao(40054),MainURL,18,wtpath + art + 'attach.png',2,True)
        addDir(traducao(40011),'pesquisa',7,wtpath + art + 'search.png',3,True)
    elif ligacao==0: addDir(traducao(40015),MainURL,6,wtpath + art + 'pasta.png',1,True)
    xbmc.executebuiltin("Container.SetViewMode(51)")

def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir(traducao(40020),MainURL,None,wtpath + art + 'refresh.png',1,True)
      addDir(traducao(40021),MainURL,8,wtpath + art + 'defs.png',1,False)

def topcolecionadores():
    username,password,site,label,color = appendValues()
    for x in range(0, len(username)):
        conteudo=clean(abrir_url_cookie(site[x] + username[x]))
        users=re.compile('<li><div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span></span></a></div>.+?<i>(.+?)</i></li>').findall(conteudo)
        for urluser,nomeuser,thumbuser,nruser in users: addDir('[B][COLOR '+color[x]+']' + nruser + 'º '+label[x]+'[/B][/COLOR] ' + nomeuser,site[x] + urluser,3,thumbuser,len(users),True)
    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def chomitecamaisrecentes(url):
    username,password,site,label,color = appendValues()
    for x in range(0, len(color)):
        conteudo=clean(abrir_url_cookie(site[x]+'action/LastAccounts/MoreAccounts'))
        users=re.compile('<div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span>').findall(conteudo)
        for urluser,nomeuser,thumbuser in users: addDir('[B][COLOR '+color[x]+']' + nomeuser + '[/B][/COLOR]',site[x] + urluser,3,thumbuser,len(users),True)
    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def pesquisa():
    opcoeslabel = []
    for x in range(0, len(MainURL)):
        if ReturnStatus(nameURL.lower()):
            conteudo=clean(abrir_url_cookie(MainURL+'action/Help'))
            if not opcoeslabel: opcoeslabel=re.compile('<option value=".+?">(.+?)</option>').findall(conteudo)
    opcoesvalue=re.compile('<option value="(.+?)">.+?</option>').findall(conteudo)
    opcoeslabel[0] = traducao(40066)
    opcoeslabel[1] = traducao(40067)
    opcoeslabel[2] = traducao(40068)
    opcoeslabel[3] = traducao(40069)
    opcoeslabel[4] = traducao(40070)
    opcoeslabel[5] = traducao(40071)
    opcoeslabel[6] = traducao(40072)
    index = xbmcgui.Dialog().select(traducao(40022), opcoeslabel)
    if index > -1:
        caixadetexto('pesquisa',ftype=opcoesvalue[index])
    else:sys.exit(0)

def favoritos():
    username,password,site,label,color = appendValues()
    for x in range(0, len(username)):
        conteudo=abrir_url_cookie(site[x] + username[x])
        chomikid=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        if name==traducao(40037):pagina=1
        else: pagina = re.compile('\[.+?\].+? (\d) .+?').findall(name)[0]
        form_d = {'page':pagina,'chomikName':chomikid,'__RequestVerificationToken':token}
        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':site[x].replace('https://','').replace('/',''),'Origin':site[x],'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
        endlogin=site[x] + 'action/Friends/ShowAllFriends'
        info= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        info=info.replace('javascript:;','/javascript:;')
        users=re.compile('<div class="friend avatar".+?<a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" />').findall(info)
        for urluser,nomeuser,thumbuser in users: addDir(nomeuser,site[x] + urluser,3,thumbuser,len(users),True)
        paginas(info)
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def proxpesquisa_ck():
    from t0mm0.common.addon import Addon
    addon=Addon(addon_id)
    form_d=addon.load_data('temp.txt')
    ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'chomikuj.pl','Origin':'https://chomikuj.pl','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
    form_d['Page']= form_d['Page'] + 1
    endlogin=MainURL + 'action/SearchFiles/Results'
    net.set_cookies(cookies)
    conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
    addon.save_data('temp.txt',form_d)
    pastas(MainURL + 'action/nada','coco',conteudo=conteudo)

def atalhos(type=False):
      pastatracks = os.path.join(pastaperfil, "atalhos")
      if not os.path.exists(pastatracks):
            os.makedirs(pastatracks)
            savefile('ref.tmp','0',pastafinal=pastatracks)
      if type=='addfolder':
            ref=int(openfile('ref.tmp',pastafinal=pastatracks)) + 1
            builder='{"name":"""%s""","url":"""%s""","type":"folder"}' % (name,url)
            savefile('%s.txt' % ref,builder,pastafinal=pastatracks)
            savefile('ref.tmp',str(ref),pastafinal=pastatracks)
            xbmc.executebuiltin("XBMC.Notification(Chomiteca,Atalho adicionado,'500000',"+iconpequeno.encode('utf-8')+")")
      elif type=='addfile':
            ref=int(openfile('ref.tmp',pastafinal=pastatracks)) + 1
            builder='{"name":"""%s""","url":"""%s""","type":"file"}' % (name,url)
            savefile('%s.txt' % ref,builder,pastafinal=pastatracks)
            savefile('ref.tmp',str(ref),pastafinal=pastatracks)
            xbmc.executebuiltin("XBMC.Notification(Chomiteca,Atalho adicionado,'500000',"+iconpequeno.encode('utf-8')+")")
      elif type=='remove':
            try:os.remove(os.path.join(pastatracks,name))
            except:pass
            xbmc.executebuiltin("Container.Refresh")
      else:
            try:lista = os.listdir(pastatracks)
            except: lista=[]
            for atal in lista:
                  content=openfile(atal,pastafinal=pastatracks)
                  try:ftype=re.compile('"type":"(.+?)"').findall(content)[0]
                  except:ftype=''
                  try:fname=re.compile('"name":"""(.+?)"""').findall(content)[0]
                  except:fname=''
                  try:furl=re.compile('"url":"""(.+?)"""').findall(content)[0]
                  except:furl=''
                  path=urllib.unquote_plus('/'.join(''.join(furl.split(MainURL)).split('/')[:-1]).replace('*','%'))
                  if ftype=='file': addCont('%s (%s)' % (fname,path),furl,4,'',wtpath + art + 'file.png',len(lista),False,atalhos=atal)
                  elif ftype=='folder': addDir('%s (%s)' % (fname,path),furl,3,wtpath + art + 'pasta.png',len(lista),True,atalhos=atal)
                  xbmc.executebuiltin("Container.SetViewMode(51)")

def pastas(url,name,formcont={},conteudo='',past=False,deFora=False,listagem=False):
    MainPlayList = []
    uniqueList = []
    if foldertype == 1 and re.search('action/SearchFiles',url):
        source = xbmcgui.Dialog().select
        selectlist = []
        urllist = []
    sitebase,name,color,mode = returnValues(url)
    host = sitebase.replace('https://','').replace('/','')
    if re.search('action/SearchFiles',url):
        ref_data = {'Host': host, 'Connection': 'keep-alive', 'Referer': 'https://'+host+'/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'https://'+host+'/'}
        endlogin=sitebase + 'action/SearchFiles'
        conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
        if re.search('O ficheiro n&#227;o foi encontrado',conteudo): mensagemok(host,'Sem resultados.')
        try:
              filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
              try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
              except: ftype='All'
              pagina=1
              token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
              if selfAddon.getSetting('activate-size') == 'true': form_d = {'IsGallery':'False','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token,'SizeFrom':selfAddon.getSetting('min-size'),'SizeTo':selfAddon.getSetting('max-size')}
              else: form_d = {'IsGallery':'False','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token}
              from t0mm0.common.addon import Addon
              addon=Addon(addon_id)
              addon.save_data('temp.txt',form_d)
              ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'https://'+host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
              endlogin=sitebase + 'action/SearchFiles/Results'
              conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        except: pass
    else:
        if conteudo=='':
              extra=returnExtra()
              conteudo=clean(abrir_url_cookie(url + extra))
    if re.search('ProtectedFolderChomikLogin',conteudo):
        chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        passwordfolder=caixadetexto('password')
        form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'https://' + host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
        endlogin=sitebase + 'action/Files/LoginToFolder'
        teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        teste=urllib.unquote(teste)
        if re.search('IsSuccess":false',teste):
              mensagemok('Erro',traducao(40002))
              sys.exit(0)
        else: pastas_ref(url)
    elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
        chomiktype=re.compile('<input id="ChomikType" name="ChomikType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        accname=re.compile('<input id="AccountName" name="AccountName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        passwordfolder=caixadetexto('password')
        form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','IsAdult':isadult,'Sex':sex,'AccountName':accname,'AdultFilter':adultfilter,'ChomikType':chomiktype,'TargetChomikId':chomikid}
        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'https://'+host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
        endlogin=sitebase + 'action/UserAccess/LoginToProtectedWindow'
        teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        teste=urllib.unquote(teste)
        if re.search('<div class="ui-tooltip-titlebar">',teste): mensagemok('Chomikuj',traducao(40002))
        else: pastas_ref(url)
    else:
        try:
              conta=re.compile('<div class="fileInfoFrame borderRadius">.+?<span class="bold">.+?</span>.+?<span class="bold">(.+?)</span>\s+(.+?)</p>').findall(conteudo)[0]
              nomeconta=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
              addLink('[COLOR gold][B]' + traducao(40023) + nomeconta + '[/B][/COLOR]: ' + conta[0] + conta[1],'',wtpath + art + 'star.png')
        except: pass
        try:
              checker=url.split('/')[:-1]
              if len(checker) > 3 and not re.search('action/SearchFiles',url) and not re.search('/action/nada',url):
                    urlbefore='/'.join(checker)
                    #addDir('[COLOR gold][B]' + traducao(40060) + '[/B][/COLOR]',urlbefore,3,wtpath + art + 'seta.png',1,True)
        except: pass
        try:
              pastas=re.compile('<div id="foldersList">(.+?)</table>.+?').findall(conteudo)
              seleccionados=re.compile('<a href="/(.+?)".+?title="(.+?)">(.+?)</a>').findall(pastas[0])
              for urlpasta,nomepasta,password in seleccionados:
                    if re.search('<span class="pass">',password): displock=' (' + traducao(40024)+')'
                    else:displock=''
                    if nomepasta == 'Dokumenty' or nomepasta == 'Documentos': nomepasta=traducao(40057)
                    if nomepasta == 'Galeria': nomepasta=traducao(40058)
                    if nomepasta == 'Prywatne' or nomepasta == 'Privada': nomepasta=traducao(40059)
                    addDir('[B][COLOR white]' + nomepasta + '[/COLOR][/B]' + displock,sitebase + urlpasta,3,wtpath + art + 'pasta.png',len(seleccionados),True)
        except: pass
        reslist = []
        reslist = ReturnConteudo(conteudo,past,color,url,deFora)
        if reslist:
            if deFora:
                if foldertype == 1:
                    if selfAddon.getSetting('search-order') == 'true': reslist = sorted(reslist, key=getKey,reverse=True)
                    for part1,part2 in reslist:
                        if not part2[1]+part2[2]+part2[3] in uniqueList:
                            uniqueList.append(part2[1]+part2[2]+part2[3])
                            selectlist.append(part2[1]+part2[2]+part2[3])
                            urllist.append(sitebase + part2[4])
                    choose=source('Link a Abrir',selectlist)
                    if listagem==True: return urllist
                    else:
                                                if choose > -1: analyzer(urllist[choose])
                else:
                    reslist = sorted(reslist, key=getKey,reverse=True)
                    if listagem==True: return reslist
                    else:
                                                if choose > -1:
                                                        analyzer(sitebase + reslist[1][1][4])
            else:
                if re.search('action/SearchFiles',url) and selfAddon.getSetting('search-order') == 'true': reslist = sorted(reslist, key=getKey,reverse=True)
                for part1,part2 in reslist:
                    if foldertype == 1 and re.search('action/SearchFiles',url):
                        if not part2[0] in uniqueList:
                            uniqueList.append(part2[0])
                            selectlist.append(part2[0])
                            urllist.append(part2[1])
                    else:
                        if not (part2[1].replace(part2[2],'') + part2[2] + part2[3]) in uniqueList:
                            if '(video)' in part2[4] or '(audio)' in part2[4]: MainPlayList.append([ReplaceSpecialChar(part2[1]),sitebase + part2[4]])
                            uniqueList.append(part2[1].replace(part2[2],'') + part2[2] + part2[3])
                            addCont('[B][COLOR '+part2[0]+']' + part2[1].replace(part2[2],'') + part2[2] + '[/COLOR][/B]' + '[COLOR white]' + part2[3] + '[/COLOR]',sitebase + part2[4],part2[5],part2[3],part2[6],len(reslist))
                if foldertype == 1 and re.search('action/SearchFiles',url):
                    choose=source('Link a Abrir',selectlist)
                    if choose > -1:    analyzer(urllist[choose])
                savefile('playlist.txt',str(MainPlayList))
        if foldertype == 0 or (foldertype == 1 and not re.search('action/SearchFiles',url)) and not deFora: paginas(conteudo)
    if foldertype == 0 or (foldertype == 1 and not re.search('action/SearchFiles',url)) and not deFora: xbmc.executebuiltin("Container.SetViewMode(51)")

#Mafarricos,sn - Novas alterações
def returnExtra():
    fileListSortType = 'Name'
    fileListAscending = 'True'
    option1 = int(selfAddon.getSetting('filesorder'))
    option2 = int(selfAddon.getSetting('fileasc'))
    if option1 == 0: fileListSortType = 'Name'
    elif option1 == 1: fileListSortType = 'Type'
    elif option1 == 2: fileListSortType = 'Size'
    elif option1 == 3: fileListSortType = 'Date'
    if option2 == 0: fileListAscending = 'True'
    elif option2 == 1: fileListAscending = 'False'
    return '?IsGallery=False&requestedFolderMode=filesList&fileListSortType='+fileListSortType+'&fileListAscending='+fileListAscending

def GetThumbExt(extensao):
    extensao=extensao.replace(' ','').lower()
    if extensao=='.7z': return wtpath + art + 'rar/7z.png'
    elif extensao=='.ace': return wtpath + art + 'rar/ace.png'
    elif extensao=='.hqx': return wtpath + art + 'rar/hqx.png'
    elif extensao=='.jar': return wtpath + art + 'rar/jar.png'
    elif extensao=='.rar': return wtpath + art + 'rar/rar.png'
    elif extensao=='.sit': return wtpath + art + 'rar/sit.png'
    elif extensao=='.sitx': return wtpath + art + 'rar/sitx.png'
    elif extensao=='.tar': return wtpath + art + 'rar/tar.png'
    elif extensao=='.zip': return wtpath + art + 'rar/zip.png'

    elif extensao=='.aac': return wtpath + art + 'music/aac.png'
    elif extensao=='.aiff': return wtpath + art + 'music/aiff.png'
    elif extensao=='.midi': return wtpath + art + 'music/midi.png'
    elif extensao=='.m4a': return wtpath + art + 'music/mp4.png' #Convinha dizer m4a
    elif extensao=='.mp3': return wtpath + art + 'music/mp3.png'
    elif extensao=='.ogg': return wtpath + art + 'music/ogg.png'
    elif extensao=='.ra': return wtpath + art + 'music/ra.png'
    elif extensao=='.rmva': return wtpath + art + 'music/ra.png'
    elif extensao=='.wav': return wtpath + art + 'music/wav.png'
    elif extensao=='.wma': return wtpath + art + 'music/wma.png'
    elif extensao=='.ac3': return wtpath + art + 'musica.png'
    elif extensao=='.flac': return wtpath + art + 'musica.png'
    elif extensao=='.m3u': return wtpath + art + 'musica.png'

    elif extensao=='.bmp': return wtpath + art + 'foto/bmp.png'
    elif extensao=='.gif': return wtpath + art + 'foto/gif.png'
    elif extensao=='.ico': return wtpath + art + 'foto/ico.png'
    elif extensao=='.jpeg': return wtpath + art + 'foto/jpeg.png'
    elif extensao=='.jpg': return wtpath + art + 'foto/jpg.png'
    elif extensao=='.png': return wtpath + art + 'foto/png.png'
    elif extensao=='.tga': return wtpath + art + 'foto/tga.png'
    elif extensao=='.tif': return wtpath + art + 'foto/tif.png'
    elif extensao=='.tiff': return wtpath + art + 'foto/tiff.png'
    #elif extensao=='.webp': return wtpath + art + 'foto/webp.png'

    elif extensao=='.bin': return wtpath + art + 'img/bin.png'
    elif extensao=='.ccd': return wtpath + art + 'img/ccd.png'
    elif extensao=='.cue': return wtpath + art + 'img/cue.png'
    elif extensao=='.img': return wtpath + art + 'img/img.png'
    elif extensao=='.iso': return wtpath + art + 'img/iso.png'
    elif extensao=='.mdf': return wtpath + art + 'img/mdf.png'
    elif extensao=='.mds': return wtpath + art + 'img/mds.png'

    elif extensao=='.avi': return wtpath + art + 'video/avi.png'
    elif extensao=='.dat': return wtpath + art + 'video/dat.png'
    elif extensao=='.ifo': return wtpath + art + 'video/ifo.png'
    elif extensao=='.mov': return wtpath + art + 'video/mov.png'
    elif extensao=='.mpg': return wtpath + art + 'video/mpeg.png'
    elif extensao=='.mpeg': return wtpath + art + 'video/mpeg2.png'
    elif extensao=='.mkv': return wtpath + art + 'video.png' #Estes todos estão a faltar
    elif extensao=='.ogm': return wtpath + art + 'video.png'
    elif extensao=='.mp4': return wtpath + art + 'video.png'
    elif extensao=='.3gp': return wtpath + art + 'video.png'
    elif extensao=='.rm': return wtpath + art + 'video/rm.png'
    elif extensao=='.rmvb': return wtpath + art + 'video/rm.png'
    elif extensao=='.wmv': return wtpath + art + 'video/wmv.png'

    elif extensao=='.doc': return wtpath + art + 'files/doc.png'
    elif extensao=='.pdf': return wtpath + art + 'files/pdf.png'
    elif extensao=='.ppt': return wtpath + art + 'files/ppt.png'
    elif extensao=='.rtf': return wtpath + art + 'files/rtf.png'
    elif extensao=='.txt': return wtpath + art + 'files/txt.png'
    elif extensao=='.torrent': return wtpath + art + 'files/torrent.png'
    else: return wtpath + art + 'file.png'

def ReturnConteudo(conteudo,past,color,url2,deFora):
    diffItems = False
    reslist = []
    section = re.compile('<div class="filerow fileItemContainer">.+?<a class="expanderHeader downloadAction"(.+?)</ul></div>\s+</div>', re.DOTALL).findall(conteudo)
    if not section: section = re.compile('fileItemContainer">(.+?)</div></div>', re.DOTALL).findall(conteudo)
    if not section: section = re.compile('<li class="fileItemContainer">(.+?)<li><span class="date">', re.DOTALL).findall(conteudo)
    for part in section:
        if color=="green": name = re.compile('data-title="(.+?)"', re.DOTALL).findall(part)
        if color=="blue": name = re.compile('title="(.+?)"', re.DOTALL).findall(part)
        if not name: name = re.compile('<span class="bold">(.+?)</span>.{4}\s+</a>', re.DOTALL).findall(part)
        tituloficheiro = ReplaceSpecialChar(h.unescape(name[0].decode('utf-8').replace('<span class="e">','').replace(' </span>','')))

        if(
            ('.7z' in tituloficheiro[-3:]) or ('.ra' in tituloficheiro[-3:]) or ('.rm' in tituloficheiro[-3:])
            ): extensao = tituloficheiro[-3:]
        if(
            ('.ace' in tituloficheiro[-4:]) or ('.hqx' in tituloficheiro[-4:]) or ('.jar' in tituloficheiro[-4:]) or ('.rar' in tituloficheiro[-4:]) or ('.sit' in tituloficheiro[-4:]) or ('.tar' in tituloficheiro[-4:]) or ('.zip' in tituloficheiro[-4:]) or 
            ('.aac' in tituloficheiro[-4:]) or ('.m4a' in tituloficheiro[-4:]) or ('.mp3' in tituloficheiro[-4:]) or ('.ogg' in tituloficheiro[-4:]) or ('.wav' in tituloficheiro[-4:]) or ('.wma' in tituloficheiro[-4:]) or ('.ac3' in tituloficheiro[-4:]) or ('.m3u' in tituloficheiro[-4:]) or 
            ('.bmp' in tituloficheiro[-4:]) or ('.gif' in tituloficheiro[-4:]) or ('.ico' in tituloficheiro[-4:]) or ('.jpg' in tituloficheiro[-4:]) or ('.png' in tituloficheiro[-4:]) or ('.tga' in tituloficheiro[-4:]) or ('.tif' in tituloficheiro[-4:]) or 
            ('.bin' in tituloficheiro[-4:]) or ('.ccd' in tituloficheiro[-4:]) or ('.cue' in tituloficheiro[-4:]) or ('.img' in tituloficheiro[-4:]) or ('.iso' in tituloficheiro[-4:]) or ('.mdf' in tituloficheiro[-4:]) or ('.mds' in tituloficheiro[-4:]) or 
            ('.dat' in tituloficheiro[-4:]) or ('.ifo' in tituloficheiro[-4:]) or ('.mpg' in tituloficheiro[-4:]) or ('.3gp' in tituloficheiro[-4:])or 
            ('.doc' in tituloficheiro[-4:]) or ('.pdf' in tituloficheiro[-4:]) or ('.ppt' in tituloficheiro[-4:]) or ('.rtf' in tituloficheiro[-4:]) or ('.txt' in tituloficheiro[-4:])
            ): extensao = tituloficheiro[-4:]
        if(
            ('.sitx' in tituloficheiro[-5:]) or ('.aiff' in tituloficheiro[-5:]) or ('.midi' in tituloficheiro[-5:]) or ('.rmva' in tituloficheiro[-5:]) or ('.flac' in tituloficheiro[-5:]) or ('.jpeg' in tituloficheiro[-5:]) or ('.tiff' in tituloficheiro[-5:]) or ('.webp' in tituloficheiro[-5:]) or ('.mpeg' in tituloficheiro[-5:]) or ('.rmva' in tituloficheiro[-5:])
            ): extensao = tituloficheiro[-5:]
        if(
            ('.torrent' in tituloficheiro[-8:])
            ): extensao = tituloficheiro[-8:]
        if(
            ('.avi' in tituloficheiro[-4:]) or ('.mov' in tituloficheiro[-4:]) or ('.mkv' in tituloficheiro[-4:]) or ('.ogm' in tituloficheiro[-4:]) or ('.mp4' in tituloficheiro[-4:]) or ('.wmv' in tituloficheiro[-4:])
            ): extensao = tituloficheiro[-4:]
        else:
            if color=="green":
                ext = re.compile('<span class="bold">.+?</span>(\..+?)\s+</a>\s+<img', re.DOTALL).findall(part)
                if ext: extensao = ext[0]
            if color=="blue":
                ext = re.compile('<span class="bold">.+?</span>(\..+?)\s+</a>\s+</h3>', re.DOTALL).findall(part)
                if ext: extensao = ext[0]
            if not ext: extensao = '.not'

        if ( (selfAddon.getSetting('caminho-enable') == 'true') ):
            imagem = (wtpath + covers + tituloficheiro + '.png')
            online = str(xbmcvfs.exists(imagem))
            if (online == '1'):
                existe='true'
            else:
                existe='false'
                online='404'
        else:
            existe='false'

        if (existe == 'false'):
            if ( (selfAddon.getSetting('servidor-enable') == 'true') and servidor_ut ):
                imagem = 'https://' + servidor_ut + tituloficheiro + '.png'
                online = str(urllib.urlopen(imagem).getcode())
            else: online='404'

        if ( (extensao == '.mkv') or (extensao == '.mp4') or (extensao == '.avi') or (extensao == '.ogm') ):
            if (online != '404'): thumb = imagem
            else: thumb = GetThumbExt(extensao)
        else: thumb = GetThumbExt(extensao)

        url = re.compile('href="/(.+?)"', re.DOTALL).findall(part)
        size = re.compile('<li><span>(.+?)</span></li>', re.DOTALL).findall(part)
        if not size: size = re.compile('<li>\s+(.+?)\s+</li>', re.DOTALL).findall(part)
        if not size: size = '0'
        urlficheiro = url[0]

        try: tamanhoficheiro = size[0]
        except: tamanhoficheiro = '0'
        tamanhoficheiro=tamanhoficheiro.replace(',','.').replace(' ','')
        num_format = re.compile("^[0-9]+.?[0-9]+?K?M?G?B")

        if(selfAddon.getSetting('imagens-disable') == 'true'):
            if( (extensao == '.bmp') or (extensao == '.gif') or (extensao == '.ico') or (extensao == '.jpg') or (extensao == '.png') or (extensao == '.tga') or (extensao == '.tif') or (extensao == '.tiff') or (extensao == '.webp') ):
                tamanhoficheiro='0'

        if(selfAddon.getSetting('legendas-disable') == 'true'):
            if( (extensao == '.srt') or (extensao == '.sub') or (extensao == '.ass') or (extensao == '.ssa') ):
                tamanhoficheiro='0'

        if( tamanhoficheiro != '0' and re.match(num_format,tamanhoficheiro) ):
            tamanhoparavariavel=' (' + tamanhoficheiro + ')'
            if deFora: reslist = SearchResults(tamanhoficheiro,color,tituloficheiro,extensao,tamanhoparavariavel,urlficheiro,4,thumb,reslist)
            elif foldertype == 1 and re.search('action/SearchFiles',url2): reslist = SearchResultsFora(tamanhoficheiro,tituloficheiro+extensao+tamanhoparavariavel,MainURL + urlficheiro,color,reslist)
            else: reslist = SearchResults(tamanhoficheiro,color,tituloficheiro,extensao,tamanhoparavariavel,urlficheiro,4,thumb,reslist)

        elif re.match(num_format,tamanhoficheiro):
            xbmc.executebuiltin("XBMC.Notification(Chomiteca,"+tamanhoficheiro+",'500000',"+iconpequeno.encode('utf-8')+")")
            tamanhoficheiro = '0'
            tamanhoparavariavel=' (' + tamanhoficheiro + ')'
            if deFora: reslist = SearchResults(tamanhoficheiro,color,tituloficheiro,extensao,tamanhoparavariavel,urlficheiro,4,thumb,reslist)
            elif foldertype == 1 and re.search('action/SearchFiles',url2): reslist = SearchResultsFora(tamanhoficheiro,tituloficheiro+extensao+tamanhoparavariavel,MainURL + urlficheiro,color,reslist)
            else: reslist = SearchResults(tamanhoficheiro,color,tituloficheiro,extensao,tamanhoparavariavel,urlficheiro,4,thumb,reslist)
    return reslist

def SearchResults(tamanhoficheiro,color,tituloficheiro,extensao,tamanhoparavariavel,urlficheiro,modo,thumb,reslist):
    listresults = []
    listresults.append(color)
    listresults.append(tituloficheiro)
    listresults.append(extensao)
    listresults.append(tamanhoparavariavel)
    listresults.append(urlficheiro)
    listresults.append(modo)
    listresults.append(thumb)
    if 'GB' in tamanhoficheiro: tamanhoficheiro = str(float(tamanhoficheiro.replace('GB','').replace(',','.'))*1024).replace('.',',')+'MB'
    if 'KB' in tamanhoficheiro: tamanhoficheiro = str(float(tamanhoficheiro.replace('KB','').replace(',','.'))/1024).replace('.',',')+'MB'
    tamanhoficheiro = round(float(tamanhoficheiro.replace('GB','').replace('MB','').replace('KB','').replace(',','.')),2)
    reslist.append([tamanhoficheiro,listresults])
    return reslist

def SearchResultsFora(tamanhoficheiro,label,url,color,reslist):
    listresults = []
    listresults.append(label)
    listresults.append(url)
    if 'GB' in tamanhoficheiro: tamanhoficheiro = str(float(tamanhoficheiro.replace('GB','').replace(',','.'))*1024).replace('.',',')+'MB'
    if 'KB' in tamanhoficheiro: tamanhoficheiro = str(float(tamanhoficheiro.replace('KB','').replace(',','.'))/1024).replace('.',',')+'MB'
    tamanhoficheiro = round(float(tamanhoficheiro.replace('GB','').replace('MB','').replace('KB','').replace(',','.')),2)
    reslist.append([tamanhoficheiro,listresults])
    return reslist

def getKey(item):
    return item[0]

def pastas_de_fora(url,name,formcont={},conteudo='',past=False):
    login(True)
    if selfAddon.getSetting('activate-size') == 'true': formcont = {'submitSearchFiles': 'Procurar', 'IsGallery':'False','FileName':name,'FileType':'video','ShowAdultContent':'True','SizeFrom':selfAddon.getSetting('min-size'),'SizeTo':selfAddon.getSetting('max-size')}
    else: formcont = {'submitSearchFiles': 'Procurar', 'FileType': 'video', 'IsGallery': 'False', 'FileName': name }
    pastas(url,name,formcont,conteudo,False,True)

def criarplaylist(url,name):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    conteudo = openfile('playlist.txt')
    playlistsearch=re.compile("\['(.+?)', '(.+?)'\]").findall(conteudo)
    for titulo,url in playlistsearch: analyzer(url,subtitles='',playterm='playlist',playlistTitle=titulo)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist)

def trailer(name):
    youtube_trailer_search = 'https://www.googleapis.com/youtube/v3/search?part=id,snippet&q=%s-Trailer&maxResults=1&key=AIzaSyCgpWUrGw2mySqmxxzlrsUoNhpGCBVJD7s'
    cleanname=re.compile('COLOR .+?\](.+?)\[/COLOR').findall(name)
    if cleanname: name = cleanname[0][:-4]
    ytpage = abrir_url(youtube_trailer_search % (urllib.quote_plus(name)))
    youtubeid = re.compile('"videoId": "(.+?)"').findall(ytpage)
    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtubeid[0]
    if url == None: return
    item = xbmcgui.ListItem(path=url)
    item.setProperty("IsPlayable", "true")
    xbmc.Player().play(url, item)

def ReturnStatus(site):
    if selfAddon.getSetting(site+'-enable') == 'true': return True
    return False

def appendValues():
    username = []
    password = []
    site = []
    label = []
    color = []
    if ReturnStatus('chomikuj'):
        username.append(username_ck)
        password.append(selfAddon.getSetting('chomikuj-password'))
        site.append(MainURL)
        label.append('Chomikuj')
        color.append('green')
    return username,password,site,label,color

def returnValues(link):
    sitebase = ''
    nextname = ''
    color = ''
    mode = ''
    if re.search('chomikuj.pl',link):
        sitebase=MainURL
        nextname='Chomikuj'
        color='green'
        mode=24
    return sitebase,nextname,color,mode
#Mafarricos,en - Fim de Novas alterações

def obterlistadeficheiros():
            string=[]
            nrdepaginas=71
            for i in xrange(1,int(nrdepaginas)+1):
                  url='https://minhateca.com.br/qqcoisa,%s' % i
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))
                  items1=re.compile('<li class="fileItemContainer">\s+<p class="filename">\s+<a class="downloadAction" href=".+?">    <span class="bold">.+?</span>(.+?)</a>\s+</p>\s+<div class="thumbnail">\s+<div class="thumbnailWrapper expType" rel="Image" style=".+?">\s+<a href="(.+?)" class="thumbImg" rel="highslide" style=".+?" title="(.+?)">\s+<img src=".+?" rel=".+?" alt=".+?" style=".+?"/>\s+</a>\s+</div>\s+</div>\s+<div class="smallTab">\s+<ul>\s+<li>\s+(.+?)</li>\s+<li><span class="date">(.+?)</span></li>').findall(conteudo)
                  for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1: string.append(tituloficheiro)
                  items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
                  for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2: string.append(tituloficheiro)
                  if not items1:
                        if not items2:
                              conteudo=clean(conteudo)
                              items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                              for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3: string.append(tituloficheiro)
            print string

def pastas_ref(url):
      pastas(url,name)

def paginas(link):
    sitebase,nextname,color,mode = returnValues(link)
    try:
        idmode=3
        try: conteudo=re.compile('<div id="listView".+?>(.+?)<div class="filerow fileItemContainer">').findall(link)[0]
        except:
              try:conteudo=re.compile('<div class="paginator clear searchListPage">(.+?)<div class="clear">').findall(link)[0]
              except:
                    conteudo=re.compile('<div class="paginator clear friendspager">(.+?)<div class="clear">').findall(link)[0]
                    idmode=9
        try:
              if(color=='blue'):
                pagina=re.compile('anterior.+?<a href="/(.+?)" class="right" rel="(.+?)"').findall(conteudo)[0]
              else:
                pagina=re.compile('poprzednia.+?<a href="/(.+?)" class="right" rel="(.+?)"').findall(conteudo)[0]
              urlpag=pagina[0]
              urlpag=urlpag.replace(' ','+')
              addDir('[COLOR gold]' + traducao(40062) + pagina[1] + '[/COLOR] - [COLOR '+color+']' + nextname + '[/COLOR]',sitebase + urlpag,idmode,wtpath + art + 'page.png',1,True)
        except:
              nrpagina=re.compile('type="hidden" value="([^"]+?)" /><input type="submit" value="p.+?gina seguinte.+?" /></form>').findall(link)[0]
              addDir('[COLOR gold' + traducao(40062) + nrpagina + '[/COLOR] - [COLOR '+color+']' + nextname + '[/COLOR]',sitebase,mode,wtpath + art + 'seta.png',1,True)
    except: pass

########################################################### PLAYER ################################################
def analyzer(url,subtitles='',playterm=False,playlistTitle='',returning=False):
    final = ''
    countloop = 0
    sitebase,sitename,color,mode = returnValues(url)
    host = sitebase.replace('https://','').replace('/','')
    if playlistTitle == '': mensagemprogresso.create(sitename, traducao(40025))
    linkfinal=''
    if subtitles=='sim': conteudo=abrir_url_cookie(url)
    else:conteudo=abrir_url_cookie(url,erro=False)
    if re.search('Pode acontecer que a mensagem de confirma',conteudo):
        mensagemok(sitename,'Necessitas de activar a tua conta '+sitename+'.')
        return
    try:
        fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0]
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        form_d = {'fileId':fileid,'__RequestVerificationToken':token}
        ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'https://' + host, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://'+host+'/','User-Agent':user_agent}
        endlogin=sitebase + 'action/License/Download'
        while final == '' and countloop <= 3:
            try: final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
            countloop = countloop + 1
        final=final.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
    except: pass
    try:
        if re.search('action/License/acceptLargeTransfer',final):
              fileid=re.compile('<input type="hidden" name="fileId" value="(.+?)"').findall(final)[0]
              orgfile=re.compile('<input type="hidden" name="orgFile" value="(.+?)"').findall(final)[0]
              userselection=re.compile('<input type="hidden" name="userSelection" value="(.+?)"').findall(final)[0]
              form_d = {'fileId':fileid,'orgFile':orgfile,'userSelection':userselection,'__RequestVerificationToken':token}
              ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'https://' + sitebase, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://'+sitebase+'/','User-Agent':user_agent}
              endlogin=sitebase + 'action/License/acceptLargeTransfer'
              final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
    except: pass
    try:
        if re.search('causar problemas com o uso de aceleradores de download',final):linkfinal=re.compile('a href=\"(.+?)\"').findall(final)[0]
        else: linkfinal=re.compile('"redirectUrl":"(.+?)"').findall(final)[0]
        if subtitles=='sim':return linkfinal
    except:
        if subtitles=='':
              if re.search('Por favor, tenta baixar este ficheiro mais tarde.',final):
                    mensagemok(sitename,traducao(40026))
                    return
              else:
                    mensagemok(sitename,traducao(40027))
                    print str(final)
                    print str(linkfinal)
                    return
        else: return
    if playlistTitle == '': mensagemprogresso.close()
    linkfinal=linkfinal.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
    if returning==True:
                return linkfinal
    if re.search('.jpg',url) or re.search('.png',url) or re.search('.gif',url) or re.search('.bmp',url):
        if re.search('.jpg',url): extfic='temp.jpg'
        elif re.search('.png',url): extfic='temp.png'
        elif re.search('.gif',url): extfic='temp.gif'
        elif re.search('.bmp',url): extfic='temp.bmp'
        fich=os.path.join(pastaperfil, extfic)
        try:os.remove(fich)
        except:pass
        if playterm=="download":fazerdownload(extfic,linkfinal)
        else:fazerdownload(extfic,linkfinal,tipo="fotos")
        xbmc.executebuiltin("SlideShow("+pastaperfil+")")
    elif re.search('.mkv',url) or re.search('.ogm',url) or re.search('.avi',url) or re.search('.wmv',url) or re.search('.mp4',url) or re.search('.mpg',url) or re.search('.mpeg',url):
        endereco=legendas(fileid,url)
        if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm,legendas=endereco)
        else: comecarvideo(name,linkfinal,playterm=playterm,legendas=endereco)
    elif re.search('.mp3',url) or re.search('.aac',url) or re.search('.m4a',url) or re.search('.ac3',url) or re.search('.wma',url):
        if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm)
        else: comecarvideo(name,linkfinal,playterm=playterm)
    else:
        if selfAddon.getSetting('aviso-extensao') == 'true': mensagemok(sitename,traducao(40028),traducao(40029),traducao(40030))
        if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm)
        else: comecarvideo(name,linkfinal,playterm=playterm)

def comecarvideo(name,url,playterm,legendas=None):
        #url=url.replace('&pv=2','&pv=1')
        #url=url + '|User-Agent=' + urllib.quote(user_agent)
    content=''
    dbid=''
    if not playterm:
        try: xbmc.Player().stop()
        except: pass
    sitename='Chomikuj - '+clean_folder(name.replace(',',''))
    playeractivo = xbmc.getCondVisibility('Player.HasMedia')
    if playterm=='download':
          fazerdownload(name,url)
          return
    thumbnail=''
    playlist = xbmc.PlayList(1)
    if not playterm and playeractivo==0: playlist.clear()
    listitem = xbmcgui.ListItem(path=url)
    title = name
    if not playterm:
        title='%s' % (name.split('[/B]')[0].replace('[B]',''))

        try:
            print "Testing Movie"
            modtitle = title.replace (" ", "+")+".strm"
            modtitle = modtitle.replace ("(", "%28")
            modtitle = modtitle.replace (")", "%29")
            meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter": {"field": "path", "operator": "contains", "value": "%s"}, "properties" : ["title", "originaltitle", "year", "genre", "studio", "country", "runtime", "rating", "votes", "mpaa", "director", "writer", "plot", "plotoutline", "tagline", "thumbnail", "file"]}, "id": 1}' % title)
            print str(meta)

            meta = unicode(meta, 'utf-8', errors='ignore')
            meta = json.loads(meta)['result']['movies']
            selfmeta = [i for i in meta if i['file'].endswith(modtitle)][0]
            meta = {'title': selfmeta['title'].encode('utf-8'), 'originaltitle': selfmeta['originaltitle'].encode('utf-8'), 'year': selfmeta['year'], 'genre': str(" / ".join(selfmeta['genre']).encode('utf-8')), 'studio' : str(" / ".join(selfmeta['studio']).encode('utf-8')), 'country' : str(" / ".join(selfmeta['country']).encode('utf-8')), 'duration' : selfmeta['runtime'], 'rating': selfmeta['rating'], 'votes': selfmeta['votes'], 'mpaa': selfmeta['mpaa'].encode('utf-8'), 'director': str(" / ".join(selfmeta['director']).encode('utf-8')), 'writer': str(" / ".join(selfmeta['writer']).encode('utf-8')), 'plot': selfmeta['plot'].encode('utf-8'), 'plotoutline': selfmeta['plotoutline'].encode('utf-8'), 'tagline': selfmeta['tagline'].encode('utf-8')}

            dbid = selfmeta['movieid']
            thumb = selfmeta['thumbnail']
            content='Movie'
        except:
            try:
                print "Testing TV"
                modtitle = title.replace (" ", "+")+".strm"
                season, episode = re.compile('.+?S(..)E(..)').findall(title)[0]
                season, episode = '%01d' % int(season), '%01d' % int(episode)
                meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "season", "episode", "showtitle", "firstaired", "runtime", "rating", "director", "writer", "plot", "thumbnail", "file"]}, "id": 1}' % (int(season), int(episode)))
                print str(meta)

                meta = unicode(meta, 'utf-8', errors='ignore')
                meta = json.loads(meta)['result']['episodes']
                selfmeta = [i for i in meta if i['file'].endswith(modtitle)][0]
                meta = {'title': selfmeta['title'].encode('utf-8'), 'season' : selfmeta['season'], 'episode': selfmeta['episode'], 'tvshowtitle': selfmeta['showtitle'].encode('utf-8'), 'premiered' : selfmeta['firstaired'], 'duration' : selfmeta['runtime'], 'rating': selfmeta['rating'], 'director': str(" / ".join(selfmeta['director']).encode('utf-8')), 'writer': str(" / ".join(selfmeta['writer']).encode('utf-8')), 'plot': selfmeta['plot'].encode('utf-8')}

                dbid = selfmeta['episodeid']
                thumb = selfmeta['thumbnail']
                poster = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter": {"field": "title", "operator": "is", "value": "%s"}, "properties": ["thumbnail"]}, "id": 1}' % selfmeta['showtitle'])
                poster = unicode(poster, 'utf-8', errors='ignore')
                poster = json.loads(poster)['result']['tvshows'][0]['thumbnail']
               #thumb = poster     # Uncomment to switch to TV Show Poster Instead of Episode Thumb
                content='TV'
            except:
                meta=''
                content=''
                thumb=''
                dbid=''
        listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
        listitem.setInfo(type="Video", infoLabels = meta)

    else:
        listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
        listitem.setInfo("Video", {"title":title})
        listitem.setInfo("Music", {"title":title})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    if playterm <> 'playlist':
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create('Video', 'A carregar...')
    playlist.add(url, listitem)
    if playterm <> 'playlist':
        dialogWait.close()
        del dialogWait
    xbmcPlayer = internalPlayer.Player(title=title,dbid=dbid,content=content)
    if not playterm and playeractivo==0: xbmcPlayer.play(playlist, listitem)
    if legendas!=None: xbmcPlayer.setSubtitles(legendas)
    else:
        if selfAddon.getSetting("subtitles") == 'true':
            try: totalTime = xbmcPlayer.getTotalTime()
            except: totalTime = 0
            print '##totaltime',totalTime
            if totalTime >= int(selfAddon.getSetting("minsize"))*60:
                print '#pesquisar legendas'
                from resources.lib import subtitles
                try: legendas = subtitles.getsubtitles(name,selfAddon.getSetting("sublang1"),selfAddon.getSetting("sublang2"))
                except:
                    print '#error searching subtitles'
                    legendas = None
                    pass
                if legendas!=None: xbmcPlayer.setSubtitles(legendas)
    if selfAddon.getSetting('track-player')=='true' and not playterm:
        while xbmcPlayer.playing:
            xbmc.sleep(5000)
            xbmcPlayer.track_time()
    if playterm=='playlist': xbmc.executebuiltin("XBMC.Notification("+sitename+","+traducao(40039)+",'500000',"+iconpequeno.encode('utf-8')+")")

def limparplaylist():
        playlist = xbmc.PlayList(1)
        playlist.clear()
        xbmc.executebuiltin("XBMC.Notification(Chomiteca,"+traducao(40048)+",'500000',"+iconpequeno.encode('utf-8')+")")

def comecarplaylist():
        playlist = xbmc.PlayList(1)
        if playlist:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(playlist)

def legendas(moviefileid,url):
    url=url.replace(','+moviefileid,'').replace('.mkv','.srt').replace('.mp4','.srt').replace('.avi','.srt').replace('.wmv','.srt')[:-7]
    try:
        if(urllib2.urlopen(url).getcode() == 200): legendas=analyzer(url,subtitles='sim')
    except Exception:
        legendas=url
    return legendas

def add_to_library_batch(updatelibrary=True):
    source = xbmcgui.Dialog().select
    selectlist = ["Filmes","Séries","Videoclips"]
    optionlist = ['movie', 'tvshow', 'musicvideo']
    choose=source('Tipo',selectlist)
    if choose > -1:    type = optionlist[choose]
    else: sys.exit(0)
    conteudo = openfile('playlist.txt')
    playlistsearch=re.compile('\[["|\'](.+?)["|\'], \'(.+?)\'\]').findall(conteudo)
    for titulo,url in playlistsearch:
        add_to_library(titulo,url,type,'0',False)
    if updatelibrary: xbmc.executebuiltin("XBMC.UpdateLibrary(video)")

def ReplaceSpecialChar(name):
    try: name = name.encode('utf-8')
    except: pass
    return name.replace('/','-')

def ReplaceSpecialCharExtra(name):
    try: name = name.encode('utf-8')
    except: pass
    return name.replace('/','-').replace('Ç','C').replace('ç','c').replace('À','A').replace('Á','A').replace('Ã','A').replace('Â','A').replace('Ä','A').replace('à','a').replace('á','a').replace('ã','a').replace('â','a').replace('ä','a').replace('È','E').replace('É','E').replace('Ê','E').replace('Ë','E').replace('è','e').replace('é','e').replace('ê','e').replace('ë','e').replace('Ì','I').replace('Í','I').replace('Î','I').replace('Ï','I').replace('ì','i').replace('í','i').replace('î','i').replace('ï','i').replace('Ò','O').replace('Ó','O').replace('Õ','O').replace('Ô','O').replace('Ö','O').replace('ò','o').replace('ó','o').replace('õ','o').replace('ô','o').replace('ö','o').replace('Ù','U').replace('Ú','U').replace('Û','U').replace('Ü','U').replace('ù','u').replace('ú','u').replace('û','u').replace('ü','u')

def clean_title(title):
    return title.replace('+',' ').replace('%27',"'").replace('%2C',',').replace('%28','(').replace('%29',')').replace('%26','&').replace('%24','$').replace('%5Cxc2%5Cxba','º').replace('%5Cxc3%5Cx87','Ç').replace('%5Cxc3%5Cxa7','ç').replace('%5Cxc3%5Cx80','À').replace('%5Cxc3%5Cx81','Á').replace('%5Cxc3%5Cx83','Ã').replace('%5Cxc3%5Cx82','Â').replace('%5Cxc3%5Cx84','Ä').replace('%5Cxc3%5Cxa0','à').replace('%5Cxc3%5Cxa1','á').replace('%5Cxc3%5Cxa3','ã').replace('%5Cxc3%5Cxa2','â').replace('%5Cxc3%5Cxa4','ä').replace('%5Cxc3%5Cx88','È').replace('%5Cxc3%5Cx89','É').replace('%5Cxc3%5Cx8a','Ê').replace('%5Cxc3%5Cx8b','Ë').replace('%5Cxc3%5Cxa8','è').replace('%5Cxc3%5Cxa9','é').replace('%5Cxc3%5Cxaa','ê').replace('%5Cxc3%5Cxab','ë').replace('%5Cxc3%5Cx8c','Ì').replace('%5Cxc3%5Cx8d','Í').replace('%5Cxc3%5Cx8e','Î').replace('%5Cxc3%5Cx8f','Ï').replace('%5Cxc3%5Cxac','ì').replace('%5Cxc3%5Cxad','í').replace('%5Cxc3%5Cxae','î').replace('%5Cxc3%5Cxaf','ï').replace('%5Cxc3%5Cx92','Ò').replace('%5Cxc3%5Cx94','Ó').replace('%5Cxc3%5Cx95','Õ').replace('%5Cxc3%5Cx93','Ô').replace('%5Cxc3%5Cx96','Ö').replace('%5Cxc3%5Cxb2','ò').replace('%5Cxc3%5Cxb3','ó').replace('%5Cxc3%5Cxb5','õ').replace('%5Cxc3%5Cxb4','ô').replace('%5Cxc3%5Cxb6','ö').replace('%5Cxc3%5Cx99','Ù').replace('%5Cxc3%5Cx9a','Ú').replace('%5Cxc3%5Cx9b','Û').replace('%5Cxc3%5Cx9c','Ü').replace('%5Cxc3%5Cxb9','ù').replace('%5Cxc3%5Cxba','ú').replace('%5Cxc3%5Cxbb','û').replace('%5Cxc3%5Cxbc','ü')

def clean_folder(folder):
    return folder.replace('\\xc3\\xa0','à').replace('\\xc3\\xa1','á').replace('\\xc3\\xa2','â').replace('\\xc3\\xa3','ã').replace('\\xc3\\xa4','ä').replace('\\xc3\\xa5','å').replace('\\xc3\\xa6','æ').replace('\\xc3\\xa7','ç').replace('\\xc3\\xa8','è').replace('\\xc3\\xa9','é').replace('\\xc3\\xaa','ê').replace('\\xc3\\xab','ë').replace('\\xc3\\xac','ì').replace('\\xc3\\xad','í').replace('\\xc3\\xae','î').replace('\\xc3\\xaf','ï').replace('\\xc3\\xb2','ò').replace('\\xc3\\xb3','ó').replace('\\xc3\\xb4','ô').replace('\\xc3\\xb5','õ').replace('\\xc3\\xb6','ö').replace('\\xc3\\xb9','ù').replace('\\xc3\\xba','ú').replace('\\xc3\\xbb','û').replace('\\xc3\\xbc','ü').replace('\\xc3\\x80','À').replace('\\xc3\\x81','Á').replace('\\xc3\\x82','Â').replace('\\xc3\\x83','Ã').replace('\\xc3\\x84','Ä').replace('\\xc3\\x85','Å').replace('\\xc3\\x86','Æ').replace('\\xc3\\x87','Ç').replace('\\xc3\\x88','È').replace('\\xc3\\x89','É').replace('\\xc3\\x8a','Ê').replace('\\xc3\\x8b','Ë').replace('\\xc3\\x8c','Ì').replace('\\xc3\\x8d','Í').replace('\\xc3\\x8e','Î').replace('\\xc3\\x8f','Ï').replace('\\xc3\\x92','Ò').replace('\\xc3\\x93','Ó').replace('\\xc3\\x94','Ô').replace('\\xc3\\x95','Õ').replace('\\xc3\\x96','Ö').replace('\\xc3\\x99','Ù').replace('\\xc3\\x9a','Ú').replace('\\xc3\\x9b','Û').replace('\\xc3\\x9c','Ü')

def clean_url(url):
    return url.replace('%C3%A0','à').replace('%C3%A1','á').replace('%C3%A2','â').replace('%C3%A3','ã').replace('%C3%A4','ä').replace('%C3%A5','å').replace('%C3%A6','æ').replace('%C3%A7','ç').replace('%C3%A8','è').replace('%C3%A9','é').replace('%C3%AA','ê').replace('%C3%AB','ë').replace('%C3%AC','ì').replace('%C3%AD','í').replace('%C3%AE','î').replace('%C3%AF','ï').replace('%C3%B2','ò').replace('%C3%B3','ó').replace('%C3%B4','ô').replace('%C3%B5','õ').replace('%C3%B6','ö').replace('%C3%B9','ù').replace('%C3%BA','ú').replace('%C3%BB','û').replace('%C3%BC','ü').replace('%C3%80','À').replace('%C3%81','Á').replace('%C3%82','Â').replace('%C3%83','Ã').replace('%C3%84','Ä').replace('%C3%85','Å').replace('%C3%86','Æ').replace('%C3%87','Ç').replace('%C3%88','È').replace('%C3%89','É').replace('%C3%8A','Ê').replace('%C3%8B','Ë').replace('%C3%8C','Ì').replace('%C3%8D','Í').replace('%C3%8E','Î').replace('%C3%8F','Ï').replace('%C3%92','Ò').replace('%C3%93','Ó').replace('%C3%94','Ô').replace('%C3%95','Õ').replace('%C3%96','Ö').replace('%C3%99','Ù').replace('%C3%9A','Ú').replace('%C3%9B','Û').replace('%C3%9C','Ü')

def add_to_library_opt(name,url,updatelibrary=True):
    source = xbmcgui.Dialog().select
    selectlist = ["Filmes","Séries","Videoclips"]
    optionlist = ['movie', 'tvshow', 'musicvideo']
    choose=source('Tipo',selectlist)
    if choose > -1:    type = optionlist[choose]
    else: sys.exit(0)
    add_to_library(name,url,type,'1',False)

def add_to_library(name,url,type,batch,updatelibrary=True):
    episode = ''
    tvshow = ''
    season = ''
    title = ''

    name2 = re.compile('\[B\]\[COLOR .+?\](.+?)\[/COLOR\]\[/B\]').findall(name)
    if name2:
        name = ReplaceSpecialChar(h.unescape(name2[0]))
        cleaned = re.sub('[^-a-zA-Z0-9ÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇáàãâäéèêëíìîïóòõôöúùûüç&$,.\'()\\\/ ]+', ' ', name[:-4])
        cleaned = re.sub(' +$', '', cleaned)
        cleaned = re.sub('\.$', '', cleaned)
        cleaned_title = re.sub('^ +', '', cleaned)
    else:
        name = ReplaceSpecialChar(h.unescape(name))
        cleaned = re.sub('[^-a-zA-Z0-9ÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇáàãâäéèêëíìîïóòõôöúùûüç&$,.\'()\\\/ ]+', ' ', name)
        cleaned = re.sub(' +$', '', cleaned)
        cleaned = re.sub('\.$', '', cleaned)
        cleaned_title = re.sub('^ +', '', cleaned)
    if type == 'movie':
        if not xbmcvfs.exists(moviesFolder): xbmcvfs.mkdir(moviesFolder)
    elif type == 'tvshow':
        if not xbmcvfs.exists(tvshowFolder): xbmcvfs.mkdir(tvshowFolder)
    elif type == 'musicvideo':
        if not xbmcvfs.exists(musicvideoFolder): xbmcvfs.mkdir(musicvideoFolder)
    if type == 'tvshow':
        if(selfAddon.getSetting('tvshowname-enable') == 'true'):
            tvshow,season,episode = GetTVShowNameResolved(cleaned_title)
            titulo = clean_folder(cleaned_title)
        else:
            tvshow,season,episode = GetTVShowNameResolved(cleaned_title)
    if (type == 'movie') or (type == 'musicvideo') or (type == 'tvshow' and tvshow == ''):
        keyb = xbmc.Keyboard(cleaned_title, traducao(40053))
        if(batch != '0'):
            keyb.doModal()
            if (keyb.isConfirmed()):
                title = keyb.getText()
                if title=='': sys.exit(0)
            else: sys.exit(0)
        else:
            title = clean_folder(cleaned_title)
            if title=='': sys.exit(0)
    if title <> '':
        title = re.sub('[^-a-zA-Z0-9ÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇáàãâäéèêëíìîïóòõôöúùûüç&$,.\'()\\\/ ]+', ' ', ReplaceSpecialChar(title))
        title = re.sub(' +$', '', title)
        title = re.sub('\.$', '', title)
        title = re.sub('^ +', '', title)
    if type == 'movie':
        try:
            if(selfAddon.getSetting('movielibrary-enable') == 'true'): file_folder = os.path.join(moviesFolder,title)
            else: file_folder = os.path.join(moviesFolder,'')
        except:
            if(selfAddon.getSetting('movielibrary-enable') == 'true'): file_folder = os.path.join(moviesFolder,cleaned_title)
            else: file_folder = os.path.join(moviesFolder,'')
    elif type == 'tvshow':
        tvshow = clean_folder(tvshow)
        tvshow = re.sub('\.$', '', tvshow)
        if tvshow <> '':
            file_folder1 = os.path.join(tvshowFolder,tvshow)
            if not xbmcvfs.exists(file_folder1): tryFTPfolder(file_folder1)
            if(selfAddon.getSetting('tvshowlibrary-enable') == 'true'):
                if(selfAddon.getSetting('tvshowname-enable') == 'false'):
                    file_folder = os.path.join(tvshowFolder,tvshow+'/',tvshow+' '+traducao(40073)+' '+season)
                    title = tvshow + ' S'+season+'E'+episode
                else:
                    file_folder = os.path.join(tvshowFolder,tvshow+'/',tvshow+' '+traducao(40073)+' '+season)
                    title = titulo
            else:
                if(selfAddon.getSetting('tvshowname-enable') == 'false'):
                    file_folder = os.path.join(tvshowFolder,tvshow)
                    title = tvshow + ' S'+season+'E'+episode
                else:
                    file_folder = os.path.join(tvshowFolder,tvshow)
                    title = titulo
        else:
            if title == '': title = cleaned_title
            tvshow,season,episode = GetTVShowNameResolved(title)
            if tvshow <> '':
                file_folder1 = os.path.join(tvshowFolder,tvshow)
                if not xbmcvfs.exists(file_folder1): tryFTPfolder(file_folder1)
                file_folder = os.path.join(tvshowFolder,title+'/','S'+season)
                title =  tvshow + ' S'+season+'E'+episode
            else: file_folder = os.path.join(tvshowFolder,title)
    elif type == 'musicvideo': file_folder = musicvideoFolder
    if not xbmcvfs.exists(file_folder): tryFTPfolder(file_folder)
    strm_contents = 'plugin://plugin.video.chomiteca/?url=' + url +'&mode=25&name=' + urllib.quote_plus(title)
    if type == 'movie': savefile(clean_url(clean_title(urllib.quote_plus(title)))+'.strm',strm_contents,file_folder)
    if type == 'tvshow': savefile((urllib.unquote_plus(title))+'.strm',strm_contents,file_folder)
    if updatelibrary: xbmc.executebuiltin("XBMC.UpdateLibrary(video)")

def tryFTPfolder(file_folder):
    if 'ftp://' in file_folder:
        try:
            from ftplib import FTP
            ftparg = re.compile('ftp://(.+?):(.+?)@(.+?):?(\d+)?/(.+/?)').findall(file_folder)
            ftp = FTP(ftparg[0][2],ftparg[0][0],ftparg[0][1])
            try: ftp.cwd(ftparg[0][4])
            except: ftp.mkd(ftparg[0][4])
            ftp.quit()
        except: print 'Nao conseguiu criar %s' % file_folder
    else: xbmcvfs.mkdir(file_folder)

def GetTVShowNameResolved(title):
    episode = ''
    tvshow = ''
    season = ''
    epi = re.compile('(.+?)[ ]?[Ss]?(\d{1,4})[EeXx.](\d{1,4}[ab]?).+?').findall(title)
    if epi:
        for n,s,e in epi:
            tvshow = n.replace('-','').strip()
            season = s
            if len(season) == 1 : season = '0'+season
            episode = e
            if len(episode) == 1 : episode = '0'+episode
    else:
        epi = re.compile('(.+?)[ \._]?E?p?(\d{1,4}).?[?[A-Fa-f0-9]*]?').findall(title)
        for n,e in epi:
            tvshow = n.replace('-','').strip()
            season = '01'
            episode = e
            if len(episode) == 1 : episode = '0'+episode
    return tvshow,season,episode

def play_from_outside(name,url):
    login(True)
    analyzer(url.replace(' ','+'))

################################################## PASTAS ################################################################
def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta,atalhos=False):
      contexto=[]
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      contexto.append((traducao(40047), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40056), 'RunPlugin(%s?mode=17&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      if atalhos==False:contexto.append((traducao(40055), 'RunPlugin(%s?mode=20&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      else:contexto.append((traducao(40065), 'RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),atalhos)))
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems(contexto, replaceItems=False)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addCont(name,url,mode,tamanho,iconimage,total,pasta=False,atalhos=False):
    contexto=[]
    try: name = name.encode('ascii', 'xmlcharrefreplace')
    except: pass
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&tamanhof="+urllib.quote_plus(tamanho)
    liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    contexto.append((traducao(40038), 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
    contexto.append((traducao(40050), 'XBMC.RunPlugin(%s?mode=15&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
    contexto.append((traducao(40046), 'XBMC.RunPlugin(%s?mode=13&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
    contexto.append((traducao(40047), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
    contexto.append((traducao(40051), 'XBMC.RunPlugin(%s?mode=26&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),urllib.quote_plus(name))))
    contexto.append((traducao(40051)+' - Batch', 'XBMC.RunPlugin(%s?mode=30&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),urllib.quote_plus(name))))
    contexto.append((traducao(40056), 'RunPlugin(%s?mode=17&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
    if atalhos==False: contexto.append((traducao(40055), 'RunPlugin(%s?mode=19&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
    else: contexto.append((traducao(40065), 'RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),atalhos)))
    contexto.append((traducao(40040), 'XBMC.RunPlugin(%s?mode=11&url=%s&name=%s&tamanhof=%s)' % (sys.argv[0], urllib.quote_plus(url),name,tamanho)))
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    liz.addContextMenuItems(contexto, replaceItems=True)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

######################################################## DOWNLOAD ###############################################
### THANKS ELDORADO (ICEFILMS) ###
def fazerdownload(name,url,tipo="outros"):
      vidname=name.replace('[B]','').replace('[/B]','').replace('\\','').replace(str(tamanhoparavariavel),'')#.replace('[/COLOR]','')
      vidname=vidname.split(']')[1].split('[')[0]
      vidname = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  vidname)
      dialog = xbmcgui.Dialog()
      if tipo=="fotos": mypath=os.path.join(pastaperfil, vidname)
      else:
            downloadPath = dialog.browse(int(3), traducao(40041),'myprograms')
            if os.path.exists(downloadPath): mypath=os.path.join(downloadPath,vidname)
            else: return
      if os.path.isfile(mypath) is True:
            ok = mensagemok('Chomiteca',traducao(40042),'','')
            return False
      else:
            from resources.lib import downloader
            downloader.download(url, mypath, 'Chomiteca')

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
            kbps_speed = numblocks * blocksize / (time.time() - start_time)
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed
            else: eta = 0
            kbps_speed = kbps_speed / 1024
            total = float(filesize) / (1024 * 1024)
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total)
            e = ' (%.0f Kb/s) ' % kbps_speed
            tempo = traducao(40045) + ': %02d:%02d' % divmod(eta, 60)
            dp.update(percent, mbs + e,tempo)
      except:
            percent = 100
            dp.update(percent)
      if dp.iscanceled():
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value
      def __str__(self): return repr(self.value)

######################################################## OUTRAS FUNÇÕES ###############################################
def caixadetexto(url,ftype=''):
    ultpes=''
    save=False
    if url=='pastas': title=traducao(40010) + "Chomikuj"
    elif url=='password': title=traducao(40061)
    elif url=='pesquisa':
        title=traducao(40031)
        ultpes=selfAddon.getSetting('ultima-pesquisa')
        save=True
    else: title="Minhateca"
    keyb = xbmc.Keyboard(ultpes, title)
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        if search=='': sys.exit(0)
        encode=urllib.quote_plus(search)
        if save==True: selfAddon.setSetting('ultima-pesquisa', search)
        if url=='pastas': pastas(MainURL + search,name)
        elif url=='password': return search
        elif url=='pesquisa':
            if ReturnStatus('chomikuj'):
                form_d = {'FileName':encode,'submitSearchFiles':'Szukaj','FileType':ftype,'IsGallery':'False'}
                pastas(MainURL + 'action/SearchFiles',name,formcont=form_d,past=True)
    else: sys.exit(0)

def abrir_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def savefile(filename, contents,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal,filename)
        fh = xbmcvfs.File(destination, 'w')
        fh.write(str(contents))
        fh.close()
    except: print "Não gravou os temporários de: %s | %s" % (filename,destination)

def openfile(filename,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal, filename)
        fh = xbmcvfs.File(destination)
        contents = fh.read()
        fh.close()
        return contents
    except:
        traceback.print_exc()
        print "Não abriu conteúdos de: %s" % filename
        return None

def abrir_url_cookie(url,erro=True):
    net.set_cookies(cookies)
    try:
        if ReturnStatus('chomikuj'): ref_data = {'Host': 'chomikuj.pl', 'Connection': 'keep-alive', 'Referer': 'https://chomikuj.pl','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'https://chomikuj.pl'}
        link=net.http_POST(url,ref_data).content.encode('latin-1','ignore')
        return link
    except urllib2.HTTPError, e:
        if erro==True: mensagemok('Chomiteca',str(urllib2.HTTPError(e.url, e.code, traducao(40032), e.hdrs, e.fp)),traducao(40033))
        sys.exit(0)
    except urllib2.URLError, e:
        if erro==True: mensagemok('Chomiteca',traducao(40032)+traducao(40033))
        sys.exit(0)

def redirect(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    gurl=response.geturl()
    return gurl

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

def clean(text):
    command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&amp;':'&','&ntilde;':'ñ','&#35;':'#','&#39;':'\'','&#40;':'(','&#41;':')','&#44;':',','&#46;':'.','&#170;':'ª','&#178;':'²','&#179;':'³','&#192;':'À','&#193;':'Á','&#194;':'Â','&#195;':'Ã','&#199;':'Ç','&#201;':'É','&#202;':'Ê','&#205;':'Í','&#211;':'Ó','&#212;':'Ô','&#213;':'Õ','&#217;':'Ù','&#218;':'Ú','&#224;':'à','&#225;':'á','&#226;':'â','&#227;':'ã','&#231;':'ç','&#232;':'è','&#233;':'é','&#234;':'ê','&#237;':'í','&#243;':'ó','&#244;':'ô','&#245;':'õ','&#249;':'ù','&#250;':'ú'}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def traducao(texto):
    return traducaoma(texto).encode('utf-8')

def test(pesquisa):
    login(True)
    encode=urllib.quote_plus(pesquisa)
    form_d = {'FileName':encode,'submitSearchFiles':'Buscar','FileType':'video','IsGallery':'False'}
    return pastas(MainURL + 'action/SearchFiles',name,formcont=form_d,past=True,deFora=True,listagem=True)

params=get_params()
url=None
name=None
mode=None
tamanhoparavariavel=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: tamanhoparavariavel=urllib.unquote_plus(params["tamanhof"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Name: "+str(tamanhoparavariavel)

if mode==None or url==None or len(url)<1:
    if (selfAddon.getSetting('chomikuj-enable') == 'false'):
        ok = mensagemok('Chomiteca','Precisa de configurar a conta do Chomikuj','para aceder aos conteúdos.')
        entrarnovamente(1)
    else:
        if (selfAddon.getSetting('chomikuj-enable') == 'true' and not selfAddon.getSetting('chomikuj-username')== '') : login()
        menu_principal(1)
elif mode==1: topcolecionadores()
elif mode==2: chomitecamaisrecentes(url)
elif mode==3: pastas(url,name)
elif mode==4: analyzer(url)
elif mode==5: caixadetexto(url)
elif mode==6: login()
elif mode==7: pesquisa()
elif mode==8: selfAddon.openSettings()
elif mode==9: favoritos()
elif mode==10: analyzer(url,subtitles='',playterm='playlist')
elif mode==11: analyzer(url,subtitles='',playterm='download')
elif mode==13: comecarplaylist()
elif mode==14: limparplaylist()
elif mode==15: criarplaylist(url,name)
elif mode==16: obterlistadeficheiros()
elif mode==17: trailer(name)
elif mode==18: atalhos()
elif mode==19: atalhos(type='addfile')
elif mode==20: atalhos(type='addfolder')
elif mode==21: atalhos(type='remove')
elif mode==22: pastas('/'.join(url.split('/')[:-1]),name)
elif mode==23: pastas_de_fora(url,name)
elif mode==24: proxpesquisa_ck()
elif mode==25: play_from_outside(name,url)
elif mode==26: add_to_library_opt(name,url)
elif mode==30: add_to_library_batch()

if 'Chomiteca' in xbmcaddon.Addon().getAddonInfo('name'): xbmcplugin.endOfDirectory(int(sys.argv[1]))
