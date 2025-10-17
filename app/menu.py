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

            # Updating tasks
            elif choice == 6 :
                pid = int(input("Enter project ID: "))
                tid = int(input("Enter task ID: "))
                title = input("Enter NEW task title: ")
                description = input("Enter NEW task description: ")
                status = input("Enter new task status (todo / doing / done): ")
                todo.update_task(pid, tid, title=title, description=description, status=status)
                print("Task updated successfully")

            # Deleting task
            elif choice == 7 :
                pid = int(input("Enter project ID: "))
                tid = int(input("Enter task ID: "))
                todo.delete_task(pid, tid)
                print("Task deleted successfully")

            # Updating task state
            elif choice == 8 :
                pid = int(input("Enter project ID: "))
                tid = int(input("Enter task ID: "))
                status = input("Enter status (doto / doing / done): ")
                todo.update_task(pid, tid, status=status)
                print("Task status updated successfully")

            # Listing tasks
            elif choice == 9 :
                pid = int(input("Enter project ID: "))
                tasks = todo.list_tasks(pid)
                if not tasks :
                    print("Such task does not exist !")
                else :
                    for t in tasks :
                        print(f"{t.id} - {t.title} [{t.status}]")

            # Exit
            elif choice == 0 :
                print("Exit")
                break

            else :
                print("Invalid choice")

        except Exception as e :
            print("Error", e)