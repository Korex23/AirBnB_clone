# 0x00. AirBnB clone - The console

## 0x00.Table of contents

- [0x01 Introduction](#0x01-Introduction)
- [0x02 Environment](#0x02-Environment)
- [0x03 Installation](#0x03-Installation)
- [0x04 Testing](#0x04-Testing)
- [0x05 Usage](#0x05-Usage)
- [0x06 Authors](#0x06-Authors)

## 0x01 Introduction

Team project to build a clone of [AirBnB](https://www.airbnb.com/).

The console is a command line interpreter to manage abstraction between objects, manipulation of objects and their storage in a file.

The console will perform the following tasks:

- create a new object
- retrieve an object from a json file
- perform operations on objects
- destroy an object

### Storage

Storage for all classes are handled by the `Storage` engine in the `FileStorage` Class.

## 0x02 Environment

<!-- ubuntu -->

<a href="https://ubuntu.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Ubuntu&color=E95420&logo=Ubuntu&logoColor=E95420&labelColor=2F333A" alt="Suite CRM"></a> <!-- python--> <a href="https://www.python.org" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Python&color=FFD43B&logo=python&logoColor=3776AB&labelColor=2F333A" alt="python"></a> </a> <!-- vim --> <a href="https://www.vim.org/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Vim&color=019733&logo=Vim&logoColor=019733&labelColor=2F333A" alt="Suite CRM"></a> <!-- git --> <a href="https://git-scm.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Git&color=F05032&logo=Git&logoColor=F05032&labelColor=2F333A" alt="git distributed version control system"></a> <!-- github --> <a href="https://github.com" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=GitHub&color=181717&logo=GitHub&logoColor=f2f2f2&labelColor=2F333A" alt="Github"></a>

 <!-- Style guidelines -->

- Style guidelines:
  - [pycodestyle (version 2.8.\*)](https://pypi.org/project/pycodestyle/)
  - [PEP8](https://pep8.org/)

All the development and testing was runned over an operating system Ubuntu 20.04 LTS using programming language Python 3.8.5. The editors used were VIM 8.1.2269. Control version using Git 2.25.1.

## 0x03 Installation

```bash
git clone https://github.com/Arnthorny/AirBnB_clone.git
```

change to the `AirBnb` directory and run the command:

```bash
 ./console.py
```

### Execution

In interactive mode

```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) quit
$
```

in Non-interactive mode

```bash
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
```

## 0x04 Testing

All the test are defined in the `tests` folder.

### Documentation

- Modules:

```python
python3 -c 'print(__import__("my_module").__doc__)'
```

- Classes:

```python
python3 -c 'print(__import__("my_module").MyClass.__doc__)'
```

- Functions (inside and outside a class):

```python
python3 -c 'print(__import__("my_module").my_function.__doc__)'
```

and

```python
python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'
```

### Python Unit Tests

- unittest module
- File extension `.py`
- Files and folders start with `test_`
- Organization for: `models/base.py`, unit tests in: `tests/test_models/test_base.py`
- Execution command: `python3 -m unittest discover tests` to run all tests
- or: `python3 -m unittest tests/test_models/test_base.py` to run specific test

### run test in interactive mode

```bash
echo "python3 -m unittest discover tests" | bash
```

### run test in non-interactive mode

To run the tests in non-interactive mode, and discover all the test, you can use the command:

```bash
python3 -m unittest discover tests
```

## 0x05 Usage

- Start the console in interactive mode:

```bash
$ ./console.py
(hbnb)
```

- Use help to see the available commands:

```bash
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb)
```

- Quit the console:

```bash
(hbnb) quit
$
```

### Commands

> The commands are displayed in the following format _command / usage / example with output_

- Create

> _Create a new instance for a given class. The class' ID is printed and the instance is saved to a file.json file._

```bash
create <class>
```

```bash
(hbnb) create User
e6ef4eca-85f2-4f13-b7e9-e41701156ebd
(hbnb)
```

- Show

```bash
show <class> <id>
```

```bash
(hbnb) show User e6ef4eca-85f2-4f13-b7e9-e41701156ebd
[User] (e6ef4eca-85f2-4f13-b7e9-e41701156ebd) {'id': 'e6ef4eca-85f2-4f13-b7e9-e41701156ebd', 'created_at': datetime.datetime(2023, 8, 14, 13, 58, 24, 448794), 'updated_at': datetime.datetime(2023, 8, 14, 13, 58, 24, 448855)}
(hbnb)
```

- Destroy

> _Deletes an instance of a given class with a given ID._ > _Update the file.json_

```bash
(hbnb) create User
e79e744a-55d4-45a3-b74a-ca5fae74e0e2
(hbnb) destroy User e79e744a-55d4-45a3-b74a-ca5fae74e0e2
(hbnb) show User e79e744a-55d4-45a3-b74a-ca5fae74e0e2
** no instance found **
(hbnb)
```

- all

> _Prints all string representation of all instances of a given class._ > _Print all classes if no class arg is passed._

```bash
(hbnb) create User
e6ef4eca-85f2-4f13-b7e9-e41701156ebd
(hbnb) all User
["[User] (e6ef4eca-85f2-4f13-b7e9-e41701156ebd) {'id': 'e6ef4eca-85f2-4f13-b7e9-e41701156ebd', 'created_at': datetime.datetime(2023, 8, 14, 13, 58, 24, 448794), 'updated_at': datetime.datetime(2023, 8, 14, 13, 58, 24, 448855)}"]
(hbnb)
```

- count

> _Prints the number of instances for a given class._

```bash
(hbnb) create City
abc2b83f-fe8e-4159-a037-b778052d604c
(hbnb) create City
ea9eae14-5d14-4cc4-b297-f678721c709d
(hbnb) count City
2
(hbnb)
```

- update

> _Updates an instance based on the class name, id, and keyword args passed._ > _Updates the stored json file too_

```bash
(hbnb) create User
f7f46172-8dfc-4c7b-926f-d7196078da93
(hbnb) show User f7f46172-8dfc-4c7b-926f-d7196078da93
[User] (f7f46172-8dfc-4c7b-926f-d7196078da93) {'id': 'f7f46172-8dfc-4c7b-926f-d7196078da93', 'created_at': datetime.datetime(2023, 8, 14, 13, 55, 56, 820244), 'updated_at': datetime.datetime(2023, 8, 14, 13, 55, 56, 820301)}
(hbnb) update User f7f46172-8dfc-4c7b-926f-d7196078da93 first_name "Git"
(hbnb) show User f7f46172-8dfc-4c7b-926f-d7196078da93
[User] (f7f46172-8dfc-4c7b-926f-d7196078da93) {'id': 'f7f46172-8dfc-4c7b-926f-d7196078da93', 'created_at': datetime.datetime(2023, 8, 14, 13, 55, 56, 820244), 'updated_at': datetime.datetime(2023, 8, 14, 13, 56, 26, 77964), 'first_name': 'Git'}
(hbnb)
```
# AirBnB_clone
