# raft_heatmap - QGIS Plugin

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![flake8](https://img.shields.io/badge/linter-flake8-green)](https://flake8.pycqa.org/)

**View the official Documentation, including installation, usage, and development instructions, :star: [here](https://alxwstn.github.io/RAFTHeatmapMkr/>) :star:**

Or copy the link here :point_down::
```
https://alxwstn.github.io/RAFTHeatmapMkr/>
```

### RAFT Heatmap QGIS Plugin Project Info

The boilerplate code for this plugin was generated using this [qgis plugin cookiecutter project](https://oslandia.gitlab.io/qgis/template-qgis-plugin/usage/result.html). Initial POC work was developed on top of boilerplate generated using [Plugin Builder 3](https://plugins.qgis.org/plugins/pluginbuilder3/). Many thanks to the developers who created these projects! Check them out! I learned a great deal from their code, as well as the code of several other open source QGIS plugins available on Github.

### Tooling

This project is configured with the following tools:

- [Black](https://black.readthedocs.io/en/stable/) to format the code without any existential question
- [iSort](https://pycqa.github.io/isort/) to sort the Python imports

Code rules are enforced with [pre-commit](https://pre-commit.com/) hooks.  
Static code analysis is based on: Flake8

See also: [contribution guidelines](CONTRIBUTING.md).

## CI/CD

Plugin is linted, tested, packaged and published with GitHub. As this plugin is of limited use outside of the SDRPF RAFT program, it is not deployed to the official QGIS plugins repository. See the [official documentation](https://alxwstn.github.io/RAFTHeatmapMkr/) for installation instructions.

### Documentation

The documentation is located in `docs` subfolder, written in Markdown using [myst-parser](https://myst-parser.readthedocs.io/), structured in two main parts, Usage and Contribution, generated using Sphinx (have a look to [the configuration file](./docs/conf.py)) and is automatically generated through the CI and published on Pages: <https://alxwstn.github.io/RAFTHeatmapMkr/>.

## License

Distributed under the terms of the [`GPLv2+` license](LICENSE).
