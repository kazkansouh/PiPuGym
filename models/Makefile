# set path to location of openscad installation
OPENSCAD = openscad

TARGETS = case.stl back.stl

default: ${TARGETS}

%.stl: %.scad
	${OPENSCAD} -o $@ $<

clean:
	-rm -f ${TARGETS}

.PHONY: clean default
