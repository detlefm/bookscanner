import requests
import base64
from PIL import Image, ImageFile
from io import BytesIO
from pathlib import Path
from collections import defaultdict
import shutil
import re
import os



image_extensions = ['.png','.jpg','.jpeg']




base64_mime_type = {
    '/9j/':'image/jpeg',
    'iVBORw0KGgoAAA':'image/png',
    'R0lGOD':'image/gif',
    'PHN2Zy':'image/svg+xml',
    'JVBERi0xLj':'application/pdf',
    # 'data:text/plain;base64,':'text/plain',
    # 'data:text/html;base64,':'text/html',
    # 'data:application/json;base64,':'application/json',
    # 'data:application/xml;base64,':'application/xml',
    'UEsDBBQ':'application/zip',
}


# Todo: Only tested with jpg and png

def mimetype_base64(text:str): 
    prefix = text[:min(50,len(text))]
    if prefix.startswith('data:'):
        match = re.search(r"data:(.*);", text)
        if match:
            return match.group(1)
    elif (found := [key for key in base64_mime_type.keys() 
                        if prefix.startswith(key)]):
        return base64_mime_type[found[0]]
    raise LookupError(f'Unknown mime type {text[:min(50,len(text))]}...')


def load_img(image_url:str) ->ImageFile:
    # URL des externen Bildes
    #image_url = "https://example.com/path/to/image.jpg"

    # Bild von der URL herunterladen
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image

def image2base64(img_file:Image) -> str:
    buffered = BytesIO()
    img_file.save(buffered,format = "PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def getfiles(path,suffixes:list=image_extensions)-> list[Path]:
    if isinstance(path,str):
        path = Path(path)
    return sorted( [p for p in path.glob('*.*') 
                    if p.is_file() and 
                    p.suffix in suffixes])


def create_folder(folder:str|Path):
    if not os.path.exists(folder):
        os.makedirs(folder)

def normalize_lens_filenames(files:list[Path]):
    for file in [f for f in files if f.stem.endswith('Office Lens')]:
        new = file.with_stem(file.stem+' (0)')
        shutil.move(file,new)



