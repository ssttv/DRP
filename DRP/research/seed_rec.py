import load_cg, parse_rxn, uuid
import rebuildCDT

#Variable Setup.
CG = load_cg.load_cg()

reactant_fields = {
	"reactant_1": ("quantity_1", "unit_1"),
	"reactant_2": ("quantity_2", "unit_2"),
	"reactant_3": ("quantity_3", "unit_3"),
	"reactant_4": ("quantity_4", "unit_4"),
	"reactant_5": ("quantity_5", "unit_5"),
}

def get_reactants_indices(reaction):
	indices = dict()
	for r_f in reactant_fields:
		if reaction[r_f] not in CG:
			continue

		reactant_type = is_valid_reactant(reaction, r_f)
		if reactant_type == "Org":
			indices["org"] = r_f 
		elif reactant_type == "Inorg":
			if "metal_1" in indices:
				indices["metal_2"] = r_f
			else:
				indices["metal_2"] = r_f 
		elif reactant_type == "Water":
			indices["water"] = r_f	
	if "metal_1" not in indices or "metal_2" not in indices or "org" not in indices or "water" not in indices:
		raise Exception("Missing a metal or amine")
	return indices


def is_valid_reactant(reaction, r_f):
	if reaction[r_f] not in CG:
		raise Exception("Reactant not in cg: {0}".format(reaction[r_f]))
	if reaction[reactant_fields[r_f][1]] != "g":
		raise Exception("These aren't grams: {0}".format(reaction[r_f]))
	if not CG[reaction[r_f]]["mw"]:
		raise Exception("MW is zero: {0}".format(reaction[r_f]))

	return CG[reaction[r_f]]["type"]

def get_amine_moles(reaction, amine_index):
	return CG[reaction[amine_index]]["mw"] / reaction[reactant_fields[amine_index][0]]
	

def row_generator(reaction, indices, amine_moles, amine_list):
	
	metal_1 = reaction[indices["metal_one"]]
	metal_2 = reaction[indices["metal_two"]]
	amine = reaction[indices["org"]]
	water = reaction[indices["water"]]

	metal_1_mass = reaction[reactant_fields[indices["metal_one"]][0]]
	metal_2_mass = reaction[reactant_fields[indices["metal_two"]][0]]
	amine_moles = get_amine_moles(reaction, indices["org"])
	water_mass = reaction[reactant_fields[indices["water"]][0]]

	amine_range = get_amine_range(amine_moles)
	pH_range = [1,3,5]

	for amine in amine_list:
		if amine not in CG:
			print "Not in CG: {0}".format(amine)
			continue
		for moles in amine_range:
			mass = moles*CG[amine]["mw"]
			for pH in ph_range:
				yield ["--", metal_1, metal_1_mass, "g", metal_2, metal_2_mass,
					"g", amine, mass, "g", water, water_mass, "g", 
					reaction["temp"], reaction["time"], reaction["pH"], "yes", "no", 4, 2, ""]

def generate_grid(reaction, amine_list):
	#Variable Setup.
	indices = get_reactions_indices(reaction)
	amine_moles = get_amine_moles(reaction, indices["amine"])
	prefix = "/home/drp/web/..."
	fileprefix = str(uuid.uuid4())
	ml_convert = json.load(open("mlConvert.json"))
	hdrs = ",".join(rebuildCDT.headers)
	row_gen = row_generator(reaction, indices, amine_moles, amine_list)
	rows =[ ",".join([str(c).replace(",","c") for c in parse_rxn.parse_rxn(row, CG, ml_convert)])) for row in row_gen] 
	with open(prefix + fileprefix + ".csv", "w") as outfile:
		for row in rows:
			outfile.write(row+"\n")
			
	clean2arff.clean(prefix+fileprefix)

	#TODO: rewrite test_model
	cmd = "sh /home/drp/research/chemml-research-streamlined/scripts/test_model.sh {0}".format(name)
	result = subprocess.check_output(cmd, shell=True)

	weka_results_file = "/home/drp/blablabla..."
	results = []
	with open(prefix + weka_results_file, "r") as weka_results:
		for i in xrange(5):
			weka_results.next()

		for row in weka_results:
			if "4" in row and "+" not in row:
				conf = float(row.split()[-1])
				idx = int(row.split()[0])
				results.append( (idx, conf))









