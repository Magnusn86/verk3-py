
import os
import sys
import shutil
import re
#sys.argv[1]
from guessit import guessit
def clean(path, dest):

    r = []
    files = os.listdir(path)

    '''
    for f in files:
        if f.endswith(".avi") or f.endswith('.mp4'):
            print (f)
    '''
    # e = { 'episode title' : { 'season': [ [ episode name, episode path] ]
    epFullDetails = {}
    # e = { 'episode title' : { 'episode number': [ [ episode path] ]
    epNoSeason = {}
    # m = { 'movie title' : [ [ 'title', path ] ] } -
    m = {}
    s = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".avi") or file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.mpeg4') or file.endswith('.m4v'):
                f = os.path.join(root, file)
                d = guessit(f)
                print(d['title'])
                if d['type'] == 'movie':
                    m.setdefault((d['title']).title(), []).append(f)
                elif d['type'] == 'episode':
                    if 'episode' in d: #checkar hvort það fann episode í guessit outputtinu ef ekki bara ignore for now þarf að laga
                        if not d.get('season', None) == None:
                            epFullDetails.setdefault((d['title']).title(), {}).setdefault(d['season'], set()).add((d['episode'], f))
                        else:
                            epNoSeason.setdefault((d['title']).title(), {}).setdefault(d['episode'], set()).add(f)

                '''if not re.search('((s|S)[0-9]+(e|E)[0-9]+)', f):
                    print()
                    print(os.path.join(root, file))'''

                '''if re.search("[a-z]", f):
                    g = re.split('(\/)', f)
                    print (len(g))
                    print('split')
                    for i in g:
                        print (i)'''

                #print(dest)
                #shutil.move(f, dest)
                #with open(os.path.join(root, file), 'r') as f:
                    #for l in f:
                        #print(l)
                        #shutil.move(l, dest+ '/'+ path)

    episodePath = dest + '/Shows'
    moviePath = dest + '/Movies'
    if not os.path.exists(episodePath):
            os.makedirs(episodePath)
    if not os.path.exists(moviePath):
            os.makedirs(moviePath)
    for i in epNoSeason:
        if not os.path.exists(episodePath+'/'+i):
            os.makedirs(episodePath+'/' + i + '/Undefined')
        for k in epNoSeason[i]:
            for s in epNoSeason[i][k]:
                shutil.copy(s, episodePath+'/' + i + '/Undefined')

    for i in epFullDetails:
        if not os.path.exists(episodePath+'/'+i):
            os.makedirs(episodePath+'/'+i)
        for k in epFullDetails[i]:
            if not os.path.exists(episodePath+'/'+i+'/Season '+ str(k)):
                os.makedirs(episodePath+'/'+i+'/Season '+ str(k))
            for s in epFullDetails[i][k]:
                shutil.copy(s[1], episodePath+'/'+i+'/Season ' + str(k))

    for i in m:
        if not os.path.exists(moviePath+'/'+i):
            os.makedirs(moviePath+'/'+i)
        shutil.copy(m[i][0], moviePath+'/'+i)

print (clean('downloads','downloads1'))
