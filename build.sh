#!/bin/bash

PKG=epcqrcode
COMPILE="pdflatex -interaction=nonstopmode"

function cleantex() {
	EXT=("aux" "fdb_latexmk" "fls" "log" "synctex.gz" "glo" "hd" "idx" "ilg" "ind" "out")

	if [ "$1" == "all" ]; then
		EXT+=("pdf" "sty" "zip")
	fi
	
	for FILE in "${EXT[@]}"; do
		rm -vf *.$FILE
	done
}

cleantex all

$COMPILE "$PKG.ins"
$COMPILE "$PKG.dtx"

cleantex

zip epcqrcode.zip $PKG.dtx $PKG.ins README $PKG.pdf
