function h2=convierteH(h,nodos)
% Convierte h = [in,out] a h2 seriada (de izq a dcha y de arriba abajo)
% nodos: nubes de datos
if nargin < 2, nodos = 3; end

H = zeros(nodos);
H(h(2),h(1))=1;
h2 = H(:);
h2([1:nodos+1:end])=[];
h2 = find(h2);