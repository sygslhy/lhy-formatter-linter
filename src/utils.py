import subprocess
import re
import os
from packaging import version


def _get_exec_version(exec):
    output = subprocess.check_output([exec, '--version']).decode('utf-8')
    return (version.Version(re.search(r'([\d.]+)', output).group(1)))


def get_subfolders_recursive(path):
    """
    Returns a list of all subfolders in the given path, recursively.
    """
    subfolders = []
    for item in path.iterdir():
        if item.is_dir():
            subfolders.append(item)
            subfolders.extend(get_subfolders_recursive(item))
    return subfolders


def exec_on_files(exec,
                  root_dir,
                  expressions,
                  ignore_dirs,
                  exec_args,
                  verbose=False,
                  dry_run=False):
    """
    Launch exec with given args on filtered files. Executable name is given as 1st argument

    Parameters
    ----------
    exec: string
        executable name.
    root_dir: string
        root directory pathname from which the search has to be launched
    expressions: list of strings
        list of expressions defining the files on which executable has to be launched
    ignore_dirs: list os strings
        list of directories in root_dir to exclude from search.
    exec_args: list of strings
        list of arguments to be passed to executable.
    """
    version_num = _get_exec_version(exec)
    if verbose:
        print('{} --version: {}'.format(exec, version_num))
        print('root_dir:', root_dir)
    num_failed = 0
    failed_commands = []
    all_folders = get_subfolders_recursive(root_dir)
    all_folders.append(root_dir)
    filtered_folders = [
        folder for folder in all_folders if not any(
            folder.is_relative_to(ignore_dir) for ignore_dir in ignore_dirs)
    ]
    filtered_folders = list(set(filtered_folders))
    all_files = []
    for d in filtered_folders:
        for expr in expressions:
            files = list(d.glob(expr))
            if files:
                all_files += files
                command_line = ' '.join(map(str, [exec] + exec_args + files))
                if verbose:
                    print(command_line)
                if dry_run:
                    print('dry-run: ' + command_line)
                else:
                    ret = subprocess.run([exec] + exec_args + files)
                    if ret.returncode != 0:
                        num_failed += 1
                        failed_commands.append(' '.join(
                            map(str, [exec] + exec_args + files)))

    return num_failed, failed_commands
