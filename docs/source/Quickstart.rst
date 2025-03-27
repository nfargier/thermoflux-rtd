Quick start
===========
As a first example, we will show how to start from a stoichiometric model and build the thermodynamic model using a toy model (e.coli core metabolism). For more details, please have a look at the examples/ecoli/textbook/Ecoli_example_textbook.ipynb.

Building the thermo-model object
********************************

Load a Cobra model
>>> model = cobra.io.load_model('e_coli_core')
Create the thermo model object from the cobra model 
>>> tmodel = ThermoModel(model)

