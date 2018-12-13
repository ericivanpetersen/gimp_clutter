#!/usr/bin/env python

import sys
from gimpfu import *

def make_clutter_gimpfile(orbit, region, hival=50, gamma=1.5):
	"""Function to produce layered gimp file including
	Cluttersim, Left Cluttersim, Right Cluttersim,
	PDS Radargram, and Echo Map (layers in that order).
	Cluttersims are also brightened for greater ease of
	viewing

	:param orbit: 7-digit orbit number (6-digit orbit 
		numbers must be preceded by a 0)
	:param region: region name relevant to SWIMming 
		POOL Filepaths; options include:
		Onilus
		Utopia
		Arcadia
		Acidalia
	:param hival: Cutoff point for bright pixels used
		when altering levels for Cluttersims. 
		Value of 50 by default
	:param gamma: Gamma value used in altering levels
		for Cluttersims"""

	# Set up file paths to Cluttersims on SWIMming Pool:
		# (These paths can be altered to customize the 
		# 	plugin for non-SWIM computer):
	filepath = '//marstherm/Pool/ClutterSims/' + region + '/'
	simfile = filepath + 's_0' + orbit + '_geom_combined.png'
	leftfile = filepath + 's_0' + orbit + '_geom_left.png'
	rightfile = filepath + 's_0' + orbit + '_geom_right.png'
	echofile = filepath + 's_0' + orbit + '_geom_echomap_adjusted.png'
	# Set up file path to PDS Radargram TIFF File:
	pdsfile = '//marstherm/Pool/Browse Products/' + region.lower() + '_tiff/s_0' + orbit + '_tiff.tif'
	
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
	img.active_layer.translate(0, 3000)

	# Save as XCF File (inactive):
	#drawable = img.active_drawable
	#pdb.gimp_xcf_save(0, img, drawable, outfile, outfile)

	# Display image and return:
	pdb.gimp_display_new(img)
	return img

# Register Plug-in for use in GIMP:
args = [(PF_STRING, "Orbit", "Orbit Number", '0'),
	(PF_STRING, "Region", "Region Name", '0')]
register(
	"clutter",
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
