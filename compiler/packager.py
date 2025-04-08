
# pylint: disable=wrong-import-order,C0413,missing-module-docstring,missing-function-docstring

# Logging to console
import logging
from logging import log, INFO, WARN, ERROR, CRITICAL, DEBUG # pylint: disable=unused-import
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# System manipulation
from os import remove as os_remove
from subprocess import CompletedProcess, run as run_process # like os.system()
from shutil import rmtree

# Values
from sys import argv as sys_argv, exit
from time import strftime
from random import randint

# 1. Compile the site and get a build number
try:
    from compiler import main as compile_site
except (ModuleNotFoundError, ImportError):
    from compiler.compiler import main as compile_site


def command(cmd: list, *, dryrun: bool=False) -> None:
    """
    Execute a command using the subprocess.run function and log the command before execution.

    Parameters:
    cmd (list): The command to execute. This parameter should be a list of strings, where each
                string represents a part of the command. For example, to execute the command
                "ls -l", the input should be ['ls', '-l'].

    dryrun (bool, optional): A flag indicating whether to perform a dry run (simulate the execution
                            without actually running the command). Default is False.

    Returns:
    None: The function does not return any value. It logs the command before execution and the exit
          code of the command after execution.
    """
    log(INFO, f"\t{cmd}")
    if dryrun:
        log(INFO, "Simulated command execution :)")
        return

    result: CompletedProcess = run_process(cmd, check=True)
    log(INFO, f"Command completed with exit code {result.returncode}")

def main(args: list[str]|None=None):
    if args is None:
        args=[]
    test_mode = '--testmode' in args
    commit_quest = (
        ('--commit' in args and '--no-commit' not in args)
        if ('--commit' in args) or ('--no-commit' in args)
        else None)
    push_quest = (
        ('--push' in args and '--no-push' not in args)
        if ('--push' in args) or ('--no-push' in args)
        else None)
    dry_quest_cmd = ('--dryrun' in args) or ('--dryrun-all' in args)
    dry_quest_all = '--dryrun-all' in args

    build_no = generate_build_no()
    build(build_no, test_mode=test_mode, dryrun=dry_quest_all)
    if ask_commit(commit_quest):
        do_commit(build_no, dryrun=dry_quest_cmd)
    if ask_push(push_quest):
        do_push(dryrun=dry_quest_cmd)
    cleanup()

def generate_build_no() -> tuple[str, dict]:
    """
    Generate a unique build number in the format "YY-MM-DD_hh.mm.ss_RAND".

    The build number consists of the current date, time, and a random 4-digit hexadecimal number.
    The date and time are formatted as "YYYY-MM-DD" and "HH.MM.SS" respectively.
    The random number is generated using the `randint` function from the `random` module.

    Parameters:
    None

    Returns:
    tuple[str, dict]: A tuple containing the generated build number as a string and a dictionary
                    containing the individual components of the build number. The dictionary
                    has the following keys: 'date', 'time', and 'rand'.
    """
    build_id = {
        'date': strftime('%Y-%m-%d'),
        'time': strftime('%H.%M.%S'),
        'rand': hex(randint(0, 0xFFFF))[2:].zfill(4).upper()
    }
    build_no = f"{build_id['date']}_{build_id['time']}_{build_id['rand']}"
    log(INFO, f"Build#: {build_no}")
    return build_no, build_id

def build(build_no_id: tuple[str, dict], test_mode: bool, dryrun: bool):
    build_no, build_id = build_no_id
    log(INFO, f"Building on {build_id['date']} at {build_id['time']} with #{build_id['rand']}")

    log(INFO, "Running compilation...")
    compile_site(test_mode=test_mode, dryrun=dryrun)
    log(INFO, "Compilation finished")
    log(INFO, "Writing build#...")
    with open('BUILD', 'w', encoding='utf-8') as f:
        f.write(build_no)

    log(INFO, "Build complete!")

def ask_commit(definative: bool|None=None) -> bool:
    # 2. Ask weather to commit
    # 2.1. If not, exit early

    if definative is True:
        log(INFO, "Committing via CLI argument")
        return True
    elif definative is False:
        log(INFO, "Not committing via CLI argument")
        return False
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
                return True
            elif weather in ('n', ''):
                log(INFO, "User has decided not to commit.")
                return False
            else:
                print(f"Invalid input {weather}. Please say Y, N, or just press enter.")


def do_commit(build_no: str, dryrun: bool=False):
    # 3. Switch to version branch and commit to the build number file

    log(INFO, "Switching to version branch...")
    command(['git', 'checkout', '-b', 'version'], dryrun=dryrun)
    log(INFO, "Adding build#")
    command(['git', 'add', 'BUILD'], dryrun=dryrun)
    log(INFO, "Committing build#")
    command(["git", "commit", "-m", f"Build #{build_no}"], dryrun=dryrun)

    # 4. Switch to the output branch

    log(INFO, "Switching to output branch...")
    command(['git', 'checkout', '-b', 'output'], dryrun=dryrun)
    log(INFO, "Adding output directory...")
    command(['git', 'add', 'output'], dryrun=dryrun)
    log(INFO, "Adding build#")
    if not dryrun:
        with open("BUILD", 'w', encoding='utf-8') as f:
            f.write(build_no)
    command(['git', 'add', 'BUILD'], dryrun=dryrun)
    log(INFO, "Committing build# and output directory")
    command(["git", "commit", "-m", f"Build #{build_no}"], dryrun=dryrun)

def ask_push(definative: bool|None=None) -> bool:
    # 6. Push version and output branches to github

    if definative is True:
        log(INFO, "Pushing via CLI argument")
        return True
    elif definative is False:
        log(INFO, "Not pushing via CLI argument")
        return False
    else:
        log(INFO, "Requesting weather to push....")
        log(INFO, "Use the terminal to decide what to do")
        log(INFO, "You can avoid this step by passing --with-push")
        while True:
            # Get the first non-empty case-insensitive letter of the input
            weather = input("Push (y/N)? ").lower().strip()[0]
            if weather == 'y':
                log(INFO, "User has decided to push.")
                return True
            elif weather in ('n', ''):
                log(INFO, "User has decided not to push.")
                return False
            else:
                print(f"Invalid input {weather}. Please say Y, N, or just press enter.")

def do_push(dryrun: bool=False):
    log(INFO, "Pushing version branch...")
    command(['git', 'push', 'origin', 'version'], dryrun=dryrun)
    log(INFO, "Pushing output branch...")
    command(['git', 'push', 'origin', 'output'], dryrun=dryrun)
    log(INFO, "Push complete!")

def cleanup():
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

if __name__ == '__main__':
    if '--help' in sys_argv:
        print("""\
        Packager.

        > python3 compiler/packager.py [options]

        DESCRIPTION:
            Compiles the site from content/, static/ and templates/ into the output/.
            Can also commit and push the compiled site.

        OPTIONS:
            --testmode      Will attempt to replace all internal links of / with
                            /output/. This will let the site be hosted from the project
                            root. DO NOT do this in production.
            --commit        Will commit the outputed build to the output branch, and
                            will commit the build number to the version branch. If
                            neither this nor --no-commit are applied, the user will be
                            asked instead.
            --no-commit     Does NOT commit the build and build number. Does not ask the
                            user. Overrides --commit.
            --push          Will push the output and version branches to remote. Has no
                            effect if no commit is made. If neither this nor --no-push
                            are applied, the user will be asked instead.
            --no-push       Does NOT push the output and version branches to remote.
                            Does not ask the user. Overrides --push.
            --dryrun        Will pretend to run commands, but not actually run them,
                            causing no harm. --commit, for example, will still say it's
                            committing the site, but ultimately, not do such a thing.
            --dryrun-all    Does --dryrun, but also will not write files from the
                            compilation of the site. --dryrun only stops commands, while
                            --dryrun-all stops all manipulation. The site will still
                            be fully compiled, but only in memory, and that will be
                            cleared when the program exits.
        """)
        exit(0)
    main(sys_argv)
