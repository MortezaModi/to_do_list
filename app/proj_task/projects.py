from datetime import datetime
from typing import List

class Projects:

    def __init__(self, id: int, full_name: str, descrip: str):
        self.id = id
        self.full_name = full_name
        self.descrip = descrip
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks: List = []

    def updating(self, full_name: str, descrip: str):
        self.full_name = full_name
        self.descrip = descrip

        if full_name != None :
            self.full_name = full_name
        if descrip != None :
            self.descrip = descrip
        self.updated_at = datetime.now()