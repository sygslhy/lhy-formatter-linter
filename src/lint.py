import argparse
import sys
import pathlib

def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        description='Lint the code.',
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
                               help='Which languages to lint')

    required_args.add_argument('-s',
                               '--skip-dirs',
                               nargs="+",
                               type=pathlib.Path,
                               help='Path of directories where linter ignores')
    
    required_args.add_argument('--cmake-lint-config',
                               type=pathlib.Path,
                               help='Path of cmake lint custom config file')
        
    required_args.add_argument('--clang-tidy-config',
                               type=pathlib.Path,
                               help='Path of clang tidy custom config file')
    
    required_args.add_argument('--flake8-config',
                               type=pathlib.Path,
                               help='Path of flake8 custom config file')


    return parser.parse_args(argv)

def main():
    args = parse_command_line(sys.argv[1:])

    try:
        pass
    except Exception as e:
        sys.exit("Exception caught in code-lint, check the error log: {}.".
                 format(str(e)))


if __name__ == '__main__':
    main()
