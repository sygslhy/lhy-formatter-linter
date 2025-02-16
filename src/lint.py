import argparse
import pathlib
import sys

from utils import exec_on_files, pasre_ignore_dirs, print_exec_info


def lint_code(args):
    assert args.project_root_dir.exists(), 'Path {} does not exist.'
    root_dir = args.project_root_dir.absolute()
    if args.verbose:
        print('root_dir:', root_dir)
    if args.ignore_dirs:
        assert isinstance(args.ignore_dirs,
                          list), 'invalid param --ignore-dirs: {}'.format(
                              args.ignore_dirs)

    ignore_dirs_list = pasre_ignore_dirs(args.ignore_dirs, root_dir)
    if args.verbose:
        print('ignore dirs: ', ignore_dirs_list)

    if 'cmake' in args.languages:
        cmake_lint_args = [
            '-c', str(pathlib.Path(root_dir, args.cmake_lint_config))
        ] if args.cmake_lint_config else []

        num_failed, failed_commands = exec_on_files(
            ['cmake-lint'],
            root_dir, ['*.cmake', 'CMakeLists.txt'],
            ignore_dirs_list,
            cmake_lint_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('cmake-lint', num_failed, failed_commands)

    if 'cxx' in args.languages:
        clang_tidy_args = [
            '--style=file:{}'.format(
                str(pathlib.Path(root_dir, args.clang_tidy_config)))
        ] if args.clang_tidy_config else []

        num_failed, failed_commands = exec_on_files(
            ['clang-tidy'],
            root_dir, ['*.h', '*.hpp', '*.cpp', '*.cu'],
            ignore_dirs_list,
            clang_tidy_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('clang-tidy', num_failed, failed_commands)

    if 'python' in args.languages:
        flake8_args = [
            '--style {}'.format(str(pathlib.Path(root_dir,
                                                 args.flake8_config)))
        ] if args.flake8_config else []

        num_failed, failed_commands = exec_on_files(['flake8'],
                                                    root_dir, ['*.py'],
                                                    ignore_dirs_list,
                                                    flake8_args,
                                                    verbose=args.verbose,
                                                    dry_run=args.dry_run)
        print_exec_info('flake8', num_failed, failed_commands)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        description='lint the code.',
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
                               help='Which languages to lint')
    optional_args.add_argument('--ignore-dirs',
                               nargs="+",
                               type=pathlib.Path,
                               help='Path of directories where linter ignores')

    cmake_args = parser.add_argument_group('optional cmake lint arguments')
    cmake_args.add_argument('--cmake-lint-config',
                            type=pathlib.Path,
                            help='Path of cmake lint custom config file')
    cxx_args = parser.add_argument_group('optional c++ format arguments')
    cxx_args.add_argument('--clang-tidy-config',
                          type=pathlib.Path,
                          help='Path of clang tidy custom config file')
    python_args = parser.add_argument_group('optional python format arguments')
    python_args.add_argument('--flake8-config',
                             type=pathlib.Path,
                             help='Path of flake8 custom config file')

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
    lint_code(args)


if __name__ == '__main__':
    main()
