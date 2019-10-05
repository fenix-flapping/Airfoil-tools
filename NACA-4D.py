name="5555"
#def NACA_4D(name,n_points,separation)
coef=[]
for x in name:
    coef.append(int(x))
print(coef)

#a0=0.2969;a1=-0.1260;a2=-0.3516;a3=0.2843;
#% Leading edge cerrado, para abierto se usa a4=0.1015;
#a4=-0.1036;
#
#h=0.01;  %first layer
#% generacion de puntos
#n=250;   % numero de puntos
#
#% max thickness
#XX=18/100;  %max thickness
#M=3/100;    %primer digito
#P=3/10;     %segundo digitoç
#c=0.32;     %cuerda
#
#tita=0:(pi/2/(n-1)):pi/2;
#xc=cos(tita);   % Distribucion cosenoidal de puntos "x"
#%xc=0:1/n:1
#
#for i=1:length(xc)
#    if xc(i)<P
#        yc(i)=(M/(P^2))*(2*P*xc(i)-(xc(i)^2));
#        dyc(i)=((2*M)/P^2)*(P-xc(i));
#    else
#        yc(i)=(M/(1-P)^2)*(1-2*P+2*P*xc(i)-(xc(i).^2));
#        dyc(i)=(2*M/(1-P)^2)*(P-xc(i));
#    end
#    yt(i)=(5*XX)*(a0*sqrt(xc(i))+a1*(xc(i))+a2*(xc(i)^2)+a3*(xc(i)^3)+a4*(xc(i)^4));
#    t(i)=atan(dyc(i));
#    
#    Xu(i)=(xc(i)-yt(i)*sin(t(i)))*c;
#    Xl(i)=(xc(i)+yt(i)*sin(t(i)))*c;
#    
#    Yu(i)=(yc(i)+yt(i)*cos(t(i)))*c;
#    Yl(i)=(yc(i)-yt(i)*cos(t(i)))*c;
#end
#
#% Filtrado y reacomodo de datos
#% Falta agregar && c*.25<X(i)>c*.90
#Xa=([Xu flip(Xl)]);
#Ya=([Yu flip(Yl)]);
#s=0;
#Y(1)=0;
#X(1)=c;
#for i=2:length(Xa)-1
#    if abs(Ya(i)-Ya(i+1))>1e-4  %Filtrado de diferencias pequeñas
#        if abs(Ya(i))>1e-4  % Filtrado de valores cercanos al cero de Y
#            Y(i-s)=Ya(i);
#            X(i-s)=Xa(i);
#        else
#            Y(i-s)=0;
#        end
#        if abs(Xa(i))>1e-4 %Filtrado de valores cercanos al cero de X
#            X(i-s)=Xa(i);
#        else
#            X(i-s)=0;
#        end
#    else
#        s=s+1;
#    end
#end
#Y(length(Y)+1)=0;
#X(length(X)+1)=c;
#
#% for i=1:length(xc)-1
#%     tt(i)=atan((Yu(i+1)-Yu(i))/((Xu(i+1)-Xu(i))));
#%     if i<=1
#%         Xblu(i)=c+h;
#%         Yblu(i)=0;
#%     else
#%         tt(i)=(Yu(i+1)-Yu(i))/((Xu(i+1)-Xu(i)));
#%         Xblu(i)=Xu(i)-h*sin(t(i));
#%         Yblu(i)=Yu(i)+h*cos(t(i));  % Buscar la derivada real y no la de la curvatura cambiar t(i)
#%     end
#% end
#
#% Escritura de Datos
#% DATA=[transpose(X),transpose(Y),zeros(length(X),1)];  %3D
#DATA=[transpose(X),transpose(Y)];   %2D
#dlmwrite('NACA-Puntos.txt',DATA,'delimiter','\t','precision','%1.4f')
#
#% Ploteo de perfil y linea de curvatura
#plot(Xu,Yu)
#hold on
#plot(Xl,Yl)
#axis equal
#plot(Xu,yc*c)
#grid on
#hold off
#