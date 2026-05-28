function y2=convierteY(y,enlaces)
% Convierte y = [enlace,subida('u')/bajada('d')] a y2 seriada (de izq a dcha y de arriba abajo)
% subida es cualquier camino a->b cuando a<b
% nodos: nubes de datos

Y = zeros(enlaces,2);
d = (y(2)=='d');
Y(str2num(y(1)),d+1)=1;
y2 = find(Y(:));
