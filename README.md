# CSIT Mini Challenge: Fix The Wicked Pipeline

**To undertake this challenge, you're required to fork the repository with the broken pipeline. With this approach, you will have the freedom to work on the project independently, while Mighty Saver Rabbit can easily track your progress in rectifying the pipeline.**

Let's focus on rectifying the problems to make the pipeline run successfully for each job:

1. Lint: The primary purpose of this job is to check the code formatting using a linter. Your task is to ensure this job succeeds without any formatting errors.

2. Test: This job is designed to run the unit tests on the FastAPI application. Your objective is to ensure that all unit tests pass successfully.

3. Build: In this job, the Docker image of the FastAPI application is built. Your responsibility is to ensure the image is constructed without any errors.

During this challenge, **flags** are hidden within certain jobs of the CI/CD pipeline. These flags will only be revealed when a job is successfully completed. Your task is to gather these flags as evidence of your achievement. **Moreover, you are required to deploy your completed FastAPI application onto a cloud service of your choice. Once deployed, please submit the URL of the deployed application as proof of the functioning pipeline and successful deployment.**

Mighty Saver Rabbit awaits your return from this ghostly endeavor with bated breath!

**NOTE:** Using GitLab's shared runner for the CI/CD pipeline requires credit card information for verification. **Rest assured, you will not be charged.** This is a preventive measure by GitLab to counter abuse.

# Contents

[[_TOC_]]

## TODO

**Fix the CD/CD Pipeline**

- [ ] [Setup](#development)
- [ ] [Rectify lint errors](#linting)
- [ ] Fix `nearest_spooky_site()` function in [routers/standard.py](/app/routers/standard.py)
- [ ] [Correct `routers/standard.py` to ensure all test cases pass](#testing)
- [ ] [Build and push the Docker image to DockerHub](#build-image)
- [ ] [Deploy the application to a cloud service of your choice](#deployment)
- [ ] [Submit!](https://go.gov.sg/csit-cloudminichallenge-validation-page)

## Prerequisites

Before running the FastAPI application, ensure that the following prerequisites are met:

- Python 3.7 or higher
- Pip package manager
- Docker

## Variables

### Environment variables

| Variable | Sample                                                             | Required | Notes                            |
| -------- | ------------------------------------------------------------------ | -------- | -------------------------------- |
| API_KEY  | `ADHm97APqXZnNS1QXERUrfS29WiECFMhx0ARq4yfFOWs37M2OflxFH5uvJufyGtj` | Yes      | please generate your own API_KEY |

For this application, an API key is essential. Therefore, you will need to create your own API key and set it as an environment variable. You can create and store your environment variables in a `.env` file in the root directory of your project. You get a random value by running the command `python -c "import secrets; print(secrets.token_hex(16))"`.

## CI/CD Variables

| Variable        | Sample                                                             | Notes                                                                                          |
| --------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| API_KEY         | `ADHm97APqXZnNS1QXERUrfS29WiECFMhx0ARq4yfFOWs37M2OflxFH5uvJufyGtj` | please generate your own API_KEY                                                               |
| DOCKER_USERNAME | `MSRabbit23`                                                       | Your DockerHub account username.                                                               |
| DOCKER_PAT      | NIL                                                                | Personal Access Token (PAT) for DockerHub. Make sure to keep it confidential after generation. |

Make sure to set the values of DOCKER_USERNAME and DOCKER_PAT to the respective values from your DockerHub account.

- Every variables are mandatory for the CI pipeline to succeed
- Environment-specific and secret variables stored in CI environment variables

## Project Structure

- `app` directory contains the main application code, including API logic, core components, and data models.
- `app/model` directory contains the data models used in the application.
- `app/routers` directory contains the router modules that handle the HTTP requests for different routes in the application.
- `app/utils` directory contains utility modules that provide helper functions and tools for the application's business logic.
- `tests` directory is used for unit tests and integration tests.
- `data` directory contains all required json files for the application.
- `README.md` file provides an overview of the project and instructions on how to get started.
- `requirements.txt` file lists the required Python dependencies.

### Data Source

The MRT station coordinates data used in this project was sourced from Kaggle. Find the dataset at the following link: [https://www.kaggle.com/datasets/yxlee245/singapore-train-station-coordinates](https://www.kaggle.com/datasets/yxlee245/singapore-train-station-coordinates).

**Disclaimer**: Please be aware that the dataset has not been updated for four years. Therefore, some information may not reflect the most current state of the MRT stations.

## Development

Fork this repository to your account.

For the development and testing of your fixes, you have two options: Using Docker or setting it up locally.

### Option 1: Gitpod

You can use Gitpod, an online IDE, for development:

1. Navigate to your forked repository on GitHub.
2. Click on the "Edit" button (usually represented by a pencil icon).
3. From the dropdown or available options, select "Gitpod".

If not, you can also manually input the URL.

Open the repository in Gitpod:

```bash
   https://gitpod.io/#https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME
```

1. Gitpod will automatically set up your development environment, following the .gitpod.yml file configuration if you have one.

2. Start developing and testing directly within the Gitpod environment.

### Option 2: Local Setup

To setup and run the application locally on your machine, use these steps:

```bash
python -m venv env
# activate your virtual environment based on your local environment
source env/bin/activate # Linux/macOS
env\Scripts\activate.bat # In CMD
env\Scripts\Activate.ps1 # In Powershell
pip install -r requirements.txt
uvicorn main:app --reload
```

This will start the application locally, allowing you to make and test your changes.

### Linting

- Run `make lint` to see linting errors
- Run `make format` to format the files in-place

### Testing

A comprehensive suite of tests has been prepared by Mighty Saver Rabbit to ensure that the application functions as intended. These tests cover various aspects of the application and are crucial for verifying its correct behavior.

The scope of this challenge does not require the addition of new tests or modification of the existing test suite. However, running these tests and ensuring their successful completion is a vital part of this challenge. The Test job in the CI/CD pipeline is designed to run these tests automatically.

Tests can be run locally using the command `make test`. It should be noted that these tests are designed to pass when the application is set up correctly. If any tests are failing, it may indicate an issue with the application itself or the way it's configured in the environment.

## Build Image

For building Docker images in the GitLab CI/CD environment, we leverage the Kaniko Project. Below is an outline of the process:

- **Build Stage**: We have defined a `build` job in the `build` stage.
- **Docker Image**: The Kaniko Project's Docker image (`gcr.io/kaniko-project/executor:v1.9.0-debug`) is utilized for this purpose.
- **Variables**: Key environment variables are set to streamline the build process. Remember to replace `your-image-name` in the `DOCKER_IMAGE_NAME` variable with your desired image name.
- **Before Script**: This script validates essential variables and sets up Kaniko for Docker registry authentication.
- **Script**: This instructs Kaniko to construct the Docker image using the given Dockerfile and then pushes it to the specified registry.

**Important**: Make sure to replace `your-image-name` in the `DOCKER_IMAGE_NAME` variable with the image name of your choice.

To effectively use this build process:

1. Ensure your GitLab repository includes the CI configuration and the `Dockerfile`.
2. Modify paths in the `gitlab-ci.yml` if your `Dockerfile` isn't at the root of your repository.
3. Adjust environment variables in the GitLab CI/CD settings or within the `.yml` file as required.

## Deployment

To deploy the application onto a cloud service of your choice (like AWS, Google Cloud, Azure) follow these general steps:

1. Create an account with your chosen cloud service provider. Ensure you are familiar with their pricing and free tier options if available.

2. Set up a new server instance. You might want to use an operating system like Ubuntu and choose appropriate resource limits.

3. Deploy your Dockerized application to the server instance. The deployment method will depend on your provider, so refer to their documentation for specific instructions.

4. Install necessary software on the server. This includes Python, project dependencies, a WSGI server such as Uvicorn or Hypercorn, and a process supervisor.

5. Configure your server. Set up your WSGI server and process supervisor with the correct settings for your application.

Remember that these are general guidelines and specific steps may vary based on the chosen cloud provider. Always refer to the specific instructions of the provider you choose.

### Security and Compatibility Enhancements

- Set up HTTPS and TLS: Ensuring the implementation of HTTPS and TLS will guarantee that the data being exchanged between your client and server is encrypted and secure.

- Enable CORS (Cross-Origin Resource Sharing): Allowing CORS ensures your application can make requests to the server from a different domain or origin, providing necessary compatibility for diverse client-side requests.

## Troubleshooting

### pytest not working

If you encountered `ModuleNotFoundError: No module named 'app'`, it is likely due to the default Python interpreter searching for the file only in the current directory. To resolve this issue, you can explicitly set the `PYTHONPATH` variable using the terminal.

```bash
# Linux/ macOS
pwd # get path to directory
export PYTHONPATH="path/to/directory"

# Windows
pwd # get path to directory
SET PYTHONPATH="path/to/directory"
```

Replace `/path/to/directory` or `C:\path\to\directory` (can also try forward slash `/`) with the actual path to the directory containing the 'app' module. This will ensure that Python can find the module and resolve the error.
