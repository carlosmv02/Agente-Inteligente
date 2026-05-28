function ej2(opc)
% opc(1): A-D
% opc(2): A-D
% opc(3): A-B

LANs=3;
E=5;
PATHs=2;
if opc(2)=='A', K=3; end

switch opc(1),
  case {'A', 'B', 'D'} 
    V=4;
    
  case {'C'}
    V=5;

end

# macros
macros

# variables
if opc(3)=='A',
  if opc(2)=='D',
    for i=1:length(hi),
      for j=1:E,
        for s=1:2,
          vx{i,j} = sprintf('x(%d,%du,0)',i,j); 
          vx{i,j+E} = sprintf('x(%d,%dd,0)',i,j);
          vx{i,j+2*E} = sprintf('x(%d,%du,1)',i,j); 
          vx{i,j+3*E} = sprintf('x(%d,%dd,1)',i,j); 
        endfor
      endfor
    endfor
  else
    for i=1:length(hi),
      for j=1:E,
        vx{i,j} = sprintf('x(%d,%du)',i,j); 
        vx{i,j+E} = sprintf('x(%d,%dd)',i,j); 
      endfor
    endfor
  end
else
  for i=1:V,
    for j=1:E,
      vx{i,j} = sprintf('x(%d,%du)',i,j); 
      vx{i,j+E} = sprintf('x(%d,%dd)',i,j);
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
  else
    f = 'f = sum_e [eps(e) y(e)]';
    if opc(3)=='A',
      d = sprintf('sum_d x(d,e) <= y(e)],     e = 1...%d',E*2);
    else
      d = sprintf('sum_t x(t,e) <= y(e)],     e = 1...%d',E*2);
    end
  end
  
  if opc(2)=='B',
      PATHs=2;
    if opc(3)=='A',
      c2 = sprintf('sum_p [dlt(e,d,p) x(d,p)] = x(d,e),     e = 1...%d, d = 1...%d, ',E*2,length(hi));
    else
      return
    end
    
    c = sprintf('x(d,p) = h(d) u(d,p),         p = 1...%d, d = 1...%d, ',PATHs,length(hi));
    c = [c sprintf('\n\nsum_p u(d,p) = 1,         d = 1...%d, ',length(hi))]; 
    
  for i=1:length(hi),
    for j=1:PATHs,
      vx2{i,j} = sprintf('x(%d,%d)',i,j); 
      if opc(2)=='B'
        vu{i,j} = sprintf('u(%d,%d)',i,j); 
      else
        vu = {};
      end
    endfor
  endfor
  
  else
    c = '';
    c2 = '';
  end
  
  if opc(2)=='C',
    
    if opc(3)=='A',
      f = [f ' + 1K€ sum_e sum_d x(d,e)'];
    else
      f = [f ' + 1K€ sum_e sum_t x(t,e)'];
    end
    
  end
  
  if opc(2)=='D',
    
    if opc(3)=='A',
      d2 = sprintf('sum_d x(d,e,1) <= y(e)]],     e = 1...%d-{2u,2d,3u,3d}',E*2);
      d3 = sprintf('sum_d x(d,e,1) <= 0,     e = 2u,2d,3u,3d');
    else
      d2 = sprintf('sum_t x(t,e,1) <= y(e)]],     e = 1...%d-{2u,2d,3u,3d}',E*2);
      d3 = sprintf('sum_t x(t,e,1) <= 0,     e = 2u,2d,3u,3d');
    end
    
  else
    d2 = '';
    d3 = '';
  end
  
end

if opc(3)=='A',
  if  opc(2)=='D',
    i = sprintf('sum_e [a(e,v)x(d,e,s) - b(t,v)x(d,e,s)] = ...  ,     v = 1...%d d = 1...%d s = 0,1',V,length(hi));
  else    
    i = sprintf('sum_e [a(e,v)x(d,e) - b(t,v)x(d,e)] = ...  ,     v = 1...%d d = 1...%d',V,length(hi));
  end
else
  if  opc(2)=='D',
    i = sprintf('sum_e [a(e,v)x(t,e,s) - b(t,v)x(t,e,s)] = ...  ,     v = 1...%d t = 1...%d s = 0,1',V,V);
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
disp('')
disp(c)  
disp('') 
disp(c2) 
disp('')
disp(d) 
disp('')
disp(d2) 
disp('')
disp(d3) 
disp('')

disp(sprintf('Vars X... %d variabes',length(vx(:))))
disp(vx)
disp('')

if opc(2)=='B' 
  disp(sprintf('Vars X (FCD)... %d variabes',length(vx2(:))))
  disp(vx2)
  disp('')
  disp(sprintf('Vars U... %d variabes',length(vu(:))))
  disp(vu)
  disp('')
end

disp(sprintf('Vars Y... %d variabes',length(vy(:))))
disp(vy)
disp('')

variables = {};
for i=1:length(vx(:)),
  variables{i} = vx{i};
end

if opc(2)=='B' 
  j=1;
  for i=length(variables)+1:length(variables)+length(vx2(:)),
    variables{i} = vx2{j};
    j=j+1;
  end  
  j=1;
  for i=length(variables)+1:length(variables)+length(vu(:)),
    variables{i} = vu{j};
    j=j+1;
  end  
end
j=1;
for i=length(variables)+1:length(variables)+length(vy(:)),
    variables{i} = vy{j};
    j=j+1;
end  
 







