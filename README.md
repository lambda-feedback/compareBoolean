# Boolean Comparison Evaluation Function

This repository contains the code for an evaluation function that compares two boolean expressions and returns feedback based on the outcome of the comparison. The function is designed to be used in the Lambda Feedback system, which is a platform for providing automated feedback on student submissions.

## Repository Structure

```bash
app/
    __init__.py
    evaluation.py # Script containing the main evaluation_function
    preview.py # Script containing the preview_function
    docs.md # Documentation page for this function (required)
    evaluation_tests.py # Unittests for the main evaluation_function
    preview_tests.py # Unittests for the preview_function
    requirements.txt # list of packages needed for algorithm.py
    Dockerfile # for building whole image to deploy to AWS

.github/
    workflows/
        test-and-deploy.yml # Testing and deployment pipeline

config.json # Specify the name of the evaluation function in this file
.gitignore
```

## Usage

### Getting Started

1. Merge commits into the default branch

   - This will trigger the `test-and-deploy.yml` workflow, which will build the docker image, push it to a shared ECR repository, then call the backend `grading-function/ensure` route to build the necessary infrastructure to make the function available from the client app.

2. You are now ready to start developing your function:

   - Edit the `app/evaluation.py` file, which ultimately gets called when the function is given the `eval` command
   - Edit the `app/preview.py` file, which is called when the function is passed the `preview` command.
   - Edit the `app/evaluation_tests.py` and `app/preview_tests.py` files to add tests which get run:
     - Every time you commit to this repo, before the image is built and deployed
     - Whenever the `healthcheck` command is supplied to the deployed function
   - Edit the `app/docs.md` file to reflect your changes. This file is baked into the function's image, and is made available using the `docs` command. This feature is used to display this function's documentation on our [Documentation](https://lambda-feedback.github.io/Documentation/) website once it's been hooked up!

---

## How it works

The function is built on top of a custom base layer, [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer), which contains tools, tests and schema checking relevant to all evaluation functions.

### Parser

The parser is built using the Lark library, which is a powerful and easy-to-use parsing library for Python. The parser is able to recognize set expressions written in both asciimath or LaTeX and convert them into SymPy expressions. The parser can be found in the [`evaluation-function-toolkit-python`](https://github.com/lambda-feedback/toolkit-python) package.

### Docker & Amazon Web Services (AWS)

The grading scripts are hosted AWS Lambda, using containers to run a docker image of the app. Docker is a popular tool in software development that allows programs to be hosted on any machine by bundling all its requirements and dependencies into a single file called an **image**.

Images are run within **containers** on AWS, which give us a lot of flexibility over what programming language and packages/libraries can be used. For more information on Docker, read this [introduction to containerisation](https://www.freecodecamp.org/news/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b/). To learn more about AWS Lambda, click [here](https://geekflare.com/aws-lambda-for-beginners/).

### Middleware Functions

In order to run the algorithm and schema on AWS Lambda, some middleware functions have been provided to handle, validate and return the data so all you need to worry about is the evaluation script and testing.

The code needed to build the image using all the middleware functions are available in the [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer) repository.

### GitHub Actions

Whenever a commit is made to the GitHub repository, the new code will go through a pipeline, where it will be tested for syntax errors and code coverage. The pipeline used is called **GitHub Actions** and the scripts for these can be found in `.github/workflows/`.

On top of that, when starting a new evaluation function, you will have to complete a set of unit test scripts, which not only make sure your code is reliable, but also helps you to build a _specification_ for how the code should function before you start programming.

Once the code passes all these tests, it will then be uploaded to AWS and will be deployed and ready to go in only a few minutes.

## Pre-requisites

Although all programming can be done through the GitHub interface, it is recommended you do this locally on your machine. To do this, you must have installed:

- Python 3.9 or higher.

- GitHub Desktop or the `git` CLI.

- A code editor such as Atom, VS Code, or Sublime.
