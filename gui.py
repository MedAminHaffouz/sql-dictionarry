import tkinter as tk
import tkinter.ttk as ttk
import database
import random
from tkinter import messagebox

#database.add_word(mot,lang,t,genre,pl)
#it will add a new word

#database.add_meaning(lang,txt)
#it will add a new meaning

#database.getword(mot,lang,t)
#backend fct that returns the id of that word

#database.getmeaning(lang,txt)
#backend fct that returns the id of that meaning

#database.link_wm(langw,word,t,langm,txt)
#it will link a certain word to a certain meaning

#database.link_s(l1,l2,t,w1,w2)
#it will link 2 words =

#database.link_a(l1,l2, t, w1, w2)
#it will link 2 !=

#database.searchword(w)
#it will give all existant words

#database.showall(letter)
#it will return all the letters of that word

#database.getallmeanings()
#returns all existant meanings

#database.getallwords()
#returns all existant words

def randomcolorcode():
    return "#" + "".join(random.choices("0123456789abcdef", k=6))


def lighten_color(hex_color, factor=1.2):
    """
    Lightens a given hex color by a specific factor.

    Args:
        hex_color (str): The color in hex format (e.g., "#RRGGBB").
        factor (float): The factor by which to lighten the color (default is 1.2, or 20% lighter).

    Returns:
        str: The lighter color in hex format.
    """
    # Ensure the hex_color starts with "#"
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    # Extract RGB components
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    # Lighten each component
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))

    # Convert back to hex
    lighter_color = f"#{r:02X}{g:02X}{b:02X}"

    return lighter_color

def save_word():
    to_delete=[]
    global data_dict
    for word,elements in data_dict.items():
        database.add_word(word,elements["language"],elements["type"],elements["gender"],elements["plurality"])
        for meaning in meanings:
            database.add_meaning(meaning[1],meaning[0])
            database.link_wm(elements["language"],word,elements["type"],meaning[1],meaning[0])
        to_delete.append(word)

    for word in to_delete:
        del data_dict[word]


def new_word_gui():
    # A global dictionary to store the data
    global data_dict
    data_dict = {}

    # Create the new word GUI window
    global new_word_window
    new_word_window = tk.Toplevel()
    new_word_window.title("New Word")
    new_word_window.geometry("400x300")
    color = randomcolorcode()
    light_color = lighten_color(color)
    new_word_window.configure(background=color)

    # Info frame for input fields
    infoframe = tk.Frame(new_word_window, bg=light_color)
    wordlab = tk.Label(infoframe, text="Word:")
    wordent = tk.Entry(infoframe)
    langlab = tk.Label(infoframe, text="Language:")
    langent = tk.Entry(infoframe)
    typelab = tk.Label(infoframe, text="Type:")

    selected_option = tk.StringVar(value="Unspecified")
    options = ["Unspecified", "Verb", "Noun", "Adjective", "Others"]
    dropdown = tk.OptionMenu(infoframe, selected_option, *options)

    # Layout the input fields
    wordlab.grid(row=0, column=0, padx=5, pady=5)
    wordent.grid(row=0, column=1, padx=5, pady=5)
    langlab.grid(row=1, column=0, padx=5, pady=5)
    langent.grid(row=1, column=1, padx=5, pady=5)
    typelab.grid(row=2, column=0, padx=5, pady=5)
    dropdown.grid(row=2, column=1, padx=5, pady=5)
    infoframe.pack(pady=10)

    def handle_new_word():
        word = wordent.get().strip()
        language = langent.get().strip()
        word_type = selected_option.get()

        # Validate input
        if not word or not language:
            tk.messagebox.showerror("Error", "Please enter both the word and the language.")
            return

        # Initialize the dictionary with default values
        data_dict[word] = {
            "word": word,
            "language": language,
            "type": word_type,
            "gender": None,  # Default None unless it's a noun
            "plurality": None  # Default None unless it's a noun
        }

        # Handle "Noun" type
        if word_type == "Noun":
            def save_noun_details():
                gender = lentg.get().strip().lower()
                plurality = lentp.get().strip().lower()

                if gender in ["m", "f", "none"] and plurality in ["s", "p", "none"]:
                    data_dict[word]["gender"] = gender if gender != "none" else None
                    data_dict[word]["plurality"] = plurality if plurality != "none" else None
                    save_word()  # Call save_word after saving noun details
                    type_set_window.destroy()
                else:
                    tk.messagebox.showerror(
                        "Error", "Please enter valid values (Gender: m/f/none, Plurality: s/p/none)."
                    )

            # Create a new window for noun details
            type_set_window = tk.Toplevel()
            type_set_window.title("Noun Details")
            type_set_window.geometry("300x200")

            gendlab = tk.Label(type_set_window, text="Gender (m/f/none):")
            lentg = tk.Entry(type_set_window)
            plurlab = tk.Label(type_set_window, text="Plurality (s/p/none):")
            lentp = tk.Entry(type_set_window)
            save_btn = tk.Button(type_set_window, text="Save", command=save_noun_details)

            # Layout the noun details fields
            gendlab.grid(row=0, column=0, padx=5, pady=5)
            lentg.grid(row=0, column=1, padx=5, pady=5)
            plurlab.grid(row=1, column=0, padx=5, pady=5)
            lentp.grid(row=1, column=1, padx=5, pady=5)
            save_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Handle "Others" type
        elif word_type == "Others":
            def save_custom_type():
                custom_type = lent.get().strip()
                if custom_type:
                    data_dict[word]["type"] = custom_type
                    save_word()  # Call save_word after saving custom type
                    type_set_window.destroy()
                else:
                    tk.messagebox.showerror("Error", "Please enter a valid custom type.")

            # Create a new window for custom type
            type_set_window = tk.Toplevel()
            type_set_window.title("Custom Type")
            type_set_window.geometry("300x200")

            labeltitle = tk.Label(type_set_window, text="For 'Others', please specify the type:")
            label = tk.Label(type_set_window, text="Type:")
            lent = tk.Entry(type_set_window)
            validb = tk.Button(type_set_window, text="OK", command=save_custom_type)

            # Layout the custom type fields
            labeltitle.pack(pady=5)
            label.pack(pady=5)
            lent.pack(pady=5)
            validb.pack(pady=5)

        else:
            # For all other types, just save directly
            tk.messagebox.showinfo("Success", f"Word '{word}' added successfully!")
            save_word()  # Call save_word for other types

    # Create Word button
    create_btn = tk.Button(new_word_window, text="Create Word", command=handle_new_word)


    #-----------------------------------------------------------------------------------------------------------------


    global meanings
    meanings=[]

    global showed
    showed = False
    global items_ex
    items_ex = {}
    choosen_m = []  # To store the selected meaning

    def selected(text, lang):
        """
        Function called when a meaning is selected.
        Stores the selected text and language in choosen_m.
        """
        global showed, items_ex, choosen_m
        choosen_m = [text, lang]  # Store the selected language and text
        print(f"Selected: Text='{text}', Language='{lang}'")  # Print the selected meaning
        child_window.destroy()
        print(choosen_m)
        meanings_manager_window.destroy()
        meanings.append(choosen_m)
        manage_meanings()
        showed=False



    def select_meaning_from_existants():
        global child_window
        child_window = tk.Toplevel()
        child_window.title('get meaning from existant meanings')
        child_window.geometry("300x200")

        arr=[]
        arr=[["Hello", "English"], ["Bonjour", "French"], ["Hola", "Spanish"]]
        #arr=database.getallmeanings()

        filtered_arr = [meaning for meaning in arr if meaning not in meanings]

        global showed, items_ex
        if not showed:
            for idx, (text, lang) in enumerate(filtered_arr):

                items_ex[idx] = []
                items_ex[idx].append(tk.Frame(child_window))  # Create a frame for the row
                f = items_ex[idx][0]

                # Create labels for text and language
                items_ex[idx].append(tk.Label(f, text=f"Text: {text}"))
                items_ex[idx].append(tk.Label(f, text=f"Language: {lang}"))

                # Create the "Select" button, passing text and lang to `selected`
                items_ex[idx].append(
                    tk.Button(f, text="Select", command=lambda t=text, l=lang: selected(t, l))
                )

                # Arrange the widgets in the row
                items_ex[idx][1].grid(column=0, row=0, padx=5, pady=5)  # Text label
                items_ex[idx][2].grid(column=1, row=0, padx=5, pady=5)  # Language label
                items_ex[idx][3].grid(column=2, row=0, padx=5, pady=5)  # Select button

                # Display the frame
                f.pack(pady=5)
            showed = True


    def manage_meanings():
        items = {}
        global meanings_manager_window
        meanings_manager_window=tk.Toplevel()
        meanings_manager_window.title("Meanings Manager")
        meanings_manager_window.geometry("300x200")

        for idx, (text, lang) in enumerate(meanings):
            items[idx] = []
            items[idx].append(tk.Frame(meanings_manager_window))  # Create a frame for the row
            f = items[idx][0]

            # Create labels for text and language
            items[idx].append(tk.Label(f, text=f"Text: {text}"))
            items[idx].append(tk.Label(f, text=f"Language: {lang}"))


            # Arrange the widgets in the row
            items[idx][1].grid(column=0, row=0, padx=5, pady=5)  # Text label
            items[idx][2].grid(column=1, row=0, padx=5, pady=5)  # Language label

            # Display the frame
            f.pack(pady=5)

        add_existant_meaning=tk.Button(meanings_manager_window, text="Add Meaning From list of existant meanings",command=select_meaning_from_existants)
        add_existant_meaning.pack(pady=10)


    managemeaningsbtn=tk.Button(new_word_window, text="Manage Meanings",command=manage_meanings)

    managemeaningsbtn.pack(pady=5)
    create_btn.pack(pady=5)

def expand_word(word,typeword,lang):
    res=database.showword(word,lang,typeword)
    print(res)
    res=list(res[0])
    print(res)
    child_window=tk.Toplevel()
    child_window.title(f"{word}({lang})")
    child_window.geometry("300x200")

    label=tk.Label(child_window, text="")
    output=""
    output+=res[0]+" ("+res[2]+")"
    if res[3]!=None:
        output+=" "+res[3]+" "
    if res[4]!=None:
        output+=" "+res[4]+" "
    output+="\nlanguage :"+res[1]+"\n"
    if res[5]!=None:
        output+="Meanings :"+res[5]+"\n"
    if res[6]!=None:
        output += "Synonyms :" + res[5] + "\n"
    if res[7]!=None:
        output += "Antonyms :" + res[5] + "\n"
    label.configure(text=output)
    label.pack(pady=5)


def show_dictio():
    show_dictio=tk.Toplevel()
    show_dictio.title("Dictionary Explorer")
    show_dictio.geometry("500x500")

    words=[]
    words=database.getallwords()
    for word in words:
        items=[]
        items.append(tk.Frame(show_dictio))
        f=items[0]
        items.append(tk.Label(f, text="["+word[1]+"]"))
        items.append(tk.Label(f, text=word[0]))
        items.append(tk.Label(f, text="("+word[2]+")"))
        items.append(tk.Button(f, text="Show More >",command=lambda w=word[0],l=word[1],t=word[2]: expand_word(w,t,l)))
        items[1].grid(row=0, column=0, padx=5, pady=5)
        items[2].grid(row=0, column=1, padx=5, pady=5)
        items[3].grid(row=0,column=2, padx=5, pady=5)
        items[4].grid(row=0,column=3, padx=5, pady=5)
        f.pack(pady=5)

def new_meaning_gui():
    new_meaning_window=tk.Toplevel()
    new_meaning_window.title("New Meaning")
    new_meaning_window.geometry("500x500")
    color = randomcolorcode()
    light_color = lighten_color(color)
    new_meaning_window.configure(background=color)

    def create_meaning():
        lang=langent.get()
        txt=textentry.get()
        database.add_meaning(lang, txt)
        tk.messagebox.showinfo("Success", "meaning added successfully!")
        new_meaning_window.destroy()

    langlab=tk.Label(new_meaning_window, text="Language :")
    langent=tk.Entry(new_meaning_window)
    textlab=tk.Label(new_meaning_window, text="Text :")
    textentry=tk.Entry(new_meaning_window)
    validbutton=tk.Button(new_meaning_window,text="Add Meaning to the list",command=create_meaning)

    langlab.grid(row=0, column=0, padx=5, pady=5)
    langent.grid(row=0, column=1, padx=5, pady=5)
    textlab.grid(row=1, column=0, padx=5, pady=5)
    textentry.grid(row=1, column=1, padx=5, pady=5)
    validbutton.grid(row=2, column=0, padx=5, pady=5,columnspan=2)


def create_gui():
    global root
    root = tk.Tk()
    root.title("Dictionarry")
    root.geometry("400x400")

    b_addw=tk.Button(root, text="Add a new word",command=new_word_gui)
    b_addm=tk.Button(root, text="Add a new meaning",command=new_meaning_gui)
    b_ls=tk.Button(root, text="Link synonyms")
    b_la=tk.Button(root, text="Link antonyms")
    b_exp=tk.Button(root, text="Explore dictionary",command=show_dictio)
    b_outcsv=tk.Button(root, text="Export to CSV",bg="red",fg="white")
    b_incsv=tk.Button(root, text="Import CSV",bg="red",fg="white")

    b_addw.pack(pady=5,padx=30)
    b_addm.pack(pady=5,padx=30)
    b_ls.pack(pady=5,padx=30)
    b_la.pack(pady=5,padx=30)
    b_exp.pack(pady=5,padx=30)
    b_outcsv.pack(pady=5,padx=30)
    b_incsv.pack(pady=5,padx=30)

    menu_bar = tk.Menu(root)

    tools_menu = tk.Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label="Explore dictionary")
    tools_menu.add_command(label="Export to CSV")
    tools_menu.add_command(label="Import from CSV")
    menu_bar.add_cascade(label="Tools", menu=tools_menu)

    menu_bar.add_command(label="Settings")

    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    help_menu.add_command(label="About Us")
    menu_bar.add_cascade(label="Help", menu=help_menu)

    menu_bar.add_command(label="Exit",command=root.quit)

    root.config(menu=menu_bar)

    root.mainloop()

create_gui()
