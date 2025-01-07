from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
def login():
    if usernameEntry.get()=='' and passEntry.get()=='':
        messagebox.showerror('WHYAREYOULIKETHIS','ARE YOU REALLY THAT DUMB?')
    elif usernameEntry.get()=='':
        messagebox.showerror('WHYAREYOULIKETHIS','Write something into the damn Username box!!')
    elif passEntry.get()=='':
        messagebox.showerror('WHYAREYOULIKETHIS','Enter your damn password in the box!!')
    elif usernameEntry.get()=='Shreya' and passEntry.get()=='1234':
        messagebox.showinfo('WellDone','Welcome to Monsters University, you are gonna love it here.... or maybe not.')
        window.destroy()
        import sms

    else:
        messagebox.showerror('WrongAgain','Do you want to rethink this college?'
                                          '(You might get bullied for being dumb.)')



window=Tk()

window.geometry('1280x786+0+0')
window.title('Monster University Student Login System')
window.resizable(False,False)


backgroundImage=ImageTk.PhotoImage(file='bg.jpg')

bglabel=Label(window,image=backgroundImage)
bglabel.place(x=0,y=0)


loginFrame=Frame(window,bg='black')
loginFrame.place(x=460,y=340)

logoImage = PhotoImage(file='logo.png')

logoLabel=Label(loginFrame, image=logoImage,bd=0)
logoLabel.grid(row=0,column=0,columnspan=2,pady=5)

usernameImage=PhotoImage(file='user.png')
usernameLabel=Label(loginFrame,image=usernameImage ,text='Username:', compound=LEFT,bg='black',fg='white',font=('Snap ITC',15,'bold'))
usernameLabel.grid(row=1,column=0,padx=5)

usernameEntry=Entry(loginFrame,bg='black', fg='white',bd=1,font=('Snap ITC',10,'italic')
                    ,cursor='heart')
usernameEntry.grid(row=1,column=1,padx=5,pady=5)

passImage=PhotoImage(file='pass.png')
passLabel=Label(loginFrame,image=passImage ,text='Password:', compound=LEFT,bg='black',fg='white',font=('Snap ITC',15,'bold'))
passLabel.grid(row=2,column=0,padx=20)

passEntry = Entry(loginFrame,bg='black', fg='white',bd=1,font=('Snap ITC',10,'italic'),cursor='heart')
passEntry.grid(row=2,column=1,padx=10,pady=10)

loginButton=Button(loginFrame,text='LOGIN',bg='black',bd=2,
                   fg='white',font=('Snap ITC',15,'bold'),activebackground='black',activeforeground='white',
                   cursor='heart',command=login)
loginButton.grid(row=3,column=1,pady=10)

window.mainloop()

