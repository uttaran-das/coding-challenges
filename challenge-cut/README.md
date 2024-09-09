# Cut Tool

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## About

[Challenge Cut from John Crickett](https://codingchallenges.fyi/challenges/challenge-cut/)

## Features

- **Feature 1**: It can cut based on the field number(s).
- **Feature 2**: It can cut based on different delimiters.
- **Feature 3**: Integrates with other Linux tools.

## Installation

The file can be used as a stand alone file, so you don't need to install anything for Linux and Windows. You need to run the python script itself for running this on MacOS

### Linux
Download the [cut](https://github.com/uttaran-das/coding-challenges/blob/main/challenge-cut/cut) file.

### Windows
Download the [cut.exe](https://github.com/uttaran-das/coding-challenges/blob/main/challenge-cut/cut.exe) file.

### MacOS
Make sure you already have python installed in your machine. [Guide](https://docs.python.org/3/using/mac.html)

**1**. Download these two files [cut.py](https://github.com/uttaran-das/coding-challenges/blob/main/challenge-cut/cut.py) and [requirements.txt](https://github.com/uttaran-das/coding-challenges/blob/main/challenge-cut/requirements.txt) and put them in a folder of your choice.

**2**. Create a virtual environment in that folder. [Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

**3**. Run
```
pip install -r requirements.txt
```

## Usage

Arguments:

```
file: Path to the file. Use '-' to read from standard input.
```

Options:

```
-f or --field : Field number to extract (default is 1). Comma or whitespace separated.
-d or --delimiter : Delimiter character to use. Default is tab.
```

#### Example:

This example is for linux. Use cut.exe file for Windows and cut.py for MacOS.

```
./cut -d, -f"1 2" fourchords.csv
```

## Contributing

*  **Step 1:** Fork the Project

*  **Step 2:** Create your Feature Branch (git checkout -b feature/AmazingFeature)

*  **Step 3:** Commit your Changes (git commit -m 'Add some AmazingFeature')

*  **Step 4:** Push to the Branch (git push origin feature/AmazingFeature)

*  **Step 5:** Open a Pull Request