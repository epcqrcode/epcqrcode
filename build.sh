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

	rm -rvf $PKG/
}

cleantex all

$COMPILE "$PKG.ins"
$COMPILE "$PKG.dtx"

mkdir $PKG
cp -v $PKG.ins $PKG/
cp -v $PKG.dtx $PKG/
cp -v $PKG.pdf $PKG/$PKG-doc.pdf
cp -v README $PKG/
zip $PKG.zip -r $PKG/

cleantex
