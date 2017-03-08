# -*- coding: utf-8 -*-
from variables import *

def addDirectoryItem(name, query, thumb, icon, queue=False, isAction=True, isFolder=True):
        artPath = None
        addonFanart = thumb
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        #thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True and isPlayable == True: cm.append((lang(30155).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))
        itemcontent = item(label=name, iconImage=thumb, thumbnailImage=thumb)
        itemcontent.addContextMenuItems(cm, replaceItems=False)
        itemcontent.setProperty('Fanart_Image', thumb)
        addItem(handle=int(sys.argv[1]), url=url, listitem=itemcontent, isFolder=isFolder)

def endDirectory(cacheToDisc=True):
        directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)

def Debug(content):
        xbmc.log(str(content), level=xbmc.LOGNOTICE)

def warning_dialog(title="CopiaPop.com",text=""):
        try:
                xbmc.executebuiltin("ActivateWindow(10147)")
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(title)
                window.getControl(5).setText(text)
        except: pass
