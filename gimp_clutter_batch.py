#!/usr/bin/env python

from __future__ import print_function
from os import path
from glob import glob
from gimpfu import *
import sys

def batch_make_clutter_gimpfiles(dirpath, pdspath, outpath):
	"""Function to read in directory path and
	find all cluttersims found within, producing
	layered gimp files containing radar and 
	clutter simulation images.

	:param str dirpath: path to the directory
		containing cluttersims.
	:param str pdspath: path to the directory
		containing pds radargrams.
	:param str outpath: path to the directory
		you wish to output gimp files.
	"""

	sys.stderr = open(outpath + 'gimpstderr.txt','w')
	sys.stdout = open(outpath + 'gimpstdout.txt','w')

	clutter_pattern = dirpath + '*_geom_combined.png'
	clutter_list = sorted(glob(clutter_pattern))
	orbit_list = [path.basename(o)[:10] for o in clutter_list]
	num_orbits = len(orbit_list)
	print("{} orbits found in {}".format(num_orbits, dirpath))
	for orbit in orbit_list:
		print("Orbit # {}".format(orbit[2:]))
		outfile = outpath + orbit + '.xcf'
		if path.exists(outfile):
			print("    Gimp file already exists for this orbit at {}".format(outfile))
		else:
			simfile = dirpath + orbit + '_geom_combined.png'
			leftfile = dirpath + orbit + '_geom_left.png'
			rightfile = dirpath + orbit + '_geom_right.png'
			echofile = dirpath + orbit + '_geom_echomap_adjusted.png'
			pdsfile = pdspath + orbit + '_tiff.tif'
			if not path.exists(pdsfile):
				print("    PDS Radargram not found for {}. Continuing.".format(orbit))
				continue
			print("    Making gimp file at {}".format(outfile))
			make_clutter_gimpfile(simfile, leftfile, rightfile, echofile, pdsfile, outfile)
	print("Job Completed!")
	return

def make_clutter_gimpfile(simfile, leftfile, rightfile, echofile, pdsfile, outfile, hival=50, gamma=1.5):
	"""Function to produce layered gimp file including
	Cluttersim, Left Cluttersim, Right Cluttersim,
	PDS Radargram, and Echo Map (layers in that order).
	Cluttersims are also brightened for greater ease of
	viewing
	"""

	# Load in standard clutter simulation:
	img = pdb.file_png_load(simfile, simfile)
	#pdb.gimp_convert_rgb(img) # Make sure is RGB (not indexed color)
	pdb.gimp_levels(img.active_layer, 0, 0, hival, gamma, 0, 255) #Brighten levels on Cluttersim (also applied to left/right products)
	# Add in left side clutter sim
	left = pdb.gimp_file_load_layer(img, leftfile)
	img.add_layer(left, 0)
	pdb.gimp_levels(img.active_layer, 0, 0, hival, gamma, 0, 255)
	# Add in right side clutter sim
	right = pdb.gimp_file_load_layer(img, rightfile)
	img.add_layer(right, 0)
	pdb.gimp_levels(img.active_layer, 0, 0, hival, gamma, 0, 255)
	# Add in PDS Radargram:
	pds = pdb.gimp_file_load_layer(img, pdsfile)
	img.add_layer(pds, 0)
	# Add in Echo Power map and move down for better viewing:
	echo = pdb.gimp_file_load_layer(img, echofile)
	img.add_layer(echo, 0)
	img.active_layer.translate(0, 2750)

	# Save as XCF File (inactive):
	drawable = img.active_drawable
	pdb.gimp_xcf_save(0, img, drawable, outfile, outfile)

	# Display image and return:
	#pdb.gimp_display_new(img)
	return img

# Register Plug-in for use in GIMP:
args = [(PF_STRING, "dirpath", "Path to directory with clutter sims", '0'),
	(PF_STRING, "pdspath", "Path to directory with PDS Radargram tifs", "0"),
	(PF_STRING, "outpath", "Desired output path", '0')]
register(
	"clutter_batch",
	"Compile Cluttersims", 
	"batch_make_clutter_gimpfiles(dirpath, pdspath, outpath) -> img", 
	"Eric Petersen", 
	"", 
	"2018", 
	"", 
	"RGB*",
	args,
	[],
	batch_make_clutter_gimpfiles,
	menu = "<Image>/Filters/",
	domain = ("gimp20-python", gimp.locale_directory)
	)

main()
