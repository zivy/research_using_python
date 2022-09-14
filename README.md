# Guide for development of research code<br><sup>(using Anaconda Python)</sup>

# TL;DR:
### One time setup
0. Install [git](https://git-scm.com/) and go through its [one time setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup), bare minimum:
    ```
    git config --global user.name “First Last”
    git config --global user.email “firstlast@work.com”
    git config --global core.editor editor_of_choice
    ```
   Editor option for the few folks on windows (haven't tried it myself):
   ```
   git config --global core.editor "'input/path/to/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"
   ```
1. Install [git-lfs](https://git-lfs.github.com) and run `git lfs install`.
2. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html).
3. Sign up for a [GitHub account](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account).
4. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and [add it to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

### Once per repository setup
0. [Create empty repository on GitHub](https://docs.github.com/en/get-started/quickstart/create-a-repo), lets call it my_project.
1. Initial commit into local repository and push to remote:
    0. Create local repository (also creates new directory) `git init my_project`
    1. Create a [markdown](https://en.wikipedia.org/wiki/Markdown) file, README.md describing the project.
    2. Create an `environment_dev.yml` file based on [this example](environment_dev.yml). Change the environment name to an appropriate one and add relevant packages.
    3. Copy this [pre-commit configuration file](.pre-commit-config.yaml).
    4. Copy this [.gitignore file](.gitignore) and add file types you want git to ignore.
    5. Add file types to be tracked by git-lfs based on file extension, creates the .gitattributes file (e.g. `git lfs track "*.pth"`)
    6. Copy this [.flake8](.flake8) file to customize the tool settings.

  ```
  git add README.md environment_dev.yml .pre-commit-config.yaml .gitattributes .gitignore .flake8
  git commit
  git branch -M main
  git remote add origin git@github.com:user_name/my_project.git
  git push -u origin main
  ```
2. Create virtual environment activate it and set up pre-commit:
    ```
    conda env create -f environment_dev.yml
    conda activate my_project_dev
    pre-commit install
    ```

### Start working
0. Activate virtual environment `conda activate my_project_dev`
1. Create new branch off of `main`:
```
git checkout main
git checkout -b my_new_branch
```
2. Work.
3. Commit locally and push to remote (origin can be either a fork, if using a triangular workflow, or the original repository if using a centralized workflow):
```
git add file1 file2 file3
git commit
git push origin my_new_branch
```
4. Create a [pull request on GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) and after tests pass merge into main branch.

**If code is not in the remote repository, consider it lost.**

# Long version

## Why should you care?

Most scientists need to write code as part of their research. This is a "physical" embodiment of the underlying algorithmic and mathematical theory. Traditionally the software engineering standards applied to code written as part of research have been rather low (rampant code duplication...). In the past decade we have seen this change. Primarily because it is now much more common for researchers to share their code (often due to the "encouragement" of funding agencies) in all its glory.

When sharing code, we expect it to comply with some minimal software engineering standards including design, readability, and testing.

I strive to follow the guidance below, but don't always. Still, it's important to have a goal to strive towards. To quote Lewis Carol (If you don't know where you're going, any road will take you there). From [Alice's Adventures in Wonderland](https://www.gutenberg.org/ebooks/11):

“Would you tell me, please, which way I ought to go from here?” “That depends a good deal on where you want to get to,” said the Cat. “I don’t much care where-” said Alice. “Then it doesn’t matter which way you go,” said the Cat. "-so long as I get somewhere,” Alice added as an explanation.“Oh, you’re sure to do that,” said the Cat, “if you only walk long enough.”

Personal pet peeves, in no particular order:
  * A single commit of all the code in the GitHub repository. Yes, you're sharing code but it did not magically materialize in its final form, be transparent so that we can trust the code and see how it developed over time. We can learn from paths that did not pan out almost as much as from the path that did. By providing all of the history we can see which algorithmic paths were attempted and did not work out. Help others avoid going down dead-end paths.
  * Repository contains `.DS_Store` files. Yes, we know you are proud of your Mac. I like OSX too, but seriously, you should have added this file type to the .gitignore file when setting up the repository.
  * Deep learning code sans-data, sans-weight files. This is completely useless in terms of reproducibility. Don't "share" like this.
  * Code duplication with minor, hard to detect, differences between copies.



## Version control
1. Use a version control system, currently [Git](https://git-scm.com/) is the VCS of the day. Learn how to use it (introduction to git [slide deck](https://yanivresearch.info/writtenMaterial/introduction2git.pptx)).
2. Use a remote repository, your cloud backup. Keep it private during development and then make it public upon publication acceptance. Free services [GitHub](https://github.com/), [BitBucket](https://www.atlassian.com/software/bitbucket).
3. Do not commit binary or large files into the repository. Use [git-lfs](https://git-lfs.github.com/). Beware the Jupyter notebook. Do not commit notebooks with output as this will cause the repository size to blow up, particularly if output includes images. Clear the output before committing.
4. Use the [pre-commit framework](https://pre-commit.com/) to improve (1) compliance to code style (2) avoid commits of large/binary files, AWS credentials and private keys. We all need a little help complying with our self imposed constraints ([example configuration file](.pre-commit-config.yaml)). Note that git pre-commit hooks **do not preclude non-compliant commits**, as a determined user can go around the hooks, `git commit --no-verify`.

## Writing code (Python as a use case)

Many languages have style, testing and documentation tools and conventions. Here we focus on Python, but the concepts are similar for all languages.

1. Style - Use consistent style and **enforce** it. Other human beings need to read the code and readily understand it.
Write code that is compliant with [PEP8](https://www.python.org/dev/peps/pep-0008/) (the Python style guide):
   * Use [flake8](https://flake8.pycqa.org/en/latest/) to enforce PEP8.
   * Use the [Black](https://github.com/psf/black) code formatter, works for scripts and Jupyter notebooks (for Jupyter notebook support `pip install black[jupyter]` instead of the regular `pip install black`). It does not completely agree with flake8, so use both?
   * Some folks don't like the Black formatting, it isn't all roses. An alternative is [autopep8](https://github.com/hhatto/autopep8).
2. Testing - Write nominal regression tests at the same time you implement the functionality. Non-rigorous regression testing is acceptable in a research setting as we explore various solutions. The more rigorous the testing the easier it will be for a development team to get code into production. Use [pytest](https://docs.pytest.org/) for this task.
3. Documentation - Write the documentation while you are implementing. Start by adding a README file to your repository (use [markdown](https://en.wikipedia.org/wiki/Markdown) or [restructured text](https://en.wikipedia.org/wiki/ReStructuredText)). It should include a general description of the repository contents, how to run the programs and possibly instructions on how to build them from source code. Generally, when we postpone writing documentation we will likely never do it. That's fine too, as long as you are willing to admit to yourself that you are consciously choosing to not document your code.
In Python, use a consistent [Docstring](https://www.python.org/dev/peps/pep-0257/) format. Two popular ones are [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) and [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard).
4. Reproducible environment - include instructions or configuration files to reproduce the environment in which the code is expected to work. In Python you provide files listing all package dependencies enabling the creation of the appropriate virtual environment in which to run the program. A [requirements.txt](https://pip.pypa.io/en/latest/reference/requirements-file-format/) for plain Python, or an [environment.yml](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) for the anaconda Python distribution. For development we often rely on additional packages not required for usage (e.g. pytest). Consequentially we include a `requirements_dev.txt` (`environment_dev.yml`) in addition to the `requirements.txt` (`environment.yml`) files. Sample [requirements.txt](requirements.txt), [requirements_dev.txt](requirements_dev.txt) and [environment.yml](environment.yml), [environment_dev.yml](environment_dev.yml) files.
5. Your code is a mathematical multi-parametric function that depends on many parameters beyond the input. These parameters are either:
  * Hard coded - best avoided if they need to be changed for different inputs.
  * Given as arguments on the command-line, appropriate when you have a few, less than five. Several popular Python modules/packages that support parsing command-line arguments: [argparse](https://docs.python.org/3/library/argparse.html), [click](https://palletsprojects.com/p/click/) and [docopt](http://docopt.org/). Personally I use argparse ([example usage available here](argparse_example.py)).
  * Specified in a configuration file. These usually use [XML](https://en.wikipedia.org/wiki/XML) or [JSON](https://en.wikipedia.org/wiki/JSON) formats. I use JSON ([example configuration file](parameters.json) and [short script](json_config_example.py) that reads it). The parameters file is given on the command-line so we also get to use argparse.

## Continuous integration

Automate testing and possibly delivery using continuous integration. There are many CI services that readily integrate with remote hosted git services. In the past I've used [TravisCI](https://www.travis-ci.com/) and [CircleCI](https://circleci.com/). Currently using [GitHub Actions](https://docs.github.com/en/actions). All of these rely on a yaml based configuration files to define workflows.

An example GitHub actions workflow which runs the same tests as the pre-commit defined above is [available here](.github/workflows/pre_commit.yml).
