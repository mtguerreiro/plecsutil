Quickstart guide
================

Installation
------------

Currently, the package is not available the Python package index (PyPI), and must be installed manually. To do so, create a new folder, change to the new folder and clone the repository:

.. code-block:: console
   
   git clone https://github.com/mtguerreiro/plecsutil .

Alternatively, it is also possibly to simply download the repository from GitHub without using git. Simply download the repository, unzip it, and navigate to the new folder.

To install ``plecsutil``, run

.. code-block:: console
   
   python -m pip install -e .

This installs ``plecsutil`` in editable mode. To update ``plecsutil`` with git, simply pull the changes from the remote repository.

Examples
--------

Try ``plecsutil`` with the examples provided in the `examples page <https://github.com/mtguerreiro/plecsutil/tree/main/examples>`_. The examples show how to run PLECS simulations with different model parameters, multiple controllers, and how to save and load simulation results.
