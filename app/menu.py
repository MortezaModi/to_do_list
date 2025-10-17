from csv import excel

from app.proj_task.crud import manager

def run_menu() :
    todo = manager()
    while True :
        print("\n  To Do list menu:")
        print("1  Create new project")
        print("2  Update projects")
        print("3  Delete projects")
        print("4  List projects")
        print("5  Create tasks")
        print("6  Update tasks")
        print("7  Delete tasks")
        print("8  Change task status")
        print("9  List tasks")
        print("0  Exit")

        choice = int(input("Enter your choice: "))

        try:
            # create project
            if choice == 1 :
                name = input("Enter project name: ")
                description = input("Enter project description: ")
                todo.create_project(name, description)
                print("Project created successfully")

               


        except Exception as e :