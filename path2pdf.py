from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.enums import TA_JUSTIFY
from pathlib import Path
import sys
from PIL import Image
# reportlab docs at https://docs.reportlab.com/reportlab/userguide/ch2_graphics/

image_extensions = ['.png','.jpg','.jpeg']

def getfiles(path,suffixes:list=image_extensions)-> list[Path]:
    if isinstance(path,str):
        path = Path(path)
    return sorted( [p for p in path.glob('*.*') 
                    if p.is_file() and 
                    p.suffix in suffixes])


def pdf_from_images(outfile:str|Path, files:list[Path], deckblatt:Image=None, background:Image=None):

    # start creating pdf file
    c = canvas.Canvas(str(outfile), pagesize=A4)
    width, height = A4

    if deckblatt:
        c.drawImage(deckblatt,0,0,width=width,height=height)
        c.showPage()

    for file in files:
        if background:    
            c.drawImage(background,0,0,width=width,height=height)
        c.drawImage(file, 0, 4, width=width, height=height-8 , preserveAspectRatio=True)
        c.showPage()
    c.save()




if __name__ == "__main__":
    if len(sys.argv)<3:
        print(f'usage: {sys.argv[0]}  pathtoimages outfilename')
        exit(-1)
    files = getfiles(path=sys.argv[1])
    pdf_from_images(outfile=sys.argv[2],files=files,deckblatt=None)
    
    
