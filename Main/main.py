# TODO:
#  GUI? Tkinter

import os
import random
import json
import sys
from tkinter import *



root = Tk()
#Window setting
root.title("E-CET")
root.minsize(1000, 700) #Minimum size of the window
root.geometry("300x300+50+50") #Position of the window in the screen

#Label
startingText = Label(root, text="To start setup the question and answer folder \n Then press the button start")
startingText.pack()




#all the widgets and other setting must be written before mainloop()
root.mainloop()




###################################################################MAIN CODE###########################################################################
# #Setting the config file
# config_File = './conf.JSON'
# check_file = os.path.isfile(config_File)

# #Check if config file already exist
# if check_file == False:
#     print("no folder config found...\ncreating now....")
#     question_folder = input("select question folder: ")
#     answer_folder = input("select answer folder: ")
    
#     #Preparing folder datas to write in the json file    
#     dict = {"question_folder":question_folder, "answer_folder": answer_folder}
#     valueToWrite = json.dumps(dict)
#     jsonConf = open("conf.json", "w")
#     jsonConf.write(valueToWrite)
#     jsonConf.close()
    
#     #open config file to read the values
#     with open('conf.json', 'r') as conf_file:
#         load_file = json.load(conf_file)
# else:
#     #Config file already exist
#     print("config file already exists...\nreading folders from config....")
#     with open('conf.json', 'r') as conf_file:
#         load_file = json.load(conf_file)


# #Read the value from json
# quest_folder =  load_file["question_folder"] 
# ans_folder =  load_file["answer_folder"]


# #Get all the files in a list
# questList = os.listdir(quest_folder)
# ansList = os.listdir(ans_folder)

# #Choosing a random file to open
# rand_Quest = random.choice(questList)
# #Getting the index of the random question
# questIndex = questList.index(rand_Quest)
# #opening the choosen file
# os.startfile(quest_folder + '/' + rand_Quest)
# #Waiting for user's input, if the input is 'y' then the file containing the answers is opened, otherwise the program will be closed
# answer = input("do you want to see the answer?")
# if answer == "y":
#     os.startfile(ans_folder + '/' + ansList[questIndex])
# else:
#     sys.exit()
