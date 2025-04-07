
# pylint: disable=wrong-import-order,C0413,missing-module-docstring

# Logging to console
import logging
from logging import log, INFO, WARN, ERROR, CRITICAL, DEBUG # pylint: disable=unused-import
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# System manipulation
from os import remove as os_remove
from subprocess import CompletedProcess, run as run_process # like os.system()
from shutil import rmtree

# Values
from sys import argv as sys_argv, exit # pylint: disable=redefined-builtin
from time import strftime
from random import randint

# 1. Compile the site and get a build number
try:
    from compiler import main as compile_site
except (ModuleNotFoundError, ImportError):
    from compiler.compiler import main as compile_site

# YY-MM-DD_hh.mm.ss_RAND
# Where RAND is a random 4-digit hex integer
build_id = {
    'date': strftime('%Y-%m-%d'),
    'time': strftime('%H.%M.%S'),
    'rand': hex(randint(0, 0xFFFF))[2:].zfill(4).upper()
}
build_no = f"{build_id['date']}_{build_id['time']}_{build_id['rand']}"
log(INFO, f"Build#: {build_no}")
log(INFO, f"Building on {build_id['date']} at {build_id['time']} with #{build_id['rand']}")

log(INFO, "Running compilation...")
compile_site()
log(INFO, "Compilation finished")
log(INFO, "Writing build#...")
with open('BUILD', 'w', encoding='utf-8') as f:
    f.write(build_no)

log(INFO, "Build complete!")

# 2. Ask weather to commit
# 2.1. If not, exit early

if '--with-commit' in sys_argv:
    log(INFO, "Committing via CLI argument")
elif '--no-commit' in sys_argv:
    log(INFO, "Not committing via CLI argument")
    exit(0)
else:
    log(INFO, "Requesting weather to commit....")
    log(INFO, "Use the terminal to decide what to do")
    log(INFO, "You can avoid this step by passing --with-commit")
    while True:
        # Get the first non-empty case-insensitive letter of the input
        weather = input("Commit (y/N)? ").lower().strip()
        if len(weather) != 0:
            weather = weather[0]
        if weather == 'y':
            log(INFO, "User has decided to commit.")
            break
        elif weather in ('n', ''):
            log(INFO, "User has decided not to commit.")
            exit(0)
        else:
            print(f"Invalid input {weather}. Please say Y, N, or just press enter.")

# 3. Switch to version branch and commit to the build number file


def command(cmd: list) -> None:
    """
    Execute a command using the subprocess.run function and log the command before execution.

    Parameters:
    command (list): The command to execute.

    Returns:
    None: The function does not return any value.
    """
    log(INFO, f"\t{cmd}")
    result: CompletedProcess = run_process(cmd, check=True)
    log(INFO, f"Command completed with exit code {result.returncode}")

log(INFO, "Switching to version branch...")
command(['git', 'checkout', '-b', 'version'])
log(INFO, "Adding build#")
command(['git', 'add', 'BUILD'])
log(INFO, "Committing build#")
command(["git", "commit", "-m", f"Build #{build_no}"])

# 4. Switch to the output branch

log(INFO, "Switching to output branch...")
command(['git', 'checkout', '-b', 'output'])
log(INFO, "Adding output directory...")
command(['git', 'add', 'output'])
log(INFO, "Adding build#")
with open("BUILD", 'w', encoding='utf-8') as f:
    f.write(build_no)
command(['git', 'add', 'BUILD'])
log(INFO, "Committing build# and output directory")
command(["git", "commit", "-m", f"Build #{build_no}"])
# 6. Push version and output branches to github

if '--with-push' in sys_argv:
    log(INFO, "Pushing via CLI argument")
elif '--no-push' in sys_argv:
    log(INFO, "Not pushing via CLI argument")
    exit(0)
else:
    log(INFO, "Requesting weather to push....")
    log(INFO, "Use the terminal to decide what to do")
    log(INFO, "You can avoid this step by passing --with-push")
    while True:
        # Get the first non-empty case-insensitive letter of the input
        weather = input("Push (y/N)? ").lower().strip()[0]
        if weather == 'y':
            log(INFO, "User has decided to push.")
            break
        elif weather in ('n', ''):
            log(INFO, "User has decided not to push.")
            exit(0)
        else:
            print(f"Invalid input {weather}. Please say Y, N, or just press enter.")


log(INFO, "Pushing version branch...")
command(['git', 'push', 'origin', 'version'])
log(INFO, "Pushing output branch...")
command(['git', 'push', 'origin', 'output'])

# 7. Go back to main

log(INFO, "Switching back to main...")
command(['git', 'checkout','main'])

# 8. Delete the output directory


log(INFO, "Cleaning up.....")

log(INFO, "Deleting output directory...")
rmtree('output')
log(INFO, "Deleting build# file...")
os_remove('BUILD')

log(INFO, "Cleanup complete!")
