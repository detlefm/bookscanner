from dataclasses import dataclass,asdict, field
from openai.types.chat.chat_completion import ChatCompletion
import json

ANSW_CONTENT = "content"
ANSW_FINISH = "finish_reason"


@dataclass
class Chat_Result:
    token:int
    answers:list[dict] 
    metadata:dict = field(init=False,default_factory=dict)

    
    def __init__(self, *args, **kwargs):
        # Überprüfen, ob die erforderlichen Argumente vorhanden sind
        if 'token' not in kwargs or 'answers' not in kwargs:
            raise ValueError("token and answers are required")
        
        # Setzen der erforderlichen Argumente
        self.token = kwargs.pop('token')
        self.answers = kwargs.pop('answers')
        
        # Alle verbleibenden Argumente in optional_args speichern
        self.metadata = kwargs.get('metadata',{})

    
    @staticmethod
    def from_completion(completion:ChatCompletion) -> "Chat_Result":
        lst = []
        for answer in completion.choices:
            lst.append({ANSW_CONTENT: answer.message.content,ANSW_FINISH:answer.finish_reason})   
        return Chat_Result(token=completion.usage.completion_tokens,answers=lst) 
    
    def to_json(self)->str:
        d = asdict(self)
        return json.dumps(d,indent=2)

    @staticmethod
    def from_json(jsonstr:str) -> "Chat_Result":
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
    
    def get_metadata(self,key:str):
        if self.metadata:
            return self.metadata.get(key,None)
        return None
    
    def set_metadata(self,key:str,val):
        self.metadata[key] = val



