from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class QuizTopic:
    name: str
    id: str
