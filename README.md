# Face Recognition Service

[![Web-App CI](https://github.com/software-students-fall2023/5-final-project-jungle-gap/actions/workflows/web_app_test.yml/badge.svg)](https://github.com/software-students-fall2023/5-final-project-jungle-gap/actions/workflows/web_app_test.yml)
[![Machine-Learning-Client CI](https://github.com/software-students-fall2023/5-final-project-jungle-gap/actions/workflows/ml_client_test.yml/badge.svg)](https://github.com/software-students-fall2023/5-final-project-jungle-gap/actions/workflows/ml_client_test.yml) 
[![Build and Deploy (CD)](https://github.com/software-students-fall2023/5-final-project-jungle-gap/actions/workflows/build_and_deploy.yml/badge.svg)](https://github.com/software-students-fall2023/5-final-project-jungle-gap/actions/workflows/build_and_deploy.yml) 

## Container Images
Our container images are hosted on [DockerHub](https://hub.docker.com/). Click the following link to view our web-app's image and machine-learning-client's image respectively:
- [web-app](https://hub.docker.com/r/isomorphismss/web_app)
- [machine-learning-client](https://hub.docker.com/r/isomorphismss/ml_client)

## Introduction
Our Face Recognition Service offers a user-friendly interface for either capturing a selfie or uploading a pre-existing image. Once you submit your photo, we will process it, identifying and highlighting each human face with a distinct red box.

## Team Members
- [Jiasheng Wang](https://github.com/isomorphismss)
- [Xuefeng Song](https://github.com/wowwowooo)
- [Vincent Bai](https://github.com/VincentBai-dotcom)

## Setup

### Accessing the Deployed Application

The application is deployed and publicly accessible. You can interact with it directly without installing anything locally.

- **URL**: [http://134.209.170.83:6001](http://134.209.170.83:6001)
- Just click the link or copy-paste it into your browser's address bar.

#### Special Instructions for Chrome Users
If you are using Google Chrome and need to use features that require camera access (like taking a photo), follow these steps to bypass security restrictions due to the site being hosted on a bare IP address:

1. **Open Chrome Flags**:
   - Type `chrome://flags/#unsafely-treat-insecure-origin-as-secure` in your Chrome address bar and press `Enter`.

2. **Enable Insecure Origins**:
   - In the "Insecure origins treated as secure" section, add `http://134.209.170.83:6001`.
   - Change the dropdown from 'Disabled' to 'Enabled'.

3. **Relaunch Chrome**:
   - Click the 'Relaunch' button to apply the changes.

Please note that this workaround should be used cautiously as it can introduce security risks. It's recommended only for testing or non-sensitive use. We apologize for any inconvenience and are working to provide a more seamless experience in future updates.


### Prerequisites for Local Setup
- Ensure you have [Python](https://www.python.org/downloads/) 3.12 installed on your system.
- Make sure you have [Docker](https://docs.docker.com/get-docker/) installed and running on your computer. 
- Our project includes a feature to take a selfie from the front-end. For this, ensure your computer has a camera and that it is accessible via your browser.

### Running the Application Locally
- Clone the repository:

    ```shell
    git clone https://github.com/software-students-fall2023/5-final-project-jungle-gap 
    ```
- Navigate to the project root directory:

    ```shell
    cd 5-final-project-jungle-gap
    ```
- Start the `Docker` application.
- Use `docker` to pull the images from [Docker Hub](https://hub.docker.com/repositories/isomorphismss):

    ```shell
    docker pull isomorphismss/web_app:latest
    docker pull isomorphismss/ml_client:latest
    ```
- Start the application using `docker-compose`:

    ```shell
    docker-compose up
    ```
- Verify that the project is up and running by checking for the following messages in your terminal:

    ```shell
    my_web_app    |  * Running on all addresses (0.0.0.0)
    my_web_app    |  * Running on http://127.0.0.1:5000
    ```

    ```shell
    my_ml_client  |  * Running on all addresses (0.0.0.0)
    my_ml_client  |  * Running on http://127.0.0.1:5000
    ```
- Access the application in your browser at:

    ```shell
    http://localhost:6001
    ```

### How to Use the Application
After starting the application (either locally or via the deployed URL) and navigating to the home page, you have the option to either register for an account or use the app as a guest. You can upload an existing image or take a new picture using the app's "Turn on camera" button. Once the image is processed, you'll be able to see all human faces in the image be bounded by red boxes.

If you choose to register and log in, you gain additional features like viewing your image recognition history (by clicking the archive button). 

### Kind Reminders
- Please avoid uploading excessively large image files, as this could lead to slow processing times. The system's timeout is set to 60 seconds.
- Currently, the supported image file formats are `.jpg` `.jpeg` `.png`.

### Stopping the Application
To stop the application and remove the containers, execute the following command in your terminal:

```shell
docker-compose down
```

## Tests
Our project uses `pytest` (for the machine-learning-client) and `pytest-flask` (for the web-app), with test coverage reported by `coverage`. To run these tests locally, follow these steps:

### Prerequisites
- Ensure you have [Python](https://www.python.org/downloads/) 3.12 installed on your system.
- The application also depends on [gcc/g++](https://gcc.gnu.org/) and [cmake](https://cmake.org/download/). If you don't already have these installed on your computer, you may choose your preferred method of installation. Alternatively, you can follow the instructions provided below for a guided setup:

    - Windows:
        - Download and install [msys2](https://www.msys2.org/) by following the instructions under "installation" section.
        - Open `msys2-UCRT64` terminal and type the following commands to install gcc/g++ and cmake:

            ```shell
            pacman -S mingw-w64-ucrt-x86_64-gcc
            ```

            ```shell
            pacman -S mingw-w64-ucrt-x86_64-cmake
            ```
        - Add the `\msys64\ucrt64\bin` folder to the `PATH` environment variables.
        - Verify installation by typing the following commands in your terminal, you should be able to see the version number of each program:
        
            ```shell
            gcc --version
            ```

            ```shell
            g++ --version
            ```

            ```shell
            cmake --version
            ```
    - MacOS:

        - Ensure you have Homebrew installed. If not, install it with the following command in the terminal:

            ```shell
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            ```
        
        - Install GCC/G++ and CMake via Homebrew with the commands:

            ```shell
            brew install gcc
            ```

            ```shell
            brew install cmake
            ```

        - Verify the installations by checking the versions:

            ```shell
            gcc --version
            ```

            ```shell
            g++ --version
            ```

            ```shell
            cmake --version
            ```
        If you can't get the file version after installation, please make sure these programs are in `usr/local/bin` and the `/usr/local/bin` is already in `PATH`.
    
### Cloning the Project

```shell
git clone https://github.com/software-students-fall2023/5-final-project-jungle-gap
```

### Navigating to the Project Root Directory

```shell
cd 5-final-project-jungle-gap
```

### Installing pipenv
If `pipenv` is not installed on your machine, install it using:

```shell
pip install pipenv
```

### Installing Dependencies
Install all the necessary dependencies by executing:

```shell
pipenv install
```

### Activating the Virtual Environment
Activate the virtual environment using:

```shell
pipenv shell
```

### Running Tests
Navigate to either the `web-app` or `machine-learning-client` subdirectory depending on which component you want to test.

For the web-app:

```shell
cd web-app
```

For the machine-learning-client:

```shell
cd machine-learning-client
```

Run `pytest` and view the coverage report:

```shell
pipenv run coverage run -m pytest
```

```shell
pipenv run coverage report
```

To view a detailed HTML report showing lines covered and missed:

```shell
pipenv run coverage html
```

### Test Coverage Report (as of 12/17/2023, reported by Github Action)
- Machine-Learning-Client Coverage:

    ```shell
    Name                   Stmts   Miss  Cover
    ------------------------------------------
    app.py                    49      7    86%
    ml_client.py              15      0   100%
    tests/__init__.py          0      0   100%
    tests/test_ml_app.py      24      0   100%
    ------------------------------------------
    TOTAL                     88      7    92%
    ```

- Web-App Coverage:

    ```shell
    Name                    Stmts   Miss  Cover
    -------------------------------------------
    app.py                     96     15    84%
    tests/__init__.py           0      0   100%
    tests/test_web_app.py      79      1    99%
    -------------------------------------------
    TOTAL                     175     16    91%
    ```

## Conclusion
Thanks for trying out our application. If you have any questions or feedback, feel free to reach out to us via [GitHub Discussions](https://docs.github.com/en/discussions) for our repository. We appreciate your interest and support!
