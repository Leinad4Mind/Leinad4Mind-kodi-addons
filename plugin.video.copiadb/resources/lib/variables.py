# -*- coding: utf-8 -*-

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs,re,os,sys,urllib,json
import time
from random import randint

CopiaPopURL = 'http://copiapop.com'
SearchParam = '/action/SearchFiles'
addon_id = 'plugin.video.abelhas'
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
lang = xbmcaddon.Addon().getLocalizedString
setting = xbmcaddon.Addon().getSetting
setSetting = xbmcaddon.Addon().setSetting
addon = xbmcaddon.Addon
addItem = xbmcplugin.addDirectoryItem
item = xbmcgui.ListItem
directory = xbmcplugin.endOfDirectory
content = xbmcplugin.setContent
property = xbmcplugin.setProperty
addonInfo = xbmcaddon.Addon().getAddonInfo
infoLabel = xbmc.getInfoLabel
condVisibility = xbmc.getCondVisibility
jsonrpc = xbmc.executeJSONRPC
window = xbmcgui.Window(10000)
dialog = xbmcgui.Dialog()
progressDialog = xbmcgui.DialogProgress()
windowDialog = xbmcgui.WindowDialog()
button = xbmcgui.ControlButton
image = xbmcgui.ControlImage
keyboard = xbmc.Keyboard
sleep = xbmc.sleep
execute = xbmc.executebuiltin
skin = xbmc.getSkinDir()
player = xbmc.Player()
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
resolve = xbmcplugin.setResolvedUrl
openFile = xbmcvfs.File
makeFile = xbmcvfs.mkdir
deleteFile = xbmcvfs.delete
listDir = xbmcvfs.listdir
transPath = xbmc.translatePath
skinPath = xbmc.translatePath('special://skin/')
addonPath = xbmc.translatePath(addonInfo('path'))
dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
settingsFile = os.path.join(dataPath, 'settings.xml')
sysaddon = sys.argv[0]
