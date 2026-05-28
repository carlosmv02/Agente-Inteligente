function ej2(opc)
% opc(1): A-E
% opc(2): A-B
% opc(3): A-B

LANs=3;
E=5;
PATHs=2;
if opc(2)=='A', K=3; end

switch opc(1),
  case {'A', 'B', 'D'} 
    V=4;
    
  case {'C', 'E'}
    V=5;

end

# macros
macros

# variables
if opc(3)=='A',
    for i=1:length(hi),
      for j=1:E,
        if opc(2)=='A',
          vx{i,j} = sprintf('x(%d,%du)',i,j); 
          vx{i,j+E} = sprintf('x(%d,%dd)',i,j); 
        else
          for s=0:2,
            vx{i,j+s*2*E} = sprintf('x(%d,%du,%d)',i,j,s); 
            vx{i,j+s*2*E+E} = sprintf('x(%d,%dd,%d)',i,j,s); 
          endfor
        end
      endfor
    endfor
else
  for i=1:V,
    for j=1:E,
        if opc(2)=='A',
          vx{i,j} = sprintf('x(%d,%du)',i,j); 
          vx{i,j+E} = sprintf('x(%d,%dd)',i,j);
        else
          for s=0:2,
            vx{i,j+s*2*E} = sprintf('x(%d,%du,%d)',i,j,s); 
            vx{i,j+s*2*E+E} = sprintf('x(%d,%dd,%d)',i,j,s); 
          end
        end
    endfor
  endfor
end

if opc(2)=='A',  
  for e=1:E,
    for k=1:K,
    vy{e,k} = sprintf('y(%du,%d)',e,k);
    vy{e+E,k} = sprintf('y(%dd,%d)',e,k);
    end 
  end 
else
  for e=1:E,
    vy{e} = sprintf('y(%du)',e);
    vy{e+E} = sprintf('y(%dd)',e);
  end   
endif
  
   
#demandas
H = [0 100 50; 66  0  10; 150 47  0];

% opc1 = A-E
switch opc(1) % Topologías: RELLENAR MANUALMENTE
  case 'A'
    
    tabla(u1(),:) = [1,1,3]; % [enlace,nodo in,nodo fin] 
    tabla(u2(),:) = [2,1,4]; % RELLENAR MANUALMENTE 
    tabla(u3(),:) = [3,2,3];
    tabla(u4(),:) = [4,3,4];
    tabla(u5(),:) = [5,2,4]; % FIN RELLENAR MANUALMENTE
    tabla(d1(),:) = tabla(u1(),[1 3 2]);
    tabla(d2(),:) = tabla(u2(),[1 3 2]);
    tabla(d3(),:) = tabla(u3(),[1 3 2]);
    tabla(d4(),:) = tabla(u4(),[1 3 2]);
    tabla(d5(),:) = tabla(u5(),[1 3 2]);
    
   case 'B'
    
    tabla(u1(),:) = [1,1,4]; % [enlace,nodo in,nodo fin] 
    tabla(u2(),:) = [2,1,2]; % RELLENAR MANUALMENTE 
    tabla(u3(),:) = [3,2,3];
    tabla(u4(),:) = [4,3,4];
    tabla(u5(),:) = [5,2,4]; % FIN RELLENAR MANUALMENTE
    tabla(d1(),:) = tabla(u1(),[1 3 2]);
    tabla(d2(),:) = tabla(u2(),[1 3 2]);
    tabla(d3(),:) = tabla(u3(),[1 3 2]);
    tabla(d4(),:) = tabla(u4(),[1 3 2]);
    tabla(d5(),:) = tabla(u5(),[1 3 2]);
       
   case 'C'
    
    tabla(u1(),:) = [1,1,4]; % [enlace,nodo in,nodo fin] 
    tabla(u2(),:) = [2,1,5]; % RELLENAR MANUALMENTE 
    tabla(u3(),:) = [3,2,4];
    tabla(u4(),:) = [4,2,5];
    tabla(u5(),:) = [5,3,4]; % FIN RELLENAR MANUALMENTE
    tabla(d1(),:) = tabla(u1(),[1 3 2]);
    tabla(d2(),:) = tabla(u2(),[1 3 2]);
    tabla(d3(),:) = tabla(u3(),[1 3 2]);
    tabla(d4(),:) = tabla(u4(),[1 3 2]);
    tabla(d5(),:) = tabla(u5(),[1 3 2]);
   
   case 'D'
    
    tabla(u1(),:) = [1,1,3]; % [enlace,nodo in,nodo fin] 
    tabla(u2(),:) = [2,1,4]; % RELLENAR MANUALMENTE 
    tabla(u3(),:) = [3,2,3];
    tabla(u4(),:) = [4,3,4];
    tabla(u5(),:) = [5,1,2]; % FIN RELLENAR MANUALMENTE
    tabla(d1(),:) = tabla(u1(),[1 3 2]);
    tabla(d2(),:) = tabla(u2(),[1 3 2]);
    tabla(d3(),:) = tabla(u3(),[1 3 2]);
    tabla(d4(),:) = tabla(u4(),[1 3 2]);
    tabla(d5(),:) = tabla(u5(),[1 3 2]);
 
   case 'E'
    
    tabla(u1(),:) = [1,1,4]; % [enlace,nodo in,nodo fin] 
    tabla(u2(),:) = [2,3,5]; % RELLENAR MANUALMENTE 
    tabla(u3(),:) = [3,2,4];
    tabla(u4(),:) = [4,2,5];
    tabla(u5(),:) = [5,3,4]; % FIN RELLENAR MANUALMENTE
    tabla(d1(),:) = tabla(u1(),[1 3 2]);
    tabla(d2(),:) = tabla(u2(),[1 3 2]);
    tabla(d3(),:) = tabla(u3(),[1 3 2]);
    tabla(d4(),:) = tabla(u4(),[1 3 2]);
    tabla(d5(),:) = tabla(u5(),[1 3 2]);
end

% opc2 
disp('Formulación...')

for e=1:E,
  if opc(2)=='A',
    f = 'f = sum_e sum_k [eps(k) y(e,k)]';
    if opc(3)=='A',
      d = sprintf('sum_d x(d,e) <= sum_k [C(k) y(e,k)]],     e = 1...%d',E*2);
    else
      d = sprintf('sum_t x(t,e) <= sum_k [C(k) y(e,k)]],     e = 1...%d',E*2);
    end
    d2 = '';
    d3 = '';
    d4 = '';
    d5 = '';
  else
    f = 'f = sum_e [eps(e) y(e)]';
    if opc(3)=='A',
      d = sprintf('sum_d x(d,e,0) <= y(e)],     e = 1...%d',E*2);
      d2 = sprintf('sum_d x(d,e,1) <= y(e)]],     e = 1...%d-{2u,2d}',E*2);
      d3 = sprintf('sum_d x(d,e,1) <= 0,     e = 2u,2d');
      d4 = sprintf('sum_d x(d,e,2) <= y(e)]],     e = 1...%d-{3u,3d}',E*2);
      d5 = sprintf('sum_d x(d,e,2) <= 0,     e = 3u,3d');
    else
      d = sprintf('sum_t x(t,e,0) <= y(e)],     e = 1...%d',E*2);
      d2 = sprintf('sum_t x(t,e,1) <= y(e)]],     e = 1...%d-{2u,2d}',E*2);
      d3 = sprintf('sum_t x(t,e,1) <= 0,     e = 2u,2d');
      d4 = sprintf('sum_t x(t,e,2) <= y(e)]],     e = 1...%d-{3u,3d}',E*2);
      d5 = sprintf('sum_t x(t,e,2) <= 0,     e = 3u,3d');
    end
  end

end

if opc(3)=='A',
  if  opc(2)=='B',
    i = sprintf('sum_e [a(e,v)x(d,e,s) - b(t,v)x(d,e,s)] = ...  ,     v = 1...%d d = 1...%d s = 0,1,2',V,length(hi));
  else    
    i = sprintf('sum_e [a(e,v)x(d,e) - b(t,v)x(d,e)] = ...  ,     v = 1...%d d = 1...%d',V,length(hi));
  end
else
  if  opc(2)=='B',
    i = sprintf('sum_e [a(e,v)x(t,e,s) - b(t,v)x(t,e,s)] = ...  ,     v = 1...%d t = 1...%d s = 0,1,2',V,V);
  else   
    i = sprintf('sum_e [a(e,v)x(t,e) - b(e,v)x(t,e)] = ...  ,     v = 1...%d t = 1...%d',V,V);
  end
end


disp('')
disp('>> Minimiza') 
disp('')
disp(f) 
disp('')
disp('>> Sujeto A')
disp('')
disp(i)  
disp(d) 
disp('')
disp(d2) 
disp('')
disp(d3) 
disp('')
disp(d4) 
disp('')
disp(d5) 
disp('')

disp(sprintf('Vars X... %d variabes',length(vx(:))))
disp(vx)
disp('')

disp(sprintf('Vars Y... %d variabes',length(vy(:))))
disp(vy)
disp('')

variables = {};
for i=1:length(vx(:)),
  variables{i} = vx{i};
end

j=1;
for i=length(variables)+1:length(variables)+length(vy(:)),
    variables{i} = vy{j};
    j=j+1;
end  
 







