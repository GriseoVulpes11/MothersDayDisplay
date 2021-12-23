
from PIL import Image, ImageTk, ExifTags
import tkinter as tk
import os
from imbox import Imbox
import traceback
import glob



def getPictureNames():
    import glob, os
    os.chdir(r"C:\Users\BCoop\Desktop\Programing\MothersDayDisplay\pictureFolder")
    picturenames = []
    for file in glob.glob("*.jpg"):
        picturenames.append(file)
    for file in glob.glob("*.png"):
        picturenames.append(file)
    return picturenames


def refreshFiles():
    dir = 'path/to/dir'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
    # enable less secure apps on your google account
    # https://myaccount.google.com/lesssecureapps

    host = "imap.gmail.com"
    username = "PictureDisplay123"
    password = 'Tantillion7'
    download_folder = r'C:\Users\BCoop\Desktop\Programing\MothersDayDisplay\pictureFolder'

    filelist = glob.glob(os.path.join(download_folder, "*"))
    for f in filelist:
        os.remove(f)

    if not os.path.isdir(download_folder):
        os.makedirs(download_folder, exist_ok=True)

    mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
    messages = mail.messages()  # defaults to inbox

    for (uid, message) in messages:
        mail.mark_seen(uid)  # optional, mark message as read

        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{att_fn}"
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            except:
                print(traceback.print_exc())

    mail.logout()


class App(tk.Tk):
    def __init__(self, image_files, delay):
        tk.Tk.__init__(self)
        self.run_at = None
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry("%dx%d+0+0" % (self.w, self.h))
        self.delay = delay
        self.pictures = []
        self.track_img_ndex = 0
        for img in image_files:
            self.pictures.append(img)
        self.picture_display = tk.Label(self)
        self.picture_display.pack(expand=False, fill="none")
        self.picture_display.config(bg="Black")
        self.config(bg="black")

    def show_slides(self):
        try:
            if self.track_img_ndex < len(self.pictures):
                x = self.pictures[self.track_img_ndex]
                self.track_img_ndex += 1
                original_image = Image.open(x)
                width, height = original_image.size
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation': break
                exif = dict(original_image._getexif().items())

                if exif[orientation] == 3:
                    original_image = original_image.rotate(180)
                elif exif[orientation] == 6:
                    original_image = original_image.rotate(270)
                elif exif[orientation] == 8:
                    original_image = original_image.rotate(90)

                resized = original_image.resize((int(width / 4), int(height / 4)), Image.ANTIALIAS)
                new_img = ImageTk.PhotoImage(resized)
                self.picture_display.config(image=new_img)
                self.picture_display.image = new_img
                self.title(os.path.basename(x))
                self.after(self.delay, self.show_slides)
                self.after(43200000000, self.update)
            else:
                self.track_img_ndex = 0
                self.show_slides()
        except RecursionError:
            self.update()

    def update(self):
        self.destroy()
        refreshFiles()
        runSlideshow()


def runSlideshow():
    delay = 3500
    image_files = getPictureNames()
    fullImageDirectory = []
    for image in image_files:
        fullImageDirectory.append(fr'C:\Users\BCoop\Desktop\Programing\MothersDayDisplay\pictureFolder\\' + image)
    app = App(fullImageDirectory, delay)
    app.show_slides()
    app.mainloop()


runSlideshow()
