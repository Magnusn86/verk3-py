import os
import shutil
import sys
import re
from guessit import guessit
import datetime

path = 'downloads 8'
dest = 'TestFolder'


if not os.path.isdir(path):
    print ('Path ' + path + ' is not an existing path on this computer')
    exit()

# epFullDetails = { 'episode title' : { 'season': [ [ episode name, episode path] ]
epFullDetails = {}

# epNoSeason = { 'episode title' : [ [ episode path] ]
epNoSeason = {}

#epUndefined = [ path , path ]
epUndefined = []

# movies = { 'movie title' : [ [ path, year ]  }
movies = {}

# music = [ path ]
music = []

#Name of all TV Shows found
episodesFound = set()

#Name of all Movies found
moviesFound = set()

#All undefined titled movies
moviesUndefined = []

#Folders to remove
removeFolder = set()

#otherFiles that are dont match what we are looking for
otherFiles = []

#path to files to delete
deleteFiles = []

#TODO prompt user for if he wants movies sorted after year

print('Guessing titles, episode names etc....')
for root, dirs, files in os.walk(path):

    for file in files:
        f = os.path.join(root, file)

        if re.search('((s|S)(a|A)(m|M)(p|P)(l|L)(e|E))', file):
            os.remove(os.path.join(root, file))
            removeFolder.add(root)

        elif file.endswith((".avi", '.mp4', '.mkv', '.mpeg4', '.m4v', '.mov', '.flv', '.wmv', '.mpg', '.mpeg', '.srt', '.sub', '.sbv')):

            f = os.path.join(root, file)
            d = guessit(f)

            if d['type'] == 'movie':
                if not d.get('title', None) == None:

                    if d.get('year', None) == None:
                        year = 'N/A'
                    else:
                        year = d['year']

                    movies.setdefault((d['title']).title(), []).append([f, year])
                    moviesFound.add(d['title'])
                else:
                    moviesUndefined.append((f))
                removeFolder.add(root)

            elif d['type'] == 'episode':
                if 'title' in d:
                    if not d.get('season', None) == None:
                        epFullDetails.setdefault((d['title']).title(), {}).setdefault(d['season'], []).append((f))
                    else:
                        epNoSeason.setdefault((d['title']).title(), []).append(f)
                    episodesFound.add((d['title']).title())
                    removeFolder.add(root)
                else:
                    if not file.startswith('.'):
                        epUndefined.append(f)
                        removeFolder.add(root)
        elif file.endswith('mp3'):
            music.append(f)
            removeFolder.add(root)
        else:
            otherFiles.append(f)

#Print out all found TV shows and episodes
print('\nList of all TV shows found in the "/' + path + '" directory')
if len(epFullDetails) > 0 or len(epNoSeason) > 0:
    for i in episodesFound:
        print(i)
        for j in epFullDetails.get(i, []):
            print('\tSeason ' + str(j))
            for k in epFullDetails[i][j]:
                print('\t\t'+ str(k.split('/')[-1]))

        if not len(epNoSeason.get(i, [])) == 0:
            print('\tUndefined')
        for j in epNoSeason.get(i, []):
            print('\t\t' + str(j.split('/')[-1]))

    #TODO prompt user for correcting name of TV Show
else:
    print('None')

if len(movies) > 0:
    print('\n\nList of all Movies found in ' + path + ' directory')
    for i in movies:
        for j in movies[i]:
            print('\t' +i)

    #TODO prompt user for changing names of Movies or if wants to put movies in folders sorted after year

if len(music) > 0:
    print('\n\nList of all Movies found in ' + path + ' directory')
    for i in music:
        print('\t' + i.split('/')[-1])




#Moveing all files to their structured directories
print('\nMoving files to nicely structured folders in ' + dest)
if not os.path.exists(dest):
    os.makedirs(dest)
episodePath = dest + '/TV Shows'
moviePath = dest + '/Movies'
musicPath = dest + '/Music'
if not os.path.exists(episodePath):
        os.makedirs(episodePath)
if not os.path.exists(moviePath):
        os.makedirs(moviePath)

for i in epNoSeason:
    if not os.path.exists(episodePath+'/'+i):
        os.makedirs(episodePath+'/' + i + '/Undefined')
    for s in epNoSeason[i]:
        temp = s.split('/')
        temp = episodePath+'/' + i + '/Undefined' + '/' + temp[len(temp)-1]
        if not os.path.isfile(temp) and os.path.isfile(s):
            try:
                shutil.move(s, episodePath+'/' + i + '/Undefined')
            except Exception as e:
                print(e)
        else:
            os.remove(s)

for i in epFullDetails:
    if not os.path.exists(episodePath+'/'+i):
        os.makedirs(episodePath+'/'+i)
    for k in epFullDetails[i]:
        if not os.path.exists(episodePath+'/'+i+'/Season '+ str(k)):
            os.makedirs(episodePath+'/'+i+'/Season '+ str(k))
        for s in epFullDetails[i][k]:
            temp = s.split('/')
            temp = episodePath+'/'+i+'/Season ' + str(k) + '/' + temp[len(temp)-1]
            if not os.path.isfile(temp) and os.path.isfile(s):
                try:
                    shutil.move(s, episodePath+'/'+i+'/Season ' + str(k))
                except Exception as e:
                    print(e)
            else:
                os.remove(s)

for i in movies:
    if not os.path.exists(moviePath+'/'+i):
        os.makedirs(moviePath+'/'+i)
    for j in movies[i]:
        temp = j[0].split('/')
        temp = moviePath + '/' + i + '/' + temp[len(temp)-1]
        if not os.path.isfile(temp) and os.path.isfile(j[0]):
            try:
                shutil.move(j[0], moviePath + '/' + i)
            except Exception as e:
                print(e)
        else:
            os.remove(j[0])

for i in music:
    if not os.path.exists(musicPath +'/'+i):
        os.makedirs(musicPath +'/'+i)
    temp = i.split('/')
    temp = musicPath + '/' + i + '/' + temp[len(temp)-1]
    if not os.path.isfile(temp) and os.path.isfile(i):
        try:
            shutil.move(i, musicPath + '/' + i)
        except Exception as e:
            print(e)
    else:
        os.remove(i)





print('\nAll files moved to '+ dest +', movies are in Movies folder, shows in Shows folder and files we couldnt guess are in the Undefined folder.')



#Write out the episodes added to a file to see what was migrated

date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
filename = dest + '/Import at ' + date

file = open(filename, "w")

file.write('Import log from ' + date + '\n')

file.write('\nEpisodes added:' + '\n')
if len(episodesFound) == 0:
    file.write('None' + '\n')
else:
    for i in episodesFound:
        file.write(i + '\n')
        for j in epFullDetails.get(i, []):
            file.write('\tSeason ' + str(j))
            for k in epFullDetails[i][j]:
                file.write('\t\t'+ str(k.split('/')[-1]))

        if not len(epNoSeason.get(i, [])) == 0:
            file.write('\tUndefined')
        for j in epNoSeason.get(i, []):
            file.write('\t\t' + str(j.split('/')[-1]))

file.write('\nMovies added:' + '\n')
if len(movies) == 0:
    file.write('None' + '\n')
else:
    for i in movies:
        file.write(i + '\n')

file.write('\nMusic added:' + '\n')
if len(music) == 0:
    file.write('\t' + 'None' + '\n')
else:
    for i in music:
        file.write('\t' + i.split('/')[-1] + '\n')

file.close()


#Remove all the files that are not needed
for i in otherFiles:
    os.remove(i)


for i in removeFolder:
    try:
        os.removedirs(i)
    except:
        var = 'Do nothing'
