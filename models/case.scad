/*
    Housing for leds and controller
*/

include <params.scad>

module led_matrix(wide,deep) {
    height = 5;

    union() {
        for (i = [1 : wide]) {
            for (j = [1 : deep]) {
                translate([i*hob_spacing, j*hob_spacing, 0])
                cylinder(r1 = hob_radius,r2 = hob_radius,$fn = 12,h = height, center=false);
            }
        }

    };
};

difference() {
    translate([0,0,case_width/3])
    rotate([0,90,0])
        cylinder(h=case_length, r = case_width/2);
    translate([case_thick,0,case_width/3])
    rotate([0,90,0])
        cylinder(h=case_length-case_thick*2, r = case_width/2 - case_thick);
    translate([-0.5, -case_width/2, -case_width/2 + case_width/3])
        cube([case_length+1, case_width, case_slice]);
    translate([hob_spacing/2,-((hobs_deep+1)*hob_spacing)/2,case_width/2 + case_width/3 - case_thick - 1])
        led_matrix(hobs_wide,hobs_deep);
    translate([case_thick/3 * 2, -5, -case_width/2 + case_width/3 + case_slice + 1])
        cube([case_length - case_thick*2 + case_thick/3 * 2,10,1]);
};
