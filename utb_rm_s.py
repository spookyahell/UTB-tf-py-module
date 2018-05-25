from urllib3.poolmanager import PoolManager
from json import loads
import time
import sys
import re
import requests
from importlib import util
from sys import stdout
import certifi

pyvlc = False

if util.find_spec('vlc') != None:
	from vlc import MediaPlayer, State
	pyvlc = True
	
manager = PoolManager(num_pools=1,
	cert_reqs = 'CERT_REQUIRED',
	ca_certs = certifi.where())

def toUTB(url, idx = 0, max = 1):
	
	start_time = time.time()
	
	r = requests.get('https://uptobox.com/')
	pos1 = r.text.find('<form id="fileupload" action="')+32
	pos2 = r.text[pos1:].find('.')
	server = r.text[pos1:][:pos2]	
	
	time_s = time.strftime('%y.%m.%d %H:%M:%S')
	print(f'{time_s}: Launching the post command for URL {idx+1}/{max}, using server: {server}...', end = '', flush = True)

	r = manager.request('POST', f'https://{server}.uptobox.com/remote?sess_id=$SESSION_ID',
		fields={'urls': f'["{url}"]'}, preload_content=False)

	downloadUrl = ''
	rjson = ''
	names = []
	sizes = []
	progresses = []
	init = False
	while downloadUrl == '':
		try:
			a = r.read(amt=1).decode('utf-8')
		except UnicodeDecodeError:
			a = '<?>'
		rjson += a
		if a == '\n':
			if rjson.strip() != '':
				rj = loads(rjson.strip())
				
				i = rj['id']
				
				if 'name' in rj:
					names.append(rj['name'])
					sizes.append(rj['size'])
				elif 'url' in rj:
					downloadUrl = rj['url']
					end_time = time.time()
					dur = end_time - start_time
					print(f'\nDownload url for file {i+1}: {downloadUrl}')
					print(f'The transfer took {dur:0.002f} seconds.')
                    #~ Uncomment if you want to play a sound when all transfers have finished
					#~ if pyvlc and idx == max-1:
						#~ p = MediaPlayer(r'C:\Program Files\iTunes\iTunes.Resources\complete.wav')
						#~ p.play()
						#~ while p.get_state() != State.Ended:
							#~ continue
					return 'OK'
				elif 'progress' in rj:
					if init is False:
						print('Names for ids:')
						for idx, name in enumerate(names):
							print(f'{idx+1}: {name}')
							
						init = True
					progress = rj['progress']/int(sizes[i])*100
					if len(progresses) >= i+1:
						progresses[i] = f'{progress:0.2f}%'
					else:
						progresses.append( f'{progress:0.2f}%')
					progress_str = 'Progressess: '
					for idx,progress in enumerate(progresses):
						progress_str += f'{idx+1}: {progress} '
					stdout.write(f'\r{progress_str}')
				elif 'error' in rj:
					err = rj['error']
					return f'uptobox.com said: {err!r}'
					#~ print(f'File {names[i]!r} has failed: {err!r}') 
			rjson = ''
