=======
History
=======

0.5.3 (2022-11-18)
------------------

* Features:

  * Add support for installing agent script's requirements via requirements file (#71).

* Improvements

  * Add support for dry running ``beobench run`` with ``--dry-run`` flag. This aims to help with testing and debugging.
  * Add explicit warning for windows users with recommended fixes (i.e. using WSL instead).

* Fixes:

  * Fix Sinergym data ranges in Sinergym experiment container definition in beobench_contrib (#96). Fix by @XkunW, thanks!
  * Remove default normalisation with Sinergym (as this may fail with newer Sinergym versions as pointed out by @kad99kev (thanks!)).
  * Pin the version of sinergym to the currently latest version to avoid future issues (v2.1.2).
  * Change the way Beobench is installed inside experiment containers. Previously this was done using conditional logic inside Dockerfiles. Now the logic is done in Python, with two different dockerfiles for local and pypi installations. This enables the use of non-buildx in the construction of Beobench experiment containers. Credit and thanks to @HYDesmondLiu and @david-woelfle for finding and sharing the underlying error.
  * Fix #90 by removing access to env config before env_creator script. Thanks to @HYDesmondLiu, who first flagged this bug in #82.
  * If one of the Beobench scheduler subprocesses fails (e.g. docker run) the main process now fails as well.


0.5.2 (2022-07-01)
------------------

* Known issues

  * This release breaks the experiment build process for most machines. Thus, this release was yanked on pypi and is not installed unless specifically pinned to. See #82 for more details.

* Improvements:

  * Add more informative error when there are issues with access to Docker from Beobench.

* Fixes:

  * Revert default build command to ``docker build`` from ``docker buildx build``. Only arm64 machines use ``buildx`` now. This aims to enable usage of older docker versions such as v19.03 on non-arm64 machines. Arm64 machines require buildx and thus also newer docker versions.
  * Fix wrong env name in logging output. Removes unused default env name var and fix logging output to use new env name location.



0.5.1 (2022-06-28)
------------------

* Features:

  * Add pretty logging based on loguru package. Now all Beobench output is clearly marked as such.

* Improvements:

  * Enable adding wrapper without setting config.
  * Add ``demo.yaml`` simple example config.

* Fixes:

  * Update Sinergym integration to latest Sinergym version.

0.5.0 (2022-05-26)
------------------

* Features:

  * Mean and cummulative metrics can now be logged by WandbLogger wrapper.
  * Support for automatically running multiple samples/trials of same experiment via ``num_samples`` config parameter.
  * Configs named `.beobench.yml` will be automatically parsed when Beobench is run in directory containing such a config. This allows users to set e.g. wandb API keys without referring to the config in every Beobench command call.
  * Configs from experiments now specify the Beobench version used. When trying to rerun an experiment this version will be checked, and an error thrown if there is a mismatch between installed and requested version.
  * Add improved high-level API for getting started. This uses the CLI arguments ``--method``, ``--gym`` and ``--env``. Example usage: ``beobench run --method ppo --gym sinergym --env Eplus-5Zone-hot-continuous-v1`` (#55).

* Improvements:

  * Add ``CITATION.cff`` file to make citing software easier.
  * By default, docker builds of experiment images are now skipped if an image with tag corresponding to installed Beobench version already exists.
  * Remove outdated guides and add yaml configuration description from docs (#38, #76, #78).
  * Add support for logging multidimensional actions to wandb.
  * Add support for logging summary metrics on every env reset to wandb.
  * Energym config now uses ``name`` argument like other integrations (#34).

* Fixes:

  * Updated BOPTEST integration to work with current version of Beobench.

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
