// OpenSCAD code for mechanism visualization
$fn=50; // Smooth rendering
color("red" )
translate([-28.0, -5.0,-1]) cylinder(h=2,r=2);
color("blue")
translate([-16.0, 23.0,-1]) cylinder(h=2,r=2);
color("blue")
translate([-54.0, 6.5,-1]) cylinder(h=2,r=2);
color("blue")
translate([-44.0, -21.5,-1]) cylinder(h=2,r=2);
color("blue")
translate([-21.0, -35.0,-1]) cylinder(h=2,r=2);
color("blue")
translate([-35.0, -70.0,-1]) cylinder(h=2,r=2);
color("red")
translate([0, 0,-3]) cylinder(h=2,r=10);
color("blue")
translate([10.0, 0.0,-1]) cylinder(h=2,r=2);
module connection(p1, p2) {{dx = p2[0] - p1[0]; dy = p2[1] - p1[1]; length = sqrt(dx*dx + dy*dy); translate(p1) {{rotate([0, 0, atan2(dy, dx)]) {{translate([length/2, 0, 0]) cube([length, 2, 2], center=true); }}}}}}
color("gray")
connection([10.0, 0.0,0], [-16.0, 23.0,0]);
color("gray")
connection([10.0, 0.0,0], [-21.0, -35.0,0]);
color("gray")
connection([-16.0, 23.0,0], [-28.0, -5.0,0]);
color("gray")
connection([-16.0, 23.0,0], [-54.0, 6.5,0]);
color("gray")
connection([-54.0, 6.5,0], [-28.0, -5.0,0]);
color("gray")
connection([-54.0, 6.5,0], [-44.0, -21.5,0]);
color("gray")
connection([-44.0, -21.5,0], [-21.0, -35.0,0]);
color("gray")
connection([-44.0, -21.5,0], [-35.0, -70.0,0]);
color("gray")
connection([-35.0, -70.0,0], [-21.0, -35.0,0]);
color("gray")
connection([-21.0, -35.0,0], [-28.0, -5.0,0]);