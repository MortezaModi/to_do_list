import click
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# Import the specific command function we want to run periodically
from app.commands.autoclose_overdue import autoclose_overdue


# A simple wrapper function to execute the click command
def run_job_wrapper(command):
    """
    Wraps a click command function so it can be executed by the scheduler.
    This ensures the scheduler runs the job logic without needing the CLI context.
    """
    try:
        command()
    except Exception as e:
        # In a real application, you would use a robust logger here
        print(f"Scheduler Job Failed ({command.name}): {e}")


@click.command("scheduler:start")
@click.option('--daemon', is_flag=True, default=False, help='Run the scheduler in the background as a daemon.')
def start_scheduler_cli(daemon: bool):
    """
    Starts the in-process job scheduler for background tasks.
    """

    # 1. Initialize the Scheduler
    scheduler = BackgroundScheduler()

    # 2. Add the Jobs
    # Example: Run the autoclose_overdue command every day at 2:00 AM
    scheduler.add_job(
        func=lambda: run_job_wrapper(autoclose_overdue()),  # Pass the command wrapper #SUS (autoclose_overdue)
        trigger='cron',
        hour=2,
        minute=0,
        id='autoclose_overdue_tasks',
        name='Autoclose Overdue Tasks',
        misfire_grace_time=3600  # Wait up to 1 hour for a missed job
    )

    # 3. Start the Scheduler
    try:
        print("--- Starting Application Scheduler ---")
        scheduler.start()
        print(f"Scheduler started successfully. Jobs running: {scheduler.get_jobs()}")

        # 4. Graceful Shutdown
        # Ensures that background jobs are stopped when the interpreter exits.
        atexit.register(lambda: scheduler.shutdown(wait=False))

        # 5. Keep the process alive (if not running as a daemon)
        if not daemon:
            print("Scheduler running in foreground. Press Ctrl+C to exit.")
            while True:
                time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped by user.")
        scheduler.shutdown()
    except Exception as e:
        print(f"A fatal error occurred in the scheduler process: {e}")
        scheduler.shutdown()


if __name__ == '__main__':
    start_scheduler_cli(daemon=False)
