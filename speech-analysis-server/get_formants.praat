############################################################################
## get-formant.praat
##
## For all .wav files in a directory, measures marked vowel(s) and dumps measurements (F1, F2, dur) to outfile.
## 	1) for all sounds, create/modify TextGrid if option box is selected, where interval labels mark vowel
## 	2) get beginning and end of labeled intervals, making measurements as above with Formant object
##		and algebra
##
##
## Written by Robert Daland
## Dept. of Linguistics @ Northwestern University
## r-daland@northwestern.edu
## 10/18/2004
##
## adapted from code written by:
## Pauline Welby
## welby@ling.ohio-state.edu
## January 12, 2003
## 
############################################################################

# script arguments

form Input Enter directory and output file name
	boolean Modify_TextGrids 1
	sentence outFile formant-values.txt
	sentence dirName C:\Documents and Settings\Rajka Smiljanic\Desktop\praat demo\
endform

maxFormant = 5500
# men: 5000, women: 5500, children: 6000

# creates an output file with the specified name and adds headings 
# NB: if the named output file exists, it will be overwritten

outLine$ = "sound" + tab$ + "vowel" + tab$ + "f1" + tab$ + "f2" + tab$ + "duration" + newline$
outLine$ > 'dirName$''outFile$'

# If option box is checked (default), create/modify TextGrids
if modify_TextGrids
	execute label_vowels.praat 1 'dirName$'
else
	execute label_vowels.praat 0 'dirName$'
endif

Create Strings as file list... fileList 'dirName$'*.TextGrid
nFiles = Get number of strings

for i to nFiles
	# Read in sound file, textgrid, and calculate formant object
	select Strings fileList
	fileName$ = Get string... i
	Read from file... 'dirName$''fileName$'
	name$ = selected$("TextGrid")
	Read from file... 'dirName$''name$'.wav
	To Formant (burg)... 0.01 5 'maxFormant' 0.025 50

	# For each labeled interval (vowel), get measurements
	select TextGrid 'name$'
	nIntervals = Get number of intervals... 1
	for j to nIntervals
		select TextGrid 'name$'
		segment$ = Get label of interval... 1 'j'
		if length(segment$) > 0
			# retrieve/calculate time values (duration, midpoint)
			segBeg = Get starting point... 1 'j'
			segEnd = Get end point... 1 'j'
			segDur = segEnd - segBeg
			segMed = (1/2) * (segBeg + segEnd)

			# get F1 and F2 values
			select Formant 'name$'
			f1 = Get value at time... 1 'segMed' Hertz Linear
			f2 = Get value at time... 2 'segMed' Hertz Linear
			outLine$ = name$ + tab$ + segment$ + tab$ + "'f1:1'" + tab$ + "'f2:1'" + tab$ + "'segDur:4'" + newline$
			outLine$ >> 'dirName$''outFile$'
		endif
	endfor

	# clean up
	select TextGrid 'name$'
	plus Sound 'name$'
	plus Formant 'name$'
	Remove
endfor

# clean up
select Strings fileList
Remove
