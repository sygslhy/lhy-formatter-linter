# Generic formatter and linter

This package provides the formatter and linter for cmake, C++ and python, ideal for mixed C++ and python developer.

# Getting Started

## Installation

```sh
pip install lhy-formatter-linter
```

## Usage

Formatter or linter will check in your project directory recursively, format or lint all the cmake, C++ python code, by the third-party tools: 
| third-party tool | cmake        | C++             | python | 
|------------------|--------------|-----------------|--------|
| formatter        | cmake-format | clang-format    | yapf   | 
| linter           | cmake-lint   | clang-tidy      | flake8 | 

```sh
lhy -h
usage: lhy [-h] {format,lint} ...

code formatter and linter.

positional arguments:
  {format,lint}
    format       Format code
    lint         Lint code
```

### format code in yout project

```sh
lhy format -p <project-root-dir> 
```
### lint code in yout project

```sh
lhy lint -p <project-root-dir> 
```

## Optional arguments

### Choose languages 
User can choose to format or lint one or two languages by using `-l` or `--language`

```sh
lhy format -p <project-root-dir> -l cmake
```

```sh
lhy lint -p <project-root-dir> -l python
```

```sh
lhy lint -p <project-root-dir> -l cmake cxx
```

### Ignore no-source directories
In project, there must be some sub directories for sure don't contain the source code.

`lhy-formatter-linter` by default ignore the follow directories at the first level under project root dir:

`.git, build, .vscode, .cache, .pytest_cache`

User can add your custom sub directories by optional argument `-id` or `--ignore-dirs`, 
The format of sub directories to ingore could be absolute path or relative path to project root dir

```sh
lhy format -p <project-root-dir> --ignore-dirs .github py_venv <project_root_dir>/docs
```

```sh
lhy lint -p <project-root-dir> --ignore-dirs <project_root_dir>/.github  <project_root_dir>/py_venv docs
```

Or user can specify a txt file which contains the directories to ignore in content, one line for one directoy.

an example named `dirs-to-ignore.txt` text file content
```
<project_root_dir>/.github
<project_root_dir>/py_venv
docs
```
Then use optional argument `-ig`, `--ignore-file` to parse those directories to ignore to formatter or linter.

```sh
lhy format -p <project-root-dir> --ignore-file dirs-to-ignore.txt
```

### Format or lint config files

formatter or linter will use by default the format or lint config file under project root dir.

User can put format and lint config files directly under project root dir to have you own custom formatting or linting rules.


```sh

└── user
    ├── project_root_dir
    │   ├── src
    │   ├── .clang-format
    │   ├── .clang-tidy
    │   ├── .cmake-format
    │   ├── .flake8
    │   └── .style.yapf

```
Or these optional arguments below can specify the config files path:

### formatter config file path arguments
```sh
optional cmake format arguments:
  --cmake-format-config CMAKE_FORMAT_CONFIG
                        Path of cmake format custom config file (default: None)

optional c++ format arguments:
  --clang-format-config CLANG_FORMAT_CONFIG
                        Path of clang format custom config file (default: None)

optional python format arguments:
  --yapf-config YAPF_CONFIG
                        Path of yapf custom config file (default: None)
```

```sh

lhy format -p <project-root-dir> \
    --cmake-format-config <cmake-format-config-absolute-file-path> \
    --clang-format-config <clang-format-config-absolute-file-path> \
    --yapf-config <yapf-config-absolute-file-path>
```


### linter config file path arguments
```sh
optional cmake lint arguments:
  --cmake-lint-config CMAKE_LINT_CONFIG
                        Path of cmake lint custom config file (default: None)

optional c++ format arguments:
  --clang-tidy-config CLANG_TIDY_CONFIG
                        Path of clang tidy custom config file (default: None)

optional python format arguments:
  --flake8-config FLAKE8_CONFIG
                        Path of flake8 custom config file (default: None)
```

```sh

lhy format -p <project-root-dir> \
    --cmake-lint-config <cmake-lint-config-absolute-file-path> \
    --clang-tidy-config <clang-tidy-config-absolute-file-path> \
    --flake8-config <flake8-config-absolute-file-path>
```

## Integrate to CI

This package can be used in CI pipeline, to guarantee all the code on remote is in norm.


### jenkins example.
```jenkins

stage('Check code norm') {
    agent any
    steps {
        dir('script') {
            sh 'lhy lint -p <project_root_dir>'
            sh 'lhy format -p <project_root_dir>'
        }
        sh 'git diff --exit-code'
    }
}

```



# License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/sygslhy/coding_tools/blob/main/LICENSE.md) file for details.