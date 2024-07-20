import tomllib
from pathlib import Path
import os


toml_file = 'config.toml'


standard = {
    'ocr_prompt':"""
    Transcribe this image with Slovak text into plain Slovak text. Keep the formatting. 
    Return only the Slovak text without annotations.Ignore handwritten notes.
    """,
    'book_prefix': "Kniha",
    'page_prefix': "Strana",
    'pdf_background' : "./data/bg_textur.jpg",
    'doc_template' : "./data/template.docx",
}

class Config:

    def __init__(self, **kwargs):
        self.values = standard
        for k,v in kwargs.items():
            self.values[k] = v

    @staticmethod
    def create(filename:str = toml_file):
        pathes = [Path(os.getcwd())]
        try:
            pathes.append(Path(__file__).parent)
        except NameError as e:
                ...
        path:Path
        for path in [p for p in pathes if p]:
            fpath = path / filename
            if fpath.is_file():
                data  = tomllib.loads(fpath.read_text(encoding='utf-8'))
                return Config(**data)
        return Config()
    
    def getvalue(self,keyword:str) -> str:
         return self.values.get(keyword,'')
    

config = Config.create(toml_file)
