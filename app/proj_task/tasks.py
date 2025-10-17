from datetime import datetime
from typing import Optional

class tasks:
    def __init__(self,
        id: int,
        t_name :str,
        description :str,
        proj_id : int,
        deadline : Optional[datetime],
        state: str= "todo"
    ):
        self.id = id
        self.t_name = t_name
        self.description = description
        self.proj_id = proj_id
        self.deadline = deadline
        self.state = state
        self.created_at = datetime.now()
        self.updated_at = datetime.now()