# Axonius Automation Project

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Running Tests with Docker](#running-tests-with-docker)
- [Project Structure](#project-structure)


## Overview

 Automate end-to-end tests on the Airbnb website. covers interactions such as setting a destination, selecting check-in/check-out dates, setting the number of guests, filtering search results, and validating reservation details. The tests are written with pytest and Playwright.

## Features

- **Page Object Model** 
- **Dynamic Date Selection:** Random check-in/check-out dates within a specified range.
- **Guest Management:** Increase or validate guest counts.
- **Filtering and Navigation:** Apply filters and validate location data.
- **Popup Handling:** Dismiss or interact with popups
- **Logging:** Custom log functions write results to a `temp` folder..
- **Run test using Docker**

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Yaronmd/axonius_automation_project.git
   cd axonius_automation_project
   ```

2. **Create and activate the virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```
3. **Install requirements**
   ```bash
    pip install -r requirements.txt
   ```
4. **Install playwirght**
    ```bash
    python -m playwright install
    ```
    or 
     ```bash
    playwright install
    ```
## Running Tests
- **Make sure your virtual environment is activated.** 
```bash
pytest -s
```
- **can use flaky to rerun if failed** 
```bash
pytest -s --reruns 2 --reruns-delay 1
```
## Running Tests with Docker

### IMPORTANT: When running in Docker, make sure to enable headless mode:
### Example in conftest:
``` browser = playwright.chromium.launch(headless=True)```

1. **Create Image run it will install and exectue the tests and than delete image** 

```bash
docker build -t python-playwright-test .
docker run --rm python-playwright-test
```
2. **Create Image run tests and get content from temp folder**
```bash
docker run -it --name my_test_container python-playwright-test /bin/bash
```
- **Validate temp exists with conetent**
```bash
cd app/temp 
ls -a 
```
- **Open new tarminal and copy temp folder**
```bash
docker cp my_test_container:app/temp/ ./temp_copy
```
- **Delete container**
```bash
docker rm -f my_test_container
```
## Project Structure
```    
axonius_automation_project/
├── pages/ 
│   ├── base_page.py
|   |── main_page.py
|   |── place_page.py
|   |── reserve_page.py
│   ├── panels/
│   │   ├── check_in_out_panel.py
│   │   ├── filter_panel.py
│   │   └── guests_panel.py
├── tests/
│   ├── conftest.py
│   └── test_main_flows.py
├── helpers/
│   ├── logger.py
│   ├── parse_helper.py
│   ├── write_to_file_helper.py 
│   └── countries_with_codes.json
├── temp/
├── Dockerfile
├── requirements.txt
└── README.md
```

