# src/datagenerator.py

import numpy as np
import pandas as pd
from datetime import datetime
import os
import sys

# Asegurar la ruta para importar config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_reps import CONFIG
from gsheets_loader import push_clean_data_to_sheets


class SalesForceSimulator:
    def __init__(self, config=CONFIG):
        self.cfg = config
        np.random.seed(self.cfg["random_seed"])

    def _get_churn_probability(self, tenure):
        if tenure <= 3:
            return self.cfg["churn_matrix"]["range_1_3"]
        elif tenure <= 12:
            return self.cfg["churn_matrix"]["range_4_12"]
        else:
            return self.cfg["churn_matrix"]["range_13_plus"]

    def _get_ramp_up_factor(self, tenure):
        ramp_dict = self.cfg["tenure_ramp_up"]
        return ramp_dict.get(tenure, 1.0)

    def generate_panel_dataset(self):
        target_agents = self.cfg["target_active_agents"]
        regions = list(self.cfg["regions_channels"].keys())

        start_date = datetime(self.cfg["start_year"], 1, 1)
        total_months = self.cfg["simulation_years"] * 12

        agent_id_counter = 1
        active_pool = []  # List of Dicts with actual status of each agent

        # Starting initial pool of agents on month 0 (so we can be ready on month1)
        # Inicializar el pool inicial de agentes en el mes 0 (para arrancar el mes 1 listos)
        for _ in range(target_agents):
            region = np.random.choice(regions)
            channel_info = self.cfg["regions_channels"][region]
            channel = "Inbound" if np.random.rand() < channel_info["inbound_weight"] else "Outbound"

            # Lognormal skill facto (geometric mean close to 1)
            # Factor de habilidad innata con Lognormal (Media geométrica centrada cerca de 1)
            skill_alpha = np.random.lognormal(mean=0.0, sigma=0.25)

            active_pool.append({
                "agent_id": f"AGT_{agent_id_counter:04d}",
                "region": region,
                "channel": channel,
                "skill_alpha": skill_alpha,
                "tenure": np.random.randint(1, 13)  # Tenure inicial aleatorio para bootstrap realista
            })
            agent_id_counter += 1

        panel_records = []
        incoming_replacements = []  # Cola de reemplazos para el mes siguiente

        dates = pd.date_range(start=start_date, periods=total_months, freq='MS')

        for m_idx, current_date in enumerate(dates):
            month_num = current_date.month
            seasonality_factor = self.cfg["seasonality"][month_num]

            # 1. Incorporar los reemplazos generados el mes anterior
            if incoming_replacements:
                active_pool.extend(incoming_replacements)
                incoming_replacements = []

            next_month_pool = []

            # 2. Procesar la actividad del mes para cada agente activo
            for agent in active_pool:
                region = agent["region"]
                channel = agent["channel"]
                skill = agent["skill_alpha"]
                tenure = agent["tenure"]

                reg_multiplier = self.cfg["regions_channels"][region]["base_multiplier"]
                ramp_factor = self._get_ramp_up_factor(tenure)

                # Ecuación actuarial de tasa esperada (Lambda de Poisson)
                lambda_it = (
                        self.cfg["base_sales_lambda"]
                        * skill
                        * reg_multiplier
                        * seasonality_factor
                        * ramp_factor
                )

                # Simulación de ventas discretas con Distribución de Poisson
                sales_count = np.random.poisson(lam=max(lambda_it, 0.1))

                # Evaluar Churn del mes actual
                churn_prob = self._get_churn_probability(tenure)
                is_churned = np.random.rand() < churn_prob

                # Registrar el evento en el Panel Dataset
                panel_records.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "year": current_date.year,
                    "month": month_num,
                    "agent_id": agent["agent_id"],
                    "region": region,
                    "channel": channel,
                    "tenure_months": tenure,
                    "skill_alpha": round(skill, 4),
                    "expected_lambda": round(lambda_it, 2),
                    "sales_units": int(sales_count),
                    "is_churned": int(is_churned)
                })

                if is_churned:
                    # Preparar reemplazo para el SIGUIENTE mes (con tenure = 1)
                    new_region = np.random.choice(regions)
                    ch_info = self.cfg["regions_channels"][new_region]
                    new_channel = "Inbound" if np.random.rand() < ch_info["inbound_weight"] else "Outbound"
                    new_skill = np.random.lognormal(mean=0.0, sigma=0.25)

                    incoming_replacements.append({
                        "agent_id": f"AGT_{agent_id_counter:04d}",
                        "region": new_region,
                        "channel": new_channel,
                        "skill_alpha": new_skill,
                        "tenure": 1
                    })
                    agent_id_counter += 1
                else:
                    # El agente sobrevive, incrementa su tenure en 1 para el próximo mes
                    agent["tenure"] += 1
                    next_month_pool.append(agent)

            # Garantizar regla estricta: Si por alguna fluctuación el pool activo baja, rellenar para mantener base
            while len(next_month_pool) < target_agents:
                new_region = np.random.choice(regions)
                ch_info = self.cfg["regions_channels"][new_region]
                new_channel = "Inbound" if np.random.rand() < ch_info["inbound_weight"] else "Outbound"
                incoming_replacements.append({
                    "agent_id": f"AGT_{agent_id_counter:04d}",
                    "region": new_region,
                    "channel": new_channel,
                    "skill_alpha": np.random.lognormal(mean=0.0, sigma=0.25),
                    "tenure": 1
                })
                agent_id_counter += 1
                # Tomar el último agregado y pasarlo directo al pool del siguiente mes
                next_month_pool.append(incoming_replacements.pop())

            active_pool = next_month_pool

        df_panel = pd.DataFrame(panel_records)
        return df_panel


if __name__ == "__main__":
    simulator = SalesForceSimulator()
    df = simulator.generate_panel_dataset()
    SPREADSHEET_ID = "14uiCL3aPdAF6y2q7wFAmmdpR1MCNu0VunfeMXML_PiA"
    sheet_name = "synthetic"
    os.makedirs("data", exist_ok=True)
    output_path = "data/synthetic_sales_force.csv"
    push_clean_data_to_sheets(df,sheet_name, SPREADSHEET_ID)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Panel dataset generated successfully: {output_path}")
    print(f"Total rows: {len(df)} | Total unique agents: {df['agent_id'].nunique()}")
    print(df.head(5))
