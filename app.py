from dotenv import load_dotenv
import os
import sys
from ocr_folder import ocr_files
from openai_base import Chat_Result, ask
from xdocx import text_to_word
import streamlit as st
from PIL import Image
from prompts import ocr_prompt
from xfile import getfiles
from pathlib import Path
from pdfcreator import pdf_from_images
from utils import print_duration


load_dotenv(".env")

@print_duration
def ocr_terminal(folder:str,outfile:str):
    files = getfiles(folder)
    d:dict[str,Chat_Result] = ocr_files(files=files,prompt=ocr_prompt,log=True)
    print(f'Files count: {len(d)}') 
    txtlst = []
    for key in sorted(d.keys()):
        txtlst.append(d[key].content)
    outpath = os.path.join(folder,outfile)
    text_to_word(word_file=outpath,txtlst=txtlst)
    pdf_from_images(outfile=str(Path(outpath).with_suffix('.pdf')),files=files)    





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



if __name__ == "__main__":
    if len(sys.argv) == 1:
        streamlit_interface()
    else:
        args = sys.argv[1:]
        ocr_terminal(folder=args[0],outfile=args[1])








