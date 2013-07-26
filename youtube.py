import json
import subprocess
import re
from Tkinter import *
import tkMessageBox
import os
import sys
from threading import Timer
import time
import errno
from os.path import expanduser
import tkFont

class GUIFramework(Frame):
    """This is the GUI"""

    new_playlist = []
    new_videos = {}
    config = {}
    old_playlist = {}
    youtube_dl_string = ''
    ffmpeg_string = ''
    difference = []
    playlistId = ''
    music_path = ''
    video_path = ''
    
    def __init__(self, master=None):
        Frame.__init__(self, master)

        home = expanduser("~")
        json_data = open('config.json')
        self.config = json.load(json_data)
        json_data.close()

        json_data = open('playlist.json')
        self.old_playlist = json.load(json_data)
        json_data.close()

        self.customFont = tkFont.Font(family="Helvetica", size=15)
        self.customFont2 = tkFont.Font(family="Helvetica", size=12)
        self.customFont3 = tkFont.Font(family ="Helvetica", size=5)

        if os.name == 'nt':
            self.youtube_dl_string = 'youtube-dl';
            self.ffmpeg_string = 'ffmpeg'
            self.video_path = home + "/Videos/YTD/"
            self.music_path = home + "/Music/YTD/"
        else:
            self.youtube_dl_string = './youtube-dl'
            self.ffmpeg_string = './ffmpeg'
            self.video_path = home + "/Movies/YTD/"
            self.music_path = home + "/Music/YTD/"
            
        self.make_sure_path_exists(self.video_path)
        self.make_sure_path_exists(self.music_path)
        gifdir = "./"   #####what does it do?
        self.settingsImage = PhotoImage(file = "settings.gif")
        self.playImage = PhotoImage(file = "play.gif")

        self.master.title('YouTube Downloader')

        self.w = 500
        self.h = 500
        self.master.geometry(str(str(self.w)+'x'+str(self.h)))

        x = self.percentage(self.w, 10)
        y = self.percentage(self.w, 4)
        self.grid(padx = x, pady = y)

        configured_id = self.config.get('id', '')
        if configured_id:
            pid = configured_id[:35] + (configured_id[35:] and '..')
            self.lbText = Label(self, text = 'Playlist:', font = self.customFont)
            self.lbText.grid(row = 0, column = 1)
            self.playlistId = self.config.get('id', '')
            self.lbText2 = Label(self, text = pid, font = self.customFont2, justify=LEFT)
            self.lbText2.grid(row = 1, column = 1)
            self.lbText3 = Label(self, text = " ", font = self.customFont3) #just for some space
            self.lbText3.grid(row = 2, column = 0)
            self.output = Text(self, width = x, height = y)
            self.output.grid(row = 3, column = 0, columnspan = 3)
            self.lbText4 = Label(self, text = " ", font = self.customFont3) #just for some space
            self.lbText4.grid(row = 4, column = 0)
            self.btnGo = Button(self, image=self.playImage, command=self.Run)
            self.btnGo.config(state=DISABLED)
            self.btnGo.grid(row = 5, column = 0)
            self.btnGo2 = Button(self, image=self.settingsImage, command = self.Settings)
            self.btnGo2.grid(row = 5, column = 2)
            sys.stdout = self
            self.update_idletasks()
            self.startTimer = Timer(1.0, self.AutoStart)
            self.startTimer.deamon = True
            self.startTimer.start()
          
        else:
            self.lbText = Label(self, text = 'Playlist ID or Youtube link', font = self.customFont)
            self.lbText.grid(row = 0, column = 1)
            self.enText = Entry(self)
            self.enText.grid(row = 1, column = 1)
            self.btnGo = Button(self, image=self.playImage, command = self.Run)
            self.btnGo.grid(row = 0, column = 2)
            self.btnGo2 = Button(self, image=self.settingsImage, command = self.Settings)
            self.btnGo2.grid(row = 1, column = 2)
            self.output = Text(self, width = 1, height = 1)
            self.output.grid(row = 2, column = 0, columnspan = 3)
            sys.stdout = self
            self.update_idletasks()

    def AutoStart(self):
        self.startTimer.cancel()
        self.Run()    

    def Settings(self):
        self.win = Toplevel()
        self.win.title('Settings')

        x = self.percentage(self.w, 70)
        y = self.percentage(self.h, 33)
        self.win.geometry(str(str(x)+'x'+str(y)))

        self.win.lbText = Label(self.win, text = "    ", font = self.customFont3) #just for some space
        self.win.lbText.grid(row = 0, column = 0)

        self.win.idLabel = Label(self.win, text='Playlist ID')
        self.win.idLabel.grid(row = 1, column = 1)

        self.win.idText = Entry(self.win)
        self.win.idText.insert(END, self.config.get('id', ''))
        self.win.idText.grid(row = 1, column = 2)

        self.win.timeLabel = Label(self.win, text='Poll every (seconds): ')
        self.win.timeLabel.grid(row = 2, column = 1)

        self.win.timeText = Entry(self.win)
        self.win.timeText.insert(END, self.config.get('poll', ''))
        self.win.timeText.grid(row = 2, column = 2)

        self.win.lbText1 = Label(self.win, text = " ", font = self.customFont3) #just for some space
        self.win.lbText1.grid(row = 3, column = 1)

        self.win.videoLabel = Label(self.win, text='Download option: ')
        self.win.videoLabel.grid(row = 4, column = 1)

        self.videoCheckVar = IntVar()
        self.videoCheckVar.set(self.config.get('video', 2))

        self.win.videoCheck = Checkbutton(self.win, text="Keep video", variable=self.videoCheckVar)
        self.win.videoCheck.grid(row = 4, column = 2)

        self.lbText2 = Label(self.win, text = " ", font = self.customFont3) #just for some space
        self.lbText2.grid(row = 5, column = 1)

        self.win.warningLabel = Label(self.win, text='To apply the new settings you have to restart the program')
        self.win.warningLabel.grid(row = 6, column = 1, columnspan = 2)

        self.win.saveButton = Button(self.win, text='Save and Restart', command=self.save_settings)
        self.win.saveButton.grid(row = 7, column = 1)

        self.win.cancelButton = Button(self.win, text='Cancel', command=self.win.destroy)
        self.win.cancelButton.grid(row = 7, column = 2)

    def save_settings(self):
        newId = self.win.idText.get()
        newPoll = self.win.timeText.get()
        newVideo = self.videoCheckVar.get()
        self.config['id'] = newId
        self.config['poll'] = newPoll
        self.config['video'] = newVideo
        with open('config.json', 'w') as outfile:
            json.dump(self.config, outfile)
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def Run(self):
        self.btnGo.config(state=DISABLED)
        if not self.playlistId:
            self.playlistId = self.enText.get()
            self.enText.config(state=DISABLED)
        self.send_to_output("Playlist is set to: \n" + self.playlistId + '\n')
        self.get_new_videos()   

    def get_new_videos(self):
        self.get_videos_in_playlist(self.playlistId)
        for video_id in list(self.difference):
            title = self.new_videos[video_id]
            try:
                self.download_video(title, video_id)
                self.convert_to_mp3(title)
                if self.config.get('video', 1) == 0:
                    self.delete_video(title)
                if not self.old_playlist[self.playlistId]:
                    self.old_playlist[self.playlistId] = []
                self.old_playlist[self.playlistId].append(video_id)
            except Exception as e:
                self.send_to_output("An error occurred when processing video with id: " + video_id)
                self.send_to_output(e)

        with open('playlist.json', 'w') as outfile:
            json.dump(self.old_playlist, outfile)

        #t = Timer(self.config.get('poll', 3600.0), self.get_new_videos)
        t = Timer(10, self.get_new_videos)
        t.deamon = True
        t.start()
        
    def get_videos_in_playlist(self, playlistId):
        self.send_to_output("Searching for new videos")
        command = self.youtube_dl_string + ' --get-filename -o "%(title)s.%(ext)s %(id)s" --restrict-filenames ' + self.playlistId_to_youtube_link(playlistId)
        out = self.call_command(command, False)
        if not out or out == '\n':
            self.send_to_output("There was a problem searching for videos. Either the playlist is empty or the id is not correct.")
            self.send_to_output(command)
            return
        else:
            videos = out.split('\n')
        for video_data in videos:
            if video_data:
                video_data = video_data.split()
                title = video_data[0].replace('_', ' ')
                video_id = video_data[1]
                self.new_playlist.append(video_id)
                self.new_videos[video_id] = title

        self.difference = set(self.new_playlist) - set(self.old_playlist)
        if self.difference:
            self.send_to_output("Found the following new videos:")
        for video_id in list(self.difference):
            self.send_to_output(self.new_videos[video_id])
        else:
            self.send_to_output("No new videos found \n")
      
    def download_video(self, title, video_id):
        out = self.call_command(self.youtube_dl_string + " --newline -o \"" + self.video_path + title + "\" \"http://youtube.com/watch?v=" + video_id + "\"")
        
    def convert_to_mp3(self, title):
        out = self.call_command(self.ffmpeg_string + " -i \"" + self.video_path + title + "\" -acodec libmp3lame -ac 2 -ab 320k -vn -y \"" + self.music_path + title[:-4] + ".mp3\"")
    
    #-----------------Helper functions

    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            print exception
            if exception.errno != errno.EEXIST:
                raise  

    def send_to_output(self, message):
        self.output.insert(END, time.ctime() + " " + message + "\n")
        self.output.see(END)
        self.output.update_idletasks()

    def delete_video(self, title):
        self.send_to_output(self.video_path)
        self.send_to_output(title)
        filelist = [ f for f in os.listdir(self.video_path) if f == title]
        for f in filelist:
            os.remove(self.video_path + f)

    def playlistId_to_youtube_link(self, playlistId):
        return 'http://www.youtube.com/playlist?list=' + playlistId

    def call_command(self, command, printing=True):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = ''
        while True:
            out = p.stdout.readline()
            output += out
            if out == '' and p.poll() is not None:
                break
            if printing:
                self.send_to_output(out)
        return output

    def percentage(self, dimension, percentage):
        result = dimension * percentage / 100
        return result
        
        

if __name__ == "__main__":
    guiFrame = GUIFramework()
    guiFrame.mainloop()
