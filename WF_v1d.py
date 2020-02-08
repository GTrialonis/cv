"""
NEW WORD FINDER          WF_V1b.py
"""

from tkinter import filedialog
from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import *
import requests
import os
from bs4 import BeautifulSoup


mstr = ''
lexis = ''
file_name = None


def doNothing():
    pass
# -----------------------------
def clr_defins():
    text_A.delete('1.0', END)
# ------------------------------
def append():
    global file_name
    input_file_name = filedialog.askopenfilename(initialdir='/', title='Select File',
    defaultextension='*.txt', filetypes=(('Text Files ', '*.txt'), ('All Files ', '*.*')))
    if input_file_name:
        file_name = input_file_name
        with open(file_name, 'a+', encoding='utf-8') as fl:
            conts = text_B.get('1.0', END)
            fl.write(conts+"\n")
                
# --------------- DICTIONARIES TO SEARCH ---------------------------- line 17
def src_glosbe():
    """
    searches glosbe dictionary
    """
    global mstr
    text_A.delete('1.0', END)
    lexis = fndWord.get() # the word is a string
    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://glosbe.com/de/en/"+lexis
    try:
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "lxml")
        art = soup.find('div', class_='defmetas').text
        if 'Gender: feminine' in art:
            art = 'die, '
        elif 'Gender: masculine' in art:
            art = 'der, '
        elif 'Gender: feminine' in art:
            art = 'die, '
        elif 'adjective' in art:
            art = 'adj., '
        elif 'conjunction' in art:
            art = 'conj., '
        elif 'Type: verb' in art:
            art = 'v., '
        elif 'adverb;' in art:
            art = 'adv.,'
        else:
            art = ', '

        text_A.insert(END, lexis+', '+art+' = ')

        for trans in soup.find_all('div', class_='text-info'):
            mstr = trans.find('strong', class_='phr').text
            mstr = mstr+', '
            
            text_A.insert(END, mstr)
            text_A.see('end')

    except AttributeError:
        text_A.insert(END, 'Word not found! Please check spelling or other dictionary.')
# ----------------------------------------------------------------------- 56

def de_el_search():
    global mstr
    text_A.delete('1.0', END)
    lexis = fndWord.get() # the word is a string
    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://el.glosbe.com/de/el/"+lexis
    
    try:
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "lxml")
        """ find article """
        artic = soup.find('div', class_='defmetas').text
        artic = artic.split(':')
        
        if 'masculine;' in artic[2]:
            gender = 'der'
        elif 'feminine;' in artic[2]:
            gender = 'die'
        elif 'neuter;' in artic[2]:
            gender = 'das'
        else:
            gender = ''
        text_A.insert(END, lexis+', '+gender+' = ')
        
        for trans in soup.find_all('div', class_='text-info'):
            mstr = trans.find('strong', class_="phr").text
            if mstr == '':
                text_A.insert(END, 'Η λέξη δεν είναι καταχωρημένη. Ψάξε άλλα λεξικά.')
            else:
                mstr = mstr+', '
                text_A.insert(END, mstr)
    except:
        text_A.insert(END, 'Word not found! Please check spelling.')
# ----------------------------------------------------------------------
def el_de_search():
    global mstr
    text_A.delete('1.0', END)
    lexis = fndWord.get() # the word is a string
    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://el.glosbe.com/el/de/"+lexis
    try:
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "lxml")

        lexis = lexis+' = ' # get out of the loop
        text_A.insert('1.0', lexis)
        
        # Below we find the meanings and save them in mystr
        for trans in soup.find_all('div', class_='text-info'):
            mstr = trans.find('strong', class_='phr').text
            article = trans.find('div', class_='gender-n-phrase').text

            if 'masculine' in article:
                gender = 'der'
            elif 'feminine' in article:
                gender = 'die'
            elif 'neuter' in article:
                gender = 'das'
            else:
                gender = ''

            mstr = gender+' '+mstr+', '
            text_A.insert(END, mstr)

    except (AttributeError, TypeError):
        text_A.insert(END, '--')
# ---------------------------------------------------------------------------
# ------------ GLOSBE EXAMPLE SENTENCES -------------------------------------
def glosbe_exampl_gr(): # ΕΛΛΗΝΙΚΑ ΠΑΡΑΔΕΙΓΜΑΤΑ
    lexis = fndWord.get() # the word I am looking for

    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://glosbe.com/de/el/"+lexis
    
    try:
        source = requests.get(url, headers=headers).text
        
        soup = BeautifulSoup(source, "lxml")

        for exmpl in soup.find_all('div', class_='row-fluid'):
            germ = exmpl.find('div', class_='span6').text
            gre = exmpl.find('div', lang='el').text
            example = '  '+germ+' = '+gre
            if len(germ) < 70 and not germ.startswith('de '):
                text_C.insert(END, example+'\n')
            else:
                pass
        if exmpl == None:
            text_C.insert(END, 'Examples not found here.'+'\n')
                                 
    except:
        text_C.insert(END, '--')

# -------------------------------------------------------------
def src_thefreedict():
    """
    searches the Free Dictionary
    """
    global mstr
    text_A.delete('1.0', END)
    lexis = fndWord.get() # the word is a string
    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://de.thefreedictionary.com/"+lexis
    try:
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "lxml")
        transl = soup.find('span', class_='trans').text # the translation

        art1 = soup.find('div', id='Definition')
        art2 = art1.i.text # this is the article (r, e, s)
        lexis = lexis+', '+art2+' = '+transl # added

        text_A.insert(END, lexis)
        text_A.insert(END, mstr)
        text_A.see('end')

    except AttributeError:
        text_A.insert(END, 'Word not found! Please check spelling or other dictionary.')

def langescheid(): # .... 80...
    """
    Searches the Langescheid
    """
    global mstr
    text_A.delete('1.0', END)
    der = 'Maskulinum | masculine m'
    die = 'Femininum | feminine f'
    das = 'Neutrum | neuter n'
    adj = 'Adjektiv | adjective adj'
    ajj = 'adjective | Adjektiv adj'
    adv = 'Adverb | adverb adv'
    trv = 'transitives Verb | transitive verb v/t <h>'
    trr = 'transitives Verb | transitive verb v/t <irregulär, unregelmäßig | \
            irregularirr,untrennbar | inseparable untrennb, kein -ge-; h>'
    inv = 'intransitives Verb | intransitive verb v/i <h>'
    ivn = 'intransitives Verb | intransitive verb v/i'
    tve = 'transitives Verb | transitive verb v/t <kein ge-; h>'
    irr = '<irregulär, unregelmäßig | irregularirr,trennbar | \
            separable trennb; -ge-; hund | and u. sein; h>'
    ttv = 'transitives Verb | transitive verb v/t <trennbar | separabletrennb; -ge-; h>'
    ttt = 'transitives Verb | transitive verb v/t <irregulär, unregelmäßig | \
            irregularirr,trennbar | separable trennb; -ge-; h>'
    wbs = ',,,Weitere Beispiele...'
    wuz = ',,,Weitere Übersetzungen...'
    lexis = fndWord.get() # the word is a string
    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://de.langenscheidt.com/deutsch-englisch/"+lexis

    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, "lxml")
        # ----- the code below is for the searched word ----
        summary = soup.find('div', class_='summary-inner').text
        words = summary.replace('Weitere Beispiele', '')
        words = words.replace('Weitere Übersetzungen', '')
        words = words.strip()
        mstr = words.replace('  ', ',')
        # ---- for the article / genitive / transitive, etc...
        article = soup.find('span', class_='dict-additions').text
        art_plu = article.strip()
        if art_plu.startswith(der):
            rpl = art_plu.replace(der, 'der')
        elif art_plu.startswith(die):
            rpl = art_plu.replace(die, 'die')
        elif art_plu.startswith(das):
            rpl = art_plu.replace(das, 'das')
        elif art_plu.startswith(adj):
            rpl = art_plu.replace(adj, 'adj.')
        elif art_plu.startswith(ajj):
            rpl = art_plu.replace(ajj, 'adj.')
        elif art_plu.startswith(adv):
            rpl = art_plu.replace(adv, 'adv.')
        elif art_plu.startswith(trv):
            rpl = art_plu.replace(trv, 't/v.')
        elif art_plu.startswith(inv):
            rpl = art_plu.replace(inv, 'i/v.')
        elif art_plu.startswith(tve):
            rpl = art_plu.replace(tve, 't/v <kein ge->')
        elif art_plu.startswith(trr):
            rpl = art_plu.replace(trr, 't/v,')
        elif art_plu.startswith(ivn):
            rpl = art_plu.replace(ivn, 'i/v')
        elif art_plu.startswith(irr):
            rpl = art_plu.replace(irr, 'i/v,')
        elif art_plu.startswith(ttv):
            rpl = art_plu.replace(ttv, 't/v,')
        elif art_plu.startswith(ttt):
            rpl = art_plu.replace(ttt, 't/v,')
        elif art_plu.startswith(wbs):
            rpl = art_plu.replace(wbs, '')
        elif wuz in art_plu:
            rpl = art_plu.replace(wuz, '')
        else:
            rpl = art_plu

        lexis = lexis+', '+rpl
        text_A.insert(END, lexis+' = ')
        text_A.insert(END, mstr)
        text_A.see("end") # cursor goes to the end of the last word added

    except AttributeError:
        text_A.insert(END, 'Word not found! Please check spelling or other dictionary.')

# -------------------- CREATE VOCABULARY FILE ---------------- 164
def create_vocfile():
    """
    Creates vocabulary file
    """
    global file_name
    
    input_file_name = filedialog.asksaveasfilename(initialdir="/",
    defaultextension='*.txt', filetypes=(("Text Documents", "*.txt"), ("all files", "*.*")))

    if input_file_name:
        file_name = input_file_name.rsplit('.', 1)[0]+'-VOC.txt'
        with open(file_name, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text_B.get('1.0', END))
    name_voc() # the name of the dictionary (file) you just created

# ------------------------------------
def caution():
    doNothing()

def name_voc():
    """
    prints the name to the vocabulary file on the GUI
    """
    global voc_name
    if file_name is None:
        voc_name = '-VOC file: '
        lbl4 = Label(mdle2, text=voc_name, bg='#F0E68C')
        lbl4.grid(row=7, columnspan=2, padx=10, sticky=W)
        
    else:
        voc_name = '-VOC file: '+file_name
        lbl4 = Label(mdle2, text=voc_name, bg='#F0E68C')
        lbl4.grid(row=7, columnspan=2, padx=10, sticky=W)


def open_file():
    """
    open the vocabulary file you created (text_B area)
    """
    global file_name, voc_name, contvoc
    if file_name is not None and len(text_B.get("1.0", END)) == '\n': # yes file name and box not empty
        text_B.insert(END, 'no file name and box not empty')
        save(file_name)
    else:
        input_file_name = filedialog.askopenfilename(initialdir='/', title='Select File',
    defaultextension='*.txt', filetypes=(('Text Files ', '*.txt'), ('All Files ', '*.*')))
        if input_file_name:
            
            file_name = input_file_name
            if "-VOC" in file_name:
                text_B.delete('1.0', END)
                with open(file_name, encoding='UTF-8') as file:
                    contvoc = file.readlines() # the study file, ref. as 'text' below
                    contvoc = ''.join(contvoc) # the study file, again
                    text_B.insert('1.0', contvoc) # opens file inside textArea1
                    text_B.tag_configure("left", justify="left")
                    voc_name = file_name
        name_voc() # the name of the dictionary (file) you just opened

def bring_down():
    contents = text_A.get('1.0', END)
    text_B.insert(END, contents)

def save(file_name):
    """
    save the individual words you scraped from the online dictionaries
    """
    if not file_name:
        create_vocfile()
    else:
        write_to_file(file_name)

def write_to_file(file_name):
    """
    write to file
    """
    try:
        content = text_A.get('1.0', END)
        text_B.insert(END, content)
        with open(file_name, 'a', encoding='utf-8') as the_file:
            the_file.write(content)
    except IOError:
        tkinter.messagebox.showwarning("Save", "Could not save the file")

def save_update(): # ----------------------------------------------------------------------------////
    """
    save/update the vocabulary file
    """
    try:
        if file_name == None:
            content = text_B.get('1.0', END)
            save(file_name)
        
        if os.stat(file_name).st_size == 0:
            save(file_name)
        else:
            # try:
            content = text_B.get('1.0', END)
            with open(file_name, 'w', encoding='utf-8') as the_file:
                the_file.write(content)
            # except TypeError:
                # doNothing()
    except (TypeError, FileNotFoundError):
        text_B.insert(END, 'There is nothing to save.')
# -----------------------------

# -----------------------------
def clear_file():
    """
    clear file
    """
    global voc_name, file_name
    text_B.delete('1.0', END)
    file_name = ''
    voc_name = ''
    lbl4 = Label(mdle2, text=' '*144, bg='#F0E68C')
    lbl4.grid(row=7, columnspan=2, sticky=N)
    name_voc()

# -------------------------------------------------------------- 
# ////////// SEARCH EXAMPLE-SENTENCES FROM WORDREFERENCE DICTIONARY ////////
def exam_wrdref():
    """
    search Word Reference Dictionary
    """
    lexis = fndWord.get() # the word I am looking for

    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "http://www.wordreference.com/deen/"+lexis

    try:
        source = requests.get(url, headers=headers).text

        soup = BeautifulSoup(source, "lxml")

        for exmpl in soup.find_all('div', class_='examplecontainer'):
            germ = exmpl.find('span', class_='example phrase ex').text
            eng = exmpl.find('span', class_='roman').text
            example = ' '+germ+' ='+eng
            text_C.insert(END, example+'\n')

    except AttributeError:
        text_C.insert(END, 'Examples not found.')

# ////////// SEARCH EXAMPLE-SENTENCES FROM the COLLINS DICTIONARY //////////////////////
def exam_collins():
    """
    search Collins Dictionary
    """

    lexis = fndWord.get() # the word I am looking for

    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://www.collinsdictionary.com/dictionary/german-english/"+lexis

    try:
        source = requests.get(url, headers=headers).text
        # source.encoding = 'utf-8'
        soup = BeautifulSoup(source, "html.parser")

        for exmpl in soup.find_all('div', class_='cit type-example'):
            germ = exmpl.find('span', class_='quote').text
            eng = exmpl.find('span', class_='cit type-translation').text
            example = '  '+germ+' = '+eng
            text_C.insert(END, example+'\n')

    except (AttributeError, UnicodeDecodeError) as e:
        text_C.insert(END, 'Examples not found.')
        
# ////////// SEARCH EXAMPLE-SENTENCES FROM the COLLINS DICTIONARY //////////////////////
def exam_glosbe():
    """
    search Glosbe Dictionary
    """

    lexis = fndWord.get()

    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://en.glosbe.com/de/en/"+lexis

    try:
        source = requests.get(url, headers=headers).text

        soup = BeautifulSoup(source, "lxml")

        for exmpl in soup.find_all('div', class_='row-fluid'):
            germ = exmpl.find('div', class_='span6').text
            eng = exmpl.find('div', lang='en').text
            example = '  '+germ+' = '+eng
            if len(germ) < 70 and not germ.startswith('de '):
                text_C.insert(END, example+'\n')
            else:
                pass

    except AttributeError:
        text_C.insert(END, 'Other examples not found.')

# ----------------- CLEAR - SAVE EXAMPLE SENTENCES -------------------
def clear_examples():
    """
    clear examples
    """
    text_C.delete('1.0', END)

def save_examples():
    """
    save examples
    """
    try:
        os.makedirs("Desktop/FLang")
        with open('Desktop/FLang/Repository.txt', 'a',
                  encoding='utf-8') as exmpl_file:
            exmpl_file.write(text_C.get("1.0", END))
    except FileExistsError:
        # directory already exists
        with open('Desktop/FLang/Repository.txt', 'a',
                  encoding='utf-8') as exmpl_file:
            exmpl_file.write(text_C.get("1.0", END))
# -------------------------------------------------------------

# ----------------- THE GUI ------------------------------

root = Tk()
root.title('Word Finder and VOC creator')
root.geometry('550x680+820+5')
root.configure(bg='#EEE8AA')
# -------------------------------------------
def on_closing():
##    exit_Progr() # this function has not been added yet
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# --------------------------------------------
lftside=Frame(root, bg="#B8860B") # frame for the ribbon
lftside.pack(side=LEFT, ipady=25)

mdle1=Frame(root, bg="#EEE8AA", width=450) # main area, middle frame
mdle1.pack(side=TOP)

mdle2=Frame(root, bg="#EEE8AA", width=450) # where the long bar resides
mdle2.pack(side=TOP)

mdle3=Frame(root, bg="#EEE8AA", width=450) # main area, middle frame
mdle3.pack(side=TOP)

mdle4=Frame(root, bg="#EEE8AA", width=450) # main area, middle frame
mdle4.pack(side=TOP)
# ................ RIBBON WIDGET .......
# ---------------- Ribbon --------------
textL = ['M','E','A','N','I','N','G','','V','O','C','A','B','U','L','A','R','Y','','','' \
         'E','X','A','M','P','L','E','S','','']
for item in textL:
    lab1 = Label(lftside, text=item, font=('Arial',9,'bold'),fg='white', bg='#B8860B').pack(side=TOP)
    
# ................. MIDDLE FRAME WIDGETS .......................................
# ---------------- Label - Type Word ------------------- ROW = 0
label1 = Label(mdle1, text='Type word to search in dict.➜ ', font=('bold'), fg='white', bg='#556B2F')
label1.grid(row=0, column=0, pady=5, sticky=W)
# ----------------- Entry ------------------------------ ROW = 0
fndWord = StringVar()
entry_A = Entry(mdle1, textvariable=fndWord, width=23, font=('Arial', 12), bd=3)
entry_A.focus_set()
entry_A.grid(row=0, column=1, columnspan=3, sticky=E, pady=5)

label1 = Label(mdle1, text='Click dictionary:➜  ', font=('Arial', 10, 'bold'), fg='black', bg='#EEE8AA')
label1.grid(row=1, column=0, pady=3, sticky=W)

butLANG = Button(mdle1, text='Langesheidt', bg='#FFA500', fg='black', font=('Arial', 9, 'bold'),
                 command=langescheid)
butLANG.grid(row=1, column=0, pady=3, sticky=E)
butFREE = Button(mdle1, text='theFreeDict.', bg='#B8860B', fg='white', font=('Arial', 9, 'bold'),
                 command=src_thefreedict)
butFREE.grid(row=1, column=1, pady=3, sticky=W)
butGLO = Button(mdle1, text='Glosbe', bg='#99FFFF', fg='black', font=('Arial', 9, 'bold'),
                command=src_glosbe)
butGLO.grid(row=1, column=1, pady=3, padx=77)
butDE_GR = Button(mdle1, text='ΓΕΡ-ΕΛ', bg='#000000', fg='white', font=('Arial', 9, 'bold'),
                command=de_el_search)
butDE_GR.grid(row=1, column=1, pady=3, sticky=E, padx=10)
butGR_DE = Button(mdle1, text='ΕΛ-ΓΕΡ', bg='#0000FF', fg='white', font=('Arial', 9, 'bold'),
                command=el_de_search)
butGR_DE.grid(row=1, column=2, pady=3, sticky=W)
#----------------- Label: Across the Clear Box -------------
butCLR = Button(mdle2, text='CLEAR BOX', bg='#800000', fg='white', font=('Arial', 9, 'bold'),
                command=clr_defins).grid(row=1, column=0, padx=5, sticky=W)

text_A = ScrolledText(mdle2, width=48, borderwidth=5, height=4, wrap=WORD)
text_A.grid(row=1, column=0, columnspan=2, padx=85, pady=3, sticky=W) #--------- ROW = 1
text_A.config(padx=5)

# ---------------- Label: VOCABULARY AREA ----------- Row = 2
butLBL = Button(mdle2, text='CLICK to add Word to Vocabulary Area below', width=45, font=('Arial', 11, 'bold'),
                relief=RAISED, bd=5, fg='black', bg='#D8BD65', command=bring_down)
butLBL.grid(row=2, column=0, columnspan=2, ipadx=3, pady=3, sticky=N)
# ------------------------------------------------------------------
btnOp = Button(mdle3, text=' O P E N ', fg='black', font=('Arial', 9, 'bold'), bg='#FFFF04', command=open_file)
btnOp.grid(row=3, column=0, sticky=N)

btnCr = Button(mdle3, text=' CREATE', fg='white', font=('Arial', 9, 'bold'), bg='#2E8B57', command=create_vocfile)
btnCr.grid(row=4, column=0, sticky=N)

btnCl = Button(mdle3, text='  CLEAR ', fg='white', font=('Arial', 9, 'bold'), bg='#800000', command=clear_file)
btnCl.grid(row=5, column=0, sticky=N)

btnSv = Button(mdle3, text='SAVE or \nUPDATE', fg='black', font=('Arial', 9, 'bold'), bg='#CCFF99', command=save_update)
btnSv.grid(row=6, column=0, sticky=N)

btnAp = Button(mdle3, text='APPEND', fg='black', font=('Arial', 9, 'bold'), bg='#8FBC8F', command=append)
btnAp.grid(row=7, column=0, sticky=N)

text_B = ScrolledText(mdle3, width=48, borderwidth=5, height=11, wrap=WORD)
text_B.grid(row=3, rowspan=5, column=1, columnspan=3, sticky=W, padx=3, pady=3)
text_B.config(padx=5)
# ---------------- Label: EXAMPLES AREA ----------- Row = 3
label1 = Label(mdle4, text='EXAMPLES AREA BELOW ', width=44, font=('Arial', 11, 'bold'), fg='black', bg='#D8BD65')
label1.grid(row=8, column=0, columnspan=2, ipadx=45, pady=3, sticky=W)

text_C = ScrolledText(mdle4, width=59, borderwidth=5, height=10, wrap=WORD, bg='#FFFAF0')
text_C.grid(row=9, column=0, columnspan=3, sticky=W, padx=7, pady=5)
# --------------------------------------------
btnWR = Button(mdle4, text='WordRef', bg='#1E90FF', font=('Arial',9,'bold'),fg='white',command=exam_wrdref)
btnWR.grid(row=10, column=0, padx=10, sticky=W, pady=2)
btnCO = Button(mdle4, text='Collins', bg='#B22222', fg='white', font=('Arial', 9, 'bold'),command=exam_collins)
btnCO.grid(row=10, column=0, sticky=W, padx=70, pady=2)
btnGL = Button(mdle4, text='Glosbe', bg='#99FFFF', fg='black', font=('Arial', 9, 'bold'), command=exam_glosbe)
btnGL.grid(row=10, column=0, sticky=W, padx=120, pady=2)

btnDEEL = Button(mdle4, text='ΓΕΡ-ΕΛ', fg='white', bg='black', font=('Arial', 9, 'bold'), command=glosbe_exampl_gr)
btnDEEL.grid(row=10, column=1, sticky=W, padx=20, pady=2)

btnCL = Button(mdle4, text='CLEAR', bg='#800000', fg='white', font=('Arial', 9, 'bold'),command=clear_examples)
btnCL.grid(row=10, column=1, sticky=W, padx=73, pady=2)
btnSV = Button(mdle4, text=' S A V E', bg='#CCFF99', fg='black', font=('Arial', 9, 'bold'),command=save_examples)
btnSV.grid(row=10, column=1, sticky=E, padx=125, pady=2)
# ----------------------------------------------

root.mainloop()
