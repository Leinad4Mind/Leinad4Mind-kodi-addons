# -*- coding: utf-8 -*-

""" 2016~2017 fightnight/Leinad4Mind"""

import urlparse,sys
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

try: action=params['action']
except: action=None

if action==None:
    from resources.lib import main
    main.first_menu()

elif action=='search':
    from resources.lib import main
    main.search()

elif action=='user':
    from resources.lib import main
    try: query=params['query']
    except: query=None
    main.go_to_user(query)

elif action=='recents':
    from resources.lib import main
    from resources.lib.variables import *
    main.open_folder_recents(SiteURL)

elif action=='folder':
    from resources.lib import main
    try: page=params['page']
    except: page="1"
    main.open_folder(params['url'],page=page)

elif action=='play':
    from resources.lib import main
    main.resolve_url(params['url'],play=True)
