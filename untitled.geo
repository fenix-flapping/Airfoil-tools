//+
Point(1) = {0, 1, 0, 1.0};
//+
Point(2) = {0, -1, 0, 1.0};
//+
Point(3) = {1, -1, 0, 1.0};
//+
Point(4) = {1, 1, 0, 1.0};
//+
Point(5) = {0.3, 1, 0, 1.0};
//+
Point(6) = {0.3, -1, 0, 1.0};
//+
Point(7) = {1.3, 0, 0, 1.0};
//+
Point(8) = {-3, 3, 0, 1.0};
//+
Point(9) = {-3, -3, 0, 1.0};
//+
Point(10) = {5, -3, 0, 1.0};
//+
Point(11) = {5, 3, 0, 1.0};
//+
Point(12) = {5, 0, 0, 1.0};
//+
Point(13) = {0, 0, 0, 1.0};
//+
Line(1) = {1, 5};
//+
Line(2) = {5, 4};
//+
Line(3) = {4, 3};
//+
Line(4) = {3, 6};
//+
Line(5) = {6, 2};
//+
Line(6) = {2, 13};
//+
Line(7) = {13, 1};
//+
Line(8) = {4, 7};
//+
Line(9) = {7, 3};
//+
Line(10) = {7, 12};
//+
Point(14) = {0.3, 3, 0, 1.0};
//+
Point(15) = {0.3, -3, 0, 1.0};
//+
Point(16) = {-3, 0, 0, 1.0};
//+
Point(17) = {1, 0.25, 0, 1.0};
//+
Point(18) = {1.3, 0.25, 0, 1.0};
//+
Point(19) = {1.3, -0.25, 0, 1.0};
//+
Point(20) = {5, -0.25, 0, 1.0};
//+
Point(21) = {5, 0.25, 0, 1.0};
//+
Recursive Delete {
  Line{8}; 
}
//+
Recursive Delete {
  Line{9}; 
}
//+
Recursive Delete {
  Line{10}; 
}
//+
Recursive Delete {
  Point{17}; 
}
//+
Line(8) = {4, 18};
//+
Line(9) = {18, 19};
//+
Line(10) = {19, 3};
//+
Line(11) = {19, 20};
//+
Line(12) = {18, 21};
//+
Line(13) = {21, 20};
//+
Line(14) = {21, 11};
//+
Line(15) = {11, 14};
//+
Line(16) = {14, 5};
//+
Line(17) = {14, 8};
//+
Line(18) = {16, 8};
//+
Line(19) = {16, 13};
//+
Line(20) = {9, 16};
//+
Line(21) = {9, 15};
//+
Line(22) = {6, 15};
//+
Line(23) = {15, 10};
//+
Line(24) = {20, 10};
//+
Recursive Delete {
  Line{15}; 
}
//+
Recursive Delete {
  Line{23}; 
}
//+
Point(22) = {1, 3, -0, 1.0};
//+
Point(23) = {1, -3, -0, 1.0};
//+
Point(24) = {1.3, 3, -0.1, 1.0};
//+
Point(25) = {1.3, -3, -0.1, 1.0};
//+
Line(25) = {14, 22};
//+
Line(26) = {22, 4};
//+
Line(27) = {23, 3};
//+
Line(28) = {15, 23};
//+
Line(29) = {23, 25};
//+
Line(30) = {25, 19};
//+
Line(31) = {24, 18};
//+
Line(32) = {22, 24};
//+
Line(33) = {24, 11};
//+
Line(34) = {10, 25};
//+
Recursive Delete {
  Line{7}; Line{1}; Line{6}; Line{5}; 
}
//+
Circle(35) = {5, 13, 5};
//+
Recursive Delete {
  Line{35}; 
}
//+
Ellipse(35) = {5, 13, 13, 13};
//+
Recursive Delete {
  Line{35}; 
}
//+
Line(35) = {5, 13};
//+
Line(36) = {13, 6};
//+
Line Loop(1) = {16, 35, -19, 18, -17};
//+
Plane Surface(1) = {1};
//+
Line Loop(2) = {20, 19, 36, 22, -21};
//+
Plane Surface(2) = {2};
//+
Line Loop(3) = {22, 28, 27, 4};
//+
Plane Surface(3) = {3};
//+
Line Loop(4) = {29, 30, 10, -27};
//+
Plane Surface(4) = {4};
//+
Line Loop(5) = {3, -10, -9, -8};
//+
Plane Surface(5) = {5};
//+
Line Loop(6) = {31, -8, -26, 32};
//+
Plane Surface(6) = {6};
//+
Line Loop(7) = {25, 26, -2, -16};
//+
Plane Surface(7) = {7};
//+
Line Loop(8) = {11, -13, -12, 9};
//+
Plane Surface(8) = {8};
//+
Line Loop(9) = {14, -33, 31, 12};
//+
Plane Surface(9) = {9};
//+
Line Loop(10) = {11, 24, 34, 30};
//+
Plane Surface(10) = {10};
//+
Transfinite Line {17} = 10 Using Progression 1;
//+
Transfinite Line {19} = 10 Using Progression 1;
//+
Transfinite Line {21} = 10 Using Progression 1;
//+
Transfinite Line {20} = 10 Using Progression 1;
//+
Transfinite Line {22, 36} = 5 Using Progression 1;
//+
Transfinite Line {35, 16} = 5 Using Progression 1;
//+
Transfinite Line {16, 26, 8, 10, 27} = 5 Using Progression 1;
//+
Transfinite Line {31, 30} = 10 Using Progression 1;
//+
Transfinite Line {3, 9, 13} = 10 Using Progression 1;
//+
Transfinite Line {14, 24} = 10 Using Progression 1;
//+
Transfinite Line {34, 11, 12, 33} = 10 Using Progression 1;
//+
Transfinite Line {18} = 10 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {10};
//+
Transfinite Surface {9};
//+
Transfinite Surface {8};
//+
Transfinite Surface {6};
//+
Transfinite Surface {7};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Recombine Surface {10};
//+
Recombine Surface {9};
//+
Recombine Surface {8};
//+
Recombine Surface {6};
//+
Recombine Surface {7};
//+
Recombine Surface {4};
//+
Recombine Surface {3};
//+
Recombine Surface {4};
//+
Recombine Surface {6};
//+
Recombine Surface {1};
//+
Recombine Surface {2};
//+
Recombine Surface {5};
//+
Transfinite Line {32, 8, 10, 29} = 5 Using Progression 1;
//+
Transfinite Line {26, 31, 14} = 5 Using Progression 1;
//+
Transfinite Line {30, 24, 27} = 5 Using Progression 1;
//+
Transfinite Line {9, 13} = 10 Using Progression 1;
//+
Transfinite Line {3} = 10 Using Progression 1;
//+
Transfinite Line {9} = 10 Using Progression 1;
//+
Transfinite Line {3} = 10 Using Progression 1;
//+
Recombine Surface {5};
//+
Transfinite Line {8, 10} = 5 Using Progression 1;
//+
Transfinite Line {3} = 10 Using Progression 1;
//+
Transfinite Line {3} = 10 Using Progression 1;
//+
Transfinite Line {9, 3} = 10 Using Progression 1;
//+
Transfinite Surface {5};
