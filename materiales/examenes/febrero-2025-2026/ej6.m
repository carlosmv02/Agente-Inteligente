function [Cek,Ck]=ej6(opc)
% opc(1): A-C
% opc(2): A-C
% opc(3): A-C
% opc(4): A-B

% Corrección: a/b correctas 0.1, 
% c correcta 0.1,  
% variables 0.1
% 2 últimos bucles correctos && Ce y Ck bien formadas 0.2
% C correcta 0.1 (sólo si con bucles)
% ejecuta y solución correcta 0.4

D=12;
E=8;

variables = {};
for d = 1:D
  for dir = ['u', 'd']
	  for e = 1:E/2
		  variables{end+1} = ['x' num2str(d) num2str(e) dir];
    end
	end
end

K=2;

for k = 1:K
  for dir = ['u', 'd']
	  for e = 1:E/2
		  variables{end+1} = ['y' num2str(k) num2str(e) dir];
    end
	end
end

for dir = ['u', 'd']
  for e = 1:E/2
		  variables{end+1} = ['u' num2str(e) dir];
  end
end

variables

% opc1 = A-C
V=4;

switch opc(1) % Topologías: RELLENAR MANUALMENTE
  
  case 'A'
	a = [ 
	1 0 0 0 
	0 1 0 0
	1 0 0 0
	0 1 0 0
	0 0 1 0
	0 0 0 1
	0 0 0 1
	0 0 1 0]; % origen [ExV]
  
  case 'B'
	a = [ 
	1 0 0 0 
	0 1 0 0
	1 0 0 0
	0 0 1 0
	0 0 1 0
	0 0 0 1
	0 1 0 0
	0 0 0 1]; % origen [ExV]
       
   case 'C'
	a = [ 
	1 0 0 0 
	0 0 1 0
	1 0 0 0
	0 1 0 0
	0 1 0 0
	0 0 0 1
	0 0 0 1
	0 0 1 0]; % origen [ExV]
    

end

b = [ a(5:8,:); a(1:4,:)];

switch opc(2) % Demandas: RELLENAR MANUALMENTE
  case 'A'
  
	c = [ 68  81  49 -85   0   0 -54   0   0 -62   0  0
       -68   0   0  85  16  19   0 -80   0   0 -35  0
         0 -81   0   0 -16   0  54  80  81   0   0 -3
         0   0 -49   0   0 -19   0   0 -81  62  35  3  ]; % demands [VxD]
    
  case 'B'
   
	c = [ 40  64  50 -27   0   0 -33   0   0 -47   0   0
       -40   0   0  27  11  43   0 -93   0   0 -93   0
         0 -64   0   0 -11   0  33  93  28   0   0 -80
         0   0 -50   0   0 -43   0   0 -28  47  93  80 ]; % demands [VxD]
              
              
  case 'C'
  
	c = [  9  47  85 -85   0   0 -89   0   0 -24   0   0
        -9   0   0  85  93   9   0 -12   0   0 -88   0
         0 -47   0   0 -93   0  89  12  97   0   0 -52
         0   0 -85   0   0  -9   0   0 -97  24  88  52  ]; % demands [VxD] 

end
	
a
b
c

switch opc(3) % Capacidades: RELLENAR MANUALMENTE
  case 'A'
	Ck = [1, 10];
   case 'B'
	Ck = [1, 3];
   case 'C'
	Ck = [3, 10];
end

switch opc(4) % Capacidades por enlace: RELLENAR MANUALMENTE
  case 'A'
	   for e = 1:E/2
	      for k = 1:K
          Eps(e,k) = e + k;
          Eps(e+(E/2),k) = e + k; 
        end
        Kap(e) = 10*e;
        Kap(e+(E/2)) = 10*e;
     end
  case 'B'
	   for e = 1:E/2
	      for k = 1:K
          Eps(e,k) = e*k;
          Eps(e+(E/2),k) = e*k; 
        end
        Kap(e) = 100*e;
        Kap(e+(E/2)) = 100*e;
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

for e=1:E, % restricciones de desigualdad
	xcoef = zeros(E,D);
	ycoef = zeros(E,K);
	ycoef(e,:) = 1;
	ucoef = zeros(1,E);
	ucoef(e) = -100000;
	
  A = [A;[xcoef(:)' ycoef(:)' ucoef(:)']];
	B = [B;0];
end


CTYPE = char(["S"*ones(1,D*V) "U"*ones(1,E) "U"*ones(1,E)]);
C=[zeros(1,E*D) Eps(:)' Kap(:)']';
LB = zeros(1,E*D+E*K+E);
UB = Inf*ones(1,E*D+E*K+E);

VARTYPE = char(['C'*ones(1,E*D) 'I'*ones(1,E*K) 'I'*ones(1,E)]);

[XOPT, FMIN] = glpk (C, A, B, LB, UB, CTYPE, VARTYPE);

disp(sprintf('Valor de la funcion: %f',FMIN))

disp('El optimo es:')
for i=1:length(XOPT),
  disp(sprintf('\t %s: %f',variables{i},XOPT(i)))
end







