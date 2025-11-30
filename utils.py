from datetime import datetime, timedelta

def str_para_data(valor):
    return datetime.strptime(valor, "%Y-%m-%d").date()

def data_para_str(data):
    return data.strftime("%Y-%m-%d")

def calcular_proxima_data(ultima_data, intervalo):
    return ultima_data + timedelta(days=intervalo)
