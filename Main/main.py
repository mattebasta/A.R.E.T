# TODO:
#   GUI:
#       better UI style
#       Background color design: darker violet like in those modern UI
#       Widgets' style: Rounded corner buttons that seems integrated into the background
#       Sidebar icons
#   Making the script an executive
#   If subjects folders are not found show error dialog to try and find those folders
#   Delete information from config file when object is destroyed
# FIX:
#   reset position and color after deleting
#   Find a way to refresh the window without having to close and open again the whole program

import os
import random
import sys
import json
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from PIL import *

##Class Subject is used to create an object for every subjects is in the configuration json file, also it sets the button to ask question and show answers.
class Subject(Frame):
    
    curr_index = 0
    
    def __init__(self, master, name, question_folder, answer_folder):
        ##Initializing parameters
        Frame.__init__(self, master)
        self.sub_name = name
        self.question_folder = question_folder
        self.answer_folder = answer_folder
        
        
        ##Call the create index method to make the list of questions and answers
        self.create_index()
        
        ##Widgets creation
        self.sub_lbl = Label(self, text=name)
        self.index_lbl = Label(self, text="question " + str(self.curr_index))
        self.ask_question_btn = Button(self, text="Question", command = lambda : self.ask_question())
        self.show_answer_btn = Button(self, text="Answer", command = lambda : self.show_answer())
        self.index_forward_btn = Button(self, text="Next", command = lambda : self.index_forward())
        self.index_backward_btn = Button(self, text="Previous", command = lambda : self.index_backward())
        self.sub_lbl.pack()
        self.index_lbl.pack()
        self.ask_question_btn.pack()
        self.show_answer_btn.pack()
        self.index_forward_btn.pack()
        self.index_backward_btn.pack()
        
    ##Method to create the list containing the questions and answers
    def create_index(self):
        self.quest_list = os.listdir(self.question_folder)
        self.ans_list = os.listdir(self.answer_folder)
        if len(self.quest_list) == len(self.ans_list):
            rand_index = (random.sample(range(len(self.quest_list)+1),len(self.quest_list)+1))
            self.question_rand_list = rand_index
            self.answer_rand_list = rand_index
        else:
            messagebox.showerror('Fatal Error','File in folders are not the same amount')
            sys.exit()

    ##Method that take the next index in the list
    def index_forward(self):
        if self.curr_index == (len(self.question_rand_list)-1):
            print("last index, cannot go forward")
        else:
            self.curr_index += 1
            self.update_index()
            print(self.curr_index)
    
    ##Method that take the previous index in the list
    def index_backward(self):
        if self.curr_index == 0:
            print("first index, cannot go backward")
        else:    
            self.curr_index -= 1
            self.update_index()
            print(self.curr_index)

    ##Method to update the index label
    def update_index(self):
        self.index_lbl.config(text="question " + str(self.curr_index))

    ##Method to open a question with a given index
    def ask_question(self):
        os.startfile(self.question_folder + '/' + self.quest_list[self.question_rand_list[(self.curr_index)]])
        print(self.question_folder + '/' + self.quest_list[self.question_rand_list[self.curr_index]])
    
    ##Method to open an answer with a given index
    def show_answer(self):
        os.startfile(self.answer_folder + '/' + self.ans_list[self.answer_rand_list[self.curr_index]])
        print(self.answer_folder + '/' + self.ans_list[self.answer_rand_list[self.curr_index]])

##Class Subject_BTN create an object in the subject frame, in order to add a new subject or delete an existing one
class Subject_BTN(Frame):
    ##Initialization
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.lbl = Label(self, text=name)
        self.btn_del = Button(self, text="DEL", command=lambda : self.__delete_Subject__())
        self.lbl.pack()
        self.btn_del.pack()
    
    ##Method to delete a subject
    def __delete_Subject__(self):
        self.lbl.destroy()
        self.btn_del.destroy()

##Initialization of the tkinter window
root = Tk()

#Window setting
root.title("A.R.E.T - Amazing Random Exam Tutor")
root.minsize(900, 700) #Minimum size of the window
root.maxsize(900, 700) #Maximum size of the window
root.resizable(FALSE,FALSE)
root.geometry("1000x700+500+200") #Position of the window in the screen and size of the window

#Main frame settings
main_frame = Frame(root, bg='#3d1f82', highlightbackground='blue', highlightthickness=2)
main_frame.pack(side=RIGHT)
main_frame.pack_propagate(FALSE)
main_frame.configure(height=900, width=800)


#Setting the config file
config_File = './conf.JSON'
check_file = os.path.isfile(config_File)

#Check if config file already exist
if check_file == False:
    print("no folder config found...\ncreating now....")
    configFileAlert = messagebox.askquestion(title="Warning",message="No folder config file found \n would you like to make a new one?", icon='warning')
    if configFileAlert == 'yes':
        subject_name = askstring("Subject's name","Insert subject's name", parent=root)
        if subject_name == None:
            sys.exit()
        else:
            question_folder = askstring("Question Folder","Insert question folder path", parent=root)
        if question_folder == None:
            sys.exit()
        else:
            answer_folder = askstring("Answer Folder","Insert answer folder path", parent=root)
            if answer_folder == None:
                sys.exit()
    else:
        messagebox.showwarning(title="Warning", message="Subject folder not found \n program will close")
        sys.exit()
    
    
    #Preparing folder datas to write in the json file    
    dict = { 
            "Saved subjects":
            [
                {
                    "Subject_Name": subject_name,
                    "question_folder": question_folder, 
                    "answer_folder": answer_folder
                }
            ]
            }
    valueToWrite = json.dumps(dict, indent=4, separators=(',',':'))
    jsonConf = open("conf.json", "w")
    jsonConf.write(valueToWrite)
    jsonConf.close()
    
    #open config file to read the values
    with open('conf.json', 'r') as conf_file:
        load_file = json.load(conf_file)
else:
    #Config file already exist
    print("config file already exists...\nreading folders from config....")
    with open('conf.json', 'r') as conf_file:
        load_file = json.load(conf_file)

##Labels(main_frame)
starting_Label = Label(main_frame, 
                    text="Welcome to ARET\n Amazing. Random. Exam. Tutor. \n your best friend when you need someone to ask you random exam questions",
                    bg='#3d1f82',
                    )
instructions_label = Label(main_frame, 
                        text="Before you start you need to set up the folders containing your question and answers\n the program should have already asked you that, but if you need to add more subjects\n you can do that by pressing the subjects button on the left sidebar",
                        bg='#3d1f82'
                        )
starting_Label.pack()
instructions_label.pack()

##Lists where the objects for the frames are saved and used also to show object in their respective frames
subject_btn_list = []
subject_list = []
saved_sub = load_file['Saved subjects']

#Function that show the current section
def current_page(label):
    label.config(bg='#FFFFFF')
    del_current()
#Function that doesn't show white box when a section is not selected
def del_current():
    for frame in main_frame.winfo_children():
        frame.forget()


##Define the question & answers page
def qa_page():
    qa_frame = Frame(main_frame, bg='#3d1f82', highlightbackground='blue', highlightthickness=2)
    qa_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    qa_frame.pack_propagate(FALSE)
    qa_frame.configure(height=900, width=800)
    
    ####Frame Widgets#####
    for sub in saved_sub:
        subject_list.append(Subject(qa_frame, sub['Subject_Name'], sub['question_folder'], sub['answer_folder']))
        
    for subs in subject_list:
        subs.pack()  
    



##Define the subjects page
def subjects_page():
    subjects_frame = Frame(main_frame, bg='red', highlightbackground='blue', highlightthickness=2)
    subjects_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    subjects_frame.pack_propagate(FALSE)
    subjects_frame.configure(height=900, width=800)
    

    ####Frame Widgets#####
    
    for sub in saved_sub:
        subject_btn_list.append(Subject_BTN(subjects_frame,sub['Subject_Name'])) 
        
    for btns in subject_btn_list:
        btns.pack()           
    
    #Debug for loop, it shows how many buttons are in the list
    for x in range(len(subject_btn_list)):
        print (subject_btn_list[x])
    
    #Btn to add new subjects
    add_new_subjects_btn = Button(subjects_frame, text='ADD NEW', command = lambda : save_new_subject()) 
    add_new_subjects_btn.pack()


#Function to write a new subject into the configuration json file, fired after the button "ADD NEW" in the subject frame is pressed
def save_new_subject():
    new_sub_name = askstring("Subject name","Insert subject's name", parent=root)
    if new_sub_name is None:
        return
    else:
        new_quest_folder = askstring("Subject quest folder","Insert subject quest folder", parent=root)
        if new_quest_folder is None:
            return
        else:
            new_ans_folder = askstring("Subject answer folder","Insert subject answer folder", parent=root)
            if new_ans_folder is None:
                return
    
        
    def write_json(new_data, filename = 'conf.json'):
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data["Saved subjects"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    
    newdic = {
                "Subject_Name": new_sub_name,
                "question_folder": new_quest_folder, 
                "answer_folder": new_ans_folder
            }
    
    write_json(newdic)


##Define the settings page
def settings_page():
    settings_frame = Frame(main_frame, bg='#3d1f82', highlightbackground='blue', highlightthickness=2)
    settings_frame.pack(side=RIGHT)
    settings_frame.pack_propagate(FALSE)
    settings_frame.configure(height=900, width=800)
    
    ####Frame Widgets#####
    main_settings_label = Label(settings_frame, text='Settings Page',bg='#3d1f82',fg='#ffffff', font=('Times',22))
    ####Position in the frame######
    main_settings_label.pack()

##Define the more page
def more_page():
    more_frame = Frame(main_frame, bg='#3d1f82', highlightbackground='blue', highlightthickness=2)
    more_frame.pack(side=RIGHT)
    more_frame.pack_propagate(FALSE)
    more_frame.configure(height=900, width=800)
    
    ####Frame Widgets#####
    main_more_label = Label(more_frame, text='More Info Page',bg='#3d1f82',fg='#ffffff', font=('Times',22))
    ####Position in the frame######
    main_more_label.pack()


##Advice: if you want to update a label....call the method place() or pack() in a new line, otherwise it will generate a NONE error................WTF?!!!!

#Widgets and configuration of the sidebar
sidebar = Frame(root, bg="#3d1f82", highlightbackground='blue', highlightthickness=2)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(FALSE)
sidebar.configure(width=110)

#Sidebar Labels
qa_Label = Label(root, text = '', bg="#3d1f82")
subjects_folder_Label = Label(root, text = '', bg="#3d1f82")
settings_Label = Label(root, text = '', bg="#3d1f82")
more_Label = Label(root, text = '', bg="#3d1f82")

#Sidebar Buttons
qa_btn = Button(root, text='Q&A', bg="#3d1f82", bd=0, fg='#ffffff', command=lambda: [current_page(qa_Label), qa_page()])
subjects_folder_button = Button(root, text='SUBJECTS', bg="#3d1f82", bd=0, fg='#ffffff', command=lambda: [current_page(subjects_folder_Label), subjects_page()])
settings_btn = Button(root, text='SETTINGS', bg="#3d1f82", bd=0, fg='#ffffff', command=lambda: [current_page(settings_Label), settings_page()])
more_btn = Button(root, text='MORE', bg="#3d1f82", bd=0, fg='#ffffff', command=lambda: [current_page(more_Label), more_page()])


#Sidebar Buttons Positioning
qa_btn.lift()
qa_btn.place(x=20,y=30)
subjects_folder_button.lift()
subjects_folder_button.place(x=20,y=220)
settings_btn.lift()
settings_btn.place(x=20,y=420)
more_btn.lift()
more_btn.place(x=20,y=620)

#all the widgets and other setting must be written before mainloop()
root.mainloop()