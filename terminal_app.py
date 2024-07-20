import shutil
from dotenv import load_dotenv
import os
import sys
import json
from pathlib import Path
from oai import ask_openai
from chat_result import Chat_Result
from xdocx import text_to_word
import streamlit as st
from PIL import Image
#from constants import ocr_prompt, BOOK_PREFIX
from xfile import getfiles, normalize_lens_filenames
from pdfcreator import pdf_from_images
from utils import print_duration, debug_arguments
import config


load_dotenv(".env")

config = config.Config.create()

#@debug_arguments(['srcfolder'])
def normalize_filenames(srcfolder:str):
    files = getfiles(srcfolder)
    # add (0) if nessesary
    normalize_lens_filenames(files)
    # reread file names
    files = getfiles(srcfolder)
    # change names to Book_XX_Page_XX, 
    # the real word for Book and Page is defined in constants.py
    for index, file in enumerate(files):
        nn = file.with_stem(f'{config.getvalue('book_prefix')}_{config.getvalue('page_prefix')}_{(index+1):03}')
        shutil.move(file,nn)        
    #rename_to_pagenumbers(bookno=bookno,files=files)
     

@print_duration
#@debug_arguments(['srcfolder','destfile'])
def create_word(srcfolder:str,destfile:str ):  
    files = getfiles(srcfolder)
    txtlst = []
    for file in files:
        jsonfile = file.with_suffix('.json')
        if jsonfile.exists()==False:
            print(f'Missing datafile {jsonfile.name}')
            continue
        jsonstr = jsonfile.read_text('utf-8')
        txtlst.append(Chat_Result.from_json(jsonstr=jsonstr).content)
    # wordfilename = f'{BOOK_PREFIX}_{bookno:02}.docx'
    # outpath = folder / wordfilename
    text_to_word(word_file=destfile,txtlst=txtlst)


@print_duration
#@debug_arguments(['srcfolder','destfile'])
def create_pdf( srcfolder:str, destfile:str, coversheet:str=''):
    files = getfiles(path=srcfolder)
    pdf_from_images(outfile=destfile,files=files,deckblatt=coversheet)




def _run_ocr_folder(folder:str) -> dict:
    contentdict = {}
    # collect files 
    for file in getfiles(folder):
        jsonfile = file.with_suffix('.json')
        if jsonfile.exists():
            print(f'skipped ocr {file.stem}')
            jsonstr = jsonfile.read_text(encoding='utf-8')
            result = Chat_Result.from_json(jsonstr=jsonstr)
        else:
            print(f'run ocr {file.stem}')
            # run ocr
            result = ask_openai(str(file),prompt=config.getvalue('ocr_prompt'))             
            jsonfile.write_text(data=result.tojson(),encoding='utf-8')
        contentdict[str(file)] = result
    return contentdict

#@debug_arguments(['srcfolder','destfile'])
@print_duration
def ocr_folder(srcfolder:str, destfile:str) -> dict:
    content = _run_ocr_folder(srcfolder,log=False)
    with open(destfile,'w') as file:
        jsonstr = json.dumps(content,indent=2)
        file.write(jsonstr+'\n')
  



jumpdict = {
    'normalize': { 'func':normalize_filenames, 'argscount':1},
    'ocr_images':{ 'func':ocr_folder, 'argscount':2} ,
    'make_word': { 'func':create_word, 'argscount':2} ,
    'make_pdf': { 'func':create_pdf, 'argscount':2}
}

def usage(**kwargs): 
    if (msg:=kwargs.get('msg',None)):   
        print(msg)
    print(f"usage: app.py {'|'.join(jumpdict.keys())} imagefolder destination")
    exit(-1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    # we got at least one argument
    if (func_info := jumpdict.get(sys.argv[1],None))==None:
        usage(msg=f'wrong command name {sys.argv[1]}')
    if len(sys.argv)<func_info['argscount']+2:
        usage(msg=f'to less arguments {len(sys.argv)}')
    kwargs = {}
    srcfolder = sys.argv[2]
    if not (os.path.exists(srcfolder) or 
            os.path.isfile(srcfolder)):
        usage(f"folder {srcfolder} didn't exists or is not a folder")
    kwargs['srcfolder'] = srcfolder
    if func_info['argscount']==2:
        if len(sys.argv)<4:
            usage(msg=f'to less arguments {len(sys.argv)}') 
        kwargs['destfile'] = sys.argv[3]           

    if (func:= func_info.get('func')) == None:
        usage(msg='Internal error')
    func(**kwargs)

