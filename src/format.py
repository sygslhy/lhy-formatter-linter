from utils import exec_on_files

import argparse
import sys
import pathlib


def _print_format_info(exec, num_failed, failed_commands):
    print('{} execution finished, {} failed'.format(exec, num_failed))
    if num_failed > 0:
        print('{} failed commands: {}'.format(exec, failed_commands))


def _pasre_ignore_dirs(ignore_dirs, ignore_config, root_dir):
    ign_dirs = []
    for ign_dir in ignore_dirs:
        abs_ign_dir = pathlib.Path(root_dir, ign_dir)
        if abs_ign_dir.exists():
            ign_dirs.append(abs_ign_dir)
        else:
            print('Warning: ignore dir {} is not valid.'.format(
                str(abs_ign_dir)))
    return ign_dirs


def format_code(args):
    assert args.input_path.exists(), 'Path {} does not exist.'
    root_dir = args.input_path.absolute()

    if args.ignore_dirs:
        assert isinstance(args.ignore_dirs,
                          list), 'invalid param --ignore-dirs: {}'.format(
                              args.ignore_dirs)
    if args.ignore_config:
        assert isinstance(
            args.ignore_config,
            pathlib.Path), 'invalid param --ignore_config: {}'.format(
                args.ignore_dirs)

    ignore_dirs_list = _pasre_ignore_dirs(args.ignore_dirs, args.ignore_config,
                                          root_dir)
    if args.verbose:
        print('ignore dirs: ', ignore_dirs_list)

    cmake_format_args = [
        '-c',
        str(pathlib.Path(root_dir, args.cmake_format_config)), '-i'
    ] if args.cmake_format_config else ['-i']
    num_failed, failed_commands = exec_on_files('cmake-format',
                                                root_dir,
                                                ['*.cmake', 'CMakeLists.txt'],
                                                ignore_dirs_list,
                                                cmake_format_args,
                                                verbose=args.verbose,
                                                dry_run=args.dry_run)
    _print_format_info('cmake-format', num_failed, failed_commands)

    clang_format_args = [
        '--style={}'.format(
            str(pathlib.Path(root_dir, args.clang_format_config))), '-i'
    ] if args.clang_format_config else ['-i']
    num_failed, failed_commands = exec_on_files(
        'clang-format',
        root_dir, ['*.h', '*.hpp', '*.cpp', '*.cu'],
        ignore_dirs_list,
        clang_format_args,
        verbose=args.verbose,
        dry_run=args.dry_run)
    _print_format_info('clang-format', num_failed, failed_commands)

    yapf_args = [
        '--style {}'.format(str(pathlib.Path(root_dir, args.yapf_config))),
        '-i'
    ] if args.yapf_config else ['-i']
    num_failed, failed_commands = exec_on_files('yapf',
                                                root_dir, ['*.py'],
                                                ignore_dirs_list,
                                                yapf_args,
                                                verbose=args.verbose,
                                                dry_run=args.dry_run)
    _print_format_info('yapf', num_failed, failed_commands)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        description='Format the code.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i',
                               '--input-path',
                               required=True,
                               type=pathlib.Path,
                               help='Path to your code repository folder')

    optional_args = parser.add_argument_group('optional arguments')

    optional_args.add_argument('-l',
                               '--languages',
                               choices=['cxx', 'python', 'cmake'],
                               nargs="+",
                               default=['cxx', 'python', 'cmake'],
                               help='Which languages to format')

    optional_args.add_argument(
        '--ignore-dirs',
        nargs="+",
        type=pathlib.Path,
        help='Path of directories where formater ignores')

    optional_args.add_argument(
        '--ignore-config',
        type=pathlib.Path,
        help='Path of the config fiel to define directories to ignore')

    optional_args.add_argument('--cmake-format-config',
                               type=pathlib.Path,
                               help='Path of cmake format custom config file')

    optional_args.add_argument('--clang-format-config',
                               type=pathlib.Path,
                               help='Path of clang format custom config file')

    optional_args.add_argument('--yapf-config',
                               type=pathlib.Path,
                               help='Path of yapf custom config file')

    optional_args.add_argument('--isort-config',
                               type=pathlib.Path,
                               help='Path of isort custom config file')
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
