from tkinter import *
import tkinter as tk
from tkinter import font as tkFont 
import time
import pyttsx3
import tkinter.messagebox
from w2v_chatbot import W2VChatBot
from rasa_chatbot import Rasa_Bot
import threading
import pandas as pd
import os
os.chdir('../Dataset/')
saved_username = ["KKWBOT"]
ans=["KKWBOT"]
window_size = "500x500"


class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.bot_name = 'AI Girlfriend'
        #Read Data

        # Defaut data/model path
        self.w2v_model_path = 'baomoi.model.bin'
        self.rasa_model_normal = 'bot_1.tar.gz'
        self.rasa_model_tsun_path = 'Tsun_bot_model.gz'
        self.w2v_answer_normal_path = 'json_normal_bot.json'
        self.w2v_answer_tsun_path = 'Tsundere_bot.json'
        self.w2v_npy_normal_path = 'dataset_vectors.npy'
        self.w2v_npy_tsun_path = 'tsun_bot.npy'

        # Import Model
        self.is_w2v = True


        # Init bots
        self.w2v_bot = W2VChatBot()
        self.w2v_bot.load_model()
        self.w2v_bot.load_answer(self.w2v_answer_normal_path)
        self.w2v_bot.load_data_from_npy(self.w2v_npy_normal_path)
        # self.rasa_bot = Rasa_Bot()

        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 11"

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
        # Menu bar

        # File
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        # file.add_command(label="Save Chat Log", command=self.save_chat)
        file.add_command(label="Clear Chat", command=self.clear_chat)
        #  file.add_separator()
        file.add_command(label="Import data", command=None)
        file.add_command(label="Exit", command=self.chatexit)
        
        
        # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)


        #personarity 
        personality = Menu(options, tearoff=0)
        options.add_cascade(label="Personality", menu=personality)
        personality.add_command(label='Normal', command=self.personality_change_normal)
        personality.add_command(label='Tsundere', command=self.personality_change_tsun)

        # features
        features = Menu(options, tearoff=0)
        options.add_cascade(label="Features", menu=features)
        features.add_command(label="Change bot name", command=self.name_change)

        # models
        model = Menu(options, tearoff=0)
        options.add_cascade(label="Model", menu=model)
        model.add_command(label="W2V", command=lambda: self.model_change(True))
        model.add_command(label="RASA", command=lambda: self.model_change(False))

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default", command=self.font_change_default)
        font.add_command(label="Times", command=self.font_change_times)
        font.add_command(label="System", command=self.font_change_system)
        font.add_command(label="Helvetica", command=self.font_change_helvetica)
        font.add_command(label="Fixedsys", command=self.font_change_fixedsys)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=self.color_theme_default)
        color_theme.add_command(label="Grey", command=self.color_theme_grey)
        color_theme.add_command(label="Blue", command=self.color_theme_dark_blue)
        color_theme.add_command(label="Torque", command=self.color_theme_turquoise)
        color_theme.add_command(label="Hacker", command=self.color_theme_hacker)

        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="About KKWBOT", command=self.msg)
        help_option.add_command(label="Develpoers", command=self.about)

        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 14", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        # self.users_message = self.entry_field.get()

        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        # send button
        helv36 = tkFont.Font(family='Helvetica', size=12, weight='bold')
        self.send_button = Button(self.send_button_frame, text="Send", 
                                  width=6, relief=GROOVE, bg='#1F51FF', fg="white", activeforeground="#1F51FF", activebackground="white", font=helv36,
                                  bd=1, command=lambda: self.send_message_insert(None))
        self.send_button.pack(side=LEFT, ipady=5)
        self.master.bind("<Return>", self.send_message_insert)

        # Intro
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, " <--------- Chào mừng đến với bạn giái ảo phake -------->\n")
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)

        self.last_sent_label(date="No messages sent.")
        #t2 = threading.Thread(target=self.send_message_insert(name='t1'))
        #t2.start()
        self.default_format()

    def playResponce(self, responce):
        x = pyttsx3.init()
        voices = x.getProperty('voices')
        print(responce)
        x.setProperty('voice', voices[1].id)
        x.setProperty('rate', 190)
        # x.setProperty('volume', 100)
        x.say(responce)
        x.runAndWait()
        print("Played Successfully......")

    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 8", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        exit()

    def msg(self):
        tkinter.messagebox.showinfo("KKWBOT v1.0",
                                    'KKWBOT is a chatbot for answering question regranding to KKWagh college,Nashik\nIt is based on retrival-based NLP using pythons NLTK tool-kit module\nGUI is based on Tkinter')

    def about(self):
        tkinter.messagebox.showinfo("AI GirlFriend Phake Developers","Nguyễn Đức Nhật \n Vũ Văn Chí")

    def send_message_insert(self, message):
        user_input = self.entry_field.get()
        pr1 = "Human : " + user_input + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr1)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        #t1 = threading.Thread(target=self.playResponce, args=(user_input,))
        #t1.start()
        #time.sleep(1)

        # Start chatting
        # answer = 'Answer here'
        # answer = self.bot.response(user_input) # Run

        if self.is_w2v:
            answer = self.w2v_bot.response(user_input)
        else:
            answer = self.rasa_bot.response(user_input)

        # Show chat messages
        pr = f'{self.bot_name} : {answer}\n'
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        self.last_sent_label(str(time.strftime("Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.entry_field.delete(0, END)
        time.sleep(0)
        t2 = threading.Thread(target=self.playResponce, args=(answer,))
        t2.start()
        #return ob

    # ------  Model selection ------
    def model_change(self, is_w2v):
        self.is_w2v = is_w2v
        if is_w2v:
            tkinter.messagebox.showinfo("Model","Changed to W2V")
        else:
            tkinter.messagebox.showinfo("Model","Changed to Rasa")
    
    # ------  Personality selection ------
    def personality_change_tsun(self):
        # if self.is_w2v:
            self.w2v_bot.load_answer(self.w2v_answer_tsun_path)
            self.w2v_bot.load_data_from_npy(self.w2v_npy_tsun_path)
        # else:
            self.rasa_bot = Rasa_Bot(self.rasa_model_tsun_path)
            tkinter.messagebox.showinfo("Personality","Changed to Tsundere Girlfriend")
    
    def personality_change_normal(self):
        if self.is_w2v:
            self.w2v_bot.load_answer(self.w2v_answer_normal_path)
            self.w2v_bot.load_data_from_npy(self.w2v_npy_normal_path)
        else:
            self.rasa_bot = Rasa_Bot(self.rasa_model_normal_path)
        tkinter.messagebox.showinfo("Personality","Changed to Normal Girlfriend")
        
    
    def open_input_box(self):
        # Show an input box and get the user input
        user_input = tk.simpledialog.askstring("Input", "Enter your text:")
        if user_input:
            return user_input
        
    def name_change(self):
        self.bot_name = self.open_input_box()
        print(self.bot_name)

    def font_change_default(self):
        self.text_box.config(font="Verdana 11")
        self.entry_field.config(font="Verdana 11")
        self.font = "Verdana 11 bold"

    def font_change_times(self):
        self.text_box.config(font="Times 11")
        self.entry_field.config(font="Times 11")
        self.font = "Times 11"

    def font_change_system(self):
        self.text_box.config(font="System 11")
        self.entry_field.config(font="System 11")
        self.font = "System 11"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 11")
        self.entry_field.config(font="helvetica 11")
        self.font = "helvetica 11"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys 11")
        self.entry_field.config(font="fixedsys 11")
        self.font = "fixedsys 11"

    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#1F51FF", fg="white", activebackground="white", activeforeground="#1F51FF")
        # self.emoji_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    # Dark
    def color_theme_dark(self):
        self.master.config(bg="#2a2b2d")
        self.text_frame.config(bg="#2a2b2d")
        self.text_box.config(bg="#212121", fg="#FFFFFF")
        self.entry_frame.config(bg="#2a2b2d")
        self.entry_field.config(bg="#212121", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2a2b2d")
        self.send_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#2a2b2d", fg="#FFFFFF")

        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

    # Grey
    def color_theme_grey(self):
        self.master.config(bg="#444444")
        self.text_frame.config(bg="#444444")
        self.text_box.config(bg="#4f4f4f", fg="#ffffff")
        self.entry_frame.config(bg="#444444")
        self.entry_field.config(bg="#4f4f4f", fg="#ffffff", insertbackground="#ffffff")
        self.send_button_frame.config(bg="#444444")
        self.send_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.emoji_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.sent_label.config(bg="brown", fg="#ffffff")

        self.tl_bg = "#4f4f4f"
        self.tl_bg2 = "#444444"
        self.tl_fg = "#ffffff"

    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#003333")
        self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

        # Blue

    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

    # Torque
    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#003333")
        self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

    # Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="green", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")
        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()

if __name__ == "__main__":
    root = Tk()

    a = ChatInterface(root)
    root.geometry(window_size)
    root.title("AI Girlfriend Phake")
    root.iconbitmap('chatbot.ico')
    root.mainloop()
