from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import math
from scipy import stats

app = Flask(__name__)

# Inicializamos las listas X y Y para almacenar los datos de entrada
X_values = []
Y_values = []

def calcular_r2(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    X_mean = np.mean(X)
    Y_mean = np.mean(Y)
    SS_tot = sum((Y - Y_mean) ** 2)
    SS_res = sum((Y - (np.polyfit(X, Y, 1)[0] * X + np.polyfit(X, Y, 1)[1])) ** 2)
    r2 = 1 - SS_res / SS_tot
    return r2

def anova(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    n = len(X)
    X_mean = np.mean(X)
    Y_mean = np.mean(Y)
    SS_tot = sum((Y - Y_mean) ** 2)
    SS_res = sum((Y - (np.polyfit(X, Y, 1)[0] * X + np.polyfit(X, Y, 1)[1])) ** 2)
    SS_reg = SS_tot - SS_res
    MS_reg = SS_reg
    MS_res = SS_res / (n - 2)
    F = MS_reg / MS_res
    return F, SS_reg, SS_res

def calcular_t_estadistica(X, Y, alpha=0.05):
    X = np.array(X)
    Y = np.array(Y)
    n = len(X)
    beta_1, beta_0 = np.polyfit(X, Y, 1)
    s_res = np.sqrt(sum((Y - (beta_1 * X + beta_0)) ** 2) / (n - 2))
    X_mean = np.mean(X)
    s_beta_1 = s_res / np.sqrt(sum((X - X_mean) ** 2))
    t = beta_1 / s_beta_1
    p_value = 2 * (1 - stats.t.cdf(abs(t), df=n - 2))
    t_critico = stats.t.ppf(1 - alpha/2, df=n - 2)
    return t, t_critico, p_value

def intervalo_confianza_beta1(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    n = len(X)
    beta_1, beta_0 = np.polyfit(X, Y, 1)
    s_res = np.sqrt(sum((Y - (beta_1 * X + beta_0)) ** 2) / (n - 2))
    X_mean = np.mean(X)
    s_beta_1 = s_res / np.sqrt(sum((X - X_mean) ** 2))
    t_critico = stats.t.ppf(0.975, df=n - 2)
    intervalo_inferior = beta_1 - t_critico * s_beta_1
    intervalo_superior = beta_1 + t_critico * s_beta_1
    return intervalo_inferior, intervalo_superior

@app.route('/', methods=['GET', 'POST'])
def index():
    global X_values, Y_values
    error = None
    if request.method == 'POST':
        # Si se agregan nuevos valores a las listas X e Y
        try:
            new_X = float(request.form['new_X'])
            new_Y = float(request.form['new_Y'])
            X_values.append(new_X)
            Y_values.append(new_Y)
        except ValueError:
            error = "Los valores ingresados deben ser números."

    # Cuando se alcanzan los 10 datos
    if len(X_values) == 10 and len(Y_values) == 10:
        datos_tabla = []
        for x, y in zip(X_values, Y_values):
            x2 = x ** 2
            y2 = y ** 2
            xy = x * y
            datos_tabla.append({'X': x, 'Y': y, 'X2': x2, 'Y2': y2, 'XY': xy})

        sum_X = sum(X_values)
        sum_Y = sum(Y_values)
        sum_X2 = sum([d['X2'] for d in datos_tabla])
        sum_Y2 = sum([d['Y2'] for d in datos_tabla])
        sum_XY = sum([d['XY'] for d in datos_tabla])

        r2 = calcular_r2(X_values, Y_values)
        F, SS_reg, SS_res = anova(X_values, Y_values)
        t_estadistica, t_critico, p_value = calcular_t_estadistica(X_values, Y_values)
        intervalo_inf, intervalo_sup = intervalo_confianza_beta1(X_values, Y_values)

        return render_template('index.html', datos_tabla=datos_tabla, sum_X=sum_X, sum_Y=sum_Y, 
                               sum_X2=sum_X2, sum_Y2=sum_Y2, sum_XY=sum_XY, r2=r2, F=F, SS_reg=SS_reg, 
                               SS_res=SS_res, t_estadistica=t_estadistica, t_critico=t_critico, 
                               p_value=p_value, intervalo_inf=intervalo_inf, intervalo_sup=intervalo_sup)

    return render_template('index.html', X_values=X_values, Y_values=Y_values, error=error)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
