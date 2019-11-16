

import math
global MatrizD, latitudE, longitudE, altitudE
MatrizD = []


def modelo(lati, longi, alti,latitudE,longitudE,altitudE):
    try:
        latitudG = float(lati)
        longitudG = float(longi)
        altitudG = float(alti)
        alfaP = (3.141592653589793/180.0)*(float(latitudE))
        betaP = (3.141592653589793/180)*(float(longitudE))
        hP = float(altitudE)
        alfaS = (3.141592653589793/180)*(latitudG)
        betaS = (3.141592653589793/180)*(longitudG)
        hS = altitudG
        divCero = 0
        r = 6378000.0
        P = r + hP
        S = r + hS
        Px = P*math.cos(alfaP)*math.sin(betaP)
        Py = P*math.cos(alfaP)*math.cos(betaP)
        Pz = P*math.sin(alfaP)
        Sx = S*math.cos(alfaS)*math.sin(betaS)
        Sy = S*math.cos(alfaS)*math.cos(betaS)
        Sz = S*math.sin(alfaS)
        Dxyz_1 = Sx-Px
        Dxyz_2 = Sy-Py
        Dxyz_3 = Sz-Pz
        D = math.sqrt(Dxyz_1*Dxyz_1+Dxyz_2*Dxyz_2+Dxyz_3*Dxyz_3)
        Dw_1 = math.cos(-betaP)*Dxyz_1+math.sin(-betaP)*Dxyz_2
        Dw_2 = -math.sin(-betaP)*Dxyz_1+math.cos(betaP)*Dxyz_2
        Dw_3 = Dxyz_3
        Duvw_1 = Dw_1
        Duvw_2 = math.cos(alfaP)*Dw_2+math.sin(alfaP)*Dw_3
        Duvw_3 = -math.sin(alfaP)*Dw_2+math.cos(alfaP)*Dw_3
        if abs(Duvw_1) < 1:
            Duvw_1 = 0.0
        if abs(Duvw_2) < 1:
            Duvw_2 = 0.0
        if abs(Duvw_3) < 1:
            Duvw_3 = 0.0

        Distancia = math.sqrt(Duvw_1*Duvw_1+Duvw_2*Duvw_2+Duvw_3*Duvw_3)
        
        if Distancia > 0.0:
            omega_prima = math.asin(Duvw_2/Distancia)*180/3.14159265358979
            if Duvw_1 < 0.0:
                theta_prima = -math.acos(Duvw_3/math.sqrt(Duvw_1*Duvw_1+Duvw_3*Duvw_3))*180/3.141592653589793
            elif Duvw_1 > 0.0:
                theta_prima = math.acos(Duvw_3/math.sqrt(Duvw_1*Duvw_1+Duvw_3*Duvw_3))*180/3.141592653589793
            elif Duvw_1 == 0.0 and Duvw_3 == 0.0:
                theta_prima = 0.0
            else:
                theta_prima = 0.0
            angulo_omega = omega_prima
            angulo_theta = theta_prima
            return [angulo_theta, angulo_omega]
        else:
            return[0.0, 0.0]
    except Exception as e:
        print("*****ERROR CALCULANDO MODELO****")
        print(e)

def transformarTrama(latitud,longitud):
    try:
        longitud_geo = 0
        latitud_geo = 0
        if(len(longitud) > 8):
            grados_lo = float(longitud[1:3])
            minutos_lo = float(longitud[3:5])
            decimasMinutos_lo = float("0"+longitud[5:8])
        elif(len(longitud) > 9):
            grados_lo = float(longitud[0:2])
            minutos_lo = float(longitud[2:4])
            decimasMinutos_lo = float(longitud[4:8])
        else:
            grados_lo = float(longitud[1:2])
            minutos_lo = float(longitud[2:4])
            decimasMinutos_lo = float("0"+longitud[4:7])
        longitud_geo = (grados_lo + (minutos_lo + decimasMinutos_lo)/60)
        if(longitud[len(longitud)-1] == "W"):
            longitud_geo = longitud_geo * -1
        longitud_geo = str(longitud_geo)
        longitud_geo = longitud_geo[0:9]
        longitud_geo = longitud_geo.strip()
        if(len(latitud) == 9):
            grados_la = float(latitud[1:3])
            minutos_la = float(latitud[3:5])
            decimasMinutos_la = float("0"+latitud[5:8])
        elif(len(latitud) > 9):
            grados_la = float(latitud[0:2])
            minutos_la = float(latitud[2:4])
            decimasMinutos_la = float(latitud[4:8])
        else:
            grados_la = float(latitud[1:2])
            minutos_la = float(latitud[2:4])
            decimasMinutos_la = float("0"+latitud[4:7])
        latitud_geo = (grados_la + (minutos_la + decimasMinutos_la)/60)
        if(latitud[len(latitud)-1] == "S"):
            latitud_geo = latitud_geo * -1
        latitud_geo = str(latitud_geo)
        latitud_geo = latitud_geo[0:9]
        latitud_geo = latitud_geo.strip()
        return [latitud_geo,longitud_geo]
    except Exception as e:
        print("*****ERROR TRANSFORMANDO TRAMA*****")
        print(e)

      

latitud = "0650.30N"
longitud = "08901.75W"
decimales = transformarTrama(latitud,longitud)
print("coordenada convertida inicial: " + str(decimales))
latitudE = decimales[0]
longitudE = decimales[1]
altitudE = 0

latitud = "0650.31N"
longitud = "08901.75W"
decimales_1 = transformarTrama(latitud,longitud)
print("coordenada convertida con centesima adicional: "+ str(decimales_1))
latitudG = decimales_1[0]
longitudG = decimales_1[1]
altitudG = 0

angulos = modelo(latitudG,longitudG,altitudG,latitudE,longitudE,altitudE)

