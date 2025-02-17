import argparse
import pathlib
import sys

from utils import exec_on_files, pasre_ignore_dirs, print_exec_info, read_ignore_paths
from utils import DEFAULT_IGNORE_DIRS


def format_code(args):
    assert args.project_root_dir.exists(), 'Path {} does not exist.'
    root_dir = args.project_root_dir.absolute()
    if args.verbose:
        print('root_dir:', root_dir)

    ignore_dirs_list = [
        pathlib.Path(root_dir, ign_dir) for ign_dir in DEFAULT_IGNORE_DIRS
    ]
    if args.ignore_dirs:
        assert isinstance(args.ignore_dirs,
                          list), 'invalid param --ignore-dirs: {}'.format(
                              args.ignore_dirs)
        ignore_dirs = pasre_ignore_dirs(args.ignore_dirs, root_dir)
        ignore_dirs_list += ignore_dirs

    if args.ignore_file:
        assert args.ignore_file.exists(
        ), '--ignore-file: {} does not exist'.format(args.ignore_file)
        ignore_dirs_from_file = read_ignore_paths(args.ignore_file, root_dir)
        ignore_dirs_list += ignore_dirs_from_file

    if args.verbose:
        print('ignore dirs: ', ignore_dirs_list)

    if 'cmake' in args.languages:
        cmake_format_args = [
            '-c', str(pathlib.Path(root_dir, args.cmake_format_config))
        ] if args.cmake_format_config else []

        num_failed, failed_commands = exec_on_files(
            ['cmake-format', '-i'],
            root_dir, ['*.cmake', 'CMakeLists.txt'],
            ignore_dirs_list,
            cmake_format_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('cmake-format', num_failed, failed_commands)

    if 'cxx' in args.languages:
        clang_format_args = [
            '--style=file:{}'.format(
                str(pathlib.Path(root_dir, args.clang_format_config)))
        ] if args.clang_format_config else []

        num_failed, failed_commands = exec_on_files(
            ['clang-format', '-i'],
            root_dir, ['*.h', '*.hpp', '*.cpp', '*.cu'],
            ignore_dirs_list,
            clang_format_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('clang-format', num_failed, failed_commands)

    if 'python' in args.languages:
        yapf_args = [
            '--style {}'.format(str(pathlib.Path(root_dir, args.yapf_config)))
        ] if args.yapf_config else []

        num_failed, failed_commands = exec_on_files(['yapf', '-i'],
                                                    root_dir, ['*.py'],
                                                    ignore_dirs_list,
                                                    yapf_args,
                                                    verbose=args.verbose,
                                                    dry_run=args.dry_run)
        print_exec_info('yapf', num_failed, failed_commands)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        description='Format the code.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument(
        '-p',
        '--project-root-dir',
        required=True,
        type=pathlib.Path,
        help='Path to your project root directory folder.')

    optional_args = parser.add_argument_group('optional arguments')

    optional_args.add_argument('-l',
                               '--languages',
                               choices=['cxx', 'python', 'cmake'],
                               nargs="+",
                               default=['cxx', 'python', 'cmake'],
                               help='Which languages to format')
    optional_args.add_argument(
        '-id',
        '--ignore-dirs',
        nargs="+",
        type=pathlib.Path,
        help='Path of directories where formater ignores')

    optional_args.add_argument(
        '-if',
        '--ignore-file',
        type=pathlib.Path,
        help='Path of directories where formater ignores')

    cmake_args = parser.add_argument_group('optional cmake format arguments')
    cmake_args.add_argument('--cmake-format-config',
                            type=pathlib.Path,
                            help='Path of cmake format custom config file')
    cxx_args = parser.add_argument_group('optional c++ format arguments')
    cxx_args.add_argument('--clang-format-config',
                          type=pathlib.Path,
                          help='Path of clang format custom config file')
    python_args = parser.add_argument_group('optional python format arguments')
    python_args.add_argument('--yapf-config',
                             type=pathlib.Path,
                             help='Path of yapf custom config file')

    optional_args.add_argument('-v',
                               '--verbose',
                               action='store_true',
                               help='enable verbose mode')
    optional_args.add_argument('-d',
                               '--dry-run',
                               action='store_true',
                               help='enable dry-run mode')

    return parser.parse_args(argv)


def main():
    args = parse_command_line(sys.argv[1:])
    format_code(args)


if __name__ == '__main__':
    main()
