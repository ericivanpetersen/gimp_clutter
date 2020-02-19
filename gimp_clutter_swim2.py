#!/usr/bin/env python

import sys
from gimpfu import *

def make_clutter_gimpfile(orbit, region, hival=50, gamma=1.5):
	"""Function to produce layered gimp file including
	Cluttersim, Left Cluttersim, Right Cluttersim,
	PDS Radargram, and Echo Map (layers in that order).
	Cluttersims are also brightened for greater ease of
	viewing"""

	# Set up file paths:
	filepath = '//marstherm/Pool2/SHARAD_Clutter_Sim_PNGS/' + region + '/'
	simfile = filepath + 's_0' + orbit + '_geom_combined.png'
	leftfile = filepath + 's_0' + orbit + '_geom_left.png'
	rightfile = filepath + 's_0' + orbit + '_geom_right.png'
	echofile = filepath + 's_0' + orbit + '_geom_echomap_adjusted.png'
	pdsfile = '//marstherm/Pool2/SHARAD_TIFFS/' + region.lower() + '/s_0' + orbit + '_tiff.tif'
	outfile = '//marstherm/Pool2/Compiled_ClutterSims_Gimp/' + region + '/' + orbit + '.xcf'
	
	# Load in standard clutter simulation:
	img = pdb.file_png_load(simfile, simfile)
	#pdb.gimp_convert_rgb(img) # Make sure is RGB (not indexed color)
	pdb.gimp_levels(img.active_layer, 0, 0, hival, gamma, 0, 255)
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
	# Add in Echo Power map and move down:
	echo = pdb.gimp_file_load_layer(img, echofile)
	img.add_layer(echo, 0)
	img.active_layer.translate(0, 2750)
    
    # Display image:
	pdb.gimp_display_new(img)

	# Save as XCF File:
	drawable = img.active_drawable
	pdb.gimp_xcf_save(0, img, drawable, outfile, outfile)

	return img


#orbit = sys.argv[0]
#img = make_clutter_gimpfile(orbit)
args = [(PF_STRING, "Orbit", "Orbit Number", '0'),
	(PF_STRING, "Region", "Region Name", '0')]
register(
	"clutter_swim2",
	"Compile Cluttersim", 
	"make_clutter_gimpfile(orbit, region) -> img", 
	"Eric Petersen", 
	"", 
	"2018", 
	"", 
	"RGB*",
	args,
	[],
	make_clutter_gimpfile,
	menu = "<Image>/Filters/",
	domain = ("gimp20-python", gimp.locale_directory)
	)
main()
