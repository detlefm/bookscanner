import requests
import base64
from PIL import Image, ImageFile
from io import BytesIO
from pathlib import Path
from collections import defaultdict
import shutil

image_extensions = ['.png','.jpg','.jpeg']


# def mimetype_base64(text:str):
#     if text.startswith()
#     JPEG-Bilder:

# Präfix: 9j/ MIME-Typ: image/jpeg

# Präfix: iVBORw0KGgoAAA MIME-Typ: image/png

# Präfix: R0lGOD MIME-Typ: image/gif


# Präfix: PHN2Zy MIME-Typ: image/svg+xml

# Präfix: JVBERi0xLj MIME-Typ: application/pdf

# Präfix: data:text/plain;base64, MIME-Typ: text/plain


# Präfix: data:text/html;base64, MIME-Typ: text/html


# Präfix: data:application/json;base64, MIME-Typ: application/json

# Präfix: data:application/xml;base64, MIME-Typ: application/xml


# Präfix: UEsDBBQ MIME-Typ: application/zip

def load_img(image_url:str) ->ImageFile:
    # URL des externen Bildes
    #image_url = "https://example.com/path/to/image.jpg"

    # Bild von der URL herunterladen
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image

def convert2base64(img_file:Image) -> str:
    buffered = BytesIO()
    img_file.save(buffered,format = "PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def getfiles(path,suffixes:list=image_extensions)-> list[Path]:
    if isinstance(path,str):
        path = Path(path)
    return sorted( [p for p in path.glob('*.*') 
                    if p.is_file() and 
                    p.suffix in suffixes])




def normalize_filenames(files:list[Path]):
    tochange = [f for f in files if f.stem.endswith(')') == False]
    result:list[tuple[Path,Path]] = []
    for f in tochange:
        newname = f.with_stem(f.stem+' (0)')
        result.append((f,newname))
    return result


def rename_to_pagenumbers(bookno:int,files:list[Path]):
    counter = 0
    for f in files:
        counter +=1
        nn = f.with_stem(f'Buch_{bookno:02}_Page_{counter:03}')
        shutil.move(f,nn)




if __name__ == "__main__":
    import sys
    files = getfiles(sys.argv[1])
    rename_to_pagenumbers(bookno=2,files=files)
    # tochangelst = normalize_filenames(files=files)
    # for old,new in tochangelst:
    #     shutil.move(old,new)
    # print(len(tochangelst))
