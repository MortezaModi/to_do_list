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
        print("5  Add tasks")
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

            # update project
            elif choice == 2 :
                pid = int(input("Enter project ID: "))
                name = input("Enter NEW project name: ")
                description = input("Enter NEW project description: ")
                todo.update_project(pid, name, description)
                print("Project updated successfully")

            # Delete project
            elif choice == 3 :
                pid = int(input("Enter project ID: "))
                todo.delete_project(pid)
                print("Project deleted successfully")

            # List projects
            elif choice == 4 :
                projects = todo.list_projects()
                if not projects :
                    print("Such project does not exist !")
                else :
                    for p in projects :
                        print(f"{p.id} - {p.name} - {p.description}")

            # Adding tasks
            elif choice == 5 :
                pid = int(input("Enter project ID: "))
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                todo.create_task(pid, title, description)
                print("Task added successfully")

                
            elif choice == 6 :





        except Exception as e :