# TODO:
#   GUI:
#
#   Making the script an executive

#   ROADMAP:
#   Make the theme rendering instantenous (have to define some function to call to set and update the dict and all the widgets)

#   FIX:



import os
import random
import sys
import json
import shutil
import pathlib
import warnings
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
import customtkinter
import webbrowser
from PIL import *
from pypdf import PdfWriter, PdfReader
from pypdf.errors import PdfReadError


warnings.filterwarnings('ignore')

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
root.maxsize(1500, 700)  # Maximum size of the window
root.resizable(FALSE, FALSE)
root.geometry("500+200")  # Position of the window in the screen and size of the window 




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
    "Theme": [
        {
            "theme_name": "System",
            "theme_fg" : "#3689e6",
            "theme_font" : "system",
            "theme_font_size" : 20,
            "theme_text_color": "white",
            "theme_frame_color": "#00495c"
        }
    ],

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

##Lists where the objects for the frames are saved and used also to show object in their respective frames
subject_btn_list = []
subject_list = []


with open('conf.json', 'r') as f:
    load_config = json.load(f)
    
    theme_dict = {
        "theme_name" : load_config["Theme"][0]["theme_name"],
        "theme_fg" : load_config["Theme"][0]["theme_fg"],
        "theme_font" : load_config["Theme"][0]["theme_font"],
        "theme_font_size" : load_config["Theme"][0]["theme_font_size"],
        "theme_text_color" : load_config["Theme"][0]["theme_text_color"],
        "theme_frame_color" : load_config["Theme"][0]["theme_frame_color"]
        }

# Main frame settings
main_frame = customtkinter.CTkFrame(
    root, border_color = "black", border_width = 1, fg_color=theme_dict["theme_frame_color"]
)
main_frame.pack(side=RIGHT)
main_frame.pack_propagate(False)
main_frame.configure(width=1200, height=900)


##Class Subject is used to create an object for every subjects is in the configuration json file, also it sets the button to ask question and show answers.
class Subject(Frame):
    def __init__(self, master, name, question_folder, answer_folder):
        ##Initializing parameters
        Frame.__init__(
            self,
            master
        )
        self.sub_name = name
        self.question_folder = question_folder
        self.answer_folder = answer_folder
        self.curr_index = 0

        ##Call the create index method to make the list of questions and answers
        self.create_index()
        ##Widgets creation
        self.subject_custom_frame = customtkinter.CTkFrame(
            master,
            fg_color=theme_dict["theme_frame_color"]
        )
        self.sub_lbl = customtkinter.CTkLabel(self.subject_custom_frame, text=name, font = (theme_dict["theme_font"], theme_dict["theme_font_size"]), text_color = theme_dict["theme_text_color"])
        self.index_lbl = customtkinter.CTkLabel(
            self.subject_custom_frame,
            text="question "
            + str(self.curr_index + 1)
            + "/"
            + str(len(self.quest_list)),
            font = (theme_dict["theme_font"], theme_dict["theme_font_size"]),
            text_color = theme_dict["theme_text_color"]
        )
        self.ask_question_btn = customtkinter.CTkButton(
            self.subject_custom_frame, text="Question", command=lambda: self.ask_question(), fg_color=theme_dict["theme_fg"], text_color = theme_dict["theme_text_color"],  font = (theme_dict["theme_font"], theme_dict["theme_font_size"])
        )
        self.show_answer_btn = customtkinter.CTkButton(
            self.subject_custom_frame, text="Answer", command=lambda: self.show_answer(), fg_color=theme_dict["theme_fg"], text_color = theme_dict["theme_text_color"], font = (theme_dict["theme_font"], theme_dict["theme_font_size"])
        )
        self.index_forward_btn = customtkinter.CTkButton(
            self.subject_custom_frame, text="Next", command=lambda: self.index_forward(), fg_color=theme_dict["theme_fg"], text_color = theme_dict["theme_text_color"], font = (theme_dict["theme_font"], theme_dict["theme_font_size"])
        )
        self.index_backward_btn = customtkinter.CTkButton(
            self.subject_custom_frame, text="Previous", command=lambda: self.index_backward(), fg_color=theme_dict["theme_fg"], text_color = theme_dict["theme_text_color"], font = (theme_dict["theme_font"], theme_dict["theme_font_size"])
        )

        self.subject_custom_frame.pack(pady = 15, padx = 5, expand=True, fill=X)
        self.sub_lbl.pack(side=LEFT, padx=10, pady=10, expand=True)
        self.index_lbl.pack(side=LEFT, padx=10, pady=10, expand=True)
        self.ask_question_btn.pack(side=LEFT, padx=10, pady=10, expand=True)
        self.show_answer_btn.pack(side=LEFT, padx=10, pady=10, expand=True)
        self.index_forward_btn.pack(
            side=LEFT, padx=10, pady=10, expand=True
        )
        self.index_backward_btn.pack(
            side=LEFT, padx=10, pady=10, expand=True
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
        self.index_lbl.configure(
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

        self.subject_btn_custom_frame = customtkinter.CTkFrame(
            master,
            width=500,
            height=600,
            fg_color=theme_dict["theme_frame_color"]
        )
        self.lbl = customtkinter.CTkLabel(self.subject_btn_custom_frame, text=name, font=(theme_dict["theme_font"], theme_dict["theme_font_size"]), text_color = theme_dict["theme_text_color"])
        self.btn_del = customtkinter.CTkButton(
            self.subject_btn_custom_frame,
            text="DEL",
            command=lambda: self.__delete_Subject__(),
            fg_color=theme_dict["theme_fg"],
            text_color = theme_dict["theme_text_color"],
            font=(theme_dict["theme_font"], theme_dict["theme_font_size"])
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

##Labels(main_frame)
starting_Label = customtkinter.CTkLabel(
    main_frame,
    text="Welcome to ARET",
    font = (theme_dict["theme_font"], theme_dict["theme_font_size"]),
    text_color = theme_dict["theme_text_color"]
)
instructions_label = customtkinter.CTkLabel(
    main_frame,
    text="If you want to start using ARET, you will need to set up a subject into the subject page \n Or you can change your theme in the settings page \n If you still need help you can visit the more page",
    font = (theme_dict["theme_font"], theme_dict["theme_font_size"]),
    text_color = theme_dict["theme_text_color"]
)
starting_Label.pack(pady = 20)
instructions_label.pack(pady = 20)


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


##Define the question & answers page
def qa_page():
    qa_frame = customtkinter.CTkFrame(
        main_frame,
        fg_color=theme_dict["theme_frame_color"]
    )
    qa_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    qa_frame.pack_propagate(FALSE)
    

    scroll_qa_frame = customtkinter.CTkScrollableFrame(qa_frame, fg_color=theme_dict["theme_frame_color"])
    scroll_qa_frame.pack(side=LEFT, expand=True, fill=BOTH)

    add_to_subject_list(scroll_qa_frame)


##Define the subjects page
def subjects_page():
    subjects_frame = customtkinter.CTkFrame(
        main_frame,
        fg_color=theme_dict["theme_frame_color"]
    )
    subjects_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    subjects_frame.pack_propagate(FALSE)

    scroll_subject_frame = customtkinter.CTkScrollableFrame(subjects_frame, fg_color=theme_dict["theme_frame_color"])
    scroll_subject_frame.pack(side=LEFT, expand=True, fill=BOTH)

    add_to_subject_btn_list(scroll_subject_frame)

    # Btn to add new subjects
    add_new_subjects_btn = customtkinter.CTkButton(
        scroll_subject_frame, text="ADD NEW", fg_color=theme_dict["theme_fg"], text_color = theme_dict["theme_text_color"], font = (theme_dict["theme_font"], theme_dict["theme_font_size"]), command=lambda: save_new_subject()
    )
    add_new_subjects_btn.pack(pady = 50)


# Function to write a new subject into the configuration json file, fired after the button "ADD NEW" in the subject frame is pressed
def save_new_subject():
    filetype_ = [('pdf file', '*.pdf')]
    new_sub_name = askstring("Subject name", "Insert subject's name", parent=root)
    if new_sub_name is None:
        return
    elif len(new_sub_name) > 10:
        messagebox.showerror("Error", "Name cannot have more than 10 chars")
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


def setup_theme(theme_name):#[      name,             fg_color,                font,               font_size,    text_color,    frame_color]
    halloween_theme_list =       ["Spooky",           "#e65900",          "Century Gothic",           20,         "#fffdee",       "#1d0d25"] 
    system_theme_list =          ["System",           "#3689e6",          "System",                   20,         "#fffdee",       "#00495c"]
    noel_theme_list =            ["Noel",             "#BB010B",          "Lucida Handwriting",       20,         "#FAF8F8",       "#23856D"]
    nightshade_theme_list =      ["Nightshade",       "#140152",          "Rockwell",                 20,         "#fceff9",       "#04052E"]
    cottoncandy_theme_list =     ["CottonCandy",      "#e4e5f1",          "Moonbeam",                 20,         "#5575c2",       "#fafafa"]
    with open('conf.json', 'r') as file_theme:
        file_theme_data = json.load(file_theme)
        if theme_name == "System":
            file_theme_data["Theme"][0]["theme_name"] = system_theme_list[0]
            file_theme_data["Theme"][0]["theme_fg"] = system_theme_list[1]
            file_theme_data["Theme"][0]["theme_font"] = system_theme_list[2]
            file_theme_data["Theme"][0]["theme_font_size"] = system_theme_list[3]
            file_theme_data["Theme"][0]["theme_text_color"] = system_theme_list[4]
            file_theme_data["Theme"][0]["theme_frame_color"] = system_theme_list[5]
            messagebox.showinfo(title = "Theme set", message = "In order to change theme you will have to restart the program \n NOTE: All the current indexes will be reset to 1!")
        elif theme_name == "Spooky":
            file_theme_data["Theme"][0]["theme_name"] = halloween_theme_list[0]
            file_theme_data["Theme"][0]["theme_fg"] = halloween_theme_list[1]
            file_theme_data["Theme"][0]["theme_font"] = halloween_theme_list[2]
            file_theme_data["Theme"][0]["theme_font_size"] = halloween_theme_list[3]
            file_theme_data["Theme"][0]["theme_text_color"] = halloween_theme_list[4]
            file_theme_data["Theme"][0]["theme_frame_color"] = halloween_theme_list[5]
            messagebox.showinfo(title = "Theme set", message = "In order to change theme you will have to restart the program \n NOTE: All the current indexes will be reset to 1!")
        elif theme_name == "Noel":
            file_theme_data["Theme"][0]["theme_name"] = noel_theme_list[0]
            file_theme_data["Theme"][0]["theme_fg"] = noel_theme_list[1]
            file_theme_data["Theme"][0]["theme_font"] = noel_theme_list[2]
            file_theme_data["Theme"][0]["theme_font_size"] = noel_theme_list[3]
            file_theme_data["Theme"][0]["theme_text_color"] = noel_theme_list[4]
            file_theme_data["Theme"][0]["theme_frame_color"] = noel_theme_list[5]
            messagebox.showinfo(title = "Theme set", message = "In order to change theme you will have to restart the program \n NOTE: All the current indexes will be reset to 1!")
        elif theme_name == "Nightshade":
            file_theme_data["Theme"][0]["theme_name"] = nightshade_theme_list[0]
            file_theme_data["Theme"][0]["theme_fg"] = nightshade_theme_list[1]
            file_theme_data["Theme"][0]["theme_font"] = nightshade_theme_list[2]
            file_theme_data["Theme"][0]["theme_font_size"] = nightshade_theme_list[3]
            file_theme_data["Theme"][0]["theme_text_color"] = nightshade_theme_list[4]
            file_theme_data["Theme"][0]["theme_frame_color"] = nightshade_theme_list[5]
            messagebox.showinfo(title = "Theme set", message = "In order to change theme you will have to restart the program \n NOTE: All the current indexes will be reset to 1!")
        elif theme_name == "CottonCandy":
            file_theme_data["Theme"][0]["theme_name"] = cottoncandy_theme_list[0]
            file_theme_data["Theme"][0]["theme_fg"] = cottoncandy_theme_list[1]
            file_theme_data["Theme"][0]["theme_font"] = cottoncandy_theme_list[2]
            file_theme_data["Theme"][0]["theme_font_size"] = cottoncandy_theme_list[3]
            file_theme_data["Theme"][0]["theme_text_color"] = cottoncandy_theme_list[4]
            file_theme_data["Theme"][0]["theme_frame_color"] = cottoncandy_theme_list[5]
            messagebox.showinfo(title = "Theme set", message = "In order to change theme you will have to restart the program \n NOTE: All the current indexes will be reset to 1!")
        else:
            print("no theme set")
    with open('conf.json', 'w') as file_theme_to_write:
        json.dump(file_theme_data, file_theme_to_write, indent=4)

##Define the settings page
def settings_page():
    settings_frame = customtkinter.CTkFrame(
        main_frame,
        fg_color=theme_dict["theme_frame_color"]
    )
    settings_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    settings_frame.pack_propagate(FALSE)
    settings_frame.grid_columnconfigure(0, weight=1)
    settings_frame.grid_columnconfigure(4, weight=1)
    settings_frame.grid_rowconfigure(1, weight=1)
    settings_frame.grid_rowconfigure(3, weight=1)


    ####Frame Widgets#####
    settings_label = customtkinter.CTkLabel(settings_frame, text="Here you can configure the theme to use \n just choose it from the dropdown menu and hit the button Set", font=(theme_dict["theme_font"], theme_dict["theme_font_size"]), text_color = theme_dict["theme_text_color"])
    combobox_label = customtkinter.CTkLabel(settings_frame, text="Choose a theme:", font=(theme_dict["theme_font"], theme_dict["theme_font_size"]), text_color = theme_dict["theme_text_color"])
    theme_combobox = customtkinter.CTkComboBox(settings_frame, values=["System","Spooky","Noel","Nightshade","CottonCandy"])
    theme_btn = customtkinter.CTkButton(settings_frame, text="Set", command = lambda: setup_theme(theme_combobox.get()), fg_color=theme_dict["theme_fg"], text_color = theme_dict["theme_text_color"], font = (theme_dict["theme_font"], theme_dict["theme_font_size"]))
    
    ####Position in the frame######
    settings_label.grid(row=0, column=1, columnspan =3, pady = 20)
    combobox_label.grid(row=2, column=1, columnspan=1)
    theme_combobox.grid(row=2,column=2, columnspan=1)
    theme_btn.grid(row=2, column=3, columnspan=1)


def open_url(url_):
    webbrowser.open_new(url_)

##Define the more page
def more_page():
    more_frame = customtkinter.CTkFrame(
        main_frame, 
        fg_color=theme_dict["theme_frame_color"]
    )
    more_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    more_frame.pack_propagate(FALSE)
    more_frame.grid_rowconfigure(12, weight = 1)
    more_frame.grid_columnconfigure(0, weight = 1)
    more_frame.grid_columnconfigure(3, weight = 1)
    

    ####Frame Widgets#####
    main_more_label = customtkinter.CTkLabel(
        more_frame,
        text="Here you can find a small description of the program, in case you missed the starting page \n",
        text_color = theme_dict["theme_text_color"],
        font = ("Times New Roman", theme_dict["theme_font_size"])
    )
    more_label_2 = customtkinter.CTkLabel(more_frame, text = "1. Head to the 'Subjects' page \n",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    more_label_3 = customtkinter.CTkLabel(more_frame, text = "2. Press the button 'Add New'\n",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    more_label_4 = customtkinter.CTkLabel(more_frame, text = "3. Insert the subject's name or the acronym\n",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    more_label_5 = customtkinter.CTkLabel(more_frame, text = "4. Choose the question and the answer file\n",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    more_label_6 = customtkinter.CTkLabel(more_frame, text = "5. Now head to the 'Q&A' page and start your study session\n",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    more_label_7 = customtkinter.CTkLabel(more_frame, text = "Finally, in the 'Subjects' page you can delete the subjects you don't need anymore\n",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    more_label_8 = customtkinter.CTkLabel(more_frame, text = "You can find more info on the webpage:\n",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    more_label_9 = customtkinter.CTkLabel(more_frame, text = "I personally thank you for downloading and using A.R.E.T \n Good luck in your study",text_color = theme_dict["theme_text_color"],font = ("Times New Roman", theme_dict["theme_font_size"]))
    
    
    website_url = customtkinter.CTkButton(
        more_frame,
        text = "https://mattebasta.github.io/ARET-WebPage/",
        fg_color = theme_dict["theme_fg"],
        text_color = theme_dict["theme_text_color"],
        font=('Times New Roman', 24),
        command = lambda : open_url("https://mattebasta.github.io/ARET-WebPage/"))
    
    ####Position in the frame######
    main_more_label.grid(row = 1, column = 1, columnspan = 2, pady = (40, 0))
    more_label_2.grid(row = 2, column = 1, columnspan = 2)
    more_label_3.grid(row = 3, column = 1, columnspan = 2)
    more_label_4.grid(row = 4, column = 1, columnspan = 2)
    more_label_5.grid(row = 5, column = 1, columnspan = 2)
    more_label_6.grid(row = 6, column = 1, columnspan = 2, pady = (0, 20))
    more_label_7.grid(row = 7, column = 1, columnspan = 2)
    more_label_8.grid(row = 8, column = 1, pady = (10,0))
    website_url.grid(row = 8, column = 2, pady=(0,10)), 
    more_label_9.grid(row = 9, column = 1, columnspan = 2)


##Advice: if you want to update a label....call the method place() or pack() in a new line, otherwise it will generate a NONE error................WTF?!!!!

# Widgets and configuration of the sidebar
sidebar = customtkinter.CTkFrame(root, border_width=1, border_color="black", fg_color = theme_dict["theme_fg"])
sidebar.pack(side=LEFT, fill=Y, ipadx = 5)
sidebar.pack_propagate(FALSE)

sidebar.rowconfigure(0, weight=1)
sidebar.rowconfigure(5, weight=1)

# Sidebar Labels
qa_Label = Label(root, text="", bg="#3d1f82")
subjects_folder_Label = Label(root, text="", bg="#3d1f82")
settings_Label = Label(root, text="", bg="#3d1f82")
more_Label = Label(root, text="", bg="#3d1f82")



working_dir = pathlib.Path(__file__).parent.resolve()

qa_icon_name = 'Icon\\qa.png'
qa_icon_path = os.path.join(working_dir, qa_icon_name)
qa_icon_img = PhotoImage(file= qa_icon_path)

subject_icon_name = 'Icon\\folder.png'
subject_icon_path = os.path.join(working_dir, subject_icon_name)
subject_icon_img = PhotoImage(file = subject_icon_path)      

settings_icon_name = 'Icon\\setting.png'
settings_icon_path = os.path.join(working_dir, settings_icon_name)
settings_icon_img = PhotoImage(file = settings_icon_path)

more_icon_name = 'Icon\\more.png'
more_icon_path = os.path.join(working_dir, more_icon_name)
more_icon_img = PhotoImage(file = more_icon_path)


# Sidebar Buttons
qa_btn = customtkinter.CTkButton(
    sidebar,
    text="Q&A",
    text_color = theme_dict["theme_text_color"],
    fg_color = theme_dict["theme_fg"],
    font = (theme_dict["theme_font"], 20),
    image = qa_icon_img,
    command=lambda: [current_page(qa_Label), qa_page()],
)

subjects_folder_button = customtkinter.CTkButton(
    sidebar,
    text="SUBJECTS",
    text_color = theme_dict["theme_text_color"],
    fg_color = theme_dict["theme_fg"],
    font = (theme_dict["theme_font"], 20),
    image = subject_icon_img,
    command=lambda: [current_page(subjects_folder_Label), subjects_page()],
)

settings_btn = customtkinter.CTkButton(
    sidebar,
    text="SETTINGS",
    text_color = theme_dict["theme_text_color"],
    fg_color = theme_dict["theme_fg"],
    font = (theme_dict["theme_font"], 20),
    image = settings_icon_img,
    command=lambda: [current_page(settings_Label), settings_page()],
)

more_btn = customtkinter.CTkButton(
    sidebar,
    text="MORE",
    text_color = theme_dict["theme_text_color"],
    fg_color = theme_dict["theme_fg"],
    font = (theme_dict["theme_font"], 20),
    image = more_icon_img,
    command=lambda: [current_page(more_Label), more_page()],
)


# Sidebar Buttons Positioning
qa_btn.grid(column=0, row=1, pady=20, padx = (10,0))
subjects_folder_button.grid(column=0, row=2, pady=20, padx = (10,0))
settings_btn.grid(column=0, row=3, pady=20, padx = (10,0))
more_btn.grid(column=0, row=4, pady=20, padx = (10,0))


# all the widgets and other setting must be written before mainloop()
root.mainloop()
