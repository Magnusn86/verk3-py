
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
    s = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".avi") or file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.mpeg4') or file.endswith('.m4v'):
                f = os.path.join(root, file)
                print (guessit(f))
                '''if not re.search('((s|S)[0-9]+(e|E)[0-9]+)', f):
                    print()
                    print(os.path.join(root, file))'''

                '''if re.search("[a-z]", f):
                    g = re.split('(\/)', f)
                    print (len(g))
                    print('split')
                    for i in g:
                        print (i)'''

                #for i in range(len(f)):
                 #   if f[len(f)-i-1] == '.' :
                  #    s.add(f[:len(f)-i-1])

                #print(dest)
                #shutil.move(f, dest)
                #with open(os.path.join(root, file), 'r') as f:
                    #for l in f:
                        #print(l)
                        #shutil.move(l, dest+ '/'+ path)

    print('s: ')
    for i in s:
        print(i)


print (clean('downloads','downloads1'))