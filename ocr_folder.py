
from pathlib import Path
from openai_base import Chat_Result, ask





def ocr_files(files:list[str|Path], 
               prompt:str = '',
               log:bool = False) -> dict:
    contentdict = {}
    # collect files 
    for file in files:
        if isinstance(file,str):
            file = Path(file)
        jsonfile = file.with_suffix('.json')
        if jsonfile.exists():
            if log:
                print(f'skipped ocr {file.stem}')
            jsonstr = jsonfile.read_text(encoding='utf-8')
            result = Chat_Result.fromjson(jsonstr=jsonstr)
        else:
            if log:
                print(f'run ocr {file.stem}')
            # run ocr
            result = ask(str(file),prompt=prompt)             
            jsonfile.write_text(data=result.tojson(),encoding='utf-8')
        contentdict[file] = result
    return contentdict






