# TODO:
#  GUI add:
#       button to open different folders
#       better UI style
#       Add error windows
#  Making the script an executive

import os
import random
import sys
import json
from tkinter import *
from tkinter import messagebox




root = Tk()

#Window setting
root.title("E-CET")
root.minsize(1000, 700) #Minimum size of the window
root.geometry("1000x700+500+200") #Position of the window in the screen and size of the window

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
rand_index = (random.randint(0, len(questList)))


#Functions
def update_Index():
    global rand_index
    rand_index = (random.randint(0, len(questList)))
    index_Label.config(text='current index: ' + str(rand_index))


def choose_quest ():
    os.startfile(quest_folder + '/' + questList[rand_index])


##Advice: if you want to update a label....call the method place() or pack() in a new line, otherwise it will generate a NONE error................

#Widgets

##Labels
quest_Label_folder = Label(root, text='Question Folder Path\n')
quest_Text_folder = Label(root, text=quest_folder)
ans_label_folder = Label(root, text='Answer Folder Path\n')
ans_Text_folder = Label(root, text=ans_folder)
index_Label = Label(root, text='current index: ' + str(rand_index))

##Buttons
quest_btn = Button(root, text='Question', command=lambda : choose_quest())
ans_btn = Button(root, text='Answer', command=lambda : os.startfile(ans_folder + '/' + ansList[rand_index]))
update_btn = Button(root, text='Update', command=lambda : update_Index())


#Widgets' position in the root window
quest_Label_folder.place(x=80,y=60)
quest_Text_folder.place(x=80,y=90)
ans_label_folder.place(x=550,y=60)
ans_Text_folder.place(x=550,y=90)
index_Label.place(x=550,y=120)
quest_btn.place(x=200, y=180)
ans_btn.place(x=600, y=180)
update_btn.place(x=400, y=180)

#all the widgets and other setting must be written before mainloop()
root.mainloop()






