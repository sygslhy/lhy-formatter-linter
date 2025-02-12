from utils import exec_on_files

import argparse
import sys
import pathlib



def format_code(args):
    assert args.input_path.exists(), 'Path {} does not exist.'
    root_dir = args.input_path

    exec_on_files('cmake-format', root_dir, None, [], None)
    exec_on_files('clang-format', root_dir, None, [], None)
    exec_on_files('yapf', root_dir, None, [], None)

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
    required_args.add_argument('-l',
                               '--languages',
                               choices=['cxx', 'python', 'cmake'],
                               nargs="+",
                               default=['cxx','python', 'cmake'],
                               help='Which languages to format')

    required_args.add_argument('-s',
                               '--skip-dirs',
                               nargs="+",
                               type=pathlib.Path,
                               help='Path of directories where formater ignores')
    
    required_args.add_argument('--cmake-format-config',
                               type=pathlib.Path,
                               help='Path of cmake format custom config file')
        
    required_args.add_argument('--clang-format-config',
                               type=pathlib.Path,
                               help='Path of clang format custom config file')
    
    required_args.add_argument('--yapf-config',
                               type=pathlib.Path,
                               help='Path of yapf custom config file')
    
    required_args.add_argument('--isort-config',
                               type=pathlib.Path,
                               help='Path of isort custom config file')

    return parser.parse_args(argv)

def main():
    args = parse_command_line(sys.argv[1:])

    try:
        format_code(args)
    except Exception as e:
        sys.exit("Exception caught in code-format, check the error log: {}.".
                 format(str(e)))


if __name__ == '__main__':
    main()
