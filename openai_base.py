from dataclasses import dataclass,asdict
from typing import Union
from openai.types.chat.chat_completion import ChatCompletion
import json
import base64
import mimetypes
from openai import OpenAI  
from io import BytesIO



ANSW_CONTENT = "content"
ANSW_FINISH = "finish_reason"


@dataclass
class Chat_Result:
    token:int
    answers:list[dict] 

    
    @staticmethod
    def from_completion(completion:ChatCompletion) -> "Chat_Result":
        lst = []
        for answer in completion.choices:
            lst.append({ANSW_CONTENT: answer.message.content,ANSW_FINISH:answer.finish_reason})   
        return Chat_Result(token=completion.usage.completion_tokens,answers=lst) 
    
    def tojson(self)->str:
        d = asdict(self)
        return json.dumps(d,indent=2)

    @staticmethod
    def fromjson(jsonstr:str) -> "Chat_Result":
        d = json.loads(jsonstr)
        return Chat_Result(**d)
    
    @property
    def content(self) ->str:
        if not self.answers:
            return "no answers"
        return self.answers[0].get(ANSW_CONTENT,'no content')

    
    @property
    def content_all(self) ->list[str]:
        result = [self.content]
        if len(self.answers)>1:
            result.extend([a.get(ANSW_CONTENT,'') for a in self.answers[1:]])
        return result
    




client = OpenAI()



def _ask_openai(source:str|BytesIO,
               mtype="image/png",
               prompt:str='',
               max:int=2000):

    assert(prompt)
    # we assume it is a hyperlink 
    img_url_dict = {"url": source}
    # but maybe it is a BytesIO buffer
    if isinstance(source, BytesIO):
        base64_image = base64.b64encode(source.getvalue()).decode('utf-8')
        img_url_dict = {"url": f"data:{mtype};base64,{base64_image}" }  
    # or a local file
    elif source.startswith('https://')==False:
        # str, str return mimetype and encoding
        mimetype, _ = mimetypes.guess_type(source)
        with open(file=source,mode="rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')  
        img_url_dict = {"url": f"data:{mimetype};base64,{base64_image}" }             

    response = client.chat.completions.create(
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


def ask(source:str|BytesIO,
        mtype="image/png",
        prompt:str='',
        max:int=2000) -> Chat_Result:
    response = _ask_openai(source=source,mtype=mtype,prompt=prompt,max=max)
    return Chat_Result.from_completion(completion=response)




