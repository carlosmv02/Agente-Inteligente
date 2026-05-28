function [Cek,Ck]=ej3(opc)
% opc(1): A-C
% opc(2): A-B
% opc(3): A-C
% opc(4): A-B

% Corrección: a/b correctas 0.1, 
% c correcta 0.1,  
% variables 0.1
% 2 últimos bucles correctos && Ce y Ck bien formadas 0.2
% C correcta 0.1 (sólo si con bucles)
% ejecuta y solución correcta 0.4

D=6;
E=10;

variables = {};
for d = 1:D
  for dir = ['u', 'd']
	  for e = 1:E/2
		  variables{end+1} = ['x' num2str(d) num2str(e) dir];
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

% opc1 = A-C
switch opc(1),
  case {'B', 'C'} 
    V=5;
    
  case {'A'}
    V=4;
end

switch opc(1) % Topologías: RELLENAR MANUALMENTE
  
  case 'A'
	a = [ 
	1 0 0 0 
	1 0 0 0
	0 1 0 0
	0 0 1 0
	1 0 0 0
	0 0 1 0
	0 0 0 1
	0 0 1 0
	0 0 0 1
	0 1 0 0]; % origen [ExV]
  
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
	0 0 0 1 0
	1 0 0 0 0
	0 1 0 0 0
	0 1 0 0 0
	0 0 1 0 0
	0 0 0 0 1
	0 0 0 1 0
	0 0 0 1 0
	0 0 0 0 1
	0 0 0 0 1]; % origen [ExV]
    

end

b = [ a(6:10,:); a(1:5,:)];

c = zeros(V,D);
switch opc(2) % Demandas: RELLENAR MANUALMENTE
  case 'A'
	c(1:3,:) = [ 10  105 -30    0 -20   0; 
		        -10    0  30  160   0 -10;
		          0 -105   0 -160  20  10]; % demands [VxD]
    
   case 'B'
	c(1:3,:) = [ 44  25 -43    0 -340    0; 
		        -44   0  43  110    0 -510;
		          0 -25   0 -110  340  510]; % demands [VxD]

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
	for d=1:D
		xcoef = zeros(E,D);
		xcoef(:,d) = a(:,v)-b(:,v);		
		A = [A;[xcoef(:)' zeros(1,E*K) zeros(1,E)]];
		B = [B;c(v,d)];
	end
end

for e=1:E, % restricciones de desigualdad
	xcoef = zeros(E,D);
	xcoef(e,:) = ones(1,D);
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
	A = [A;[zeros(1,E*D) ycoef(:)' ccoef']];
	B = [B;Ce0];
end

CTYPE = char(["S"*ones(1,D*V) "U"*ones(1,E) "S"*ones(1,E)]);
C=[zeros(1,E*D) zeros(1,E*K) ones(1,E)]';
LB = zeros(1,E*D+E*K+E);
UB = Inf*ones(1,E*D+E*K+E);

VARTYPE = char(['C'*ones(1,E*D) 'I'*ones(1,E*K) 'C'*ones(1,E)]);

[XOPT, FMIN] = glpk (C, A, B, LB, UB, CTYPE, VARTYPE);

disp(sprintf('Valor de la funcion: %f',FMIN))

disp('El optimo es:')
for i=1:length(XOPT),
  disp(sprintf('\t %s: %f',variables{i},XOPT(i)))
end







