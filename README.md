# PRLA - Forritunarmálið Python
# Verkefni 4

###Nemendur: Magnús Norðdahl og Tumi Guðmundsson

####Implementation
Við notum guessit module úr PyPI

Tökum saman:

Allar þáttaraðir og setjum þær í dest/TV Shows/Heiti á þáttaröð/Season X/Heiti á skránni

Allar bíómyndir og setjum þær í dest/Movies/Heitið á myndinni

Alla tónlist og setjum hana í dest/Music/Nafnið á skránni

Flags:
python clean.py 1 2 3 4  
1 /path/to/download/folder   
2 /path/to/structured/folder  
3 Type of files to move:  
	- A - for all types (movies, tv shows and music) - Default  
	- T - for all tv shows  
	- M - for all movies  
	- Mu - for all music(mp3 files)  
4 Hard(H) or soft(S) clean  
	- S - soft just moves the movie, music and subtitle files - Default
	- H - hard removes all files that are not movies, music or subtitle filesx
	- if you only want to define flag #4 you must define flag #3 as well - A is the default value
	

Reglur:
Við gerðum ráð fyrir á í viðkomandi folder sé bara til þess að geyma kvikmyndir, bíómyndir og tónlist. Ef eitthvað annað er í folder-num þá er því eytt  

Ef skráin er þegar til í dest folder þá eyðum við skránni úr path folder

Ef skrá sem var færð var í folder er akkúrat þeim folder eytt Það þýðir þó ekki að allar