# Face-Track-Attendance

Camera-based attendance system using advanced Python modules for face detection and attendance monitoring.

## Badges

[![Build Status](https://img.shields.io/github/actions/workflow/status/Pruthvi-123-prog/Face-Track-Attendance/main.yml?branch=main)](https://github.com/Pruthvi-123-prog/Face-Track-Attendance/actions)
[![Stars](https://img.shields.io/github/stars/Pruthvi-123-prog/Face-Track-Attendance?style=social)](https://github.com/Pruthvi-123-prog/Face-Track-Attendance/stargazers)
[![Forks](https://img.shields.io/github/forks/Pruthvi-123-prog/Face-Track-Attendance?style=social)](https://github.com/Pruthvi-123-prog/Face-Track-Attendance/network/members)
[![Issues](https://img.shields.io/github/issues/Pruthvi-123-prog/Face-Track-Attendance)](https://github.com/Pruthvi-123-prog/Face-Track-Attendance/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/Pruthvi-123-prog/Face-Track-Attendance)](https://github.com/Pruthvi-123-prog/Face-Track-Attendance/pulls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [File Structure Overview](#file-structure-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Description

This project implements a camera-based attendance system that leverages Python's capabilities in image processing and face recognition. It's designed to automate and streamline the attendance tracking process.

## Features

- Real-time face detection using camera input.
- Automated attendance logging.
- Uses Python and related libraries for image processing and data management.
- Dockerized deployment (Dockerfile included).

## Tech Stack

- Python
- HTML
- Dockerfile

## File Structure Overview

```text
.
├── .gitignore
├── Dockerfile
├── README.md
├── data/
├── login/
├── login_project/
├── manage.py
└── requirements.txt
```

## Prerequisites

```
Python 3.6+
Docker (if using Dockerfile)
pip (for installing dependencies)
```

## Installation

```bash
git clone https://github.com/Pruthvi-123-prog/Face-Track-Attendance.git
cd Face-Track-Attendance
python -m pip install -r requirements.txt
```

## Usage

```bash
# Apply database migrations
python manage.py migrate

# Run the development server
python manage.py runserver

# For Docker deployment
docker build -t face-track-attendance .
docker run -p 8000:8000 face-track-attendance
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.  
Make sure to update tests as appropriate.

## License

This project is licensed under the MIT License.

## Contact

Pruthvi - [GitHub Repo](https://github.com/Pruthvi-123-prog/Face-Track-Attendance) - pruthvis2004@gmail.com
