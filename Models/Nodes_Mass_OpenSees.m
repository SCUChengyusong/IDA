clc;clear;
Nodes_Property = readmatrix('Property_NREL5MWJacket.xlsx', 'Sheet', 'Nodes');
Elements_Property = readmatrix('Property_NREL5MWJacket.xlsx', 'Sheet', 'Elements');
Sections_Property = readmatrix('Property_NREL5MWJacket.xlsx', 'Sheet', 'Sections');
Nodes_Mass = zeros(length(Nodes_Property),1);
Elements_Mass = zeros(length(Elements_Property),1);
Sections_Mass = zeros(length(Sections_Property),1);
for i = 1:length(Sections_Mass)
    rho = Sections_Property(i,4);
    Radius = Sections_Property(i,5)./2;
    Thickness = Sections_Property(i,6);
    Sections_Mass(i) = pi*(Radius^2-(Radius-Thickness)^2)*rho;
end
for i = 1:length(Elements_Mass)
    Node_1 = Elements_Property(i,2);
    Node_2 = Elements_Property(i,3);
    Section_ID = Elements_Property(i,4);
    Node_1_C = Nodes_Property(Node_1,2:4);
    Node_2_C = Nodes_Property(Node_2,2:4);
    Element_Length = sqrt((Node_1_C(1)-Node_2_C(1))^2+(Node_1_C(2)-Node_2_C(2))^2+(Node_1_C(3)-Node_2_C(3))^2);
    LE(i) = Element_Length;
    Elements_Mass(i) = Sections_Mass(Section_ID)*Element_Length;
    Nodes_Mass(Node_1) = Nodes_Mass(Node_1) + Elements_Mass(i)./2;
    Nodes_Mass(Node_2) = Nodes_Mass(Node_2) + Elements_Mass(i)./2;
end
Mass_all = sum(Nodes_Mass);


