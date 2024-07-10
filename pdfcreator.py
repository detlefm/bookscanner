from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.enums import TA_JUSTIFY
from pathlib import Path
import sys
from xfile import getfiles


# reportlab docs at https://docs.reportlab.com/reportlab/userguide/ch2_graphics/

def pdf_from_images(outfile:str, files:list[Path]):

    c = canvas.Canvas(outfile, pagesize=A4)
    width, height = A4

    for file in files:
        c.setFillColor(colors.wheat)
        c.rect(0, 0, width, height, fill=1)
        c.drawImage(file, 0, 0, width=width, height=height , preserveAspectRatio=True)
        # Create a new page
        c.showPage()
    c.save()


if __name__ == "__main__":
    if len(sys.argv)<3:
        print(f'usage: {sys.argv[0]}  pathtoimages outfilename')
        exit(-1)
    files = getfiles(path=sys.argv[1])
    pdf_from_images(outfile=sys.argv[2],files=files)
    
    
