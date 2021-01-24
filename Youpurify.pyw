from tkinter import *
from tkinter.ttk import *
from os import *
import sys

# convertion using auto-py-to-exe (pyinstaller)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


def get_id():
    global erreur
    global log
    try:
        if "embed" in champ.get():
            return champ.get()[champ.get().index("embed/") + 6:champ.get().index("embed/") + 6 + 11]
        elif "youtube.com" in champ.get():
            return champ.get()[champ.get().index("watch?v=") + 8:champ.get().index("watch?v=") + 8 + 11]
        elif "youtu.be" in champ.get():
            return champ.get()[champ.get().index("youtu.be/") + 9:champ.get().index("youtu.be/") + 9 + 11]
        else:
            erreur = True
            log.config(text="Le champ est invalide")
            return ""
    except:
        erreur = True
        log.config(text="Erreur inconnue Au niveau de la détection de la vidéo.")
        return ""


def get_startpos():
    global erreur
    global log
    try:
        if autoCheckVariable.get() == 1:
            if "?t=" in champ.get():
                if "&" in champ.get():
                    startpos = champ.get()[champ.get().index("?t=") + 3:champ.get().index("&") - 1]
                else:
                    startpos = champ.get()[champ.get().index("?t=") + 3:]
                return "?start=" + startpos
            elif "&t=" in champ.get():
                pos = 0
                posact = 0
                for element in champ.get()[champ.get().index("&t=") + 3:]:
                    if element == "&" and pos == 0:
                        pos = posact
                    posact += 1
                if pos != 0:
                    startpos = champ.get()[champ.get().index("&t=") + 3:champ.get().index("&t=") + 3 + pos]
                else:
                    startpos = champ.get()[champ.get().index("&t=") + 3:]
                return "?start=" + startpos
            elif "?start=" in champ.get():
                pos = 0
                posact = 0
                for element in champ.get()[champ.get().index("?start=") + 7:]:
                    if element == "&" and pos == 0:
                        pos = posact
                    posact += 1
                if pos != 0:
                    startpos = champ.get()[champ.get().index("?start=") + 7:champ.get().index("?start=") + 7 + pos]
                else:
                    startpos = champ.get()[champ.get().index("?start=") + 7:]
                return "?start=" + startpos
            else:
                return ""
        else:
            if startToVariable.get() == 1:
                try:
                    startpos = int(minuteChamp.get()) * 60 + int(secondeChamp.get())
                    return "?start=" + str(startpos)
                except:
                    global erreur
                    erreur = True
                    global log
                    log.config(text="La position de démarrage est invalide")
                    return ""
            else:
                return ""
    except:
        erreur = True
        log.config(text="Erreur inconnue Au niveau de la détection de la position au démarrage.")
        return ""


def purifier():
    global log
    global erreur
    erreur = False

    adresse = "https://www.youtube.com/embed/" + get_id() + get_startpos()
    if not erreur:
        fenetre.clipboard_clear()
        fenetre.clipboard_append(adresse)
        texteChamp.set(adresse)
        log.pack_forget()
        log.config(text="Lien de la vidéo placé dans le presse-papier.")
    else:
        log.pack_forget()
    log.pack(pady=10)


def coller():
    texte = fenetre.clipboard_get()
    texteChamp.set(texte)


def start_to_check_command():
    if startToVariable.get() == 1:
        minuteInput.config(state="normal")
        minuteLabel.config(state="normal")
        secondeInput.config(state="normal")
        secondeLabel.config(state="normal")
    else:
        minuteInput.config(state="disabled")
        minuteLabel.config(state="disabled")
        secondeInput.config(state="disabled")
        secondeLabel.config(state="disabled")


def auto_check_command():
    if autoCheckVariable.get() == 1:
        minuteInput.config(state="disabled")
        minuteLabel.config(state="disabled")
        secondeInput.config(state="disabled")
        secondeLabel.config(state="disabled")
        startToCheck.config(state="disabled")
    else:
        if startToVariable.get() == 1:
            minuteInput.config(state="normal")
            minuteLabel.config(state="normal")
            secondeInput.config(state="normal")
            secondeLabel.config(state="normal")
        startToCheck.config(state="normal")


erreur = False

# fenetre
fenetre = Tk()
fenetre.call('wm', 'iconphoto', fenetre.w, PhotoImage(file=resource_path('assets/logo.png')))
fenetre.title("Youpurify")
fenetre.geometry("600x400")
fenetre.resizable(width=False, height=False)

logo_banner = PhotoImage(file=resource_path('assets/banner.png'))
canvas = Canvas(fenetre, width=600, height=150)
item = canvas.create_image(300, 90, image=logo_banner)
canvas.pack()

textLabel = Label(fenetre, text="Entrez le lien de la vidéo Youtube", font=("Calibri", 15))
textLabel.pack(pady=20)

inputFrame = Frame(fenetre)
inputFrame.pack()

texteChamp = StringVar()
texteChamp.set("")
champ = Entry(inputFrame, width=75, textvariable=texteChamp)
champ.pack(side="left")

coller_button = Button(inputFrame, text="coller", command=coller)
coller_button.pack(side="right", padx=5)

startToFrame = Frame(fenetre)
startToFrame.pack(pady=5)

startToManualFrame = Frame(startToFrame)
startToManualFrame.pack(padx=20, side="left")

startToVariable = IntVar()
startToVariable.set(1)
startToCheck = Checkbutton(startToManualFrame, text="Démarrer à", variable=startToVariable,
                           command=start_to_check_command, state="disabled")
startToCheck.pack(side="left", padx=10)

minuteChamp = StringVar()
minuteChamp.set("00")
minuteInput = Entry(startToManualFrame, width=3, textvariable=minuteChamp, state="disabled")
minuteInput.pack(side="left")
minuteLabel = Label(startToManualFrame, text="minutes", state="disabled")
minuteLabel.pack(side="left")

secondeChamp = StringVar()
secondeChamp.set("00")
secondeInput = Entry(startToManualFrame, width=3, textvariable=secondeChamp, state="disabled")
secondeInput.pack(side="left")
secondeLabel = Label(startToManualFrame, text="secondes", state="disabled")
secondeLabel.pack(side="left")

autoCheckVariable = IntVar()
autoCheckVariable.set(1)
autoCheck = Checkbutton(startToFrame, text="Déterminer automatiquement", variable=autoCheckVariable,
                        command=auto_check_command)
autoCheck.pack(side="right", padx=20)

purifier_button = Button(fenetre, text="purifier", command=purifier, width=20)
purifier_button.pack(pady=20)

log = Label(fenetre, text="Lien de la vidéo placé dans le presse-papier.")

fenetre.mainloop()
