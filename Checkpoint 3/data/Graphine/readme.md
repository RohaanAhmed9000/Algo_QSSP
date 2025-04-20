## Graphine: A Dataset for Graph-aware Terminology Definition Generation

This is the dataset of our EMNLP 2021 paper:

**Graphine: A Dataset for Graph-aware Terminology Definition Generation**. 

Zequn Liu, Shukai Wang, Yiyang Gu, Ruiyi Zhang, Ming Zhang* and Sheng Wang*

Please cite our paper when you use this dataset in your work.

The dataset is collected from three major biomedical ontology databases, including Open Biological and Biomedical Ontology Foundry (OBO)[<sup>1</sup>](#obo), BioPortal[<sup>2</sup>](#bioportal) and EMBL-EBI Ontology Lookup Service (OLS)[<sup>3</sup>](#ols)
Each directory in ```dataset``` corresponds to a biomedical subdisciplines (a DAG). There are three files in each directory: name.txt, def.txt and graph.json.

- name.txt & def.txt: 

Each line in ```name.txt``` is a terminology and the corresponding definition is in ```def.txt``` with the same line number.

- graph.json:

graph.json stores the adjacency dictionary of the DAG. Each key of the dictionary is a node with direct parents, and the corresponding value to the key is a list of these direct parents. All nodes are recorded by their terminologies. For example,```"myotube": ["striated muscle cell", "skeletal muscle cell", "multinucleate cell"] ``` shows that "myotube" has 3 parents, "striated muscle cell", "skeletal muscle cell" and "multinucleate cell". That is to say, "myotube is a striated muscle cell", "myotube is a skeletal muscle cell" and "myotube is a multinucleate cell". 

Since the dataset is large, we suggest you to choose part of it to conduct experiments. We use the following DAGs: tao, envo, uberon, so, xao, poro, chmo, cl, planp, phipo, po, exo, apo, pato, idomal, doid, omp, ecocore, fbbt, plana, ecto, fypo, aeo, vsao, pco, eco, mp, go, aro, pr, peco, mco and nbo.

<div id="obo"></div>

- [1] Smith B, Ashburner M, Rosse C, et al. The OBO Foundry: coordinated evolution of ontologies to support biomedical data integration[J]. Nature biotechnology, 2007, 25(11): 1251-1255.

<div id="bioportal"></div>

- [2] Noy N F, Shah N H, Whetzel P L, et al. BioPortal: ontologies and integrated data resources at the click of a mouse[J]. Nucleic acids research, 2009, 37(suppl_2): W170-W173.

<div id="ols"></div>

- [3] Jupp S, Burdett T, Leroy C, et al. A new Ontology Lookup Service at EMBL-EBI[J]. SWAT4LS, 2015, 2: 118-119.