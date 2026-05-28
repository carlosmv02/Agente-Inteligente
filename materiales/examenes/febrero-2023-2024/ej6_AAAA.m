function ej6_AAAA

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

K=3;

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

V=5;

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
	0 0 0 1 0]; 
	
b = [ a(6:10,:); a(1:5,:)];

c = zeros(V,D);
c(1:3,:) = [ 10  105 -30    0 -20   0; 
		        -10    0  30  160   0 -10;
		          0 -105   0 -160  20  10]; % demands [VxD]
	
a
b
c

Ck = [1, 10, 100];

Ce0 = 2;
for e = 1:E
	Cek(e,:) = Ck + 4;
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







