# Axonius Automation Project

This repository contains an automated testing framework for an Airbnb-like application using [Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/). The project is organized using the Page Object Model (POM) for maintainable, scalable, and readable test scripts.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Axonius Automation Project is designed to automate end-to-end tests on the Airbnb website. It covers interactions such as setting a destination, selecting check-in/check-out dates, setting the number of guests, filtering search results, and validating reservation details. The tests are written with pytest and Playwright to drive a real browser for testing.

## Features

- **Page Object Model (POM):** 
- **Dynamic Date Selection:** Random check-in/check-out dates within a specified range.
- **Guest Management:** Increase or validate guest counts.
- **Filtering and Navigation:** Apply filters and validate location data.
- **Popup Handling:** Dismiss or interact with popups
- **Logging:** Custom log functions write results to a `temp` folder.
- **Cross-browser Testing:** Tests can be run on Chromium, Firefox, and WebKit (as supported by Playwright).
- **Run with Docker**

## Prerequisites

- **Python 3.8+**  
- **Virtual Environment:** It is recommended to use a virtual environment.

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