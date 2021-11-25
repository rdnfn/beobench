============
BOPTEST
============

How to use BOPTEST as part of beobench.

Use the beobench installer tool, currently available as a python module. Usage::

    import beobench.installer

    beobench.installer.install_boptest()

After installing BOPTEST using the installer, you need to set it to the PYTHONPATH using the command::

     export PYTHONPATH=$PYTHONPATH:/workspace/notebooks/tmp/beobench_external_install/boptest

Then install the requirements for BOPTEST (taken from its Dockerfile)::

     pip install --user flask-restful==0.3.9 pandas==0.24.2 flask_cors==3.0.10

Note: it may be required to relax the version requirement for pandas, I have had no problem doing this.