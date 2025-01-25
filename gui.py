import tkinter as tk
import tkinter.ttk as ttk
import database
import random
from tkinter import messagebox

#database.add_word(mot,lang,t,genre=None,pl=None)
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

def new_word_gui():
    # A global dictionary to store the data
    data_dict = {}

    # Create the new word GUI window
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

    # Create Word button
    create_btn = tk.Button(new_word_window, text="Create Word", command=handle_new_word)
    create_btn.pack(pady=10)

    #-----------------------------------------------------------------------------------------------------------------


    global meanings
    meanings=["helloworld","mc"]

    def manage_meanings():
        items = {}
        meanings_manager_window=tk.Toplevel()
        meanings_manager_window.title("Meanings Manager")
        meanings_manager_window.geometry("300x200")

        for x in meanings:
            items[x] = []
            items[x].append(tk.Frame(meanings_manager_window))
            f = items[x][0]
            items[x].append(tk.Label(f, text=x))
            # Create a button that passes the label's text to `selected`
            #items[x].append(tk.Button(f, text="Select", command=lambda text=x: selected(text)))
            items[x][1].grid(column=0, row=0)
            #items[x][2].grid(column=1, row=0)
            f.pack()

        add_existant_meaning=tk.Button(meanings_manager_window, text="Add Meaning From list of existant meanings")


    managemeaningsbtn=tk.Button(new_word_window, text="Manage Meanings",command=manage_meanings)

    managemeaningsbtn.pack(pady=10)



def create_gui():
    global root
    root = tk.Tk()
    root.title("Dictionarry")
    root.geometry("400x400")

    b_addw=tk.Button(root, text="Add a new word",command=new_word_gui)
    b_addm=tk.Button(root, text="Add a new meaning")
    b_ls=tk.Button(root, text="Link synonyms")
    b_la=tk.Button(root, text="Link antonyms")
    b_exp=tk.Button(root, text="Explore dictionary")
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
