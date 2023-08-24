from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import random, os, tempfile, smtplib
import datetime
from etudiants import *

if not os.path.exists("Reçus"):
    os.mkdir("Reçus")

db = Database("Étudiants.db")

def send_mail():
    def send_recu():
        try:
            ob = smtplib.SMTP('smtp.gmail.com', 587)
            ob.starttls()
            ob.login(sendermailEntry.get(), passwordEntry.get())
            subject = 'Paroisse St. Antoine de Padoue-Sin El Fil'
            message = email_textarea.get(1.0, END)
            encoded_message = message.encode('utf-8')
            ob.sendmail(sendermailEntry.get(), receivermailEntry.get(), encoded_message)
            ob.quit()
            messagebox.showinfo('SUCCES', 'Reçu est envoyé avec succès!', parent=root1)
        except Exception as e:
            print("An exception occurred:", e)
            messagebox.showerror('ERREUR', "Quelque chose s'est mal passé. Essayez de nouveau s'il vous plaît!", parent=root1)

    if textarea.get(1.0, END)=='\n':
        messagebox.showerror("ERREUR", "Reçu vide!")
    else:
        root1=Toplevel()
        root1.title("Envoyer E-mail")
        root1.config(bg='gray39')
        root1.resizable(0, 0)
        root1.iconbitmap("Uiconstock-Flat-Halloween-Halloween-Cross.ico")

        senderFrame = LabelFrame(root1, text="Envoyer De", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=5, relief=RIDGE)
        senderFrame.grid(row=0, column=0, padx=40, pady=20, sticky='w')

        sendermailLabel = Label(senderFrame, text="E-mail", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=0)
        sendermailLabel.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        sendermailEntry = Entry(senderFrame, font=('times new roman', 15), bd=0, width=30)
        sendermailEntry.grid(row=0, column=1, padx=10, pady=5)
        sendermailEntry.insert(0, "marwan.elhasrouny@gmail.com")

        passwordLabel = Label(senderFrame, text="Mot de Passe", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=0)
        passwordLabel.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        passwordEntry = Entry(senderFrame, font=('times new roman', 15), bd=0, width=30, show='*')
        passwordEntry.grid(row=1, column=1, padx=10, pady=5)
        passwordEntry.insert(0, "aqgfhawpqahtxpbz")

        receiverFrame = LabelFrame(root1, text="Envoyer À", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=5, relief=RIDGE)
        receiverFrame.grid(row=1, column=0, padx=40, pady=20,sticky='w')

        receivermailLabel = Label(receiverFrame, text="E-mail", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=0)
        receivermailLabel.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        receivermailEntry = Entry(receiverFrame, font=('times new roman', 15), bd=0, width=30)
        receivermailEntry.grid(row=0, column=1, padx=10, pady=5)
        receivermailEntry.insert(0, emailEntry.get())

        messageLabel = Label(receiverFrame, text="Message:", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=0)
        messageLabel.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        email_textarea=Text(receiverFrame, font=('times new roman', 15), bd=2, relief=RIDGE, height=11, width=81)
        email_textarea.grid(row=2, column=0, columnspan=16)
        email_textarea.delete(1.0, END)
        email_textarea.insert(END, textarea.get(1.0, END))

        btnsend = Button(root1, text="Envoyer E-mail", width=15, font=("times new roman", 15, "bold"), fg="gray39",
                bg="ivory2", bd=0,command=send_recu).grid(row=2, column=0, padx=10, pady=10)

        root1.mainloop()


def print_bill():
    if textarea.get(1.0, END)=='\n':
        messagebox.showerror("ERREUR", "Reçu vide!")
    else:
        file=tempfile.mktemp(".rtf")
        open(file, 'w').write(textarea.get(1.0, END))
        os.startfile(file, "print")

def search_bill():
    for i in os.listdir("Reçus/"):
        if i.split('-')[0]==receiptEntry.get():
            f=open(f"Reçus/{i}", 'r')
            textarea.delete(1.0, END)
            for data in f:
                textarea.insert(END, data)
            f.close()
            break
    else:
        messagebox.showerror("ERREUR", "Numéro invalide!")

billnumber = random.randint(0,500)

def save():
    global billnumber

    result = messagebox.askyesno("SAUVEGARDER", "Sauveguarder le reçu?")
    if result:
       bill_content = textarea.get(1.0, END)
       file = open(f"Reçus/{billnumber}-{fnameEntry.get()} {lnameEntry.get()}-Année {yearEntry.get()}.rtf", "w")
       file.write(bill_content)
       file.close()
       messagebox.showinfo("SUCCES", f"Reçu numéro {billnumber} pour l'année {yearEntry.get()} est sauvegardé!")
       billnumber = random.randint(0,500)

def reçu():

    totalEntry.delete(0, END)
    total = int(inscripEntry.get())+int(bibleEntry.get())+int(livreEntry.get())
    totalEntry.insert(0, str(total))

    if fnameEntry.get()=='' or lnameEntry.get()=='':
          messagebox.showerror('ERREUR', "Il faut écrir les détails complets de l'étudiant!")
    elif bibleEntry.get()=='0' and inscripEntry.get()=='0':
         messagebox.showerror('ERREUR', "Il faut avoir des prix pour l'inscription, le livre et la bible!")
    else:
        textarea.delete(1.0, END)
        billgenerate.delete(0, END)

        textarea.insert(END, "=========================================================================\n")
        textarea.insert(END, "\t\t   Paroisse St. Antoine de Padoue - Sin El Fil")
        textarea.insert(END, "\n=========================================================================\n")
        textarea.insert(END, f"\nNuméro du reçu : {billnumber}")
        textarea.insert(END, f"\nAnnée : {yearEntry.get()}")
        textarea.insert(END, f"\nPrénom et Nom de l'étudiant : {fnameEntry.get()} {lnameEntry.get()}")
        textarea.insert(END, f"\nDate de naissance : {datenaissEntry.get()}")
        textarea.insert(END, f"\nRite : {riteEntry.get()}")
        textarea.insert(END, f"\nBaptisé(e) : {bptmEntry.get()}")
        textarea.insert(END, f"\nClasse : {classEntry.get()}")
        if classEntry.get()=="9ème-CE2" and premcomEntry.get()!="...":
            textarea.insert(END, f"\nPremière Communion à St. Antoine de Padoue-S.E.F : {premcomEntry.get()}")
        textarea.insert(END, f"\nÉcole : {ecoleEntry.get()}")
        textarea.insert(END, f"\nFrère/Soeur : {frereEntry.get()}")
        if frereEntry.get()=="Oui":
            textarea.insert(END, f"\nPrénom et Nom du Frère/Soeur : {sonnomEntry.get()}\n")
        textarea.insert(END, "\n-------------------------------------------------------------------------\n")
        textarea.insert(END, f"\nPrénom du Père : {pereEntry.get()}")
        textarea.insert(END, f"\nCel. Père : {celpereEntry.get()}")
        textarea.insert(END, f"\nPrénom et Nom de la Mère : {mereEntry.get()}")
        textarea.insert(END, f"\nCel. Mère : {celmereEntry.get()}")
        textarea.insert(END, f"\nE-mail : {emailEntry.get()}")
        textarea.insert(END, f"\nAdresse : {adresseEntry.get()}\n")
        textarea.insert(END, "\n-------------------------------------------------------------------------\n")
        textarea.insert(END, f"\nInscription : {str(inscripEntry.get())} {unitEntry.get()}")
        textarea.insert(END, f"\nLivre : {str(livreEntry.get())} {unitEntry.get()}")
        textarea.insert(END, f"\nBible : {str(bibleEntry.get())} {unitEntry.get()}\n")
        textarea.insert(END, f"\nTOTAL : {str(totalEntry.get())} {unitEntry.get()}\n")
        textarea.insert(END, "\n-------------------------------------------------------------------------\n")
        textarea.insert(END, "\nNB : Vous avez 14 jours pour payer les frais, sinon l'inscription sera annulée.\n")
        textarea.insert(END, "\n=========================================================================\n")
        textarea.insert(END, "\t\t\t\t\tBonne Journée!")
        textarea.insert(END, "\n=========================================================================")

        billgenerate.insert(0, billnumber)

def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    print(row)
    recu.set(row[1])
    prénom.set(row[2])
    nom.set(row[3])
    classe.set(row[4])
    année.set(row[5])
    cel_père.set(row[6])
    cel_mère.set(row[7])
    email.set(row[8])

def dispalyAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)

def add_etudiant():
    if fnameEntry.get() == "" or lnameEntry.get() == "" or classEntry.get() == "" or yearEntry.get() == "" or celpereEntry.get() == "" or celmereEntry.get() == "" or emailEntry.get() == "":
        messagebox.showerror("ERREUR", "Remplissez tout les détails!")
        return
    db.insert(billgenerate.get(), fnameEntry.get(), lnameEntry.get(), classEntry.get(), yearEntry.get(), celpereEntry.get(), celmereEntry.get(), emailEntry.get())
    messagebox.showinfo("SUCCES", "Informations insérées!")
    dispalyAll()

def update_etudiant():
    if fnameEntry.get() == "" or lnameEntry.get() == "" or classEntry.get() == "" or yearEntry.get() == "" or celpereEntry.get() == "" or celmereEntry.get() == "" or emailEntry.get() == "":
        messagebox.showerror("ERREUR", "Remplissez tout les détails!")
        return
    db.update(row[0],billgenerate.get(), fnameEntry.get(), lnameEntry.get(), classEntry.get(), yearEntry.get(), celpereEntry.get(), celmereEntry.get(), emailEntry.get())

    messagebox.showinfo("SUCCES", "Informations mises à jour!")
    dispalyAll()

def delete_etudiant():
    choice = messagebox.askyesno("SUPPRIMER", "Vous désirez supprimer l'inscription de cet étudiant?")
    if choice:
        db.remove(row[0])
        prénom.set("")
        nom.set("")
        classe.set("...")
        année.set("")
        cel_père.set("")
        cel_mère.set("")
        email.set("")
        dispalyAll()
        messagebox.showinfo("SUCCES", "L'inscription est suprimée!")

def search_etud():
    root2=Toplevel()
    root2.title("Filtrer Étudiants")
    root2.config(bg='gray39')
    root2.resizable(0, 0)
    root2.iconbitmap("Uiconstock-Flat-Halloween-Halloween-Cross.ico")

    searchFrame = LabelFrame(root2, text="Filtrer Selon:", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=5, relief=RIDGE)
    searchFrame.grid(row=0, column=0, padx=40, pady=20, sticky='w')

    recherche = [
    'Numéro du Reçu',
    "Prénom de l'Étudiant",
    "Nom de l'Étudiant",
    ]
    rechercheEntry = ttk.Combobox(searchFrame, values=recherche, font=('times new roman', 14) , width=18)
    rechercheEntry.set('...')
    rechercheEntry.grid(row=0, column=0, padx=8,pady=4, sticky='w')

    chercheEntry = Entry(searchFrame, font=('times new roman', 15) , width=18)
    chercheEntry.grid(row=1, column=0, padx=8, pady=4,sticky='w')
    
    def chercher():
        recuid = billgenerate.get()
        fname = fnameEntry.get()
        lname = lnameEntry.get()
        

        if chercheEntry.get()==recuid:
            row=db.fetch("SELECT * FROM etudiants WHERE "+ recuid)
        elif chercheEntry.get()==fname:
            row=db.fetch("SELECT * FROM etudiants WHERE "+ fname)
        elif chercheEntry.get()==lname:
            row=db.fetch("SELECT * FROM etudiants WHERE "+ lname)
        else:
            row=[]

        tv.delete(*tv.get_children())
        for r in row:
            tv.insert('',END,values=r)

    btnsearch = Button(root2, text="Filtrer", width=10, font=("times new roman", 15, "bold"), fg="gray39",
                bg="ivory2", bd=0,command=chercher).grid(row=1, column=0, padx=10, pady=10)

    root2.mainloop()

def clearAll():
    prénom.set("")
    nom.set("")
    classe.set("...")
    année.set("")
    cel_père.set("")
    cel_mère.set("")
    email.set("")
    ecoleEntry.delete(0,END)
    pereEntry.delete(0, END)
    mereEntry.delete(0, END)
    adresseEntry.delete(0, END)
    inscripEntry.delete(0, END)
    inscripEntry.insert(0, 0)
    livreEntry.delete(0, END)
    livreEntry.insert(0, 0)
    bibleEntry.delete(0, END)
    bibleEntry.insert(0, 0)
    totalEntry.delete(0, END)
    totalEntry.insert(0, 0)
    textarea.delete(1.0, END)
    riteEntry.set('...')
    bptmEntry.set('...')
    frereEntry.set('...')
    unitEntry.set('...')



root = Tk()
root.title('Paroisse St. Antoine de Padoue - Sin El Fil')             
root.geometry("1505x557")
root.config(bg='gray39')
root.iconbitmap("Uiconstock-Flat-Halloween-Halloween-Cross.ico")

recu = StringVar()
prénom = StringVar()
nom = StringVar()
classe = StringVar()
année = StringVar()
cel_père = StringVar()
cel_mère = StringVar()
email = StringVar()

headingLabel = Label(root, text='École de Catéchèse - Paroisse St. Antoine de Padoue', font=('times new roman', 30, 'bold'), bg='gray39', fg='ivory2', bd=5, relief=RIDGE)
headingLabel.pack(fill=X)

student_frame = LabelFrame(root, text='Étudiant', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2', bd=5, relief=RIDGE)
student_frame.pack(fill=X)

fnameLabel = Label(student_frame, text='Prénom', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
fnameLabel.grid(row=0, column=0, padx=10, pady=4, sticky='w')
fnameEntry = Entry(student_frame, textvariable=prénom, font=('times new roman', 15), width=15)
fnameEntry.grid(row=0, column=1, padx=8, sticky='w')

lnameLabel = Label(student_frame, text='Nom', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
lnameLabel.grid(row=0, column=2, padx=10, pady=4, sticky='w')
lnameEntry = Entry(student_frame, textvariable=nom, font=('times new roman', 15), width=15)
lnameEntry.grid(row=0, column=3, padx=8, sticky='w')

yearLabel = Label(student_frame, text='Année', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
yearLabel.grid(row=0, column=4, padx=10, pady=4, sticky='w')
yearEntry = Entry(student_frame, textvariable=année,font=('times new roman', 15), width=18)
yearEntry.grid(row=0, column=5, padx=8, sticky='w')

receiptLabel = Label(student_frame, text='Numéro du Reçu', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
receiptLabel.grid(row=0, column=6, padx=10, pady=4, sticky='w')
receiptEntry = Entry(student_frame, font=('times new roman', 15), bg='grey88', width=10)
receiptEntry.grid(row=0, column=7, padx=8, sticky='w')

chercherButton = Button(student_frame, text='Chercher', font=('times new roman', 13, 'bold'),bd=0, bg='ivory2', fg='gray39', width=8, command=search_bill)
chercherButton.grid(row=1, column=7, padx=7, pady=4, sticky='e')

datenaissLabel = Label(student_frame, text='Date de Naissance', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
datenaissLabel.grid(row=1, column=0, padx=10, pady=4, sticky='w')
datenaissEntry = DateEntry(student_frame, selectmode='day', font=('times new roman', 15), width=14)
datenaissEntry.grid(row=1, column=1, padx=8,sticky='w')

riteLabel = Label(student_frame, text='Rite', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
riteLabel.grid(row=1, column=4, padx=10, pady=4, sticky='w')
rite = [
    'Latin',
    'Maronite',
    'Grec Catholique',
    'Grec Orthodox',
    'Syriaque Catholique',
    'Syriaque Orthodox',
    'Arménien Catholique',
    'Arménien Orthodox',
]
riteEntry = ttk.Combobox(student_frame, values=rite, font=('times new roman', 15) , width=17)
riteEntry.set('...')
riteEntry.grid(row=1, column=5, padx=8, sticky='w')

bptmLabel = Label(student_frame, text='Baptisé(e)', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
bptmLabel.grid(row=1, column=2, padx=10, pady=4, sticky='w')
bpt = [
    'Oui',
    'Non'
]
bptmEntry = ttk.Combobox(student_frame, values=bpt, font=('times new roman', 15) , width=14)
bptmEntry.set('...')
bptmEntry.grid(row=1, column=3, padx=8, sticky='w')

classLabel = Label(student_frame, text='Classe', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
classLabel.grid(row=2, column=0, padx=10, pady=4, sticky='w')
cours = [
    '11ème-CP',
    '10ème-CE1',
    '9ème-CE2',
    '8ème-CM1',
    '7ème-CM2',
    '6ème-EB6',
    '5ème-EB7',
    '4ème-EB8',
    '3ème-EB9',
    '2nde',
    '1ère'
]
classEntry = ttk.Combobox(student_frame, textvariable=classe, values=cours, font=('times new roman', 15) , width=14)
classEntry.set('...')
classEntry.grid(row=2, column=1, padx=8, sticky='w')

ecoleLabel = Label(student_frame, text='École', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
ecoleLabel.grid(row=2, column=2, padx=10, pady=4, sticky='w')
ecoleEntry = Entry(student_frame, font=('times new roman', 15), width=25)
ecoleEntry.grid(row=2, column=3, padx=8, sticky='w')

frereLabel = Label(student_frame, text='Frère/Soeur', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
frereLabel.grid(row=2, column=4, padx=10, pady=4, sticky='w')
frere = [
    'Oui',
    'Non'
]
frereEntry = ttk.Combobox(student_frame, values=frere, font=('times new roman', 15) , width=17)
frereEntry.set('...')
frereEntry.grid(row=2, column=5, padx=8, sticky='w')

def show_widgets():
    global premcomEntry, premcomLabel
    if classEntry.get() == "9ème-CE2":
        premcomLabel = Label(student_frame, text="Première Communion\nà St. Antoine - S.E.F", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
        premcomLabel.grid(row=3, column=0, padx=8, sticky="w")
        premcom = ['Oui', 'Non']
        premcomEntry = ttk.Combobox(student_frame, values=premcom, font=('times new roman', 15), width=14)
        premcomEntry.set('...')
        premcomEntry.grid(row=3, column=1, padx=8, sticky='w')
    elif classEntry.get() != "9ème-CE2":
        premcomEntry.grid_forget()
        premcomLabel.grid_forget()

classEntry.bind("<<ComboboxSelected>>", lambda event: show_widgets())

def hide():
    premcomEntry.grid_forget()
    premcomLabel.grid_forget()

def show_widgets2():
    global sonnomEntry, sonnomLabel
    if frereEntry.get() == "Oui":
        sonnomLabel = Label(student_frame, text="Prénom et Nom", font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
        sonnomLabel.grid(row=3, column=4, padx=8, sticky="w")
        sonnomEntry = Entry(student_frame, font=('times new roman', 15), width=25)
        sonnomEntry.grid(row=3, column=5, padx=8, sticky='w')
    elif frereEntry.get() == "Non":
        sonnomEntry.grid_forget()
        sonnomLabel.grid_forget()

frereEntry.bind("<<ComboboxSelected>>", lambda event: show_widgets2())
    
def hide2():
    sonnomEntry.grid_forget()
    sonnomLabel.grid_forget()


detailsFrame = Frame(root, bg='gray39')
detailsFrame.pack()

parentFrame = LabelFrame(detailsFrame, text="Parents de l'étudiant", font=("times new roman", 15, "bold"), bg='gray39', fg='ivory2', bd=5, relief=RIDGE)
parentFrame.grid(row=0, column=0)

pereLabel = Label(parentFrame, text="Prénom du Père", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
pereLabel.grid(row=0, column=0, pady=7, padx=10, sticky="w")
pereEntry = Entry(parentFrame, font=("times new roman", 15), width=15)
pereEntry.grid(row=0, column=1, pady=9, padx=10, sticky="w")

celpereLabel = Label(parentFrame, text="Cel. Père", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
celpereLabel.grid(row=0, column=2, pady=7, padx=10, sticky="w")
celpereEntry = Entry(parentFrame, textvariable=cel_père, font=("times new roman", 15),width=12)
celpereEntry.grid(row=0, column=3, pady=9, padx=10, sticky="w")

mereLabel = Label(parentFrame, text="Prénom et Nom de la Mère", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
mereLabel.grid(row=1, column=0, pady=7, padx=10, sticky="w")
mereEntry = Entry(parentFrame, font=("times new roman", 15),width=30)
mereEntry.grid(row=1, column=1, pady=9, padx=10, sticky="w")

celmereLabel = Label(parentFrame, text="Cel. Mère", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
celmereLabel.grid(row=1, column=2, pady=7, padx=10, sticky="w")
celmereEntry = Entry(parentFrame, textvariable=cel_mère, font=("times new roman", 15),width=12)
celmereEntry.grid(row=1, column=3, pady=9, padx=10, sticky="w")

emailLabel = Label(parentFrame, text="E-mail", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
emailLabel.grid(row=2, column=0, pady=7, padx=10, sticky="w")
emailEntry = Entry(parentFrame, textvariable= email, font=("times new roman", 15),width=30)
emailEntry.grid(row=2, column=1, pady=9, padx=10, sticky="w")

adresseLabel = Label(parentFrame, text="Adresse", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
adresseLabel.grid(row=3, column=0, pady=7, padx=10, sticky="w")
adresseEntry = Entry(parentFrame, font=("times new roman", 15),width=30)
adresseEntry.grid(row=3, column=1, pady=9, padx=10, sticky="w")

billFrame = Frame(detailsFrame, bd=8, relief=RIDGE)
billFrame.grid(row=0, column=1)

billareaLabel = Label(billFrame, text="Reçu de l'Étudiant", font=("times new roman", 15, "bold"), bd=5, relief=RIDGE)
billareaLabel.pack(fill=X)

scrollbar = Scrollbar(billFrame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)
textarea = Text(billFrame, height=11, width=73, yscrollcommand=scrollbar.set)
textarea.pack()
scrollbar.config(command=textarea.yview)

fraisFrame = LabelFrame(detailsFrame, text="Frais de l'Inscription", font=("times new roman", 15, "bold"), bg='gray39', fg='ivory2', bd=5, relief=RIDGE,width=200)
fraisFrame.grid(row=1, column=0, sticky="w")

inscripLabel = Label(fraisFrame, text="Inscription", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
inscripLabel.grid(row=0, column=0, pady=7, padx=10, sticky="w")
inscripEntry = Entry(fraisFrame, font=("times new roman", 15), width=13)
inscripEntry.grid(row=0, column=1, pady=9, padx=10, sticky="w")
inscripEntry.insert(0,0)

livreLabel = Label(fraisFrame, text="Livre", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
livreLabel.grid(row=0, column=2, pady=7, padx=10, sticky="w")
livreEntry = Entry(fraisFrame, font=("times new roman", 15),width=13)
livreEntry.grid(row=0, column=3, pady=9, padx=10, sticky="w")
livreEntry.insert(0,0)

bibleLabel = Label(fraisFrame, text="Bible", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
bibleLabel.grid(row=0, column=4, pady=7, padx=10, sticky="w")
bibleEntry = Entry(fraisFrame, font=("times new roman", 15),width=13)
bibleEntry.grid(row=0, column=5, pady=9, padx=10, sticky="w")
bibleEntry.insert(0,0)

#unitLabel = Label(fraisFrame, text='Monnaie des prix', font=('times new roman', 15, 'bold'), bg='gray39', fg='ivory2')
#unitLabel.grid(row=1, column=0, padx=10, pady=4, sticky='w')
unit = [
    'LBP',
    'USD'
]
unitEntry = ttk.Combobox(fraisFrame, values=unit, font=('times new roman', 15) , width=4)
unitEntry.set('...')
unitEntry.grid(row=0, column=6, padx=8, sticky='w')

totalLabel = Label(fraisFrame, text="TOTAL", font=("times new roman", 15, "bold"), bg="gray39", fg='ivory2')
totalLabel.grid(row=1, column=4, pady=7, padx=10, sticky="w")
totalEntry = Entry(fraisFrame, font=("times new roman", 15, "bold"), width=13)
totalEntry.grid(row=1, column=5, pady=9, padx=10, sticky="w")
totalEntry.insert(0,0)

billgenerate = Entry(fraisFrame, textvariable=recu)

buttonFrame = Frame(detailsFrame, bg="gray39", bd=5, relief=RIDGE)
buttonFrame.grid(row=1, column=1,sticky="e", columnspan=5)
recuButton = Button(buttonFrame, text="Reçu", font=("times new roman", 15, "bold"), bg='ivory2', fg="gray39", width=7, pady=8, command=reçu,bd=0)
recuButton.grid(row=0, column=0, padx=14, pady=20)

saveButton = Button(buttonFrame, text="Sauvegarder", font=("times new roman", 15, "bold"), bg='ivory2', fg="gray39", width=9, pady=8, command=save,bd=0)
saveButton.grid(row=0, column=1, padx=14, pady=20)

sendButton = Button(buttonFrame, text="Envoyer", font=("times new roman", 15, "bold"), bg='ivory2', fg="gray39", width=7, pady=8, command=send_mail,bd=0)
sendButton.grid(row=0, column=2, padx=14, pady=20)

printButton = Button(buttonFrame, text="Imprimer", font=("times new roman", 15, "bold"), bg='ivory2', fg="gray39", width=7, pady=8, command=print_bill,bd=0)
printButton.grid(row=0, column=3, padx=14, pady=20)

clearButton = Button(buttonFrame, text="Effacer", font=("times new roman", 15, "bold"), bg='ivory2', fg="gray39", width=7, pady=8,bd=0)
clearButton['command']=lambda: (clearAll(), hide(), hide2())
clearButton.grid(row=0, column=4, padx=14, pady=20)

btn_frame = Frame(detailsFrame, bg="gray39")
btn_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="w")

btnAdd = Button(btn_frame, command=add_etudiant, text="Ajouter", width=15, font=("times new roman", 15, "bold"), fg="gray39",
                bg="ivory2", bd=0).grid(row=0, column=0, padx=10)

btnEdit = Button(btn_frame, command=update_etudiant, text="Mise A Jour", width=15, font=("times new roman", 15, "bold"),
                 fg="gray39", bg="ivory2",
                 bd=0).grid(row=0, column=1, padx=10)

btnFilter= Button(btn_frame, text="Filtrer", width=15, font=("times new roman", 15, "bold"),
                 fg="gray39", bg="ivory2",
                 bd=0, command=search_etud).grid(row=0, column=2, padx=10)

btnDelete = Button(btn_frame, command=delete_etudiant, text="Supprimer", width=15, font=("times new roman", 15, "bold"),
                   fg="gray39", bg="ivory2",
                   bd=0).grid(row=0, column=3, padx=10)


tree_frame = Frame(root, bg="gray39")
tree_frame.place(x=0, y=655, width=1600, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('times new roman', 12),
                rowheight=25)
style.configure("mystyle.Treeview.Heading", font=('times new roman', 13))
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column('1', width=3)
tv.heading("2", text="Reçu")
tv.column('2', width=3)
tv.heading("3", text="Prénom")
tv.column('3', width=10)
tv.heading("4", text="Nom")
tv.column('4', width=10)
tv.heading("5", text="Classe")
tv.column('5', width=7)
tv.heading("6", text="Année")
tv.column('6', width=7)
tv.heading("7", text="Cel Père")
tv.column('7', width=7)
tv.heading("8", text="Cel Mère")
tv.column('8', width=7)
tv.heading("9", text="E-mail")
tv.column('9', width=15)
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

dispalyAll()
root.mainloop()