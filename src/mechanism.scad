// OpenSCAD code for mechanism visualization
$fn=50; // Smooth rendering
color("red" )
translate([-28.0, -5.0,-1]) cylinder(h=2,r=2);
color("red" )
translate([28.0, -5.0,-1]) cylinder(h=2,r=2);
color("blue")
<<<<<<< HEAD
translate([10.0, 35.0,-1]) cylinder(h=2,r=2);
color("red")
translate([-30, 0,-3]) cylinder(h=2,r=11.180339887498949);
color("blue")
translate([-25.0, 10.0,-1]) cylinder(h=2,r=2);
module connection(p1, p2) {{dx = p2[0] - p1[0]; dy = p2[1] - p1[1]; length = sqrt(dx*dx + dy*dy); translate(p1) {{rotate([0, 0, atan2(dy, dx)]) {{translate([length/2, 0, 0]) cube([length, 2, 2], center=true); }}}}}}
color("gray")
connection([0.0, 0.0,0], [10.0, 35.0,0]);
color("gray")
connection([10.0, 35.0,0], [-25.0, 10.0,0]);
=======
translate([-16.0, 23.0,-1]) cylinder(h=2,r=2);
color("blue")
translate([-54.0, 6.5,-1]) cylinder(h=2,r=2);
color("blue")
translate([-44.0, -21.5,-1]) cylinder(h=2,r=2);
color("blue")
translate([-21.0, -35.0,-1]) cylinder(h=2,r=2);
color("blue")
translate([-35.0, -70.0,-1]) cylinder(h=2,r=2);
color("blue")
translate([33.93072639447164, 24.88020221541209,-1]) cylinder(h=2,r=2);
color("blue")
translate([55.947804291478, -10.212507581312847,-1]) cylinder(h=2,r=2);
color("blue")
translate([72.35517987650988, -35.00762860162045,-1]) cylinder(h=2,r=2);
color("blue")
translate([46.18649895184087, -29.864658772536796,-1]) cylinder(h=2,r=2);
color("blue")
translate([33.46172075954302, -65.34817635403964,-1]) cylinder(h=2,r=2);
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
color("gray")
connection([10.0, 0.0,0], [33.93072639447164, 24.88020221541209,0]);
color("gray")
connection([10.0, 0.0,0], [46.18649895184087, -29.864658772536796,0]);
color("gray")
connection([33.93072639447164, 24.88020221541209,0], [28.0, -5.0,0]);
color("gray")
connection([33.93072639447164, 24.88020221541209,0], [55.947804291478, -10.212507581312847,0]);
color("gray")
connection([55.947804291478, -10.212507581312847,0], [28.0, -5.0,0]);
color("gray")
connection([55.947804291478, -10.212507581312847,0], [72.35517987650988, -35.00762860162045,0]);
color("gray")
connection([72.35517987650988, -35.00762860162045,0], [46.18649895184087, -29.864658772536796,0]);
color("gray")
connection([72.35517987650988, -35.00762860162045,0], [33.46172075954302, -65.34817635403964,0]);
color("gray")
connection([33.46172075954302, -65.34817635403964,0], [46.18649895184087, -29.864658772536796,0]);
color("gray")
connection([46.18649895184087, -29.864658772536796,0], [28.0, -5.0,0]);
>>>>>>> 9eb5b52a040a7d928a3fbb45f08368470f3ce4b8
