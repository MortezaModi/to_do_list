import click
# Assuming get_db_context is in app.db.session
from app.db.session import get_db_context
from app.services import TaskService


@click.command("tasks:autoclose-overdue")
def autoclose_overdue():
    """
    Auto-close all overdue tasks: deadline < now AND status != done.
    """
    click.echo("Starting overdue task processing...")

    # 1. Use the session context manager
    try:
        with get_db_context() as db:
            service = TaskService(db)
            # 2. Call the service method to execute logic
            count = service.autoclose_overdue_tasks()

        click.echo(f"Successfully closed {count} overdue tasks.")
    except Exception as e:
        click.echo(f"An error occurred during autoclose: {e}", err=True)

# Note: The `if __name__ == "__main__":` block is usually omitted in this structure,
# as it will be run via the CLI entry point (`app/cli/console.py`).
