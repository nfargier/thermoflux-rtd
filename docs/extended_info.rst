step 1 : 
For definition of membrane potentials, ‘ce’ represents the voltage between compartment ‘c’ and compartment 'e’ defined as Phic - Phie.
Table 1 (see old version)


Step 2: Definition of metabolites and chemical species 

‘Thermo-Flux’ automatically recognises the metabolite identifiers and links to the eQuilibrator compound retrieved with metabolite.compound.
 Annotations can be user-defined or updated in the attribute annotation of the metabolite class e.g. 

metabolite.annotation = {'CHEBI’:’11111’, ‘kegg’:’C00000’} 

 In ‘Thermo-Flux’, the average charge, average number of protons, and magnesium ions are returned by the function metabolite.average_charge_protons() which first interrogates the eQuilibrator compound and then uses the physical parameters defined in Step 1 to return the condition specific metabolite information. 
To facilitate the understanding of these latter average calculations, this function also returns the information on each species’ abundance and their charge, number of protons and magnesium ion (Figure 2c).   
