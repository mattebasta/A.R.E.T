# TODO:
#   GUI:
#       use customtkinter 
#       better UI style
#       Background color design: darker violet like in those modern UI
#       Widgets' style: Rounded corner buttons that seems integrated into the background
#       Sidebar icons
#       set variable to change for background and foreground color, fonts and other variable
#       changing colors of the background (?)
#
#   Making the script an executive

# FIX:



import os
import random
import sys
import json
import shutil
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
from tkinter.simpledialog import askstring
import customtkinter
from PIL import *
from pypdf import PdfWriter, PdfReader
from pypdf.errors import PdfReadError

##Lists where the objects for the frames are saved and used also to show object in their respective frames
subject_btn_list = []
subject_list = []


##Class Subject is used to create an object for every subjects is in the configuration json file, also it sets the button to ask question and show answers.
class Subject(Frame):
    def __init__(self, master, name, question_folder, answer_folder):
        ##Initializing parameters
        Frame.__init__(
            self,
            master,
            bg="#3d1f82",
            highlightbackground="white",
            highlightthickness=1,
        )
        self.sub_name = name
        self.question_folder = question_folder
        self.answer_folder = answer_folder
        self.curr_index = 0

        ##Call the create index method to make the list of questions and answers
        self.create_index()
        ##Widgets creation
        self.sub_lbl = Label(self, text=name)
        self.index_lbl = Label(
            self,
            text="question "
            + str(self.curr_index + 1)
            + "/"
            + str(len(self.quest_list)),
        )
        self.ask_question_btn = Button(
            self, text="Question", command=lambda: self.ask_question()
        )
        self.show_answer_btn = Button(
            self, text="Answer", command=lambda: self.show_answer()
        )
        self.index_forward_btn = Button(
            self, text="Next", command=lambda: self.index_forward()
        )
        self.index_backward_btn = Button(
            self, text="Previous", command=lambda: self.index_backward()
        )

        self.sub_lbl.pack(side=LEFT, padx=10, pady=10, fill=NONE, expand=FALSE)
        self.index_lbl.pack(side=LEFT, padx=10, pady=10, fill=NONE, expand=FALSE)
        self.ask_question_btn.pack(side=LEFT, padx=10, pady=10, fill=NONE, expand=FALSE)
        self.show_answer_btn.pack(side=LEFT, padx=10, pady=10, fill=NONE, expand=FALSE)
        self.index_forward_btn.pack(
            side=LEFT, padx=10, pady=10, fill=NONE, expand=FALSE
        )
        self.index_backward_btn.pack(
            side=LEFT, padx=10, pady=10, fill=NONE, expand=FALSE
        )

    ##Method to create the list containing the questions and answers
    def create_index(self):
        self.quest_list = os.listdir(self.question_folder)
        self.ans_list = os.listdir(self.answer_folder)
        if len(self.quest_list) == len(self.ans_list):
            self.rand_index = random.sample(
                range(len(self.quest_list)), len(self.quest_list)
            )
            self.question_rand_list = self.rand_index
            self.answer_rand_list = self.rand_index
        else:
            messagebox.showerror(
                "Fatal Error", "File in folders are not the same amount"
            )
            sys.exit()
    
    ##Method that take the next index in the list
    def index_forward(self):
        if self.curr_index == (len(self.question_rand_list) - 1):
            print("last index, cannot go forward")
        else:
            self.curr_index += 1
            self.update_index()

    ##Method that take the previous index in the list
    def index_backward(self):
        if self.curr_index == 0:
            print("first index, cannot go backward")
        else:
            self.curr_index -= 1
            self.update_index()

    ##Method to update the index label
    def update_index(self):
        self.index_lbl.config(
            text="question "
            + str(self.curr_index + 1)
            + "/"
            + str(len(self.quest_list))
        )

    ##Method to open a question with a given index
    def ask_question(self):
        os.startfile(
            self.question_folder
            + "/"
            + self.quest_list[self.question_rand_list[self.curr_index]]
        )

    ##Method to open an answer with a given index
    def show_answer(self):
        os.startfile(
            self.answer_folder
            + "/"
            + self.ans_list[self.answer_rand_list[self.curr_index]]
        )


##Class Subject_BTN create an object in the subject frame, in order to add a new subject or delete an existing one
class Subject_BTN(Frame):
    ##Initialization
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.sub_name = name
        # setting up the frame of every subject in the frame

        self.subject_btn_custom_frame = Frame(
            master,
            width=500,
            height=600,
            bg="green",
            highlightbackground="white",
            highlightthickness=2,
        )
        self.lbl = Label(self.subject_btn_custom_frame, text=name)
        self.btn_del = Button(
            self.subject_btn_custom_frame,
            text="DEL",
            command=lambda: self.__delete_Subject__(),
        )

        self.subject_btn_custom_frame.pack(ipadx=15, ipady=10, padx=10, pady=10)
        self.lbl.pack(pady=15, ipadx=20)
        self.btn_del.pack(pady=3, ipadx=20)

    ##Method to delete a subject, also from the conf.json
    ##The method open the config file so it can be modified, deleting the item which match the subject name. Also it deletes the value from the subject list and subject btn list
    def __delete_Subject__(self):
        self.lbl.pack_forget()
        self.btn_del.pack_forget()
        self.subject_btn_custom_frame.forget()
        with open("conf.json", "r") as config_to_modify:
            loading_modify = json.load(config_to_modify)

        for i, subs in enumerate(loading_modify["Saved subjects"]):
            if subs["Subject_Name"] == self.sub_name:
                q_folder_to_delete = loading_modify["Saved subjects"][i]["question_folder"]
                folder_to_delete = os.path.dirname(q_folder_to_delete)
                shutil.rmtree(folder_to_delete)
                del loading_modify["Saved subjects"][i]

        with open("conf.json", "w") as config_to_modify:
            json.dump(loading_modify, config_to_modify, indent=4, separators=(",", ":"))

##Method to split pdf files chosen from the user and saved into the corresponding subject folder
def file_configuration(file_q, file_a, sub_name, sub_q_dir, sub_a_dir):
    input_q_pdf = PdfReader(open(file_q,"rb"))
    input_a_pdf = PdfReader(open(file_a,"rb"))
    absolute_q_path = os.path.abspath(sub_q_dir)
    absolute_a_path = os.path.abspath(sub_a_dir)
    
    
    for i in range(len(input_q_pdf.pages)):
        out_q_files = PdfWriter()
        out_q_files.add_page(input_q_pdf.pages[i])
        output_q_path = os.path.join(absolute_q_path, sub_name + "_question_%s.pdf" % i)
        with open(output_q_path, "wb") as out_q_stream:
            out_q_files.write(out_q_stream)
    
    for j in range(len(input_a_pdf.pages)):
        out_a_files = PdfWriter()
        out_a_files.add_page(input_a_pdf.pages[j])
        output_a_path = os.path.join(absolute_a_path, sub_name + "_answer_%s.pdf" % j)
        with open(output_a_path, "wb") as out_a_stream:
            out_a_files.write(out_a_stream)

def default_sub_dir():
    if os.path.isdir('Subjects'):
        print("folder Subjects already exists")
    else:
        default_subject_folder_name = "Subjects"
        default_subject_folder_parent_dir = "./"
        default_subject_folder__path = os.path.join(default_subject_folder_parent_dir, default_subject_folder_name)
        os.mkdir(default_subject_folder__path)


##Initialization of the tkinter window
default_sub_dir()
root = customtkinter.CTk()

##Related to GUI

# Window setting
root.title("A.R.E.T - Amazing Random Exam Tutor")
root.minsize(1100, 700)  # Minimum size of the window
root.maxsize(1100, 700)  # Maximum size of the window
root.resizable(FALSE, FALSE)
root.geometry("500+200")  # Position of the window in the screen and size of the window 

# Font
helv = Font(family="Helvetica", size=16)

# Main frame settings
main_frame = Frame(
    root, bg="#3d1f82", highlightbackground="black", highlightthickness=1
)
main_frame.pack(side=RIGHT)
main_frame.pack_propagate(False)
main_frame.configure(width=1000, height=900)


# Setting the config file
config_File = "./conf.JSON"
check_file = os.path.isfile(config_File)

# Check if config file already exist
if check_file == False:
    print("no folder config found...\ncreating now....")
    configFileAlert = messagebox.showinfo(
        title="Warning",
        message="No folder config file found \n the system will create it now")

    # Preparing folder datas to write in the json file
    dict = {
        "Saved subjects": [

        ]
    }
    
    valueToWrite = json.dumps(dict, indent=4, separators=(",", ":"))
    jsonConf = open("conf.json", "w")
    jsonConf.write(valueToWrite)
    jsonConf.close()

    # open config file to read the values
    with open("conf.json", "r") as conf_file:
        load_file = json.load(conf_file)
else:
    # Config file already exist
    print("config file already exists...\nreading folders from config....")
    with open("conf.json", "r") as conf_file:
        load_file = json.load(conf_file)

##Labels(main_frame)
starting_Label = Label(
    main_frame,
    text="Welcome to ARET\n Amazing. Random. Exam. Tutor. \n your best friend when you need someone to ask you random exam questions",
    bg="#3d1f82",
    fg="white",
    font=helv,
)
instructions_label = Label(
    main_frame,
    text="Before you start you need to set up the folders containing your question and answers\n the program should have already asked you that, but if you need to add more subjects\n you can do that by pressing the subjects button on the left sidebar",
    bg="#3d1f82",
    fg="white",
    font=helv,
)
starting_Label.pack()
instructions_label.pack()


# Function that show the current section
def current_page(label):
    label.config(bg="#FFFFFF")
    del_current()


# Function that delete the current frame
def del_current():
    for frame in main_frame.winfo_children():
        frame.pack_forget()


# Function to add subject object to the subject list, used to rendering the subject into the frame
def add_to_subject_list(frame_):
    with open("conf.json", "r") as subject_file:
        load_subject_file = json.load(subject_file)
        
    for sub in load_subject_file["Saved subjects"]:
            subject_list.append(
                Subject(
                    frame_,
                    sub["Subject_Name"],
                    sub["question_folder"],
                    sub["answer_folder"],
                )
            )
    for listed in subject_list:
        listed.pack()
    

def add_to_subject_btn_list(frame_):
    with open("conf.json", "r") as subject_btn_file:
        load_subject_btn_file = json.load(subject_btn_file)
        
    for sub in load_subject_btn_file["Saved subjects"]:
        subject_btn_list.append(Subject_BTN(frame_, sub["Subject_Name"]))

    for listed in subject_btn_list:
        listed.pack()


def set_widgets_subject(frame_):
    widgets_list = []
    widgets_in_frame = frame_.winfo_children()
    for widgets in widgets_in_frame:
        widgets_list.append(widgets)
    
    for widgets_in_list in widgets_list:
        widgets_in_list.pack()


def set_widgets_subject_btn(frame_):
    widgets_list = []
    widgets_in_frame = frame_.winfo_children()
    for widgets in widgets_in_frame:
        widgets_list.append(widgets)

    # subject_btn_list.clear()


##Define the question & answers page
def qa_page():
    qa_frame = Frame(
        main_frame, bg="#3d1f82", highlightbackground="black", highlightthickness=2
    )
    qa_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    qa_frame.pack_propagate(FALSE)

    add_to_subject_list(qa_frame)
    
    
    
    # set_widgets_subject(qa_frame)


##Define the subjects page
def subjects_page():
    subjects_frame = Frame(
        main_frame, bg="#3d1f82", highlightbackground="black", highlightthickness=2
    )
    subjects_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    subjects_frame.pack_propagate(FALSE)


    add_to_subject_btn_list(subjects_frame)

    # Btn to add new subjects
    add_new_subjects_btn = Button(
        subjects_frame, text="ADD NEW", command=lambda: save_new_subject()
    )
    add_new_subjects_btn.pack()

    set_widgets_subject_btn(subjects_frame)


# Function to write a new subject into the configuration json file, fired after the button "ADD NEW" in the subject frame is pressed
def save_new_subject():
    filetype_ = [('pdf file', '*.pdf')]
    new_sub_name = askstring("Subject name", "Insert subject's name", parent=root)
    if new_sub_name is None:
        return
    else:
        new_sub_q_file = askopenfilename(title="Question File", initialdir='/', filetypes=filetype_)
        if new_sub_q_file == '':
            messagebox.showerror(title="File Selection Error", message="No file selected \n Please select a question file")
            return
        else:
            new_sub_a_file = askopenfilename(title="Answer File", initialdir = "/", filetypes=filetype_)
            if new_sub_a_file == '':
                messagebox.showerror(title="File Selection Error", message="No file selected \n Please select an answer file")
                return
            else:
                pass
        
    
    try:
        PdfReader(new_sub_q_file)
        PdfReader(new_sub_a_file)
    except PdfReadError:
        messagebox.showerror("File Error", message="File you have chosen is corrupted")
        return
    else:
        if len(PdfReader(new_sub_q_file).pages) == len(PdfReader(new_sub_a_file).pages):
            
            #Subject parent directory init
            sub_parent_dir_named = os.path.join("./Subjects", new_sub_name)
            os.mkdir(sub_parent_dir_named)
            #Question sub dir init
            new_sub_q_dir = "question_folder_%s" % new_sub_name
            new_sub_q_path = os.path.join(sub_parent_dir_named, new_sub_q_dir)
            os.mkdir(new_sub_q_path)
            #Answer sub dir init
            new_sub_a_dir = "answer_folder_%s" % new_sub_name
            new_sub_a_path = os.path.join(sub_parent_dir_named, new_sub_a_dir)
            os.mkdir(new_sub_a_path)
            
            file_configuration(new_sub_q_file, new_sub_a_file, new_sub_name, new_sub_q_path, new_sub_a_path)
        
        else:
            messagebox.showerror(title="File length", message="Choosen files have a differente length \n please choose files with the same number of pages")
            return

    def write_json(new_data, filename="conf.json"):
        with open(filename, "r+") as file:
            file_data = json.load(file)
            file_data["Saved subjects"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    newdic = {
        "Subject_Name": new_sub_name,
        "question_folder": os.path.abspath(new_sub_q_path),
        "answer_folder": os.path.abspath(new_sub_a_path),
    }

    write_json(newdic)


##Define the settings page
def settings_page():
    settings_frame = Frame(
        main_frame, bg="#3d1f82", highlightbackground="black", highlightthickness=1
    )
    settings_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    settings_frame.pack_propagate(FALSE)
    settings_frame.configure(height=900, width=800)

    ####Frame Widgets#####
    main_settings_label = Label(
        settings_frame,
        text="Settings Page",
        bg="#3d1f82",
        fg="#ffffff",
        font=("Times", 22),
    )
    ####Position in the frame######
    main_settings_label.pack()


##Define the more page
def more_page():
    more_frame = Frame(
        main_frame, bg="#3d1f82", highlightbackground="black", highlightthickness=1
    )
    more_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    more_frame.pack_propagate(FALSE)
    more_frame.configure(height=900, width=800)

    ####Frame Widgets#####
    main_more_label = Label(
        more_frame,
        text="More Info Page",
        bg="#3d1f82",
        fg="#ffffff",
        font=("Times", 22),
    )
    ####Position in the frame######
    main_more_label.pack()


##Advice: if you want to update a label....call the method place() or pack() in a new line, otherwise it will generate a NONE error................WTF?!!!!

# Widgets and configuration of the sidebar
sidebar = Frame(root, bg="#3d1f82", highlightbackground="black", highlightthickness=1)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(FALSE)
sidebar.configure(width=130)

# Sidebar Labels
qa_Label = Label(root, text="", bg="#3d1f82")
subjects_folder_Label = Label(root, text="", bg="#3d1f82")
settings_Label = Label(root, text="", bg="#3d1f82")
more_Label = Label(root, text="", bg="#3d1f82")

# Sidebar Buttons
qa_btn = Button(
    root,
    text="Q&A",
    bg="#3d1f82",
    bd=0,
    fg="#ffffff",
    command=lambda: [current_page(qa_Label), qa_page()],
)
subjects_folder_button = Button(
    root,
    text="SUBJECTS",
    bg="#3d1f82",
    bd=0,
    fg="#ffffff",
    command=lambda: [current_page(subjects_folder_Label), subjects_page()],
)
settings_btn = Button(
    root,
    text="SETTINGS",
    bg="#3d1f82",
    bd=0,
    fg="#ffffff",
    command=lambda: [current_page(settings_Label), settings_page()],
)
more_btn = Button(
    root,
    text="MORE",
    bg="#3d1f82",
    bd=0,
    fg="#ffffff",
    command=lambda: [current_page(more_Label), more_page()],
)


# Sidebar Buttons Positioning
qa_btn.lift()
qa_btn.place(x=20, y=30)
subjects_folder_button.lift()
subjects_folder_button.place(x=20, y=220)
settings_btn.lift()
settings_btn.place(x=20, y=420)
more_btn.lift()
more_btn.place(x=20, y=620)


# all the widgets and other setting must be written before mainloop()
root.mainloop()
