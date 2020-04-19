import tkinter as tk    # importing the tkinter library
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
import time
import threading
from pygame import mixer    # importing mixer class of pygame library in order to control audio files

mixer.init()    # initializing mixer

melody = tk.Tk()    # creating the root window
melody.title("Melody")  # giving the root window a title
melody.geometry("600x400")
melody.resizable(False,False)

# creating a menu
menuBar = tk.Menu(melody,bg="White",fg="Black",activebackground="Purple")

# loading image resource
icon = tk.PhotoImage(file="images/music.png")
backgroundImage = tk.PhotoImage(file="images/bgMusic.png")  
pauseButtonImage = tk.PhotoImage(file="images/pauseButton.png")
playButtonImage = tk.PhotoImage(file="images/playButton.png")
stopButtonImage = tk.PhotoImage(file="images/stopButton.png")
melody.iconphoto(False,icon)    # setting window icon
volumeButtonImage = tk.PhotoImage(file="images/volumeButton.png")
muteButtonImage = tk.PhotoImage(file="images/muteButton.png") 
rewindButtonImage = tk.PhotoImage(file="images/rewindButton.png")
# dark theme icons
playButtonDark = tk.PhotoImage(file="dark_theme/playButton.png")
pauseButtonDark = tk.PhotoImage(file="dark_theme/pauseButton.png")
stopButtonDark = tk.PhotoImage(file="dark_theme/stopButton.png")
iconDark = tk.PhotoImage(file="dark_theme/music.png")
backgroundImageDark = tk.PhotoImage(file="dark_theme/bgMusic.png")
rewindButtonDark = tk.PhotoImage(file="dark_theme/rewindButton.png")
volumeButtonDark = tk.PhotoImage(file="dark_theme/volumeButton.png")
muteButtonDark = tk.PhotoImage(file="dark_theme/muteButton.png")

# variables
fileName = ""
applicationMode = "Light"
audioFileName = ""
status = ""
volumeStatus = "On"
currentVolume = 0.3
volumeScaleReading = 30
lengthInSeconds = 0
index = 0
playlist = []

#function for browsing files
def browse_files():
    global fileName
    global audioFileName 
    fileName = filedialog.askopenfilename()
    if(fileName=="" or fileName==()):
        pass
    else:
        if(fileName.find("/")!=-1):
            audioFileName = fileName.split("/")[-1]
        elif(fileName.find("\\")!=-1):
            audioFileName = fileName.split("\\")[-1]
        else:
            audioFileName = fileName
        stop_music()
        statusBar["fg"] = "Black"
        statusBar["text"] = "Selected :-> " + audioFileName
        capitalizedName = audioFileName[:-4]
        audioFileNameSplitted = capitalizedName.split(" ")
        capitalizedName = ""
        for word in audioFileNameSplitted:
            if(word==audioFileName[-1]):
                capitalizedName += word.capitalize()
            else:
                capitalizedName += word.capitalize() + " "
        mainCanvas.itemconfig(audioFileCanvasText,text=capitalizedName)
        show_length()

def show_length():  # displays length of file
    global lengthInSeconds
    if(audioFileName[-3:]=="mp3"):
        sourceFile = MP3(fileName)
        lengthInSeconds = sourceFile.info.length
    else:
        sourceFile = mixer.Sound(fileName)
        lengthInSeconds = sourceFile.length()
    minutes,seconds = divmod(lengthInSeconds,60)
    minutes = round(minutes)
    seconds = round(seconds)
    mainCanvas.itemconfig(audioFileLength,text="Total length : {:02d}:{:02d}".format(minutes,seconds))

def dark_theme():   # implements the dark theme of the application
    global canvasImage
    global applicationMode
    global volumeStatus
    global status
    applicationMode="Dark"
    mainCanvas["bg"] = "Black"
    stopButton.config(image=stopButtonDark,bg="Black",activebackground="Black")
    rewindButton.config(bg="Black",image=rewindButtonDark,activebackground="Black")
    volumeButton.config(bg="Black",activebackground="Black")
    if(volumeStatus=="Muted"):
        volumeButton["image"] = muteButtonDark
    else:
        volumeButton["image"] = volumeButtonDark
    mainButton.config(activebackground="Black",bg="Black")
    if(status=="Paused" or status==""):
        mainButton["image"] = playButtonDark
    else:
        mainButton["image"] = pauseButtonDark
    melody.iconphoto(False,iconDark)
    bottomFrame["bg"] = "Black"
    volumeScale.config(bg="Black",fg="White")
    mainCanvas.itemconfig(canvasImage,image=backgroundImageDark)
    mainCanvas.itemconfig(audioFileCanvasText,fill="White")
    mainCanvas.itemconfig(audioFileLength,fill="White")
    menuBar.config(bg="Black",fg="White")
    fileMenu.config(bg="Black",fg="White")
    helpMenu.config(bg="Black",fg="White")
    fileMenu.entryconfigure("Dark Mode",label="Light Mode",command=disable_dark_mode)
    playlistBox.configure(fg="White",bg="Black")

def disable_dark_mode():    # disables the dark theme
    global canvasImage
    global status
    global volumeStatus
    global applicationMode
    applicationMode = "Light"
    mainCanvas["bg"] ="White"
    stopButton.config(activebackground="White",bg="White",image=stopButtonImage)
    rewindButton.config(bg="White",activebackground="White",image=rewindButtonImage)
    volumeButton.config(bg="White",activebackground="White")
    if(volumeStatus=="On"):
        volumeButton["image"] = volumeButtonImage
    else:
        volumeButton["image"] = muteButtonImage
    mainButton.config(bg="White",activebackground="White")
    if(status=="Paused" or status==""):
        mainButton["image"] = playButtonImage
    else:
        mainButton["image"] = pauseButtonImage
    melody.iconphoto(False,icon)
    bottomFrame["bg"] = "White"
    volumeScale.config(bg="White",fg="Black")
    mainCanvas.itemconfig(canvasImage,image=backgroundImage)
    mainCanvas.itemconfig(audioFileCanvasText,fill="Black")
    mainCanvas.itemconfig(audioFileLength,fill="Black")
    menuBar.config(bg="White",fg="Black")
    fileMenu.config(bg="White",fg="Black")
    helpMenu.config(bg="White",fg="Black")
    fileMenu.entryconfigure("Light Mode",label="Dark Mode",command=dark_theme)
    playlistBox.configure(fg="Black",bg="White")
    

# adding submenus
fileMenu = tk.Menu(menuBar,tearoff=0,bg="White",fg="Black",activebackground="Purple")
menuBar.add_cascade(label="File",menu=fileMenu)
fileMenu.add_command(label="Open",command=browse_files)
fileMenu.add_command(label="Exit",command=melody.quit)
fileMenu.add_command(label="Dark Mode",command= dark_theme)

def about_us():
    tkinter.messagebox.showinfo("About Melody","This an open source music player built with Python and is another version with some additional features of the original one by @attreyabhatt.") 

helpMenu = tk.Menu(menuBar,tearoff=0,bg="White",fg="Black",activebackground="Purple")
menuBar.add_cascade(label="Help",menu=helpMenu)
helpMenu.add_command(label="About us",command=about_us)

mainCanvas = tk.Canvas(melody,bg="White")  # creating the Canvas widget
canvasImage = mainCanvas.create_image(230,85,image=backgroundImage,anchor=tk.NW)
mainCanvas.pack(fill=tk.BOTH,expand=True)

def play_music():   # function to play music
    global status
    global audioFileName
    global applicationMode
    if(status=="Paused"):
        mixer.music.unpause()
        status = "Playing"
        statusBar["fg"] = "Green"
        statusBar["text"] = "Playback resumed."
        if(applicationMode=="Dark"):
            mainButton["bg"] = "Black"
            mainButton["image"] = pauseButtonDark
        else:
            mainButton["bg"] = "White"
            mainButton["image"] = pauseButtonImage
        mainButton["command"] = pause_music
    else:
        if(fileName==""):
            tkinter.messagebox.showerror("Errr...","No file selected.Can't play empty selection!")
            statusBar["fg"] = "Red"
            statusBar["text"] = "Selection empty!"
        else:
            try:
                mixer.music.load(fileName)
                mixer.music.play()
                status = "Playing"
                statusBar["fg"] = "Green"
                statusBar["text"] = "Playing :-> " + audioFileName
                if(applicationMode=="Dark"):
                    mainButton["bg"] = "Black"
                    mainButton["image"] = pauseButtonDark
                else:
                    mainButton["bg"] = "White"
                    mainButton["image"] = pauseButtonImage
                mainButton["command"] = pause_music
                thread = threading.Thread(target=show_current_time,args=(lengthInSeconds,))
                thread.start()
            except:
                tkinter.messagebox.showerror("Errr...","This file format is not supported.")

def show_current_time(lengthInSeconds):
    initialTime = 0
    global status
    while(initialTime<=lengthInSeconds and mixer.music.get_busy()):
        if(applicationMode=="Dark"):
            mainCanvas.itemconfig(currentPlayTime,fill="White")
        else:
            mainCanvas.itemconfig(currentPlayTime,fill="Black")

        if(status=="Paused"):
            continue
        else:
            min,sec = divmod(initialTime,60)
            min = round(min)
            sec = round(sec)
            time.sleep(1)
            initialTime += 1
            mainCanvas.itemconfig(currentPlayTime,text="{:02d}:{:02d}".format(min,sec))

def pause_music():    # function to pause music
    global status
    global applicationMode
    if(status=="Playing"):
        mixer.music.pause()
        status = "Paused"
        statusBar["fg"] = "Black"
        statusBar["text"] = "Playback paused."
        if(applicationMode=="Dark"):
            mainButton["bg"] = "Black"
            mainButton["image"] = playButtonDark
        else:
            mainButton["bg"] = "White"
            mainButton["image"] = playButtonImage
        mainButton["command"] = play_music 
    else:
        pass
    
def stop_music():   # function to stop music
    global status
    if(status=="Playing" or status=="Paused"):
        mixer.music.stop()
        status = "Stopped"    
        statusBar["fg"] = "Red"
        statusBar["text"] = "Playback stopped."
        mainButton["image"] = playButtonImage
        mainButton["command"] = play_music
    else:
        pass

def set_vol(val):   # function to set the volume level
    volumeLevel = int(val)/100
    mixer.music.set_volume(volumeLevel)

def mute_unmute():  # function to mute audio
    global volumeStatus
    global currentVolume
    global volumeScaleReading
    if(volumeScale.get()!=0):
        volumeScaleReading = volumeScale.get()
    
    currentVolume = (volumeScaleReading/100)
    if(volumeStatus=="Muted"):  #has a problem when scale is manually set to 0 but it works as a boon 
        mixer.music.set_volume(currentVolume)
        volumeStatus = "On"
        statusBar["fg"] = "Green"
        statusBar["text"] = "Audio on."
        volumeScale.set(volumeScaleReading)
        if(applicationMode=="Light"):
            volumeButton["bg"] = "White"
            volumeButton["image"] = volumeButtonImage
        else:
            volumeButton["bg"] = "Black"
            volumeButton["image"] = volumeButtonDark
    else:
        mixer.music.set_volume(0)
        volumeStatus = "Muted"
        statusBar["fg"] = "Red"
        statusBar["text"] = "Muted."
        volumeScale.set(0)
        if(applicationMode=="Light"):
            volumeButton["bg"] = "White"
            volumeButton["image"] = muteButtonImage
        else:
            volumeButton["bg"] = "Black"
            volumeButton["image"] = muteButtonDark

def rewind():   # function to rewind audio file
    global status
    if(status==""):
        pass
    else:
        mixer.music.play()

bottomFrame = tk.Frame(mainCanvas,bg="White")  # frame for handling bottom elements
bottomFrame.place(x=175,y=300)

audioFileCanvasText = mainCanvas.create_text(290,50,text="",fill="Black")   # text to display file name
audioFileLength = mainCanvas.create_text(290,227,text = "",fill="Black")    # text to display total length
currentPlayTime = mainCanvas.create_text(160,227,text="",fill="Black")  # text to display current playing time

mainButton = tk.Button(mainCanvas,bg="White",activebackground="White",image=playButtonImage,command=play_music)   # play Button
mainButton.place(x=250,y=239)

stopButton = tk.Button(mainCanvas,bg="White",activebackground="White",image=stopButtonImage,command=stop_music) # stop Button
stopButton.place(x=300,y=239)

rewindButton = tk.Button(bottomFrame,bg="White",activebackground="White",image=rewindButtonImage,command=rewind) # rewind Button
rewindButton.grid(row=0,column=0,padx=5)

volumeButton = tk.Button(bottomFrame,bg="White",activebackground="White",image=volumeButtonImage,command= mute_unmute) # volume Button
volumeButton.grid(row=0,column=1,padx=5)

volumeScale = tk.Scale(bottomFrame,from_=0,to_=100,bg="White",fg="Black",orient=tk.HORIZONTAL,command=set_vol) # scale function for volume control settings
volumeScale.set(30)
volumeScale.grid(row=0,column=2,padx=10)

statusBar = tk.Label(mainCanvas,text="Welcome to Melody.",bg="Sky Blue",fg="Blue",relief=tk.SUNKEN,anchor=tk.W) # Status Bar
statusBar.pack(fill=tk.X,side=tk.BOTTOM)

playlistBox = tk.Listbox(mainCanvas)
playlistBox.place(x=410,y=89)

def addToPlaylist():
    global fileName
    global audioFileName
    global playlist 
    global index
    browse_files()
    if(fileName=="" or fileName==()):
        pass
    else:
        playlistBox.insert(index,audioFileName)
        playlist.append(fileName)
        index += 1

addToPlaylistButton = tk.Button(mainCanvas,text ="Add",command=addToPlaylist)
addToPlaylistButton.place(x=410,y=280)

def deleteFromPlaylist():
    audioIndex = playlistBox.curselection()
    if(audioIndex=="" or audioIndex==()):
        pass
    else:
        playlistBox.delete(audioIndex)
        audioIndex = str(audioIndex).replace("(","").replace(")","").replace(",","")
        playlist.pop(int(audioIndex))

removeFromPlaylistButton = tk.Button(mainCanvas,text="Delete",command=deleteFromPlaylist)
removeFromPlaylistButton.place(x=465,y=280)

def on_quit():
    stop_music()
    melody.quit()

melody.config(menu=menuBar)
melody.protocol("WM_DELETE_WINDOW",on_quit)
melody.mainloop()   #calling the mainloop() function of tkinter library