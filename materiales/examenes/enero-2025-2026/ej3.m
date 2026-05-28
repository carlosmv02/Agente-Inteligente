function ej3(opc)
% opc(1): A-C
% opc(2): A-C
% opc(3): A-C
% opc(4): A-B

% Corrección: a/b correctas 0.1, 
% c correcta 0.1  
% variables 0.1
% 2 últimos bucles correctos && Ce y Ck bien formadas 0.2
% C correcta 0.1 (sólo si con bucles)
% ejecuta y solución correcta 0.4

D=6;
E=10;

% opc1 = A-C
switch opc(1),
  case {'A', 'B'} 
    V=5;
    
  case {'C'}
    V=4;
end

variables = {};
for v = 1:V
  for dir = ['u', 'd']
	  for e = 1:E/2
		  variables{end+1} = ['x' num2str(v) num2str(e) dir];
    end
	end
end

% opc(3) = A-B
switch opc(3),
  case {'A', 'B'} 
    K=3;
  case {'C'}
    K=2;
end

for k = 1:K
  for dir = ['u', 'd']
	  for e = 1:E/2
		  variables{end+1} = ['y' num2str(k) num2str(e) dir];
    end
	end
end


for dir = ['u', 'd']
  for e = 1:E/2
		  variables{end+1} = ['c' num2str(e) dir];
  end
end

variables

switch opc(1) % Topologías: RELLENAR MANUALMENTE
  
  case 'A'
	a = [ 
	1 0 0 0 0
	0 0 1 0 0
	0 1 0 0 0
	0 1 0 0 0
	0 0 1 0 0
	0 0 0 1 0
	0 0 0 0 1
	0 0 0 1 0
	0 0 0 0 1
	0 0 0 1 0]; % origen [ExV]
  
  case 'B'
	a = [ 
	1 0 0 0 0
	1 0 0 0 0
	0 1 0 0 0
	0 1 0 0 0
	0 0 1 0 0
	0 0 0 1 0
	0 0 0 0 1
	0 0 0 1 0
	0 0 0 0 1
	0 0 0 1 0]; % origen [ExV]
       
   case 'C'
	a = [ 
	1 0 0 0
	1 0 0 0
	0 1 0 0
	0 0 1 0
	0 1 0 0
	0 0 0 1
	0 1 0 0
	0 0 1 0
	0 0 0 1
	0 0 0 1]; % origen [ExV]
    

end

b = [ a(6:10,:); a(1:5,:)];

c = zeros(V,V);
switch opc(2) % Demandas: RELLENAR MANUALMENTE
  case 'A'
	c = [-50  10  105 0 0;
        30 -20  160 0 0;
        20  10 -265 0 0;
         0   0    0 0 0;
         0   0    0 0 0;]; % demands [VxV]
    
   case 'B'
	c = [-383   44   25 0 0;
         43 -554  110 0 0;
        340  510 -135 0 0;
          0    0    0 0 0;
          0    0    0 0 0;]; % demands [VxV]
          
   case 'C'
	c = [-120  100  150 0 0;
        110 -104   66 0 0;
         10    4 -216 0 0;
          0    0    0 0 0;
          0    0    0 0 0;]; % demands [VxV]

end
	
a
b
c

switch opc(3) % Capacidades: RELLENAR MANUALMENTE
  case 'A'
	Ck = [1, 10, 100];
   case 'B'
	Ck = [1, 3, 5];
   case 'C'
	Ck = [3, 10];
end

switch opc(4) % Capacidades por enlace: RELLENAR MANUALMENTE
  case 'A'
	  Ce0 = 2;
	  for e = 1:E
		  Cek(e,:) = Ck + 4;
	  end
  case 'B'
	  Ce0 = 0;
	  for k = 1:K
		  Cek(:,k) = [1 1 3 1 2 1 1 3 1 2]';
	  end
end


A = [];
B = [];

for v=1:V, % restricciones de igualdad 
	for t=1:V
		xcoef = zeros(E,V);
		xcoef(:,t) = a(:,v)-b(:,v);		
		A = [A;[xcoef(:)' zeros(1,E*K) zeros(1,E)]];
		B = [B;c(v,t)];
	end
end

for e=1:E, % restricciones de desigualdad
	xcoef = zeros(E,V);
	xcoef(e,:) = ones(1,V);
	ycoef = zeros(E,K);
	ycoef(e,:) = -Ck;
	A = [A;[xcoef(:)' ycoef(:)' zeros(1,E)]];
	B = [B;0];
end

for e=1:E, % restricciones de igualdad
	ycoef = zeros(E,K);
	ycoef(e,:) = -Cek(e,:);
  ccoef = zeros(E,1);
	ccoef(e) = 1;
	A = [A;[zeros(1,E*V) ycoef(:)' ccoef']];
	B = [B;Ce0];
end

CTYPE = char(["S"*ones(1,V*V) "U"*ones(1,E) "S"*ones(1,E)]);
C=[zeros(1,E*V) zeros(1,E*K) ones(1,E)]';
LB = zeros(1,E*V+E*K+E);
UB = Inf*ones(1,E*V+E*K+E);

VARTYPE = char(['C'*ones(1,E*V) 'I'*ones(1,E*K) 'C'*ones(1,E)]);

[XOPT, FMIN] = glpk (C, A, B, LB, UB, CTYPE, VARTYPE);

disp(sprintf('Valor de la funcion: %f',FMIN))

disp('El optimo es:')
for i=1:length(XOPT),
  disp(sprintf('\t %s: %f',variables{i},XOPT(i)))
end







