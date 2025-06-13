

# Extended Info

This section provides detailed technical guidance on how to define the physical, chemical, and thermodynamic properties necessary to build a complete and functional model with **Thermo-Flux**. It is intended for advanced users who wish to understand or customize the internal thermodynamic processing steps beyond the basic tutorials.

## Step 1: Definition of Physical and Biochemical Parameters

**Thermo-Flux** models rely on a well-defined thermodynamic environment. This includes pH, ionic strength, temperature, and compartment-specific membrane potentials.

**Membrane Potentials** Membrane potential between compartment `c` and `e` is defined as:

.. math::

```
 \Delta \Phi_{c,e} = \Phi_c - \Phi_e
```

These values are used when transforming standard Gibbs energies into condition-specific values.

Refer to *Table 1* in the legacy documentation for default values and references.

## Step 2: Definition of Metabolites and Chemical Species

**Automatic Linking to eQuilibrator**

**Thermo-Flux** automatically identifies metabolites and links them to corresponding eQuilibrator compounds via `metabolite.compound`.

To manually define or override annotations::

metabolite.annotation = {'CHEBI': '11111', 'kegg': 'C00000'}

**Species Information**

Use::

metabolite.average\_charge\_protons()

This function calculates:

- Average charge
- Average number of protons
- Average number of magnesium ions

It also provides information about the individual species used for averaging.

.. admonition:: Box 1: Additional Considerations for Metabolite Definition

**Non-Decomposable or Unknown Structures**::

```
 metabolite.formula = 'C6H12O6'
 metabolite.charge = -1
```

**Local Cache Access to eQuilibrator** On first use, **Thermo-Flux** will download and cache the eQuilibrator compound database (`compound.sqlite`), supporting local retrieval and manual edits.

```
 See: https://equilibrator.readthedocs.io/en/latest/local_cache.html
```

## Step 3: Calculation of Gibbs Formation Energies

Call::

model.update\_thermo\_info()

This updates each metabolite with:

- Transformed formation Gibbs energy (`dfG'\u2070`)
- Average charge and proton count

.. admonition:: Box 2: Advanced Considerations

**Uncertainty**::

```
 model.rmse_inf = Q_(3000, 'kJ/mol')
```

**Estimating Unknown Formation Energies**::

```
 model.update_thermo_info(fit_unknown_dfG0=True)
```

**Redox Reactions**::

```
 cyt_c_red_c.dfG0prime = Q_(-12.05, 'kJ/mol')
 cyt_c_red_c.dfG_SE = Q_(0, 'kJ/mol')
 cyt_c_red_c.redox = True
```

**Biomass Formation Energy**::

```
 dfGbm = thermo_flux.tools.drg_tools.dfGbm(H=1.613, O=0.557, N=0.158, P=0.012, S=0.003, K=0.022, Mg=0.003, Ca=0.001, units='kJ/g')
 biomass = model.metabolites.biomass
 biomass.dfGprime = dfGbm
 biomass.dfG_SE = 0
 biomass.biomass = True
```

Units should be entered as `kJ/mol`, even though biomass formation energy is typically reported in `J/gDW`.

## Step 4: Defining Transported Protons

To define additional transported protons::

reaction.transported\_h = {'e': -1, 'c': 1}

This example represents one proton moving from the extracellular space (`e`) to the cytosol (`c`).

.. admonition:: Box 3: Transporter Variants and Special Cases

**Charge-Neutral Variants**::

```
 reaction.add_transporter_variants()
```

Example: Original: `pi_e → pi_c` Added: `pi_e + H_e → pi_c + H_c`

**Chemical Transformation During Transport**::

```
 reaction.transported_mets = {Glc_e: -1}
```

**Reporting**::

```
 model.update_thermo_info(report=True)
```

**Manual Curation Example**::

```
 tmodel.reactions.ComplexII.transported_h = {'m': -2.0, 'c': 2.0}
```

## Step 5: pH-Dependent Charge and Proton Balancing

Use::

reaction.reaction\_balance(balance\_mg=True)

Balances both protons and Mg²⁺ ions based on average microspecies.

**Example**: ATP hydrolysis may add \~0.7 protons for full balancing.

## Step 6: Calculation of Reaction Gibbs Energies

After running::

model.update\_thermo\_info()

Each reaction provides:

- `reaction.drG0`: Standard reaction Gibbs energy
- `reaction.drG0prime`: Transformed Gibbs energy under current conditions

## Step 7: Thermodynamic-Stoichiometric Solution Space

**Concentration Bounds**::

metabolite.lower\_bound = Q\_(10, 'uM')

Bounds are converted to mol/L internally.

**TFBA Problem Setup**::

model.add\_TFBA\_variables() model.m.optimize()

Linear program includes thermodynamic constraints.

.. admonition:: Box 4: Whole-Cell Constraints & Relaxation

**Whole-Cell Metabolite Concentrations**::

```
 model.total_cell_conc(cell_data_df, compartment_volumes_dict)
```

**Relax Second Law**::

```
 reaction.ignore_snd = True
```

**Ignore Pseudo-Metabolites**::

```
 metabolite.ignore_conc = True
```

**Variability Analysis**::

```
 solver.gurobi.variability_analysis(['qm', 'ln_conc'])
 results = solver.gurobi.variability_results()
```

## Step 8: Regression – Fitting to Experimental Data

Use::

model.regression(data\_df)

`data_df` should provide flux or concentration measurements. This adds constraints and objectives to match these values.

.. admonition:: Box 5: Model Starting Points

To improve solver stability::

```
 thermo_flux.solver.gurobi.model_start(tmodel, 'filename.sol', ignore_vars=['all'], fix_vars=['qm', 'ln_conc'], fix='start')
```

Ensures only trusted variables are used to seed the optimization.

