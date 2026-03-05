import sys
import os
import argparse
from datetime import datetime, timezone
from rich import print
from .runner import execute
from .monitor import monitor
from .analyzer import analyze
from .database import init_db, Session
from .models import Run


def cli():
    parser = argparse.ArgumentParser(
        prog="script-run",
        description="Run scripts with performance logging."
    )

    parser.add_argument(
        "path",
        help="Path to script file"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run program interactively (required for GUI apps)"
    )

    args = parser.parse_args()

    path = args.path
    

    if not os.path.exists(path):
        print("[red]File not found.[/red]")
        sys.exit(1)

    init_db()

    print("[green]Starting execution!...[/green]")

    start = datetime.now(timezone.utc)

    try:
        proc, script_type = execute(path)
    except Exception as e:
        print(f"[red]{e}[/red]")
        sys.exit(1)

    stats = monitor(proc)

    stdout, stderr = proc.communicate()
    end = datetime.now(timezone.utc)

    status = analyze(stdout, stderr, proc.returncode)

    session = Session()

    run = Run(
        script_name=os.path.basename(path),
        script_type=script_type,
        start_time=start,
        end_time=end,
        duration=(end - start).total_seconds(),
        status=status,
        exit_code=proc.returncode,
        stdout=stdout,
        stderr=stderr,
        **stats
    )

    session.add(run)
    session.commit()
    
    
    print("\n[bold green]Execution Completed![/bold green]")
    print(f"Status: {status}")
    print(f"Duration: {run.duration:.2f}s")
    print(f"Average CPU usage: {run.avg_cpu:.2f}%")
    print(f"Max CPU usage: {run.max_cpu:.2f}%")
    print(f"Average RAM usage: {run.avg_mem:.2f}%")
    print(f"Max RAM usage: {run.max_mem:.2f}%")
    print(f"Average GPU usage: {run.avg_gpu:.2f}%")