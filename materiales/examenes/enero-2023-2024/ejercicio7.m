# Solución hecha en clase (ver video) para opciones AA y el enlace 5 con doble coste CAPEX

variables = { 'x11u', 'x12u', 'x13u', 'x14u', 'x15u', 'x11d', 'x12d', 'x13d', 'x14d', 'x15d', ...
'x21u', 'x22u', 'x23u', 'x24u', 'x25u', 'x21d', 'x22d', 'x23d', 'x24d', 'x25d', ...
'x31u', 'x32u', 'x33u', 'x34u', 'x35u', 'x31d', 'x32d', 'x33d', 'x34d', 'x35d', ...
'x41u', 'x42u', 'x43u', 'x44u', 'x45u', 'x41d', 'x42d', 'x43d', 'x44d', 'x45d', ...
'x51u', 'x52u', 'x53u', 'x54u', 'x55u', 'x51d', 'x52d', 'x53d', 'x54d', 'x55d', ...
'y11u', 'y12u', 'y13u', 'y14u', 'y15u', 'y11d', 'y12d', 'y13d', 'y14d', 'y15d', ...
'y21u', 'y22u', 'y23u', 'y24u', 'y25u', 'y21d', 'y22d', 'y23d', 'y24d', 'y25d', ...
'm'};

E = 10;
V = 5;
K = 2;


a = [ 1 0 0 0 0;
      0 0 1 0 0;
      0 1 0 0 0;
      0 1 0 0 0;
      0 0 1 0 0;
      0 0 0 1 0;
      0 0 0 0 1;
      0 0 0 1 0;
      0 0 0 0 1;
      0 0 0 1 0]; % origen [ExV]
      
b = [ 0 0 0 1 0;
      0 0 0 0 1;
      0 0 0 1 0;
      0 0 0 0 1;
      0 0 0 1 0;
      1 0 0 0 0;
      0 0 1 0 0;
      0 1 0 0 0;
      0 1 0 0 0;
      0 0 1 0 0]; % destino [ExV]
      
c = [-50 10 105 0 0;
     30 -20 160 0 0;
     20 10 -265 0 0;
     0 0 0 0 0;
     0 0 0 0 0]; % demandas [VxV]



A = [];
B = [];

for v=1:V, % restricciones de igualdad Ax = B
	for t=1:V
		xcoef = zeros(E,V);
		xcoef(:,t) = a(:,v)-b(:,v);		
		A = [A;[xcoef(:)' zeros(1,2*E+1)]];
		B = [B;c(v,t)];
	end
end

for e=1:E, % restricciones de desigualdad Ax <= B
	xcoef = zeros(E,V);
	xcoef(e,:) = ones(1,V);
  ycoef = zeros(E,K);
  ycoef(e,:) = [-10 -0.6];
	A = [A;[xcoef(:)' ycoef(:)' 1]];
	B = [B;0];
end

for e=1:E, % restricciones de desigualdad Ax <= B
	xcoef = zeros(E,V);
	xcoef(e,:) = 0.1*ones(1,V);
  ycoef = zeros(E,K);
  ycoef(e,:) = [0 -0.6];
	A = [A;[xcoef(:)' ycoef(:)' 0]];
	B = [B;0];
end

coste = 5*3*ones(1,E)+[10*ones(1,4) 20 10*ones(1,4) 20]; % CUIDADO! Esto está modificado después del vídeo porque era una errata
coste_bck = 5*1*ones(1,E)+[1*ones(1,4) 2 1*ones(1,4) 2];
 
CTYPE = char(["S"*ones(1,V*V) "U"*ones(1,2*E)]);
C = [zeros(1,E*V) coste coste_bck -0.1];
LB = zeros(1,E*(V+2)+1);
UB = Inf*ones(1,E*(V+2)+1);

VARTYPE = [repmat("C",1,E*V) repmat("I",1,E*2) "C"]; % CUIDADO! Esto está modificado después del vídeo para evitar un warning

[XOPT, FMIN] = glpk (C, A, B, LB, UB, CTYPE, VARTYPE);

disp(sprintf('Valor de la funcion: %f',FMIN))

disp('El optimo es:')
for i=1:length(XOPT),
  disp(sprintf('\t %s: %f',variables{i},XOPT(i)))
end


