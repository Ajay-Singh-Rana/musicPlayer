# musicPlayer
A basic music player based on the one by @attreyabhatt.
It has the following features -
 i) Play and pause button switch accordingly with the state of music whether it is being played or not
 ii) An stop button (which i do not like)
 iii) Dark theme (based on my understanding of dark themes)
 iv) status bar
 v) volume scale
Features to be added :
 i) seek button for managing audio progress
 ii) suypport for all formats
Current Issues:
 i) A thread was used to calculate current playing time of of the audio file.It raises an error when the window is closed without stopping the audio being played.An attempt to fix the problem was made by overriding the **X** button functionality but in vain.


 Currently it is using pygame module's mixer class to play audio files but it has a problem in playing a few files.
 
 ****All icons are downloaded from flaticon.com**** 
