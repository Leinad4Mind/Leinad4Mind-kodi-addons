# -*- coding: utf-8 -*-

""" Chomiteca
    2015-2016 fightnight/Leinad4Mind"""

import xbmc,xbmcaddon,xbmcgui,os,xbmcvfs,re

addon_id = 'plugin.video.chomiteca'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getSetting('resumefolder'))
track = selfAddon.getSetting('track-player')

class Player(xbmc.Player):
	def __init__(self,title,dbid,content):
		xbmc.Player.__init__(self)
		print "Title: "+str(title)
		self.dbid = dbid
		self.content = content

		try: self.title=re.sub('[^-a-zA-Z0-9_\.()\\\/ ]+', ' ',  re.compile("\[COLOR .+?\](.+?)\[/COLOR\]").findall(title)[0])
		except: self.title=re.sub('[^-a-zA-Z0-9_\.()\\\/ ]+', ' ',  title)
		self.playing = True
		self.time = 0
		self.totalTime = 0
		self.racio = 0
		if track == 'true':
			try: self.id = self.title
			except: self.id = None
			if not xbmcvfs.exists(datapath): xbmcvfs.mkdir(datapath)
			if self.id: self.filemedia = os.path.join(datapath,str(self.id)+'.txt')
			else: self.filemedia = None

	def onPlayBackStarted(self):
		print "Content: "+str(self.content) 
		print "DBID: "+str(self.dbid)
		try:
			self.totalTime = self.getTotalTime()
			print 'total time',self.totalTime
			if track == 'true' and self.isPlayingVideo():
				if xbmcvfs.exists(self.filemedia):
					print "Resume point available..."
					tracker=readfile(self.filemedia)
					opcao=xbmcgui.Dialog().yesno("Chomiteca", 'Resume point available.','Continue from '+ ' %s?' % (format_time(float(tracker))),'', 'No', 'Yes')
					if opcao: self.seekTime(float(tracker))
		except: pass

	def onPlayBackStopped(self):
		print 'player Stop'
		self.playing = False
		time = int(self.time)
		try: self.racio = self.time/self.totalTime
		except: self.racio = 0.50
		print 'self.racio %s' % (self.racio)
		if self.racio > 0.90:
			self.onPlayBackEnded()
			if track == 'true' and self.isPlayingVideo():
				try: xbmcvfs.delete(self.filemedia)
				except: pass
		if self.racio < 0.05:
			try: xbmcvfs.delete(self.filemedia)
			except: pass

	def onPlayBackEnded(self):
		if str(self.content) == 'TV':
			print "Marking Episode as watched"
			xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.dbid))
		elif str(self.content) == 'Movie':
			print "Marking Movie as watched"
			xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.dbid))
		xbmc.executebuiltin('Container.Refresh')
		try: self.racio = self.time/self.totalTime
		except: self.racio = 0.50
		print 'self.racio %s' % (self.racio)
		if self.racio > 0.90:
			if track == 'true': # and self.isPlayingVideo():
				try: xbmcvfs.delete(self.filemedia)
				except: pass

	def track_time(self):
		try:
			if track == 'true' and self.isPlayingVideo():
				self.time = self.getTime()
				save(self.filemedia,str(self.time))
		except: pass

def save(filename, contents):
	try:
		fh = xbmcvfs.File(filename, 'w')
		fh.write(str(contents))
		fh.close()
	except: print "Não gravou os temporários de: %s" % (filename)

def readfile(filename):
    try:
		fh = xbmcvfs.File(filename)
		string = fh.read()
		fh.close()
		return string
    except:
		traceback.print_exc()
		print "Não abriu conteúdos de: %s" % filename
		return None

def format_time(seconds):
    minutes,seconds = divmod(seconds, 60)
    if minutes > 60:
        hours,minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else: return "%02d:%02d" % (minutes, seconds)