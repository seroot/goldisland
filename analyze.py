import re
import sys
import csv
import argparse

"""
	This script runs through the input arguments ( Lammps log files) and extracts performance metrics for analyzing 
	parallel speed up on Comet using OpenMP and MPI 
"""
#Loop time of 1445.08 on 2 procs (1 MPI x 2 OpenMP) 
#\s+([\d]+)
patterns = {
	"Loop": re.compile("Loop time of\s+([\d\.]+)"),
	"Pair": re.compile("Pair  time \(\%\) =\s+([\d\.]+)"),
	"Bond": re.compile("Bond  time \(\%\) =\s+([\d\.]+)"),
	"Neigh": re.compile("Neigh time \(\%\) =\s+([\d\.]+)"),
	"Comm": re.compile("Comm  time \(\%\) =\s+([\d\.]+)"),
	"MPI": re.compile("procs \(+([\d]+)"),
	"OMP": re.compile("MPI x\s+([\d]+)")

}


def get_results(filename):
	data = {}
	with open(filename) as f:
		for l in f:
			for k, p in patterns.items():
				m = p.search(l)
				if m:
					data[k] = float(m.group(1))
					continue
	return data

def analyze(filenames):
	fieldnames = ['filename', 'Loop', 'Pair', 'Bond', 'Neigh', 'Comm', 'MPI', 'OMP']
	#fieldnames2 = ['MPI', 'OMP', 'Loop']
	with open('results.csv', 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for f in filenames:
			r = get_results(f)
			print r
			r["filename"] = f
			writer.writerow(r)
	print("Results written to results.csv :)")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description='''Tool for analysis of OpenMP, MPI Speed up of LAMMPS''')
	parser.add_argument(
		'filenames', metavar= 'filenames', type=str, nargs="+",
		help= 'Files to process. You may us wildcards')
	args = parser.parse_args()
	analyze(args.filenames)
	
