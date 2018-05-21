# set path to location of openscad installation
OPENSCAD = openscad

TARGETS = case.stl back.stl
IMAGES = $(patsubst %.stl,%.png,${TARGETS})

default: ${TARGETS}
images: ${IMAGES}

%.stl %.png: %.scad
	${OPENSCAD} -o $@ $<

clean:
	-rm -f ${TARGETS} ${IMAGES}

.PHONY: clean default images
