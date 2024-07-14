# from dataclasses import dataclass,asdict
# from typing import Union
# from openai.types.chat.chat_completion import ChatCompletion
# import json
import base64
import mimetypes
from xfile import mimetype_base64
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from io import BytesIO


_client = None

def init()-> OpenAI:
    global _client
    if not _client:
        _client = OpenAI()
    return _client



def get_chat_response(img_url_dict:dict, prompt:str, max:int ):
    client = init()
    response:ChatCompletion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"},
                    {
                        "type": "image_url",
                        "image_url": img_url_dict,
                    },
                ],
                }
            ],
            max_tokens=max
        )
    return response


def ask_openai(source:str|BytesIO,
               prompt:str='',
               max:int=2000):
    
    assert(prompt)
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

    return get_chat_response(img_url_dict, prompt, max, )


# def ask_openai_old(source:str|BytesIO,
#                mtype="image/png",
#                prompt:str='',
#                max:int=2000):
#     assert(prompt)
#     client = init()
#     # we assume it is a hyperlink 
#     img_url_dict = {"url": source}
#     # but maybe it is a BytesIO buffer
#     if isinstance(source, BytesIO):
#         base64_image = base64.b64encode(source.getvalue()).decode('utf-8')
#         img_url_dict = {"url": f"data:{mtype};base64,{base64_image}" }  
#     # or a local file
#     elif source.startswith('https://')==False:
#         # str, str return mimetype and encoding
#         mimetype, _ = mimetypes.guess_type(source)
#         with open(file=source,mode="rb") as image_file:
#             base64_image = base64.b64encode(image_file.read()).decode('utf-8')  
#         img_url_dict = {"url": f"data:{mimetype};base64,{base64_image}" }             

#     response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": f"{prompt}"},
#                     {
#                         "type": "image_url",
#                         "image_url": img_url_dict,
#                     },
#                 ],
#                 }
#             ],
#             max_tokens=max
#         )
#     return response


# def ask(source:str|BytesIO,
#         mtype="image/png",
#         prompt:str='',
#         max:int=2000) -> Chat_Result:
#     response = ask_openai(source=source,mtype=mtype,prompt=prompt,max=max)
#     return Chat_Result.from_completion(completion=response)




