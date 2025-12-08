# app/cli/console.py

"""
Main CLI module for the ToDoList application.

This module provides the command-line interface for interacting with
the ToDoList application using database persistence.
"""

from typing import Optional, List
from datetime import datetime

# Import components from our layered architecture
from app.exceptions import AppException as TodoListException  # Alias for consistency
from app.services import ProjectService, TaskService
from app.models import TaskStatus  # Enum for statuses
from app.db.session import get_db_context  # Context manager for DB session
from app.utils.config import Config

# --- Configuration (Simulated - must be created separately) ---
# NOTE: You need to create an app/utils/config.py file for this to work.
class Config:
    PROJECT_NAME_MIN_WORDS = 1
    PROJECT_NAME_MAX_WORDS = 5
    PROJECT_DESCRIPTION_MAX_WORDS = 20
    TASK_TITLE_MIN_WORDS = 1
    TASK_TITLE_MAX_WORDS = 10
    TASK_DESCRIPTION_MIN_WORDS = 1
    TASK_DESCRIPTION_MAX_WORDS = 30

    @staticmethod
    def get_valid_statuses() -> List[str]:
        return [s.value for s in TaskStatus]


# --- CLI Implementation ---

class TodoListCLI:
    """
    Command-line interface for the ToDoList application.
    """

    def __init__(self):
        """Initialize the CLI."""
        self.current_project_id: Optional[int] = None
        self.config = Config()  # Using the simulated config

    def run(self) -> None:
        """
        Main loop for the CLI application.
        """
        print("=" * 60)
        print("Welcome to ToDoList Application (Database Edition)".center(60))
        print("=" * 60)
        print()

        while True:
            self._display_main_menu()
            choice = input("\nEnter your choice: ").strip()

            try:
                # --- Command Dispatch ---
                command_map = {
                    "1": self._create_project,
                    "2": self._view_all_projects,
                    "3": self._select_project,
                    "4": self._edit_project,
                    "5": self._delete_project,
                    "6": self._create_task,
                    "7": self._view_all_tasks,
                    "8": self._view_tasks_by_status,
                    "9": self._edit_task,
                    "10": self._delete_task,
                    "11": self._mark_task_as_done,
                    "12": self._search_projects,
                    "13": self._search_tasks,
                }

                if choice == "0":
                    print("\nThank you for using ToDoList Application!")
                    print("Goodbye! 👋")
                    break
                elif choice in command_map:
                    command_map[choice]()
                else:
                    print("\n❌ Invalid choice. Please try again.")

            except TodoListException as e:
                # Catch custom business/repository errors
                print(f"\n❌ Error: {str(e)}")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
            except Exception as e:
                # Catch unexpected system errors
                print(f"\n❌ Unexpected error: {str(e)}")
                # import traceback; traceback.print_exc() # Uncomment for debugging

            input("\nPress Enter to continue...")

    # --- MENU DISPLAY ---
    def _display_main_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "=" * 60)
        print("MAIN MENU".center(60))
        print("=" * 60)

        # Display current project info
        current_project_info = "No project selected"
        if self.current_project_id:
            try:
                with get_db_context() as db:
                    proj_service = ProjectService(db)
                    task_service = TaskService(db)
                    project = proj_service.get_project_by_id(self.current_project_id)
                    task_count = task_service.get_task_count(project.id)
                    # NOTE: Assuming Project model has 'title' or 'name'. Using 'title' from Service layer.
                    current_project_info = f"📁 Current Project: {project.title} (ID: {project.id}) | Tasks: {task_count}"
            except Exception:
                self.current_project_id = None
                current_project_info = "📁 No project selected (Previous project not found)"

        print(current_project_info)
        print("-" * 60)

        print("\nProject Management:")
        print("  1. Create Project")
        print("  2. View All Projects")
        print("  3. Select Project")
        print("  4. Edit Project")
        print("  5. Delete Project")

        print("\nTask Management:")
        print("  6. Create Task")
        print("  7. View All Tasks (in current project)")
        print("  8. View Tasks by Status (in current project)")
        print("  9. Edit Task (in current project)")
        print("  10. Delete Task (in current project)")
        print("  11. Mark Task as Done (in current project)")

        print("\nSearch:")
        print("  12. Search Projects")
        print("  13. Search Tasks (in current project)")

        print("\n  0. Exit")
        print("=" * 60)

    # --- PROJECT IMPLEMENTATIONS (Using Service Layer) ---
    def _create_project(self) -> None:
        """Handle project creation."""
        print("\n" + "=" * 60)
        print("CREATE NEW PROJECT".center(60))
        print("=" * 60)

        # NOTE: Using 'title' as per ProjectService, but input prompt uses 'Name'
        title = input(
            f"\nProject Name ({self.config.PROJECT_NAME_MIN_WORDS}-"
            f"{self.config.PROJECT_NAME_MAX_WORDS} words): "
        ).strip()
        description = input(
            f"Description (optional, max {self.config.PROJECT_DESCRIPTION_MAX_WORDS} words): "
        ).strip()

        with get_db_context() as db:
            service = ProjectService(db)
            project = service.create_project(
                title=title,
                description=description if description else None
            )
            print(f"\n✅ Project created successfully!")
            print(f"   ID: {project.id}")
            print(f"   Name: {project.title}")

    def _view_all_projects(self) -> None:
        """Display all projects."""
        print("\n" + "=" * 60)
        print("ALL PROJECTS".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)
            projects = proj_service.get_all_projects()

            if not projects:
                print("\n📭 No projects found.")
                return

            for i, project in enumerate(projects, 1):
                task_count = task_service.get_task_count(project.id)
                print(f"\n{i}. Project ID: {project.id}")
                print(f"   Name: {project.title}")
                print(f"   Description: {project.description if project.description else 'N/A'}")
                print(f"   Tasks: {task_count}")
                # NOTE: Assuming 'created_at' exists on the Project model
                print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")

    def _select_project(self) -> None:
        """Handle project selection."""
        # ... (Implementation matches your provided code) ...
        # (Using 'title' instead of 'name' for consistency with Service layer)
        print("\n" + "=" * 60)
        print("SELECT PROJECT".center(60))
        print("=" * 60)

        with get_db_context() as db:
            service = ProjectService(db)
            projects = service.get_all_projects()

            if not projects:
                print("\n📭 No projects available. Create a project first.")
                return

            # Display projects
            for i, project in enumerate(projects, 1):
                task_count = TaskService(db).get_task_count(project.id)
                print(f"{i}. {project.title} (ID: {project.id}) - {task_count} tasks")

            choice = input("\nEnter project number or ID: ").strip()

            try:
                if choice.isdigit():
                    choice_int = int(choice)
                    if 1 <= choice_int <= len(projects):
                        selected_project = projects[choice_int - 1]
                        self.current_project_id = selected_project.id
                    else:
                        project = service.get_project_by_id(choice_int)
                        self.current_project_id = project.id

                print(f"\n✅ Project selected!")
            except (ValueError, TodoListException):
                print("\n❌ Invalid selection or project not found.")

    def _edit_project(self) -> None:
        """Handle project editing."""
        # ... (Implementation matches your provided code) ...
        print("\n" + "=" * 60)
        print("EDIT PROJECT".center(60))
        print("=" * 60)

        with get_db_context() as db:
            service = ProjectService(db)
            projects = service.get_all_projects()

            if not projects:
                print("\n📭 No projects available.")
                return

            for i, project in enumerate(projects, 1):
                print(f"{i}. {project.title} (ID: {project.id})")

            choice = input("\nEnter project number or ID to edit: ").strip()

            try:
                if choice.isdigit():
                    choice_int = int(choice)
                    project = projects[choice_int - 1] if 1 <= choice_int <= len(
                        projects) else service.get_project_by_id(choice_int)
                else:
                    raise ValueError

                print(f"\nCurrent Name: {project.title}")
                print(f"Current Description: {project.description if project.description else 'None'}")

                name = input("\nNew Name (or press Enter to keep current): ").strip()
                description = input(
                    f"New Description (optional, max "
                    f"{self.config.PROJECT_DESCRIPTION_MAX_WORDS} words, "
                    f"or press Enter to keep current): "
                ).strip()

                service.update_project(
                    project.id,
                    title=name if name else None,
                    description=description if description else None,
                )

                print("\n✅ Project updated successfully!")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _delete_project(self) -> None:
        """Handle project deletion."""
        # ... (Implementation matches your provided code) ...
        print("\n" + "=" * 60)
        print("DELETE PROJECT".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)
            projects = proj_service.get_all_projects()

            if not projects:
                print("\n📭 No projects available.")
                return

            for i, project in enumerate(projects, 1):
                task_count = task_service.get_task_count(project.id)
                print(f"{i}. {project.title} (ID: {project.id}) - {task_count} tasks")

            choice = input("\nEnter project number or ID to delete: ").strip()

            try:
                if choice.isdigit():
                    choice_int = int(choice)
                    project = projects[choice_int - 1] if 1 <= choice_int <= len(
                        projects) else proj_service.get_project_by_id(choice_int)
                else:
                    raise ValueError

                task_count = task_service.get_task_count(project.id)

                print(f"\n⚠️ WARNING: This will delete the project '{project.title}'")
                print(f"   and all its {task_count} tasks permanently!")
                confirm = input("\nType 'DELETE' to confirm: ").strip()

                if confirm == "DELETE":
                    proj_service.delete_project(project.id)

                    if self.current_project_id == project.id:
                        self.current_project_id = None

                    print("\n✅ Project deleted successfully!")
                else:
                    print("\n❌ Deletion cancelled.")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    # --- TASK IMPLEMENTATIONS (Using Service Layer) ---
    def _create_task(self) -> None:
        """Handle task creation."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("CREATE NEW TASK".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)
            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.title}\n")

            title = input(
                f"Task Title ({self.config.TASK_TITLE_MIN_WORDS}-"
                f"{self.config.TASK_TITLE_MAX_WORDS} words): "
            ).strip()
            description = input(
                f"Description ({self.config.TASK_DESCRIPTION_MIN_WORDS}-"
                f"{self.config.TASK_DESCRIPTION_MAX_WORDS} words): "
            ).strip()
            deadline_str = input("Deadline (YYYY-MM-DD) or leave blank: ").strip()

            print(f"\nValid statuses: {', '.join(self.config.get_valid_statuses())}")
            status = input("Status (default: todo): ").strip() or "todo"

            # Attempt to convert status string to enum (TaskStatus validation should happen in service/validation layer)
            # Find the TaskStatus enum value
            task_status = TaskStatus(status.lower())

            # The service layer expects a deadline object or None, so we convert the string
            deadline_obj = datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None

            task = task_service.create_task(
                project_id=self.current_project_id,
                title=title,
                description=description,
                due_date=deadline_obj,  # Using due_date as defined in TaskService
                status=task_status  # Passing status to handle initial state, though service layer defaults to TODO
            )

            print(f"\n✅ Task created successfully!")
            print(f"   ID: {task.id}")
            print(f"   Title: {task.title}")
            print(f"   Status: {task.status.value}")

    def _view_all_tasks(self) -> None:
        """Display all tasks in the current project."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("ALL TASKS".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.title}\n")

            # NOTE: TaskService.get_tasks_for_project is the correct method name
            tasks = task_service.get_tasks_for_project(self.current_project_id)

            if not tasks:
                print("📭 No tasks found in this project.")
                return

            for i, task in enumerate(tasks, 1):
                deadline_str = (
                    task.due_date.strftime("%Y-%m-%d")  # NOTE: Using due_date
                    if task.due_date
                    else "No deadline"
                )
                print(f"\n{i}. Task ID: {task.id}")
                print(f"   Title: {task.title}")
                print(f"   Description: {task.description}")
                print(f"   Status: {task.status.value}")
                print(f"   Deadline: {deadline_str}")

    def _view_tasks_by_status(self) -> None:
        """Display tasks filtered by status."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("VIEW TASKS BY STATUS".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.title}\n")

            print(f"Valid statuses: {', '.join(self.config.get_valid_statuses())}")
            status_input = input("\nEnter status: ").strip().lower()

            # NOTE: We need to validate the status input against the TaskStatus enum
            try:
                task_status = TaskStatus(status_input)
            except ValueError:
                raise TodoListException(f"Invalid status: '{status_input}'.")

            # NOTE: TaskService.get_tasks_for_project is the correct method name
            tasks = task_service.get_tasks_for_project(self.current_project_id, status=task_status)

            if not tasks:
                print(f"\n📭 No tasks with status '{task_status.value}' found.")
                return

            print(f"\nTasks with status '{task_status.value}':")
            for i, task in enumerate(tasks, 1):
                deadline_str = (
                    task.due_date.strftime("%Y-%m-%d")
                    if task.due_date
                    else "No deadline"
                )
                print(f"\n{i}. Task ID: {task.id}")
                print(f"   Title: {task.title}")
                print(f"   Deadline: {deadline_str}")

    def _edit_task(self) -> None:
        """Handle task editing."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("EDIT TASK".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.title}\n")

            tasks = task_service.get_tasks_for_project(self.current_project_id)

            if not tasks:
                print("📭 No tasks available.")
                return

            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title} (ID: {task.id}) - Status: {task.status.value}")

            choice = input("\nEnter task number or ID to edit: ").strip()

            try:
                if choice.isdigit():
                    choice_int = int(choice)
                    task = tasks[choice_int - 1] if 1 <= choice_int <= len(tasks) else task_service.get_task_by_id(
                        choice_int)
                else:
                    raise ValueError

                print(f"\nCurrent Title: {task.title}")
                print(f"Current Description: {task.description}")
                print(f"Current Status: {task.status.value}")
                print(
                    f"Current Deadline: "
                    f"{task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None'}"
                )

                title = input("\nNew Title (or press Enter to keep current): ").strip()
                description = input("New Description (or press Enter to keep current): ").strip()
                deadline_str = input("New Deadline (YYYY-MM-DD) or press Enter to keep current: ").strip()

                print(f"\nValid statuses: {', '.join(self.config.get_valid_statuses())}")
                status_input = input("New Status (or press Enter to keep current): ").strip()

                update_data = {}
                if title: update_data['title'] = title
                if description: update_data['description'] = description

                if deadline_str:
                    update_data['due_date'] = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                elif deadline_str is not None:
                    # Explicitly setting deadline to None if user inputs blank when current is set
                    update_data['due_date'] = None

                if status_input:
                    # NOTE: Using update_task_status for status changes to trigger business rules
                    task_service.update_task_status(task.id, TaskStatus(status_input.lower()))

                # Use generic update for details, status must be handled separately/by update_task_details
                if update_data:
                    task_service.update_task_details(task.id, **update_data)

                print("\n✅ Task updated successfully!")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _delete_task(self) -> None:
        """Handle task deletion."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("DELETE TASK".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.title}\n")

            tasks = task_service.get_tasks_for_project(self.current_project_id)

            if not tasks:
                print("📭 No tasks available.")
                return

            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title} (ID: {task.id})")

            choice = input("\nEnter task number or ID to delete: ").strip()

            try:
                if choice.isdigit():
                    choice_int = int(choice)
                    task = tasks[choice_int - 1] if 1 <= choice_int <= len(tasks) else task_service.get_task_by_id(
                        choice_int)
                else:
                    raise ValueError

                confirm = input(
                    f"\nAre you sure you want to delete '{task.title}'? (yes/no): "
                ).strip().lower()

                if confirm == "yes":
                    task_service.delete_task(task.id)
                    print("\n✅ Task deleted successfully!")
                else:
                    print("\n❌ Deletion cancelled.")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _mark_task_as_done(self) -> None:
        """Handle marking a task as done."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("MARK TASK AS DONE".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.title}\n")

            all_tasks = task_service.get_tasks_for_project(self.current_project_id)
            pending_tasks = [t for t in all_tasks if t.status != TaskStatus.DONE]

            if not pending_tasks:
                print("📭 No pending tasks to complete.")
                return

            for i, task in enumerate(pending_tasks, 1):
                print(f"{i}. {task.title} (ID: {task.id}) - Status: {task.status.value}")

            choice = input("\nEnter task number or ID to mark as done: ").strip()

            try:
                if choice.isdigit():
                    choice_int = int(choice)
                    task = pending_tasks[choice_int - 1] if 1 <= choice_int <= len(
                        pending_tasks) else task_service.get_task_by_id(choice_int)
                else:
                    raise ValueError

                task_service.mark_task_as_done(task.id)
                print(f"\n✅ Task '{task.title}' marked as done!")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    # --- SEARCH IMPLEMENTATIONS (Using Service Layer) ---
    def _search_projects(self) -> None:
        """Search projects by name or description."""
        print("\n" + "=" * 60)
        print("SEARCH PROJECTS".center(60))
        print("=" * 60)

        query = input("\nEnter search term: ").strip()

        if not query:
            print("\n❌ Search term cannot be empty.")
            return

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)
            projects = proj_service.search_projects(query)

            if not projects:
                print(f"\n📭 No projects found matching '{query}'.")
                return

            print(f"\nFound {len(projects)} project(s):")
            for i, project in enumerate(projects, 1):
                task_count = task_service.get_task_count(project.id)
                print(f"\n{i}. Project ID: {project.id}")
                print(f"   Name: {project.title}")
                print(f"   Description: {project.description}")
                print(f"   Tasks: {task_count}")

    def _search_tasks(self) -> None:
        """Search tasks in current project."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("SEARCH TASKS".center(60))
        print("=" * 60)

        with get_db_context() as db:
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.title}\n")

            query = input("Enter search term: ").strip()

            if not query:
                print("\n❌ Search term cannot be empty.")
                return

            tasks = task_service.search_tasks(self.current_project_id, query)

            if not tasks:
                print(f"\n📭 No tasks found matching '{query}'.")
                return

            print(f"\nFound {len(tasks)} task(s):")
            for i, task in enumerate(tasks, 1):
                print(f"\n{i}. Task ID: {task.id}")
                print(f"   Title: {task.title}")
                print(f"   Status: {task.status.value}")


def main():
    """
    Main entry point for the ToDoList application.
    """
    try:
        cli = TodoListCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")


if __name__ == "__main__":
    main()
