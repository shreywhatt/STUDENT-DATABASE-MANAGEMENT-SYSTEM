from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas
#functionality part

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist,columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date','Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved succesfully')


def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)

    idLabel = Label(screen, text='ID', font=('times new roman', 15, 'bold'), fg='crimson', bg='azure2', bd=0)
    idLabel.grid(row=0, column=0, padx=20, pady=15, sticky=W)
    idEntry = Entry(screen, font=('times new roman', 12, 'bold'), width=60)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='NAME', font=('times new roman', 15, 'bold'), fg='crimson', bg='azure2', bd=0)
    nameLabel.grid(row=1, column=0, padx=20, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('times new roman', 12, 'bold'), width=60)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='PHONE', font=('times new roman', 15, 'bold'), fg='crimson', bg='azure2', bd=0)
    phoneLabel.grid(row=2, column=0, padx=20, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('times new roman', 12, 'bold'), width=60)
    phoneEntry.grid(row=2, column=1, pady=15, padx=1)

    emailLabel = Label(screen, text='EMAIL', font=('times new roman', 15, 'bold'), fg='crimson', bg='azure2', bd=0)
    emailLabel.grid(row=3, column=0, padx=20, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('times new roman', 12, 'bold'), width=60)
    emailEntry.grid(row=3, column=1, pady=15, padx=13)

    addressLabel = Label(screen, text='ADDRESS', font=('times new roman', 15, 'bold'), fg='crimson', bg='azure2', bd=0)
    addressLabel.grid(row=4, column=0, padx=20, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('times new roman', 12, 'bold'), width=60)
    addressEntry.grid(row=4, column=1, pady=15, padx=13)

    genderLabel = Label(screen, text='GENDER', font=('times new roman', 15, 'bold'), fg='crimson', bg='azure2', bd=0)
    genderLabel.grid(row=5, column=0, padx=20, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('times new roman', 12, 'bold'), width=60)
    genderEntry.grid(row=5, column=1, pady=15, padx=13)

    dobLabel = Label(screen, text='DOB', font=('times new roman', 15, 'bold'), fg='crimson', bg='azure2', bd=0)
    dobLabel.grid(row=6, column=0, padx=20, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('times new roman', 12, 'bold'), width=60)
    dobEntry.grid(row=6, column=1, pady=15, padx=13)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)
    if title == 'Update Student':
        indexing = studentTable.focus()

        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


def update_data():
    query = 'update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                             genderEntry.get(), dobEntry.get(), date, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('SUCCESS', f'Id {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing = studentTable.focus()
    print(indexing)
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted succesfully')

    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def search_data():
    query = 'select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query, (
    idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(),
    dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def add_data():
    if idEntry.get()=='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('Error','All Feilds are required',parent=screen)

    else:
        try:
            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),
                                    genderEntry.get(),dobEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=screen)
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                emailEntry.delete(0,END)
                addressEntry.delete(0,END)
                genderEntry.delete(0,END)
                dobEntry.delete(0,END)
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=screen)
            return


        query='select *from student'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('',END,values=data)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host='localhost', user='root', password='root')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return

        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key, name varchar(30),mobile varchar(10),email varchar(30),' \
                    'address varchar(100),gender varchar(20),dob varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.configure(bg='white')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False, False)

    hostnameLabel = Label(connectWindow, text='Host Name', background='white', font=('times new roman', 20, 'bold'),
                          fg='dodger blue')
    hostnameLabel.grid(row=0, column=0, padx=10)
    hostEntry = Entry(connectWindow, font=('times new roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, pady=10)

    usernameLabel = Label(connectWindow, text='User name', background='white', font=('times new roman', 20, 'bold'),
                          fg='dodger blue')
    usernameLabel.grid(row=1, column=0, padx=10, pady=10)
    usernameEntry = Entry(connectWindow, font=('times new roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=10)

    passLabel = Label(connectWindow, text='Password', background='white', font=('times new roman', 20, 'bold'),
                      fg='dodger blue')
    passLabel.grid(row=2, column=0, padx=10, pady=10)
    passEntry = Entry(connectWindow, font=('times new roman', 15, 'bold'), bd=2)
    passEntry.grid(row=2, column=1, padx=20, pady=10)
    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)


count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)


# GUI Part
root = ttkthemes.ThemedTk()

root.get_themes()
root.set_theme('adapta')
root.configure(bg='azure2')
root.geometry('1174x680+0+0')
root.resizable(False, False)
root.title('Monster University Student Management System')

datetimeLabel = Label(root, text='hello', fg='dodger blue', bg='azure2', bd=0, font=('Times New Roman', 18, 'bold'))
datetimeLabel.place(x=15, y=5)
clock()
s = 'Student Management System'  # s[count]=t when count is 1
sliderLabel = Label(root, text=s, bg='white', bd=0, fg='dodger blue', background='azure2',
                    font=('times new roman', 28, 'bold'), width=30)
sliderLabel.place(x=250, y=0)
slider()

my_style = ttkthemes.ThemedStyle(root)
my_style.configure('TButton', font=('times new roman', 11, 'bold'), foreground='dodger blue', background='white')

connectButton = ttk.Button(root, text='Connect Database', command=connect_database, style='TButton')
connectButton.place(x=1000, y=10)

leftFrame = Frame(root, bd=2, highlightbackground='dodger blue', highlightthickness=2)
leftFrame.place(x=20, y=80, width=250, height=520)

logo_image = PhotoImage(file='leftframeicon.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED,
                              command=lambda: toplevel_data('Add Student', 'Add', add_data))
addstudentButton.grid(row=1, column=0, padx=13, pady=10)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Search Student', 'Search', search_data))
searchstudentButton.grid(row=2, column=0, padx=13, pady=10)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=3, column=0, padx=13, pady=10)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Update Student', 'Update', update_data))
updatestudentButton.grid(row=4, column=0, padx=13, pady=10)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, padx=13, pady=10)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=6, column=0, padx=13, pady=10)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit)
exitButton.grid(row=7, column=0, padx=13, pady=10)

rightFrame = Frame(root, bd=2, highlightbackground='dodger blue', highlightthickness=2)
rightFrame.place(x=290, y=80, width=855, height=520, )

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender',
                                                 'D.O.B', 'Added Date', 'Added Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(expand=1, fill=BOTH)

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile', text='Mobile No')
studentTable.heading('Email', text='Email Address')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Mobile', width=200, anchor=CENTER)
studentTable.column('Address', width=300, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('D.O.B', width=200, anchor=CENTER)
studentTable.column('Added Date', width=200, anchor=CENTER)
studentTable.column('Added Time', width=200, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), background='white', fieldground='white')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='dodger blue')

studentTable.config(show='headings')

root.mainloop()
