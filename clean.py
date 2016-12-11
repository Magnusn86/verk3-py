import os
import shutil
import sys
import re
from guessit import guessit

path = sys.argv[1]
dest = sys.argv[2]

# e = { 'episode title' : { 'season': [ [ episode name, episode path] ]
epFullDetails = {}
# e = { 'episode title' : { 'episode number': [ [ episode path] ]
epNoSeason = {}
# e = { 'episode title' : { 'season': [ [ episode path]
epNoEpisode = {}
# m = { 'movie title' : [ [ 'title', path ] ] } -
m = {}
s = set()
episodesFound = set()
delete = []
otherFiles = []
print('Guessing titles, episode names etc....')
for root, dirs, files in os.walk(path):
    for file in files:
        f = os.path.join(root, file)
        if re.search('((s|S)(a|A)(m|M)(p|P)(l|L)(e|E))', file):
            delete.append(f)
            break
        elif file.endswith(".avi") or file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.mpeg4') or file.endswith('.m4v') or file.endswith('.srt') or file.endswith('.sub') or file.endswith('.sbv'):
            f = os.path.join(root, file)
            #print (f)
            d = guessit(f)
            print(d)
            if d['type'] == 'movie':
                m.setdefault((d['title']).title(), []).append(f)
            elif d['type'] == 'episode':
                if 'episode' in d:
                    if not d.get('season', None) == None:
                        epFullDetails.setdefault((d['title']).title(), {}).setdefault(d['season'], set()).add((d['episode'], f))
                    else:
                        epNoSeason.setdefault((d['title']).title(), {}).setdefault(d['episode'], set()).add(f)
                else:
                    if not file.startswith('.'):
                        epNoEpisode.setdefault((d['title']).title(), set()).add(f)
        else:
            otherFiles.append(f)

print('List of all episodes Found')
for i in epFullDetails:
    print(i)
for i in epNoSeason:
    print(i)
for i in epNoEpisode:
    print(i)


print ()
print('other files')
for i in otherFiles:
    print(i)

print ()
print('delete files')
for i in delete:
    print(i)

print (m)

print('Moving files to nicely structured folders in ' + dest)
if not os.path.exists(dest):
    os.makedirs(dest)
episodePath = dest + '/Shows'
moviePath = dest + '/Movies'
if not os.path.exists(episodePath):
        os.makedirs(episodePath)
if not os.path.exists(moviePath):
        os.makedirs(moviePath)

for i in epNoEpisode:
    for k in epNoEpisode[i]:
        if not os.path.exists(dest + '/Undefined From ' + k):
            os.makedirs(dest + '/Undefined From ' + k)
        shutil.copy(k, dest + '/Undefined From ' + k)

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
print('All files moved to '+ dest +', movies are in Movies folder, shows in Shows folder and files we couldnt guess are in the Undefined folder.')



print (clean('test', 'downloads1'))