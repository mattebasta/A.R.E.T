# TODO:
#   GUI:
#       use customtkinter 
#       better UI style
#       Background color design: darker violet like in those modern UI
#       Widgets' style: Rounded corner buttons that seems integrated into the background
#       Sidebar icons
#       changing colors of the background (?)
#   Making the script an executive
#   If subjects folders are not found show error dialog to try and find those folders
#   set variable to change for background and foreground color, fonts and other variable
#   New subject generation method: Once the user has given a pdf, it will be separated in all of it's pages and automatically set to be used.
# FIX:
#   Find a way to refresh the window without having to close and open again the whole program
#   Keep the index somewhere instead of resetting it when changing the page (Put an alert when exiting the qa page)
#   Put the subject object into a scrollable text and change the size


import os
import random
import sys
import json
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
from tkinter.simpledialog import askstring
from PIL import *


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
        print(
            self.question_folder
            + "/"
            + self.quest_list[self.question_rand_list[self.curr_index]]
        )
        print(self.rand_index)

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
        self.subject_custom_frame.forget()
        with open("conf.json", "r") as config_to_modify:
            loading_modify = json.load(config_to_modify)

        for i, subs in enumerate(loading_modify["Saved subjects"]):
            if subs["Subject_Name"] == self.sub_name:
                del loading_modify["Saved subjects"][i]

        with open("conf.json", "w") as config_to_modify:
            json.dump(loading_modify, config_to_modify, indent=4, separators=(",", ":"))


##Initialization of the tkinter window
root = Tk()

##Related to GUI

# Window setting
root.title("A.R.E.T - Amazing Random Exam Tutor")
root.minsize(1100, 700)  # Minimum size of the window
root.maxsize(1100, 700)  # Maximum size of the window
root.resizable(FALSE, FALSE)
root.geometry("+500+200")  # Position of the window in the screen and size of the window

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
    configFileAlert = messagebox.askquestion(
        title="Warning",
        message="No folder config file found \n would you like to make a new one?",
        icon="warning",
    )
    if configFileAlert == "yes":
        subject_name = askstring("Subject's name", "Insert subject's name", parent=root)
        if subject_name == None:
            sys.exit()
        else:
            question_folder = askstring(
                "Question Folder", "Insert question folder path", parent=root
            )
        if question_folder == None:
            sys.exit()
        else:
            answer_folder = askstring(
                "Answer Folder", "Insert answer folder path", parent=root
            )
            if answer_folder == None:
                sys.exit()
    else:
        messagebox.showwarning(
            title="Warning", message="Subject folder not found \n program will close"
        )
        sys.exit()

    # Preparing folder datas to write in the json file
    dict = {
        "Saved subjects": [
            {
                "Subject_Name": subject_name,
                "question_folder": question_folder,
                "answer_folder": answer_folder,
            }
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

##Lists where the objects for the frames are saved and used also to show object in their respective frames
subject_btn_list = []
subject_list = []
saved_sub = load_file["Saved subjects"]


# Function that show the current section
def current_page(label):
    label.config(bg="#FFFFFF")
    del_current()


# Function that delete the current frame
def del_current():
    for frame in main_frame.winfo_children():
        frame.pack_forget()


# Function to add subject object to the subject list, used to render the subject into the frame
def add_to_subject_list(frame_):
    for sub in saved_sub:
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
    for sub in saved_sub:
        subject_btn_list.append(Subject_BTN(frame_, sub["Subject_Name"]))

    # print(*subject_btn_list)
    # for listed in subject_btn_list:
    #     listed.pack()


def set_widgets_subject(frame_):
    widgets_list = []
    widgets_in_frame = frame_.winfo_children()
    for widgets in widgets_in_frame:
        widgets_list.append(widgets)

    #####For future update use an index to dynamically calculate the widget_list[index], taking the length of the subject_btn_list and the index should only have odd numbers####
    match len(subject_list):
        case 1:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
        case 2:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(1, weight=1, uniform=0)
        case 3:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=10, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid(
                column=0, row=1, padx=30, pady=10, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[2].grid(
                column=0, row=2, padx=30, pady=10, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[2].grid_columnconfigure(2, weight=1, uniform=0)
        case 4:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[2].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[2].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(0, weight=1, uniform=0)
        case 5:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[2].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[4].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[2].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[4].grid_columnconfigure(1, weight=1, uniform=0)
        case 6:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=20, ipadx=40, ipady=10, columnspan=1
            )
            widgets_list[1].grid(
                column=1, row=0, padx=30, pady=20, ipadx=40, ipady=10, columnspan=1
            )
            widgets_list[2].grid(
                column=2, row=0, padx=30, pady=20, ipadx=40, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=0, row=1, padx=30, pady=20, ipadx=40, ipady=10, columnspan=1
            )
            widgets_list[4].grid(
                column=1, row=1, padx=30, pady=20, ipadx=40, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=1, padx=30, pady=20, ipadx=40, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[2].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[4].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
        case 7:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[2].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[4].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[6].grid(
                column=0, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[2].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[4].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[6].grid_columnconfigure(0, weight=1, uniform=0)
        case 8:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[2].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[4].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[6].grid(
                column=0, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[7].grid(
                column=1, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[2].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[4].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[6].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(1, weight=1, uniform=0)
        case 9:
            widgets_list[0].grid(
                column=0, row=0, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[1].grid(
                column=0, row=1, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[2].grid(
                column=0, row=2, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[3].grid(
                column=0, row=3, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[4].grid(
                column=0, row=4, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[5].grid(
                column=0, row=5, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[6].grid(
                column=0, row=6, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[7].grid(
                column=0, row=7, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[8].grid(
                column=0, row=8, padx=30, pady=10, ipadx=80, ipady=10, columnspan=5
            )
            widgets_list[0].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[2].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[4].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[6].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[8].grid_columnconfigure(0, weight=1, uniform=0)

        case _:
            messagebox.showerror(
                "Too Many Subjects", "Too many subjects have been added"
            )

    subject_list.clear()


def set_widgets_subject_btn(frame_):
    widgets_list = []
    widgets_in_frame = frame_.winfo_children()
    for widgets in widgets_in_frame:
        widgets_list.append(widgets)

    #####For future update use an index to dynamically calculate the widget_list[index], taking the length of the subject_btn_list and the index should only have odd numbers####
    match len(subject_btn_list):
        case 1:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
        case 2:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
        case 3:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)

        case 4:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[7].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(0, weight=1, uniform=0)
        case 5:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[7].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[9].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[9].grid_columnconfigure(1, weight=1, uniform=0)
        case 6:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[7].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[9].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[11].grid(
                column=2, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[9].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[11].grid_columnconfigure(2, weight=1, uniform=0)
        case 7:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[7].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[9].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[11].grid(
                column=2, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[13].grid(
                column=0, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[9].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[11].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[13].grid_columnconfigure(0, weight=1, uniform=0)
        case 8:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[7].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[9].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[11].grid(
                column=2, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[13].grid(
                column=0, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[15].grid(
                column=1, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[9].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[11].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[13].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[15].grid_columnconfigure(1, weight=1, uniform=0)
        case 9:
            widgets_list[1].grid(
                column=0, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[3].grid(
                column=1, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[5].grid(
                column=2, row=0, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[7].grid(
                column=0, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[9].grid(
                column=1, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[11].grid(
                column=2, row=1, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[13].grid(
                column=0, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[15].grid(
                column=1, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[17].grid(
                column=2, row=2, padx=30, pady=50, ipadx=80, ipady=10, columnspan=1
            )
            widgets_list[1].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[3].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[5].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[7].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[9].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[11].grid_columnconfigure(2, weight=1, uniform=0)
            widgets_list[13].grid_columnconfigure(0, weight=1, uniform=0)
            widgets_list[15].grid_columnconfigure(1, weight=1, uniform=0)
            widgets_list[17].grid_columnconfigure(2, weight=1, uniform=0)
        case _:
            messagebox.showerror(
                "Too Many Subjects", "Too many subjects have been added"
            )

    subject_btn_list.clear()


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

    # subject_canvas = Canvas(subjects_frame, height=700, width=1000, bg="white")
    # subject_canvas.pack()

    add_to_subject_btn_list(subjects_frame)

    # Btn to add new subjects
    add_new_subjects_btn = Button(
        subjects_frame, text="ADD NEW", command=lambda: save_new_subject()
    )
    add_new_subjects_btn.grid(
        row=4, column=1, rowspan=2, columnspan=1, padx=20, pady=20, ipadx=70, ipady=10
    )

    set_widgets_subject_btn(subjects_frame)


# Function to write a new subject into the configuration json file, fired after the button "ADD NEW" in the subject frame is pressed
def save_new_subject():
    new_sub_name = askstring("Subject name", "Insert subject's name", parent=root)
    if new_sub_name is None:
        return
    else:
        new_quest_folder = askstring(
            "Subject quest folder", "Insert subject quest folder", parent=root
        )
        if new_quest_folder is None:
            return
        else:
            new_ans_folder = askstring(
                "Subject answer folder", "Insert subject answer folder", parent=root
            )
            if new_ans_folder is None:
                return

    def write_json(new_data, filename="conf.json"):
        with open(filename, "r+") as file:
            file_data = json.load(file)
            file_data["Saved subjects"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    newdic = {
        "Subject_Name": new_sub_name,
        "question_folder": new_quest_folder,
        "answer_folder": new_ans_folder,
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
