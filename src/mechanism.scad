// OpenSCAD code for mechanism visualization
$fn=50; // Smooth rendering
color("red" )
translate([0.0, 0.0,-1]) cylinder(h=2,r=2);
color("blue")
translate([10.0, 35.0,-1]) cylinder(h=2,r=2);
color("red")
translate([-30, 0,-3]) cylinder(h=2,r=11.180339887498949);
color("blue")
translate([-25.0, 10.0,-1]) cylinder(h=2,r=2);
module connection(p1, p2) {{dx = p2[0] - p1[0]; dy = p2[1] - p1[1]; length = sqrt(dx*dx + dy*dy); translate(p1) {{rotate([0, 0, atan2(dy, dx)]) {{translate([length/2, 0, 0]) cube([length, 1.8, 1.8], center=true); }}}}}}
color("gray")
connection([0.0, 0.0,0], [10.0, 35.0,0]);
color("gray")
connection([10.0, 35.0,0], [-25.0, 10.0,0]);