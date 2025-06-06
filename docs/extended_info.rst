step 1 : 
For definition of membrane potentials, ‘ce’ represents the voltage between compartment ‘c’ and compartment 'e’ defined as Phic - Phie.
Table 1 (see old version)


Step 2: Definition of metabolites and chemical species 

‘Thermo-Flux’ automatically recognises the metabolite identifiers and links to the eQuilibrator compound retrieved with metabolite.compound.
 Annotations can be user-defined or updated in the attribute annotation of the metabolite class e.g. 

metabolite.annotation = {'CHEBI’:’11111’, ‘kegg’:’C00000’} 

 In ‘Thermo-Flux’, the average charge, average number of protons, and magnesium ions are returned by the function metabolite.average_charge_protons() which first interrogates the eQuilibrator compound and then uses the physical parameters defined in Step 1 to return the condition specific metabolite information. 
To facilitate the understanding of these latter average calculations, this function also returns the information on each species’ abundance and their charge, number of protons and magnesium ion (Figure 2c).   



Step 3. Calculation of Gibbs formation energies  

The function model.update_thermo_info() will automatically calculate the required parameters based on the defined physiochemical conditions (step 1) and the metabolites of the model will now have a defined transformed Gibbs formation energy ([Equation]) and an average charge and number of protons.

box 2 : 
uncertainty
(different default uncertainty can be specified with model.rmse_inf = Q_(3000, 'kJ/mol')),
We can also estimate a non-zero Gibbs formation energy for metabolites with non-decomposable or unknown structures (see supplementary section “metabolites with unknown formation energy”). This is implemented by the fit_unknown_dfG0=True argument when estimating Gibbs formation energies.   

redox
In ‘Thermo-Flux’ a formation energy and a standard error can be explicitly defined, and the “redox” attribute set to true to ensure the formation energy is not automatically recalculated e.g. 
cyt_c_red_c.dfG0prime() = Q_(-12.05,’kJ/mol') 
cyt_c_red_c.redox = True 
cyt_c_red_c.dfG_SE = Q_(0,’kJ/mol')  

biomass:
In ‘Thermo-Flux’ the function: thermo_flux.tools.drg_tools.dfGbm() returns the [Equation] given a specified empirical formula of biomass and can be used to explicitly define the biomass formation energy e.g. 
dfGbm = thermo_flux.tools.drg_tools.dfGbm(H=1.613,O=0.557,N=0.158, P=0.012, S=0.003, K = 0.022, Mg = 0.003, Ca= 0.001, units = kJ/g) 
model.metabolites.biomass.dfGprime() = dfGbm  
model.metabolites.biomass.biomass = True 
model.metabolites.biomass.dfG_SE = 0  


 Biomass formation energy is made dependent on the pH of the biomass metabolite’s compartment when transformed based on the number of hydrogen atoms of which it is forme. It is done automatically when building a ‘Thermo-Flux’ model if model.update_biomass_dfG0 is set to True.


step 4.
Defining additional transported protons can be achieved by altering the reaction stoichiometry (Figure 3b). Alternatively additional transported protons can be defined using reaction.transported_h() which represents additional protons transported by a reaction e.g. reaction.transported_h = {'e' : -1, 'c' : 1}, to define an additional proton moving from the extracellular (e) compartment to the cytosol (c).

box3 : 
transporter variants :
Additionally, in case of transport processes, for which at the given pH value no charge neutral transport variant exists, we suggest introducing an additional transport reaction, in which protons balancing the charge are co-translocated together with the respective species, i.e. adding a proton symporter or antiporter. This additional transport variant ensures that for every metabolite, a transport variant exists that does not translocate net charge. Addition of transporter variants can automatically be achieved with the function reaction.add_transporter_variants() which identifies the species transported in the original reaction and adds variants to represent the transport of all alternative species. For example, a model may contain a reaction for phosphate transport, pi_e -> pi_c. At pH 5, this ion exists entirely in the H2PO4- form with a charge of -1 (Figure 3a). Therefore, all the major species of the latter ion are already represented but a charge neutral transporter does not exist. A proton coupled reaction of pi_e  + H_e -> pi_c + H_c is automatically added to the model (Figure 3b). 

Some transport reactions involve chemical transformation of the transported metabolite e.g. phosphotransferase system  (PTS) sugar transporters which phosphorylate sugars during transport (McCoy et al, 2015). In this case it is not possible to automatically determine the specific metabolite that is transported, as it does not appear as both a substrate and product of the reaction. Therefore, it is necessary to manually specify the transported metabolite. using e.g.  
reaction.transported_mets = {Glc_e: -1} to represent extracellular glucose as the metabolite that is transported across the membrane. 

By setting the argument ‘report’ to True, the function model.update_thermo_info() can provide a reporting table as a pandas DataFrame, with information on the stoichiometry, balancing status and transported metabolites/charge/protons of each reaction. In this table, reactions that require inspection by the user will appear in the top rows. 

 In general, this is automatically determined but in some cases is ambiguous. Ambiguous reactions are highlighted to the user for manual curation. Curation consists of specifying manually the number of transported free protons or ions. (e.g. reaction.transported_h = {'e' : -1, 'c' : 1} to represent the transport of one proton from the extracellular to cytosolic compartment). As an example, the reaction of mitochondrial Complex II " Ubiquinone-8_c + succinate_m <=> fumarate_m +   Ubiquinol-8_c” would need the user to specify "tmodel.reactions.ComplexII.transported_h = {'m': -2.0, 'c': 2.0}" as two protons are moved from the mitochondria to the cytosol and are subsequently taken up by the protonation of Ubiquinone-8  into Ubiquinol-8. 

