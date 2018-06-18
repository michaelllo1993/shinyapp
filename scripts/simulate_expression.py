import cobra
import sys

# Read the model in
model = cobra.io.read_sbml_model(str(model_file_path))
# Get the variable from reaction_ID a proper name
gene_ID = reaction_ID
# Find the reactions that are associated with the selected gene
reactions_associated = list(model.genes.get_by_id(gene_ID).reactions)
# For each of the reactions
for rxn in reactions_associated:
    # Get the ID
    ID_ori = rxn.id
    # Get the original flux bounds
    bounds_ori = rxn.bounds
    # Get the gene-protein-reaction rule
    gpr_ori = rxn.gene_reaction_rule
    # if there is any redundancy, there is no influence of the expression change on the fluxes in this specific reaction
    # It is a logical error, yet intentional as this software is not intended to reflect the complex biology perfectly
    if "or" in gpr_ori:
        pass
    # else - the original bounds are adjusted
    else:
        lb = bounds_ori[0] * bound
        ub = bounds_ori[1] * bound
        model.reactions.get_by_id(ID_ori).bounds = (lb, ub)

# Perform FBA
flux = model.optimize().f
# Save the results
fluxes = model.optimize().fluxes.round(2)
fluxes = fluxes.to_dict()
