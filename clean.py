
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
    # m = { 'movie title' : [ [ 'title', path ] ] } - pæling að bæta við ári
    m = {}
    s = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".avi") or file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.mpeg4') or file.endswith('.m4v'):
                f = os.path.join(root, file)
                print(f)
                d = guessit(f)
                print(d)
                print(d['type'])
                if d['type'] == 'movie':
                    m.setdefault((d['title']).title(), []).append([ d['year'], f])
                elif d['type'] == 'episode':
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

    for i in epNoSeason:
        print (i)
        print (epNoSeason[i])

    for i in epFullDetails:
        print (i)
        print(epFullDetails[i])

    print (m)
    print('s: ')
    for i in s:
        print(i)


print (clean('test','downloads1'))