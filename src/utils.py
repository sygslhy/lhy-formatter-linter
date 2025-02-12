import subprocess


def exec_on_files(executable, root_dir, expressions, ignore_dirs, args):
    output = subprocess.check_output([executable, '--version']).strip().decode('utf-8')
    print('{} --version\n{}'.format(executable, output))


