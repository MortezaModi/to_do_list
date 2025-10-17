from datetime import datetime
from typing import List

class Projects:

    def __init__(self, id: int, title: str, descrip: str):
        self.id = id
        self.title = title
        self.descrip = descrip
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks: List = []

    def updating(self, title: str, descrip: str):
        self.title = title
        self.descrip = descrip

        if title != None :
            self.title = title
        if descrip != None :
            self.descrip = descrip
        self.updated_at = datetime.now()

    def __str__(self):
        return (
            "Project id : {}" + str(self.id) ,
            "Title : {}" + str(self.title),
            "description : {}" + str(self.descrip),
            "created on : {}" + str(self.created_at.strftime("%Y-%m-%d %H:%M:%S")),
            "updated at : {}" + str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
            "No. tasks : {}" + len(self.tasks)
        )

