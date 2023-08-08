import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import pymysql

root = tk.Tk()
root.geometry("1350x700+0+0")


def tab1():
    def tab2():
        label1.destroy()
        button1.destroy()
        detail_frame.destroy()
        main_frame.destroy()
        search_frame.destroy()
        data_frame.destroy()
        label2 = Label(root, text="Student Information System", font=("Arial", 30, "bold"), border=12,
                       relief=tk.GROOVE)
        label2.pack(side=tk.TOP, fill=tk.X)

        detail_frame2 = tk.LabelFrame(root, text="Course Details", font=("Arial", 20), bd=12, relief=tk.GROOVE)
        detail_frame2.place(x=30, y=90, width=390, height=575)

        data_frame2 = tk.Frame(root, bd=12, relief=tk.GROOVE)
        data_frame2.place(x=420, y=90, width=890, height=575)

        # ===== Variables =====#
        course_code = tk.StringVar()
        course_name = tk.StringVar()

        cCode_lb = tk.Label(detail_frame2, text="Course Code", font=("Arial", 15))
        cCode_lb.grid(row=0, column=0, padx=2, pady=2)

        cCode_inp = tk.Entry(detail_frame2, bd=7, font=("Arial", 15), textvariable=course_code)
        cCode_inp.grid(row=0, column=1, padx=2, pady=2)

        cName_lb = tk.Label(detail_frame2, text="Course Name", font=("Arial", 15))
        cName_lb.grid(row=1, column=0, padx=2, pady=2)

        cName_inp = tk.Entry(detail_frame2, bd=7, font=("Arial", 15), textvariable=course_name)
        cName_inp.grid(row=1, column=1, padx=2, pady=2)

        def fetch_student_database():
            conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
            curr = conn.cursor()
            curr.execute("SELECT * FROM `Course`")
            rows = curr.fetchall()
            if len(rows) != 0:
                course_table.delete(*course_table.get_children())
                for row in rows:
                    course_table.insert('', tk.END, values=row)
                conn.commit()
            conn.close()

        def add_course():
            if course_code.get() == "" or course_name.get() == "":
                messagebox.showerror("Error!", "Please fill al the fields!")
            else:
                conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
                curr = conn.cursor()
                curr.execute("INSERT INTO course VALUES (%s,%s)",
                             (course_code.get(), course_name.get()))
                conn.commit()
                conn.close()

                fetch_student_database()

        def get_cursors(event):

            cursor_row2 = course_table.focus()
            content = course_table.item(cursor_row2)
            row = content['values']
            course_code.set(row[0])
            course_name.set(row[1])

        def clear_course():
            course_code.set("")
            course_name.set("")

        def delete_course():
            conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
            curr = conn.cursor()
            curr.execute("delete from course where `Course Code`=%s", course_code.get())
            conn.commit()
            conn.close()
            fetch_student_database()
            clear_course()

        def update_course():
            conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
            curr = conn.cursor()
            curr.execute("update course set `Course`=%s where `Course Code`=%s",
                         (course_name.get(), course_code.get()))
            conn.commit()
            conn.close()
            fetch_student_database()
            clear_course()

        def search_course():
            try:
                conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
                curr = conn.cursor()
                curr.execute("select * from course where `Course Code`=%s", course_code.get())
                row = curr.fetchone()

                course_code.set(row[0])
                course_name.set(row[1])

                conn.commit()

            except:
                tkinter.messagebox.showinfo("data entry form", "No Course Found")
                clear_course()
                conn.close()

        btn_frame2 = tk.Frame(detail_frame2, bd=10, relief=tk.GROOVE)
        btn_frame2.place(x=10, y=400, width=345, height=120)

        add_btn2 = tk.Button(btn_frame2, text="Add", bd=7, font=("Arial", 13), width=15, command=add_course)
        add_btn2.grid(row=0, column=0, padx=2, pady=2)

        update_btn2 = tk.Button(btn_frame2, text="Update", bd=7, font=("Arial", 13), width=15, command=update_course)
        update_btn2.grid(row=0, column=1, padx=2, pady=2)

        delete_btn2 = tk.Button(btn_frame2, text="Delete", bd=7, font=("Arial", 13), width=15, command=delete_course)
        delete_btn2.grid(row=1, column=0, padx=2, pady=2)

        clear_btn2 = tk.Button(btn_frame2, text="Clear", bd=7, font=("Arial", 13), width=15, command=clear_course)
        clear_btn2.grid(row=1, column=1, padx=2, pady=2)

        search_frame2 = tk.Frame(data_frame2, relief=tk.GROOVE)
        search_frame2.pack(anchor=tk.SE)

        search_btn2 = tk.Button(search_frame2, text="Search", font=("Arial", 13), bd=9, width=14,
                                command=search_course)
        search_btn2.grid(row=0, column=2, padx=12, pady=2)

        main_frame2 = tk.Frame(data_frame2, bd=11, relief=tk.GROOVE)
        main_frame2.pack(fill=tk.BOTH, expand=True)

        y_scroll2 = tk.Scrollbar(main_frame2, orient=tk.VERTICAL)
        x_scroll2 = tk.Scrollbar(main_frame2, orient=tk.HORIZONTAL)

        course_table = ttk.Treeview(main_frame2, columns=("Course Code", "Course Name"),
                                    yscrollcommand=y_scroll2.set, xscrollcommand=x_scroll2.set)

        y_scroll2.config(command=course_table.yview)
        x_scroll2.config(command=course_table.xview)

        y_scroll2.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll2.pack(side=tk.BOTTOM, fill=tk.X)

        course_table.heading("Course Code", text="Course Code")
        course_table.heading("Course Name", text="Course Name")

        course_table['show'] = 'headings'

        course_table.column("Course Code", width=100)
        course_table.column("Course Name", width=100)

        course_table.pack(fill=tk.BOTH, expand=True)

        fetch_student_database()

        course_table.bind("<ButtonRelease-1>", get_cursors)

        def back():
            label2.destroy()
            button2.destroy()
            detail_frame2.destroy()
            main_frame2.destroy()
            search_frame2.destroy()
            data_frame2.destroy()
            tab1()

        button2 = Button(root, text='STUDENT', font=('Times_New_Roman', 15), command=back)
        button2.pack(side=BOTTOM)

    label1 = tk.Label(root, text="Student Information System", font=("Arial", 30, "bold"), border=12,
                      relief=tk.GROOVE)
    label1.pack(side=tk.TOP, fill=tk.X)

    detail_frame = tk.LabelFrame(root, text="Student Details", font=("Arial", 20), bd=12, relief=tk.GROOVE)
    detail_frame.place(x=30, y=90, width=350, height=575)

    data_frame = tk.Frame(root, bd=12, relief=tk.GROOVE)
    data_frame.place(x=420, y=90, width=890, height=575)

    # ===== Variables =====#

    idno = tk.StringVar()
    name = tk.StringVar()
    course = tk.StringVar()
    year = tk.StringVar()
    gender = tk.StringVar()

    # ===== Entry =====#

    idno_lb = tk.Label(detail_frame, text="ID No.", font=("Arial", 15))
    idno_lb.grid(row=0, column=0, padx=2, pady=2)

    idno_inp = tk.Entry(detail_frame, bd=7, font=("Arial", 15), textvariable=idno)
    idno_inp.grid(row=0, column=1, padx=2, pady=2)

    name_lb = tk.Label(detail_frame, text="Name", font=("Arial", 15))
    name_lb.grid(row=1, column=0, padx=2, pady=2)

    name_inp = tk.Entry(detail_frame, bd=7, font=("Arial", 15), textvariable=name)
    name_inp.grid(row=1, column=1, padx=2, pady=2)


    year_lb = tk.Label(detail_frame, text="Year", font=("Arial", 15))
    year_lb.grid(row=2, column=0, padx=2, pady=2)

    year_inp = tk.Entry(detail_frame, bd=7, font=("Arial", 15), textvariable=year)
    year_inp.grid(row=2, column=1, padx=2, pady=2)

    gender_lb = tk.Label(detail_frame, text="Gender", font=("Arial", 15))
    gender_lb.grid(row=3, column=0, padx=2, pady=2)

    gender_inp = tk.Entry(detail_frame, bd=7, font=("Arial", 15), textvariable=gender)
    gender_inp.grid(row=3, column=1, padx=2, pady=2)

    course_lb = tk.Label(detail_frame, text="Course", font=("Arial", 15))
    course_lb.grid(row=4, column=0, padx=2, pady=2)

    course_inp = tk.Entry(detail_frame, bd=7, font=("Arial", 15), textvariable=course)
    course_inp.grid(row=4, column=1, padx=2, pady=2)

    # ================#

    # ===== Functions =====#

    def fetch_data():
        conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
        curr = conn.cursor()
        curr.execute("SELECT * FROM student_info")
        rows = curr.fetchall()
        if len(rows) != 0:
            student_table.delete(*student_table.get_children())
            for row in rows:
                student_table.insert('', tk.END, values=row)
            conn.commit()
        conn.close()

    def add_student():
        if idno.get() == "" or name.get() == "" or course.get() == "" or year.get() == "" or gender.get() == "":
            messagebox.showerror("Error!", "Please fill al the fields!")
        else:
            conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
            curr = conn.cursor()
            curr.execute("INSERT INTO student_info VALUES (%s,%s,%s,%s,%s)",
                         (idno.get(), name.get(), year.get(), gender.get(), course.get()))
            conn.commit()
            conn.close()

            fetch_data()

    def get_cursor(event):
        ''' This function will fetch data of the selected row'''

        cursor_row = student_table.focus()
        content = student_table.item(cursor_row)
        row = content['values']
        idno.set(row[0])
        name.set(row[1])
        year.set(row[2])
        gender.set(row[3])
        course.set(row[4])

    def clear_students():
        idno.set("")
        name.set("")
        year.set("")
        gender.set("")
        course.set("")

    def delete_student():
        conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
        curr = conn.cursor()
        curr.execute("delete from student_info where `Student ID`=%s", idno.get())
        conn.commit()
        conn.close()
        fetch_data()
        clear_students()

    def update_student():
        conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
        curr = conn.cursor()
        curr.execute("update student_info set `Name`=%s,`Year Level`=%s, `Gender`=%s, `Course`=%s where `Student ID`=%s",
                     (name.get(), year.get(), gender.get(), course.get(), idno.get()))
        conn.commit()
        conn.close()
        fetch_data()
        clear_students()

    def search_student():
        try:
            conn = pymysql.connect(host="localhost", user="root", password="1234", database="student_database")
            curr = conn.cursor()
            curr.execute("select * from student_info where `Student ID`=%s", idno.get())
            row = curr.fetchone()

            idno.set(row[0])
            name.set(row[1])
            year.set(row[2])
            gender.set(row[3])
            course.set(row[4])

            conn.commit()

        except:
            tkinter.messagebox.showinfo("data entry form", "No student found")
            clear_students()
            conn.close()

    # ================#

    # ===== Buttons =====#

    btn_frame = tk.Frame(detail_frame, bd=10, relief=tk.GROOVE)
    btn_frame.place(x=10, y=400, width=300, height=120)

    add_btn = tk.Button(btn_frame, text="Add", bd=7, font=("Arial", 13), width=12, command=add_student)
    add_btn.grid(row=0, column=0, padx=2, pady=2)

    update_btn = tk.Button(btn_frame, text="Update", bd=7, font=("Arial", 13), width=13, command=update_student)
    update_btn.grid(row=0, column=1, padx=2, pady=2)

    delete_btn = tk.Button(btn_frame, text="Delete", bd=7, font=("Arial", 13), width=12, command=delete_student)
    delete_btn.grid(row=1, column=0, padx=2, pady=2)

    clear_btn = tk.Button(btn_frame, text="Clear", bd=7, font=("Arial", 13), width=13, command=clear_students)
    clear_btn.grid(row=1, column=1, padx=2, pady=2)

    # ================#

    # ===== Search =====#

    search_frame = tk.Frame(data_frame, relief=tk.GROOVE)
    search_frame.pack(anchor=tk.SE)

    search_btn = tk.Button(search_frame, text="Search", font=("Arial", 13), bd=9, width=14, command=search_student)
    search_btn.grid(row=0, column=2, padx=12, pady=2)

    # ================#

    # ===== Database frame =====#

    main_frame = tk.Frame(data_frame, bd=11, relief=tk.GROOVE)
    main_frame.pack(fill=tk.BOTH, expand=True)

    y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
    x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

    student_table = ttk.Treeview(main_frame, columns=("ID No.", "Name", "Year", "Gender", "Course"),
                                 yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    y_scroll.config(command=student_table.yview)
    x_scroll.config(command=student_table.xview)

    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    student_table.heading("ID No.", text="ID No.")
    student_table.heading("Name", text="Name")  
    student_table.heading("Year", text="Year")
    student_table.heading("Gender", text="Gender")
    student_table.heading("Course", text="Course")

    student_table['show'] = 'headings'

    student_table.column("ID No.", width=100)
    student_table.column("Name", width=100)
    student_table.column("Year", width=100)
    student_table.column("Gender", width=100)
    student_table.column("Course", width=100)
    
    
    

    student_table.pack(fill=tk.BOTH, expand=True)

    fetch_data()

    student_table.bind("<ButtonRelease-1>", get_cursor)

    button1 = Button(root, text='COURSE', font=('Times_New_Roman', 15), command=tab2)
    button1.pack(side=BOTTOM)


tab1()

root.mainloop()

