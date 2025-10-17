from datetime import datetime
from typing import Optional

class tasks:
    def __init__(self,
        id: int,
        t_name :str, # task name
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

    def updating(self, t_name: str, description: str, deadline: Optional[datetime], state: str):
        self.t_name = t_name
        self.description = description

        if t_name != None :
            self.t_name = t_name
        if description != None :
            self.descrip = description
        if deadline != None :
            self.deadline = deadline
        if state != None :
            self.state = state
        self.updated_at = datetime.now()

    def __str__(self):
            return (
                "Task id : {}" + str(self.id) ,
                "Task Title : {}" + str(self.t_name),
                "description : {}" + str(self.description),
                "deadline : {}" + str(self.deadline),
                "state : {}" + str(self.state),
                "created on : {}" + str(self.created_at.strftime("%Y-%m-%d %H:%M:%S")),
                "updated at : {}" + str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
            )

    def __repr__(self):
        return "Task id : {}" + str(self.id) , " Task Title : {}" + str(self.t_name), " state : {}" + self.state, " project id : {}" + str(self.proj_id)
