import numpy as np
import math # only for pi number

import matplotlib.pyplot as plt #se puede borrar usado para verificar
separation=True
name="0009"
#def NACA_4D(name,n_points,separation,chord)
n_points=100
c=1
coef=[]

if len(name)==4:
    for x in name:
        coef.append(x)
    # Max Thickness
    XX=int(coef[2]+coef[3])/100
    # First digit
    M=int(coef[0])/100
    # Second digit
    P=int(coef[1])/10
else:
    print("The NACA number must be four digits")

print(coef)
print(XX)
print(M)
print(P)

tita = np.linspace(math.pi/2, 0, n_points, True)
a0=0.2969;a1=-0.1260;a2=-0.3516;a3=0.2843;
if separation==False:
    a4=-0.1036;
else:
    a4=-0.1015;

xc=[1-math.cos(tita[x]) for x in range(len(tita))]
yt=[(5*XX)*((a0*math.sqrt(xc[x]))+a1*(xc[x])+a2*(math.pow(xc[x],2))+a3*(math.pow(xc[x],3))+a4*(math.pow(xc[x],4))) for x in range(len(tita))]
yc=[(M/(math.pow(1-P,2)))*(1-2*P+2*P*xc[x]-(math.pow(xc[x],2))) for x in range(len(xc)) if xc[x]>=P]+[(M/(math.pow(P,2)))*(2*P*xc[x]-(math.pow(xc[x],2))) for x in range(len(xc)) if xc[x]<P]
dyc=[(2*M/(math.pow(1-P,2)))*(P-xc[x]) for x in range(len(xc)) if xc[x]>=P]+[((2*M)/math.pow(P,2))*(P-xc[x]) for x in range(len(xc)) if xc[x]<P]
t=[(math.atan(dyc[x])) for x in range(len(dyc))]

Xu=[(round((xc[x]-yt[x]*math.sin(t[x]))*c,4)) for x in range(len(xc))]
Xl=[round((xc[x]+yt[x]*math.sin(t[x]))*c,4) for x in range(len(xc))]
Yu=[round(yc[x]+yt[x]*math.cos(t[x])*c,4) for x in range(len(xc))]
Yl=[round((yc[x]-yt[x]*math.cos(t[x]))*c,4) for x in range(len(xc))]

X=Xu+Xl[::-1]
Y=Yu+Yl[::-1]

fig = plt.figure()
ax = plt.axes()
plt.plot(X,Y, 'o', color='black')
plt.show()

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
#P=3/10;     %segundo digito
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

