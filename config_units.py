# config_units.py

CONFIG = {
    "random_seed": 42,
    "simulation_years": 3,
    "start_year": 2024,
    "target_active_agents": 200,
    "base_monthly_sales": 650,  # Promedio base de autos vendidos globalmente al mes

    # Proporciones globales por modelo de auto (Suma = 1.0)
    "car_model_weights": {
        "Hatchback": 0.45,
        "Sedan": 0.30,
        "SUV": 0.15,
        "Pickup": 0.10
    },

    # Distribución porcentual por región (Suma = 1.0)
    "region_weights": {
        "Center": 0.35,
        "North": 0.30,
        "South": 0.20,
        "West": 0.15
    },

    # Estacionalidad anual (Factores multiplicativos sobre la media de 650)
    "seasonality": {
        1: 0.85,  # Enero
        2: 0.90,  # Febrero
        3: 1.05,  # Marzo
        4: 1.00,  # Abril
        5: 1.10,  # Mayo
        6: 1.15,  # Junio
        7: 1.05,  # Julio
        8: 0.95,  # Agosto
        9: 0.90,  # Septiembre
        10: 1.00,  # Octubre
        11: 1.25,  # Noviembre
        12: 1.40  # Diciembre
    },

    # Matriz de probabilidad mensual de Churn basada en el Tenure (meses)
    "churn_matrix": {
        "range_1_3": 0.07,  # 7% mensual para novatos (meses 1 a 3)
        "range_4_12": 0.035,  # 3.5% mensual para intermedios (meses 4 a 12)
        "range_13_plus": 0.015  # 1.5% mensual para veteranos (13+ meses)
    },

    # Parámetros de Google Sheets (Ajusta tu ID real aquí)
    "spreadsheet_id": "14uiCL3aPdAF6y2q7wFAmmdpR1MCNu0VunfeMXML_PiA",
    "sheet_name": "Sale Detail"
}