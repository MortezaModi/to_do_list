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