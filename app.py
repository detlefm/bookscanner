from dotenv import load_dotenv
import os
import sys
from ocr_folder import ocr_files
from openai_base import Chat_Result, ask
from xdocx import text_to_word
import streamlit as st
from PIL import Image
from constants import ocr_prompt, BOOK_PREFIX
from xfile import getfiles, normalize_lens_filenames, rename_to_pagenumbers
from pathlib import Path
from pdfcreator import pdf_from_images
from utils import print_duration
import shutil


load_dotenv(".env")


def normalize_filenames(folder, bookno):
    files = getfiles(folder)
    # add (0) if nessesary
    normalize_lens_filenames(files)
    # reread file names
    files = getfiles(folder)
    # change names to Book_XX_Page_XX, 
    # the real word for Book and Page is defined in constants.py
    rename_to_pagenumbers(bookno=bookno,files=files)
     


def create_pdf(folder:str, bookno:int):
    files = getfiles(folder)
    pdffilename = f'{BOOK_PREFIX}_{bookno:02}.docx'
    outpath = os.path.join(folder,pdffilename)    
    pdf_from_images(outfile=outpath,files=files)



@print_duration
def create_word(folder:str, bookno:int):
    files = getfiles(folder)
    d:dict[str,Chat_Result] = ocr_files(files=files,prompt=ocr_prompt,log=True)
    print(f'Files count: {len(d)}') 
    txtlst = []
    for key in sorted(d.keys()):
        txtlst.append(d[key].content)
    wordfilename = f'{BOOK_PREFIX}_{bookno:02}.docx'
    outpath = os.path.join(folder,wordfilename)
    text_to_word(word_file=outpath,txtlst=txtlst)
    return files,outpath   





def streamlit_interface():
    st.set_page_config(
        layout="wide",
        page_title="OCR",
        page_icon="🚀",
    )
    st.title('OCR pictures')
    left, right = st.columns(2)
    with left:
        uploaded_file = st.file_uploader(label='Upload page',type=['.png','.jpg','.jpeg'],accept_multiple_files=False)
        if uploaded_file:  
            if st.button("start"):
                with st.spinner():
                    answer = ask(source=uploaded_file,mtype=uploaded_file.type,prompt=ocr_prompt)
                    with right:
                        st.subheader("Result")
                        st.write(answer.content)
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)


jumpdict = {
    'normalize': normalize_filenames,
    'make_word': create_word,
    'make_pdf': create_pdf
}

def usage(msg:str):    
    print(msg)
    print(f"usage: app.py {'|'.join(jumpdict.keys())} imagefolder bookno")
    exit(-1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        streamlit_interface()
        exit(0)
    # we got at least one argument
    if (func := jumpdict.get(sys.argv[1],None))==None:
        usage(f'wrong command name {sys.argv[1]}')
    if len(sys.argv)<4:
        usage(f'to less arguments {len(sys.argv)}')
    folder = sys.argv[2]
    if not (os.path.exists(folder) or 
            os.path.isfile(folder)):
        usage(f"folder {folder} didn't exists or is not a folder")
    try:
        bookno = int(sys.argv[3])
    except ValueError as v:
        usage(f'{sys.argv[3]} is not an integer')
    func(folder=folder,bookno=bookno)

