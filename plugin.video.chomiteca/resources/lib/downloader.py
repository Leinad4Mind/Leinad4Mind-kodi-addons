import urllib2
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import os
import inspect
iconpequeno = os.path.join(xbmcaddon.Addon(id='plugin.video.chomiteca').getAddonInfo('path').decode('utf-8'),'resources','art','iconpq.png')

def getResponse(url, size, referer, agent, cookie):
    try:
        req = urllib2.Request(url)

        if len(referer) > 0:
            req.add_header('Referer', referer)

        if len(agent) > 0:
            req.add_header('User-Agent', agent)

        if len(cookie) > 0:
            req.add_header('Cookie', cookie)

        if size > 0:
            size = int(size)
            req.add_header('Range',   'bytes=%d-' % size)

        resp = urllib2.urlopen(req, timeout=10)
        return resp
    except:
        return None


def download(url, dest, title=None, referer=None, agent=None, cookie=None):
    if not title:
        title  = 'Kodi Download'

    if not referer:
        referer  = ''

    if not agent:
        agent  = ''

    if not cookie:
        cookie  = ''

    script = inspect.getfile(inspect.currentframe())
    cmd    = 'RunScript(%s, %s, %s, %s, %s, %s, %s)' % (script, url, dest, title, referer, agent, cookie)

    xbmc.executebuiltin(cmd)


def doDownload(url, dest, title, referer, agent, cookie):
    file = dest.rsplit(os.sep, 1)[-1].split('-.')[0]

    resp = getResponse(url, 0, referer, agent, cookie)

    if not resp:
        xbmcgui.Dialog().ok(title, dest, 'Download falhou', 'Sem resposta do servidor')
        return

    try:    content = int(resp.headers['Content-Length'])
    except: content = 0

    try:    resumable = 'bytes' in resp.headers['Accept-Ranges'].lower()
    except: resumable = False

    #print "Download Header"
    #print resp.headers
    if resumable:
        print "Download e resumivel"

    if content < 1:
        xbmcgui.Dialog().ok(title, file, 'Tamanho do ficheiro desconhecido.', 'Impossível fazer download.')
        return

    size = 1024 * 1024
    mb   = content / (1024 * 1024)

    if content < size:
        size = content

    total   = 0
    notify  = 0
    errors  = 0
    count   = 0
    resume  = 0
    sleep   = 0

    if xbmcgui.Dialog().yesno(title, file, 'Ficheiro completo ocupa %dMB.' % mb, 'Continuar com o download?'): pass
    else: return
    print 'Download File Size : %dMB %s ' % (mb, dest)

    dialogDL=dialogCompatible() #dialog available on gotham++

    #f = open(dest, mode='wb')
    f = xbmcvfs.File(dest, 'w')

    chunk  = None
    chunks = []
    if dialogDL==True:
        pDialog = xbmcgui.DialogProgressBG()
        pDialog.create(title, file)

    while True:
        downloaded = total
        for c in chunks:
            downloaded += len(c)
        percent = min(100 * downloaded / content, 100)
        if percent >= notify:
            if dialogDL==False: xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( title + ' - ' + str(percent)+'%', file, 10000,iconpequeno))
            else: pDialog.update(percent)
            print 'Download percent : %s %s %dMB downloaded : %sMB File Size : %sMB' % (str(percent)+'%', dest, mb, downloaded / 1000000, content / 1000000)
            notify += 10

        if dialogDL==True: pDialog.update(percent)
        chunk = None
        error = False

        try:        
            chunk  = resp.read(size)
            if not chunk:
                if dialogDL==True: pDialog.close()
                if percent < 99:
                    error = True
                else:
                    
                    while len(chunks) > 0:
                        c = chunks.pop(0)
                        f.write(c)
                        del c

                    f.close()
                    print '%s download complete' % (dest)
                    if not xbmc.Player().isPlaying():
                        xbmcgui.Dialog().ok(title, file, '' , 'Download concluído')
                    return
        except Exception, e:
            print str(e)
            error = True
            sleep = 10
            errno = 0

            if hasattr(e, 'errno'):
                errno = e.errno

            if errno == 10035: # 'A non-blocking socket operation could not be completed immediately'
                pass

            if errno == 10054: #'An existing connection was forcibly closed by the remote host'
                errors = 10 #force resume
                sleep  = 30

            if errno == 11001: # 'getaddrinfo failed'
                errors = 10 #force resume
                sleep  = 30

        if chunk:
            errors = 0
            chunks.append(chunk)
            if len(chunks) > 5:
                c = chunks.pop(0)
                f.write(c)
                total += len(c)
                del c

        if error:
            errors += 1
            count  += 1
            print '%d Error(s) whilst downloading %s' % (count, dest)
            xbmc.sleep(sleep*1000)

        if (resumable and errors > 0) or errors >= 10:
            if (not resumable and resume >= 10) or resume >= 100:
                #Give up!
                print '%s download canceled - too many error whilst downloading' % (dest)
                xbmcgui.Dialog().ok(title, file, '' , 'Download falhou')
                return

            resume += 1
            errors  = 0
            if resumable:
                chunks  = []
                #create new response
                print 'Download resumed (%d) %s' % (resume, dest)
                resp = getResponse(url, total, referer, agent, cookie)
            else:
                #use existing response
                pass

def dialogCompatible():
    json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    import json
    json_query = json.loads(json_query)
    version_installed = []
    if json_query.has_key('result') and json_query['result'].has_key('version'):
        version_installed  = json_query['result']['version']
    if int(version_installed['major']) < 13: return False
    else: return True

if __name__ == '__main__':
    if 'downloader.py' in sys.argv[0]:
        doDownload(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
