# TODO:
#  GUI:
#       better UI style
#       Add error windows
#       Background color design: darker violet like in those modern UI
#       Widgets' style: Rounded corner buttons that seems integrated into the background
#       Sidebar icons
#   Making the script an executive
#   Switch between subjects
#   Button to add new subjects
#   Creation of subjects from two pdfs files, question and answer will be created from those pdfs and saved in the json as the subjects name given from user
#   If subjects folders are not found show error dialog to try and find those folders
#   Organize the structure of the json into "subjects"

import os
import random
import sys
import json
from tkinter import *
from tkinter import messagebox
from PIL import *




root = Tk()

#Window setting
root.title("E-CET")
root.minsize(900, 700) #Minimum size of the window
root.maxsize(900, 700) #Maximum size of the window
root.resizable(FALSE,FALSE)
root.geometry("1000x700+500+200") #Position of the window in the screen and size of the window

main_frame = Frame(root, bg='#3d1f82', highlightbackground='blue', highlightthickness=2)
main_frame.pack(side=RIGHT)
main_frame.pack_propagate(FALSE)
main_frame.configure(height=900, width=800)





#Main Code

#Setting the config file
config_File = './conf.JSON'
check_file = os.path.isfile(config_File)

#Check if config file already exist
if check_file == False:
    print("no folder config found...\ncreating now....")
    question_folder = input("select question folder: ")
    answer_folder = input("select answer folder: ")
    
    #Preparing folder datas to write in the json file    
    dict = {"question_folder":question_folder, "answer_folder": answer_folder}
    valueToWrite = json.dumps(dict)
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

#Read the value from json
quest_folder =  load_file["question_folder"] 
ans_folder =  load_file["answer_folder"]

#Get all the files in a list
questList = os.listdir(quest_folder)
ansList = os.listdir(ans_folder)
if len(questList) == len(ansList):
    print("list have the same amount")
else:
    print("list are different length")
    messagebox.showerror('Fatal Error','File in folders are not the same amount')
    sys.exit()

#Making rand_index a global variable is necessary, due to the need of it in and out of a function
global rand_index
rand_index = (random.randint(0, len(questList)-1))


#Functions
def update_Index(lbl):
    global rand_index
    rand_index = (random.randint(0, len(questList)-1))
    lbl.config(text='current index: ' + str(rand_index))


def choose_quest ():
    os.startfile(quest_folder + '/' + questList[rand_index])


def current_page(label):
    label.config(bg='#FFFFFF')
    del_current()

def del_current():
    for frame in main_frame.winfo_children():
        frame.destroy()

##Define the question & answers page
def qa_page():
    qa_frame = Frame(main_frame, bg='#3d1f82', highlightbackground='blue', highlightthickness=2)
    qa_frame.pack(side=RIGHT)
    qa_frame.pack_propagate(FALSE)
    qa_frame.configure(height=900, width=800)
    
    ####Frame Widgets#####
    
    index_Label = Label(qa_frame, text='current index: ' + str(rand_index),bg='#3d1f82',fg='#ffffff', font=('Times',12))
    quest_btn = Button(qa_frame, text='Question', command=lambda : choose_quest(),bg='#3d1f82',fg='#ffffff', font=('Times',12))
    ans_btn = Button(qa_frame, text='Answer', command=lambda : os.startfile(ans_folder + '/' + ansList[rand_index]),bg='#3d1f82',fg='#ffffff', font=('Times',12))
    update_btn = Button(qa_frame, text='Update', command=lambda : update_Index(index_Label),bg='#3d1f82',fg='#ffffff', font=('Times',12))
    
    ####Position in the frame######
    
    index_Label.pack()
    quest_btn.pack()
    ans_btn.pack()
    update_btn.pack()

##Define the subjects subjects page
def subjects_page():
    subjects_frame = Frame(main_frame, bg='#3d1f82', highlightbackground='blue', highlightthickness=2)
    subjects_frame.pack(side=RIGHT)
    subjects_frame.pack_propagate(FALSE)
    subjects_frame.configure(height=900, width=800)
    
    ####Frame Widgets#####
    main_subjects_label = Label(subjects_frame, text='Subjects Page',bg='#3d1f82',fg='#ffffff', font=('Times',22))
    quest_Label_folder = Label(subjects_frame, text='Question Folder Path:',bg='#3d1f82',fg='#ffffff', font=('Times',12))
    quest_Text_folder = Label(subjects_frame, text=quest_folder,bg='#3d1f82',fg='#ffffff', font=('Times',12))
    ans_label_folder = Label(subjects_frame, text='Answer Folder Path:',bg='#3d1f82',fg='#ffffff', font=('Times',12))
    ans_Text_folder = Label(subjects_frame, text=ans_folder,bg='#3d1f82',fg='#ffffff', font=('Times',12))
    
    ####Position in the frame######
    main_subjects_label.pack()
    quest_Label_folder.pack()
    quest_Text_folder.pack()
    ans_label_folder.pack()
    ans_Text_folder.pack()

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

#Widgets

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


##Buttons(main_frame)





##Frames


#Sidebar
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