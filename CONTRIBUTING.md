# Contributing Guidelines

First off, thanks for considering contributing to this project!

This plugin is quite specific to the RAFT program run by the San Diego River Park Foundation. I took part in the Geospatial Data Collection and Analysis Program December 2025 through March 2026 as a way to introduce to the environmental science and conservation sector in the San Diego area. As someone with a software engineering background, I found myself craving a deeper dive into QGIS, as the the analysis-related training that was offered during my tenure in the program focused mainly on spreadsheets. Perhaps some aspect of my experience resonates with you, and you somehow found your way here.

Here are some suggestions on what to do next:

1. If you want to develop a foundation in QGIS, consider starting with a [Gentle Introduction to GIS](https://docs.qgis.org/3.40/en/docs/gentle_gis_introduction/), the [official training manual](https://docs.qgis.org/3.44/en/docs/training_manual/), and/or this friendly [QGIS tutorial site](https://www.qgistutorials.com/en/index.html).
2. If you want to know a bit about automating QGIS workflows, challenge yourself to write a Python program that is launched from your commandline/terminal to preform the RAFT "trash join" step (IYKYK). Your program won't be adopted by SDRPF, but it's a useful learning exercise, and you can [dogfood](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) it! Start by writing your program in the [QGIS Python console](https://docs.qgis.org/3.40/en/docs/user_manual/plugins/python_console.html), then figure out what changes you need to make to run your program without actually opening QGIS.
3. If you're interested in QGIS plugin development, but getting a new plugin bootstrapped on your own is feeling a bit daunting: A number of [issues](https://github.com/alxwstn/RAFTHeatmapMkr/issues) have been added as potential future additions to this plugin. You can [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the repository, get local development set up [as described here](https://alxwstn.github.io/RAFTHeatmapMkr/development/environment.html), and give it a go! Depending on your level of experience with coding, there can be a lot of useful skills to learn as part of that process (Basic GIS, QGIS, Git, Python, Github workflows, PyQt user interfaces)!
4. If you have some familiarity with a few of the skills described above, you can go about the process of generating your own QGIS plugin using the [QGIS Plugin templater](https://oslandia.gitlab.io/qgis/template-qgis-plugin/usage/result.html). While there are several different ways to get started with plugin development, I found this one to be the most modern and friendliest. You can also start with the [QGIS Minimalist Plugin](https://github.com/wonder-sk/qgis-minimal-plugin) and build from the ground up.

You got this!

## Git hooks

This repository uses git hooks through [pre-commit](https://pre-commit.com/) to enforce and automatically check some "rules". Please install them (`pre-commit install`) before to push any commit.

See the relevant configuration file: `.pre-commit-config.yaml`.

## Code Style

Make sure your code *roughly* follows [PEP-8](https://www.python.org/dev/peps/pep-0008/) and keeps things consistent with the rest of the code:

- docstrings: [sphinx-style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html#the-sphinx-docstring-format) is used to write technical documentation.
- formatting: [black](https://black.readthedocs.io/) is used to automatically format the code without debate.
- sorted imports: [isort](https://pycqa.github.io/isort/) is used to sort imports
- static analysis: [flake8](https://flake8.pycqa.org/en/latest/) is used to catch some dizziness and keep the source code healthy.
