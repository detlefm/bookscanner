import base64
import mimetypes
from xfile import mimetype_base64
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from io import BytesIO



_model = "gpt-4o-mini"
_temperatur = 1
_top_p = 1
_frequency_penalty = 0
_presence_penalty = 0



_client = None

def init()-> OpenAI:
    global _client
    if not _client:
        _client = OpenAI()
    return _client




def _messages(img_url_dict:dict, prompt:str) -> dict:
    d = {}
    d['role']="user"
    d['content'] = [{"type": "text", "text": f"{prompt}"}]
    if img_url_dict:
        d['content'].append( 
            { "type": "image_url","image_url": img_url_dict,}
        )
    return d
       

def _chat_response(img_url_dict:dict, prompt:str, max:int ):
    client = init()
    response:ChatCompletion = client.chat.completions.create(
            model=_model,
            messages=[_messages(img_url_dict=img_url_dict,prompt=prompt)],
            max_tokens=max,
            temperature=_temperatur,
            top_p=_top_p,
            frequency_penalty= _frequency_penalty,
            presence_penalty= _presence_penalty
        )  
    return response  


def _create_img_url_dict(source:str|BytesIO) -> str:
    # we assume it is a hyperlink 
    img_url_dict = {"url": source}
    # but maybe it is a BytesIO buffer
    if isinstance(source, BytesIO):
        base64_image = base64.b64encode(source.getvalue()).decode('utf-8')
        img_url_dict = {"url": f"data:{mimetype_base64(base64_image)};base64,{base64_image}" }  
    # or a local file
    elif source.startswith('https://')==False:
        # str, str return mimetype and encoding
        mimetype, _ = mimetypes.guess_type(source)
        with open(file=source,mode="rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')  
        img_url_dict = {"url": f"data:{mimetype};base64,{base64_image}" } 
    return img_url_dict    


def ask_openai(source:str|BytesIO,
               prompt:str='',
               max:int=2000):
    
    assert(prompt)
    img_url_dict = None       
    if source:
        img_url_dict = _create_img_url_dict(source=source)
    return _chat_response(img_url_dict, prompt, max )

