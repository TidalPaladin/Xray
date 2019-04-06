# This script uses tkinter to set up a UI for the xray apparatus
# Must have PIL for python3, install w/ sudo apt-get install python3-pil.imagetk

import xray
from tkinter import *
from PIL import Image, ImageTk

# Set up main window structure
win=Tk()
win.wm_title("Xray Controller")
left_frame = Frame(win)
right_frame = Frame(win)
left_frame.pack(side=LEFT)
right_frame.pack(side=RIGHT, fill=Y)

# Divide left half into subframes
capture_frame = Frame(left_frame)
preview_frame = Frame(left_frame)
capture_frame.pack()
preview_frame.pack()


# Populate right half
status_label = Label(right_frame, text="Status")
status_frame = Frame(right_frame)
settings_apply = Button(right_frame,text="Apply")
status_frame.pack()
settings_apply.pack()

status_bar = Label(right_frame,text="Ready")
status_bar.pack(side=BOTTOM, anchor=SE)

l_aperture = Label(status_frame, text="Aperture")
aperture = StringVar()
i_aperture = Entry(status_frame, textvariable=aperture)
i_aperture.insert(0,xray.getCameraSetting('f-number'))
l_aperture.grid(row=0,column=0)
i_aperture.grid(row=0,column=1)

l_shutter = Label(status_frame,text="Shutter (s)")
shutter = StringVar()
i_shutter = Entry(status_frame,textvariable=shutter)
i_shutter.insert(0,xray.getCameraSetting('shutterspeed2'))
l_shutter.grid(row=1,column=0)
i_shutter.grid(row=1,column=1)

l_iso = Label(status_frame,text="ISO")
iso = StringVar()
i_iso = Entry(status_frame,textvariable=iso)
i_iso.insert(0,xray.getCameraSetting('iso'))
l_iso.grid(row=2,column=0)
i_iso.grid(row=2,column=1)

l_beamdur = Label(status_frame,text="Beam Duration (s)")
beamdur = DoubleVar()
i_beamdur = Entry(status_frame,textvariable=beamdur)
i_beamdur.insert(0,3)
l_beamdur.grid(row=3,column=0)
i_beamdur.grid(row=3,column=1)

l_beamcount = Label(status_frame,text="Beam Count")
beamcount = IntVar()
i_beamcount = Entry(status_frame, textvariable=beamcount)
i_beamcount.insert(0,1)
l_beamcount.grid(row=4,column=0)
i_beamcount.grid(row=4,column=1)

l_beamint = Label(status_frame,text="Beam Interval (s)")
beamint = DoubleVar()
i_beamint = Entry(status_frame, textvariable=beamint)
i_beamint.insert(0,10)
l_beamint.grid(row=5,column=0)
i_beamint.grid(row=5,column=1)


# Populate left half
def preview() :
    path = "capture_preview.jpg"
    status_bar["text"] = "Capturing preview..."
    xray.capturePreview()
    img = ImageTk.PhotoImage(Image.open(path).resize((600,400),Image.ANTIALIAS))
    panel.image = img
    panel.configure(image=img)
    status_bar.configure(text="Ready")
    
xray.capturePreview()
path = "capture_preview.jpg"
img = ImageTk.PhotoImage(Image.open(path).resize((600,400),Image.ANTIALIAS))
panel = Label(preview_frame, image=img)
panel.image = img
panel.pack()

    
capture = Button(capture_frame, text="Capture")
preview = Button(capture_frame, text="Preview",command=preview)
capture.pack(side=LEFT)
preview.pack(side=LEFT)



win.mainloop()
