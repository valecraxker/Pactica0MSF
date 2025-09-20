"""
Práctica 0: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nombres y Apellidos
Número de control: 12345678
Correo institucional: xxx.xxx@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m 
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
n = round((tend - t0)/dt)+1
t = np.linspace(t0,tend,n)
u1 = np.ones(n)
u2 = np.zeros(n); u2[round(1/dt):round(2/dt)] = 1
u3 = t/tend
u4 = np.sin(m.pi/2*t)

# Componentes del circuito RLC y función de transferencia
R,L,C = 10E3,300E-6,220E-6
num = [1]
den = [C*L,C*R,1]
sys = ctrl.tf(num,den)
print(f"funcion de transferencia del sistema: {sys}")

# Componentes del controlador
kP,kI,kD = 299.0263,7525.538,0.39157
Cr = 1E-6
Re = 1/(kI*Cr)
Rr = kP*Re
Ce = kD/Rr
print(f"el valor de la capacitancia propuesta de Cr es de {Cr} faradios.")
print(f"el valor de la resistencia propuesta de Re es de {Re} ohms.")
print(f"el valor de la capacitancia propuesta de Rr es de {Rr} ohms.")
print(f"el valor de la capacitancia propuesta de Ce es de {Ce} faradios.")

numPID = [Rr*Re*Cr*Ce,Re*Ce+Rr*Cr,1] 
denPID =[Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(f"la funcion de transferencia del controlador PID es {PID}")

# Sistema de control en lazo cerrado
X = ctrl.series(PID,sys)
sysPID = ctrl.feedback(X,1,sign = -1)
print(f"funcion de transferencia del sistema de control en lazo cerrado {sysPID}")

# Respuesta del sistema en lazo abierto y en lazo cerrado
clr1 = np.array([240,128,48])/255
clr2 = np.array([15,130,140])/255
clr6 = np.array([107,36,12])/255

_,PAu1 = ctrl.forced_response(sys,t,u1,x0)
_,PAu2 = ctrl.forced_response(sys,t,u2,x0)
_,PAu3 = ctrl.forced_response(sys,t,u3,x0)
_,PAu4 = ctrl.forced_response(sys,t,u4,x0)

_,pidu1 = ctrl.forced_response(sysPID,t,u1,x0)
_,pidu2 = ctrl.forced_response(sysPID,t,u2,x0)
_,pidu3 = ctrl.forced_response(sysPID,t,u3,x0)
_,pidu4 = ctrl.forced_response(sysPID,t,u4,x0)

fg1 = plt.figure()
plt.plot(t,u1,'-', color = clr1,label = 'Pao(t)')
plt.plot(t,PAu1,'--',color = clr2,label = 'PA(t)')
plt.plot(t,pidu1,':',linewidth = 4, color = clr6,label = 'PID(t)')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show()
fg1.savefig('step_python.pdf',bbox_inches = 'tight')

fg2 = plt.figure()
plt.plot(t,u2,'-', color = clr1,label = 'Pao(t)')
plt.plot(t,PAu2,'--',color = clr2,label = 'PA(t)')
plt.plot(t,pidu2,':',linewidth = 4, color = clr6,label = 'PID(t)')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show()
fg2.savefig('impulse_python.pdf',bbox_inches = 'tight')

fg3 = plt.figure()
plt.plot(t,u3,'-', color = clr1,label = 'Pao(t)')
plt.plot(t,PAu3,'--',color = clr2,label = 'PA(t)')
plt.plot(t,pidu3,':',linewidth = 4, color = clr6,label = 'PID(t)')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show()
fg3.savefig('ramp_python.pdf',bbox_inches = 'tight')

fg4 = plt.figure()
plt.plot(t,u4,'-', color = clr1,label = 'Pao(t)')
plt.plot(t,PAu4,'--',color = clr2,label = 'PA(t)')
plt.plot(t,pidu4,':',linewidth = 4, color = clr6,label = 'PID(t)')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1.2,1.3,0.2))
plt.xlabel('t[s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show()
fg4.savefig('sin_python.pdf',bbox_inches = 'tight')


