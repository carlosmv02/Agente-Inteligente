function ej3(opc)
% opc(1): A-D
% opc(2): A-D
% opc(3): A-C
% Corrección: a/b correctas 0.1, 
% c correcta 0.1, 
% bucles casi correctos 0.5 (hay 5 bucles, 0.1 por cada si se aproxima razonablemente)
% variables 0.1
% C correcta 0.1, 
% ejecuta y solución correcta 0.1

D=3;
E=10;


% opc(1) = A-D
switch opc(1),
  case {'A', 'B'} 
    V=5;
  case {'C', 'D'}
    V=4;
end

variables = {};
for s = 0:1
  for v = 1:V
    for dir = ['u', 'd']
      for e = 1:E/2
        variables{end+1} = ['x' num2str(v) num2str(e) dir num2str(s)];
      end
    end
  end
end

for dir = ['u', 'd']
  for e = 1:E/2
		  variables{end+1} = ['y' num2str(e) dir];
	end
end


for dir = ['u', 'd']
  for e = 1:E/2
		  variables{end+1} = ['u' num2str(e) dir];
  end
end

variables

% opc1 = A-D
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
       
  case 'D'
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
    

end

b = [ a(6:10,:); a(1:5,:)];

c = zeros(V,V);
switch opc(2) % Demandas: RELLENAR MANUALMENTE
  case 'A'
	      c(1:3,1:3) = [  0 10 105; 
                       30  0 160; 
                       20 10   0]; % demands [VxV]
    
   case 'B'
	      c(1:3,1:3) = [  0  44  25; 
                       43   0 110; 
                      340 510   0]; % demands [VxV]
    
   case 'C'
	      c(1:3,1:3) = [ 0 100 150; 
                     110   0  66; 
                      10   4   0]; % demands [VxV]
    
   case 'D'
	      c(1:3,1:3) = [  0 10 15; 
                      110  0 16; 
                      210 200 0]; % demands [VxV]

end
	
a
b
c = -diag(sum(c)) + c

A = [];
B = [];

for v=1:V, % restricciones de igualdad S0
	for t=1:V
		xcoef = zeros(E,V);
		xcoef(:,t) = a(:,v)-b(:,v);	
		xcoef1 = zeros(E,V);	
		A = [A;[xcoef(:)' xcoef1(:)' zeros(1,E) zeros(1,E)]];
		B = [B;c(v,t)];
	end
end

for v=1:V, % restricciones de igualdad S1
	for t=1:V
		xcoef1 = zeros(E,V);
		xcoef1(:,t) = a(:,v)-b(:,v);	
		xcoef = zeros(E,V);	
		A = [A;[xcoef(:)' xcoef1(:)' zeros(1,E) zeros(1,E)]];
		B = [B;c(v,t)];
	end
end

for e=1:E, % restricciones de desigualdad S0
	xcoef = zeros(E,V);
	ycoef = zeros(1,E);
	xcoef(e,:) = ones(1,V);
	ycoef(e) = -10;	
	xcoef1 = zeros(E,V);	
	A = [A;[xcoef(:)' xcoef1(:)' ycoef zeros(1,E)]];
	B = [B;-3];
end

for e=1:E, % restricciones de desigualdad S1
	xcoef1 = zeros(E,V);
	ycoef = zeros(1,E);
	xcoef1(e,:) = ones(1,V);
  switch opc(3) 
    case 'A'
	    if e~=1, ycoef(e) = -10; B = [B;-3]; else, B = [B;0]; end	
    case 'B'
	    if e~=3, ycoef(e) = -10; B = [B;-3]; else, B = [B;0]; end	
    case 'C'
	    if e~=5, ycoef(e) = -10; B = [B;-3]; else, B = [B;0]; end	
  end
  xcoef = zeros(E,V);	
	A = [A;[xcoef(:)' xcoef1(:)' ycoef zeros(1,E)]];
end

for e=1:E, % restricciones de desigualdad con u's
	xcoef = zeros(E,V);
	xcoef1 = zeros(E,V);
	ycoef = zeros(1,E);
	ycoef(e) = 1;
	ucoef = zeros(1,E);
	ucoef(e) = -1000;
	A = [A;[xcoef(:)' xcoef1(:)' ycoef ucoef]];
	B = [B;0];
end

CTYPE = char(["S"*ones(1,2*V*V) "U"*ones(1,3*E)]);
C=[zeros(1,2*E*V) 2*ones(1,E) 20*ones(1,E)]';
LB = zeros(1,2*E*V+2*E);
UB = Inf(1,2*E*V+2*E);

VARTYPE = char(['C'*ones(1,2*E*V) 'I'*ones(1,E*2)]);


[XOPT, FMIN] = glpk (C, A, B, LB, UB, CTYPE, VARTYPE);

disp(sprintf('Valor de la funcion: %f',FMIN))

disp('El optimo es:')
for i=1:length(XOPT),
  disp(sprintf('\t %s: %f',variables{i},XOPT(i)))
end







