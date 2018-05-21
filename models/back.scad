include <params.scad>

rad = 3;

arm_len = 7;
arm_width = 1;
arm_angle = 15;
arm_depth = 10;


translate([rad + sin(arm_angle)*arm_len + case_thick, -arm_depth/2, arm_len + case_width/2 - case_width/3])
rotate([-90,0,0])
linear_extrude(height=arm_depth)
difference() {
    union() {
        // arc
        difference() {
            circle(r=rad, $fn=20);
            circle(r=rad-1, $fn=20);
            translate([-rad,0,0])
                square([rad*2,rad]);
        };

        // arm 1
        translate([-rad + 0.05,-sin(arm_angle)*arm_width,0])
        rotate(arm_angle)
            square([arm_width, arm_len+5]);

        // arm 2
        translate([rad - arm_width - 0.05,-sin(arm_angle)*arm_width,0])
        rotate(-arm_angle)
            square([arm_width, arm_len+5]);
    };
    cutout_width = sin(arm_angle)*(arm_len+5)*2+rad*2;
    translate([-cutout_width/2,arm_len])
        square([cutout_width,5]);
};

union() {
    difference() {
        intersection() {
            translate([2+0.25,0,case_width/3])
            rotate([0,90,0])
                cylinder(h=case_length-case_thick*2- 0.5, r = case_width/2 - case_thick - 0.5);
            translate([-0.5, -case_width/2, -case_width/2 + case_width/3 + case_slice])
                cube([case_length+1, case_width, case_thick]);
        };
        translate([case_thick, -arm_depth/2 - 0.5, case_width/2 - case_width/3 - 0.5])
            cube([rad*2 + sin(arm_angle)*arm_len*2 - arm_width/sin(90-arm_angle), arm_depth + 1, case_thick + 1]);
    };
    translate([case_thick/3 * 2, -5, -case_width/2 + case_width/3 + case_slice + 1])
        cube([1.5,10,1]);
    translate([case_thick/3 * 2 + case_length - case_thick*2 + case_thick/3 * 2 - 2, -5, -case_width/2 + case_width/3 + case_slice + 1])
        cube([2,10,1]);
};
