import scrapewo
import tkinter as tk
import threading
import os
from tkinter import font

# Create main window
window = tk.Tk()
# Instantiate Song class
objSong = scrapewo.Song()

# File/Export command callback
def exportSongs():
    filetarget = objSong.exportList(lbx)
    lblStatus.config(text = 'File Exported: ')
    # Font req'd to underline hyperlink
    hlfont = font.Font(lblExport, lblExport.cget("font"))
    hlfont.configure(underline=True)
    # Hyperlink to exported file
    lblExport.config(text = filetarget, fg='blue', font=hlfont)
    lblExport.bind("<Button-1>", lambda e: launchfile(filetarget))
    # Hide status bar text after 60 seconds
    window.after(60000, hideStatus)

# Hide Status bar text
def hideStatus():
    lblStatus.config(text='')
    lblExport.config(text='')

# Open file in text editor (e.g. Notepad)
def launchfile(path):
    os.startfile(path)

# Menu
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Export...", command=exportSongs)
menubar.add_cascade(label="File", menu=filemenu)
window.config(menu=menubar)

# Window properties
window.minsize(400,600)
window.geometry("700x700")
window.title("Song Scraper")

# Default URL
# url = 'https://v7player.wostreaming.net/5792'
url = 'http://player.listenlive.co/64001/en/songhistory'

# This function runs when Start button is clicked
def songCallback():
    lastArtist = ''
    lastTitle = ''
    lblState.config(bg = 'lime green', text = 'ON')
    btnStart.config(state = 'disable')

    currentURL = entURL.get()
    currentInterval = int(entInterval.get())

    def autoscrape():
        nonlocal lastArtist
        nonlocal lastTitle
        tjob = threading.Timer(currentInterval, autoscrape)
        tjob.daemon = True
        tjob.start()

        objSong.grabSong(currentURL, entLoadWait.get(), entArtistClass.get(), entTitleClass.get())
        if (lastArtist != objSong.artist and lastTitle != objSong.title) or \
            (lastArtist == objSong.artist and lastTitle != objSong.title):
            lbx.insert('end', objSong.artist + " - " + objSong.title)
        lastArtist = objSong.artist
        lastTitle = objSong.title
    autoscrape()

# Button
btnStart = tk.Button(window, text = "Start", command = songCallback)
btnStart.place(x = 360, y = 50, width = 50, height = 30)

# Frame
frmStatusbar = tk.Frame(window)
frmStatusbar.pack(side = tk.BOTTOM, fill = 'x')

# Labels
lblURL = tk.Label(window, text = "URL")
lblURL.place(x = 50, y = 50)

lblInterval = tk.Label(window, text = "Interval")
lblInterval.place(x = 50, y = 100)

lblTimeUnit = tk.Label(window, text = "seconds")
lblTimeUnit.place(x = 125, y = 100)

lblLoadWait = tk.Label(window, text = "Wait")
lblLoadWait.place(x = 200, y = 100)

lblTimeUnit2 = tk.Label(window, text = "seconds")
lblTimeUnit2.place(x = 260, y = 100)

lblState = tk.Label(window, bg = "red", text = "OFF")
lblState.place(x = 360, y = 100, width = 50, height = 30)

lblArtistClass = tk.Label(window, text = "Artist")
lblArtistClass.place(x = 50, y = 150)

lblTitleClass = tk.Label(window, text = "Title")
lblTitleClass.place(x = 50, y = 200)

lblStatus = tk.Label(frmStatusbar)
lblStatus.pack(side="left")

lblExport = tk.Label(frmStatusbar)
lblExport.pack(side="left")

# Entry
entURL = tk.Entry(window)
entURL.place(x = 100, y = 50, width = 250)
entURL.insert(0, url)

entInterval = tk.Entry(window)
entInterval.place(x = 100, y = 100, width = 25)
entInterval.insert(0, 60)

# Wait value is time to wait after page loads before scraping
entLoadWait = tk.Entry(window)
entLoadWait.place(x = 235, y = 100, width = 25)
entLoadWait.insert(0, 5)

entArtistClass = tk.Entry(window)
entArtistClass.place(x = 100, y = 150, width = 250)
entArtistClass.insert(0, 'artist')

entTitleClass = tk.Entry(window)
entTitleClass.place(x = 100, y = 200, width = 250)
entTitleClass.insert(0, 'title')

#Listbox
lbx = tk.Listbox(window)
lbx.place(x = 50, y = 250, width = 500, height = 400)

# Message Pump
window.mainloop()