=======
History
=======

0.4.4 (2022-05-09)
------------------

* Features:

  * Add general support for wrappers. (#28)

* Improvements:

  * Make dev beobench build part of image build process for improved
    speed.
  * Add number of environment steps (``env_step``) to wandb logging.
  * Update logo to new version (#48)
  * Update docs and main readme to include more useful quickstart guide, which includes a custom agent (#47)

* Fixes:

  * Enable automatic episode data logging in RLlib integration for long training periods.
  * Update broken links in main readme env list (#40)

0.4.3 (2022-04-12)
------------------

* Feature: enable easy access to standard configs via util method
* Feature: add non-normalised observations to info in energym integration (#62)
* Feature: enable logging full episode data from RLlib and adding this data
  to wandb (#62)
* Feature: ship integrations with package improving image build times (#44)
* Feature: add wandb logging support for random agent script (#59)
* Feature: add rule-based agent script based on energym controller (#60)
* Fix: add importlib-resources backport package to requirements
* Fix: allow users to disable reset() method in energym envs (#43)
* Aux: add automatic deployment of PyPI package via GitHub actions (#50)
* Aux: add tests and automatic checks on PRs (#25)

0.4.2 (2022-04-04)
------------------

* Feature: defining all relevant options/kwargs of CLI an API is now supported
  yaml files (#54)
* Feature: allow multiple configs to be given to both CLI
  (giving multiple ``-c`` options) and Python API (as a list) (#51)
* Fix: adapted Energym env reset() method to avoid triggering
  long warm-up times with additional simulation runs (#43)
* Fix: enable container build even if prior build failed midway
  and left artifacts

0.4.1 (2022-03-30)
------------------

* Feature: enable package extras to be given in development mode
* Feature: add support for arm64/aarch64-based development by forcing
  experiment containers to run as amd64 containers on those systems (#32)
* Fix: add gym to extended package requirements


0.4.0 (2022-03-28)
------------------

* Make dependencies that are only used inside experiment/gym
  containers optional
  (for all dependencies install via ``pip install beobench[extended]``)
* Add two part experiment image build process so that there is shared beobench
  installation dockerfile
* Add support for yaml config files (!)
* Overhaul of documentation, including new envs page and new theme
* Enable RLlib free experiment containers when not required
* Add beobench_contrib as submodule
* Simplify Pypi readme file
* Remove GPU requirement for devcontainer

0.3.0 (2022-02-14)
------------------

* Add complete redesign of CLI: main command changed from
  ``python -m beobench.experiment.scheduler`` to ``beobench run``.
* Add support for energym environments
* Add support for MLflow experiment tracking
* Add support for custom agents


0.2.1 (2022-02-03)
------------------

* Add integration with sinergym
* Move gym integrations to separate beobench_contrib repo
* Make usage of GPUs in containers optional

0.2.0 (2022-01-18)
------------------

* Enable adding custom environments to beobench with
  *docker build context*-based syntax
* Save experiment results on host machine
* Major improvements to documentation
* Remove unnecessary wandb arguments in main CLI

0.1.0 (2022-01-10)
------------------

* First release on PyPI.
