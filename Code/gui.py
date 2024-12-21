from tkinter import *
import tkinter as tk
from tkinter import font as tkFont 
import time
from gtts import gTTS
from playsound import playsound
import tkinter.messagebox
from w2v_chatbot import W2VChatBot
from rasa_chatbot import Rasa_Bot
import threading
import os
os.chdir('../Dataset/')
# saved_username = ["KKWBOT"]
# ans=["KKWBOT"]
window_size = "500x500"


class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.bot_name = 'PHAKEBOT'
        #Read Data

        # Defaut data/model path
        self.w2v_model_path = 'baomoi.model.bin'
        self.rasa_model_normal_path = 'Normal_bot_model.gz'
        self.rasa_model_tsun_path = 'Tsun_bot_model.gz'
        self.w2v_answer_normal_path = 'Normal_bot.json'
        self.w2v_answer_tsun_path = 'Tsundere_bot.json'
        self.w2v_npy_normal_path = 'w2v_normal_bot.npy'
        self.w2v_npy_tsun_path = 'w2v_tsun_bot.npy'

        # Import Model
        self.is_w2v = True
        self.is_normal_persona = True

        # Init bots
        self.w2v_bot = W2VChatBot()
        self.w2v_bot.load_model()
        self.w2v_bot.load_answer(self.w2v_answer_normal_path)
        self.w2v_bot.load_data_from_npy(self.w2v_npy_normal_path)

        self.rasa_bot_normal = Rasa_Bot(self.rasa_model_normal_path)
        self.rasa_bot_tsun = Rasa_Bot(self.rasa_model_tsun_path)

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
        self.personality_var = tk.StringVar(value="Normal")  # Default personality
        personality = Menu(options, tearoff=0)
        options.add_cascade(label="Personality", menu=personality)
        personality.add_radiobutton(label='Normal', variable=self.personality_var, value='Normal', command=self.personality_change_normal)
        personality.add_radiobutton(label='Tsundere', variable=self.personality_var, value='Tsundere', command=self.personality_change_tsun)

        # features
        features = Menu(options, tearoff=0)
        options.add_cascade(label="Features", menu=features)
        features.add_command(label="Change bot name", command=self.name_change)

        # models
        self.model_var = tk.StringVar(value="W2V")  # Default model
        model = Menu(options, tearoff=0)
        options.add_cascade(label="Model", menu=model)
        model.add_radiobutton(label="W2V", variable=self.model_var, value="W2V", command=lambda: self.model_change(True))
        model.add_radiobutton(label="RASA", variable=self.model_var, value="RASA", command=lambda: self.model_change(False))

        # font
        self.font_var = tk.StringVar(value="Default")  # Default font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_radiobutton(label="Default", variable=self.font_var, value="Default", command=self.font_change_default)
        font.add_radiobutton(label="Times", variable=self.font_var, value="Times", command=self.font_change_times)
        font.add_radiobutton(label="System", variable=self.font_var, value="System", command=self.font_change_system)
        font.add_radiobutton(label="Helvetica", variable=self.font_var, value="Helvetica", command=self.font_change_helvetica)
        font.add_radiobutton(label="Fixedsys", variable=self.font_var, value="Fixedsys", command=self.font_change_fixedsys)

        # color theme
        self.color_theme_var = tk.StringVar(value="Default")  # Default color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_radiobutton(label="Default", variable=self.color_theme_var, value="Default", command=self.color_theme_default)
        color_theme.add_radiobutton(label="Grey", variable=self.color_theme_var, value="Grey", command=self.color_theme_grey)
        color_theme.add_radiobutton(label="Blue", variable=self.color_theme_var, value="Blue", command=self.color_theme_dark_blue)
        color_theme.add_radiobutton(label="Torque", variable=self.color_theme_var, value="Torque", command=self.color_theme_turquoise)
        color_theme.add_radiobutton(label="Hacker", variable=self.color_theme_var, value="Hacker", command=self.color_theme_hacker)

        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="About AI Girlfriend Chatbot", command=self.msg)
        help_option.add_command(label="Developers", command=self.about)

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
        self.text_box.tag_configure('center', justify=CENTER)
        self.text_box.tag_configure("human_style", font=("Helvetica", 12, "bold"), foreground="dodger blue")
        self.text_box.tag_configure("bot_style", font=("Helvetica", 12, "bold"), foreground="deep pink")

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
        self.text_box.insert(END, "< Chào mừng đến với bạn gái ảo PHAKEBOT >\n", 'center')
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)

        self.last_sent_label(date="No messages sent.")
        #t2 = threading.Thread(target=self.send_message_insert(name='t1'))
        #t2.start()
        self.default_format()

    def playResponce(self, responce):
        print(responce)
        try:
            # Create the audio file
            tts = gTTS(text=responce, lang='vi')
            filename = "responce_audio.mp3"
            tts.save(filename)

            # Play the audio file
            playsound(filename)
            print("Played Successfully......")
            # Delete the audio file
            os.remove(filename)

        except Exception as e:
            print(f"An error occurred: {e}")

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
        tkinter.messagebox.showinfo("PHAKEBOT v1.0",
                                    'PHAKEBOT is a girlfriend chatbot for answering questions and communication\nIt is based on retrival-based NLP using Rasa framework, word2vex, underthesea libary\nGUI is based on Tkinter')

    def about(self):
        tkinter.messagebox.showinfo("AI GirlFriend PHAKEBOT Developers","Students in HUS, VNU \nNguyễn Đức Nhật - 21001573 \nNguyễn Minh Trí - 21000401")

    def send_message_insert(self, message):
        user_input = self.entry_field.get()
        human = "Human "
        pr1 = f': {user_input}\n'
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, human, "human_style")
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
            answer = self.w2v_bot.response(user_input)[1]
        else:
            if self.is_normal_persona:
                answer = self.rasa_bot_normal.response(user_input)
            else:
                answer = self.rasa_bot_tsun.response(user_input)
        

        # Show chat messages
        entity = self.bot_name
        pr = f' : {answer}\n'

        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, entity, "bot_style")
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
        if self.is_w2v:
            self.w2v_bot.load_answer(self.w2v_answer_tsun_path)
            self.w2v_bot.load_data_from_npy(self.w2v_npy_tsun_path)

        # Update personality state
        self.is_normal_persona = False
        tkinter.messagebox.showinfo("Personality","Changed to Tsundere Girlfriend")
    
    def personality_change_normal(self):
        if self.is_w2v:
            self.w2v_bot.load_answer(self.w2v_answer_normal_path)
            self.w2v_bot.load_data_from_npy(self.w2v_npy_normal_path)
        self.is_normal_persona = True
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
        # self.emoji_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
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
        # self.emoji_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
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
        # self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
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
        # self.emoji_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
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
        # self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
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
        # self.emoji_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
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
    root.title("AI Girlfriend Chatbot: PHAKEBOT")
    root.iconbitmap('chatbot.ico')
    root.mainloop()
