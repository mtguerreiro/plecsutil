.. plecsutil documentation master file, created by
   sphinx-quickstart on Sun Oct 20 09:48:45 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

User guide
==========

Image about the structure

Introduction
============

Creating the PLECS model
------------------------

To work with ``plecsutil``, the PLECS model needs at least two elements: an output data port in the top-level circuit, and a link to the ``.m`` file containing the model parameters. 

The output data port (or ports) in the top-level circuit defines which signals are sent to Python at the end of each simulation. A data port can contain a single signal, or many signals can be multiplexed and connected to a single data port. :numref:`fig-user-guide-schematic` shows an example of a Buck converter with output data ports in the top-level circuit. (You can download the example by clicking :download:`here <media/user_guide/intro/buck_intro.plecs>`.)


.. figure:: media/user_guide/intro/images/schematic.svg
   :name: fig-user-guide-schematic
   :scale: 85%
   :align: center
   :alt: Output data port in top-level.
   
   PLECS model with output data port in the top-level circuit.

The link to the ``.m`` file is given in the initialization tab of the simulation parameters, as shown in :numref:`fig-user-guide-initialization`. It is important that the name of the ``.m`` matches the name of the PLECS  model (the simulation file). Thus, if the name of the PLECS model is ``buck_intro.plecs``, the name of the initialization file must be indicated in the simulation parameters must be ``buck_intro.m``.

.. figure:: media/user_guide/intro/images/initialization.png
   :name: fig-user-guide-initialization
   :scale: 50%
   :align: center
   :alt: Initialization of simulation parameters .
   
   Initialization of the simulation parameters.


Creating the Python script
--------------------------

Running the PLECS simulation requires creating a :class:`plecsutil.ui.PlecsModel` object informing the name of the PLECS model, its path, and a Python dictionary containing all of the parameters of the model.

An example of a Python script is shown below. Note that the script assumes to be in the same folder as that the PLECS model, since it defines the ``plecs_file_path`` as the current working directory.

.. literalinclude:: media/user_guide/intro/buck_intro.py
   :caption: Running a PLECS simulation with ``plecsutil`` (:download:`download source <media/user_guide/intro/buck_intro.py>`)
   :language: python

In this example, when calling :meth:`plecsutil.ui.PlecsModel.sim` to run the simulation, ``plecsutil`` will generate a ``.m`` file. This files contains the model parameters given by the ``model_params`` dictionary is used to initialize the :class:`plecsutil.ui.PlecsModel` object. After generating the ``.m`` file, the simulation is launched, which then uses the ``.m`` as source.


Simulation results
------------------

After running a simulation, :meth:`plecsutil.ui.PlecsModel.sim` returns a :class:`plecsutil.ui.DataSet` dataclass holding the simulation results. In addition to the data points, :class:`plecsutil.ui.DataSet` contains a ``meta`` field. This field has  a dictionary with a ``model_params`` entry that  stores the  model parameters used to produce the associated simulation results. Thus, the simulation results are always saved with the parameters used to produce them.


Running simulations with different model parameters
---------------------------------------------------

The :meth:`plecsutil.ui.PlecsModel.sim` accepts a ``sim_params`` dictionary that can be used to overwrite the default model parameters defined when initializing the :class:`plecsutil.ui.PlecsModel` object. The ``sim_params`` dictionary doesn't need to contain all model parameters, but just the parameters to be overwritten. In the example Python script shown above, calling :meth:`plecsutil.ui.PlecsModel.sim` as

.. code-block:: python
   
   data = pm.sim({'R': 4})

will run the simulation with ``R = 4``, instead of the default value of 10 defined by ``model_params``.

An example of running the simulation of the Buck converter with different ``R`` values is shown below. In this example, :meth:`plecsutil.ui.PlecsModel.sim` is called with ``sim_params`` specifying different values for ``R``.

.. literalinclude:: media/user_guide/intro/buck_intro_var_r.py
   :caption: Running the PLECS model with different model parameters (:download:`download source <media/user_guide/intro/buck_intro_var_r.py>`)
   :language: python


The ``model.py`` file
----------------------

In the previous examples, the dictionary containing the model parameters (``model_params``) was defined in the script that runs the simulation. This makes managing the model parameters more difficult when there are multiple Python scripts to perform different simulations of the same model. In the Buck model used as example, one might create one script to run the model with different values for ``R``, and another one for different values of ``f_pwm``. If the parameters of the PLECS model need to be updated, all scripts need to be modified to include the new parameters.

This can be avoided by creating a ``model.py`` associated with the PLECS model. In this way, the model parameters are defined in a single location, and all scripts  running simulations can simply import the model from the ``model.py`` file. 

Although the ``model.py`` can be created and define the dictionary with the model parameters, it is more flexible to create a function that returns the parameters instead. The advantages of this approach become clear when adding controllers to the simulation.

For the Buck example discussed thus far, we can create an associated ``model.py`` with the following contents:

.. literalinclude:: media/user_guide/intro/model.py
   :caption: Example of ``model.py`` file (:download:`download source <media/user_guide/intro/model.py>`)
   :language: python

Now, ``model.py`` can be imported by Python scripts to get the model parameters. For example, to run the Buck converter model with varying values for ``R``:

.. literalinclude:: media/user_guide/intro/buck_intro_model.py
   :caption: Using ``model.py`` to run simulations (:download:`download source <media/user_guide/intro/buck_intro_model.py>`)
   :language: python

