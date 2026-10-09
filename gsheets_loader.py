# src/gsheets_loader.py

import os
import sys
import gspread
from google.oauth2.service_account import Credentials
#from gspread_dataframe import set_with_dataframe

# Asegurar ruta raíz
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#from datagenerator import SalesForceSimulator



# Pega aquí el ID de tu Google Sheet (lo sacas de la URL de tu navegador)
SPREADSHEET_ID = "14uiCL3aPdAF6y2q7wFAmmdpR1MCNu0VunfeMXML_PiA"
sheet_name="synthetic"

def push_clean_data_to_sheets(df, sheet_name=sheet_name, SPREADSHEET_ID=SPREADSHEET_ID):
  creds_path = "service-account.json"
  SCOPES = [
      "https://www.googleapis.com/auth/spreadsheets",
      "https://www.googleapis.com/auth/drive",
  ]
  if not os.path.exists(creds_path):
    raise FileNotFoundError(f"No se encontró el archivo de credenciales en: {creds_path}")

  print("[INFO] Autenticando con Google Cloud Service Account...")
  creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
  client = gspread.authorize(creds)

  spreadsheet = client.open_by_key(SPREADSHEET_ID)
  worksheet = spreadsheet.worksheet(sheet_name)

  print(f"[INFO] Limpiando datos anteriores en la pestaña '{sheet_name}' desde A2 en adelante...")
  # Borramos desde A2 hasta una fila segura (ej. 10,000) y columna Z para no tocar la fila 1 (headers)
  worksheet.batch_clear(["A2:Z10000"])

  # Extraer SOLO los valores del DataFrame (sin los títulos de columnas)
  data_values = df.values.tolist()

  print(f"[INFO] Insertando {len(data_values)} filas a partir de la celda A2...")
  # Actualizamos el rango 'A2' escribiendo únicamente los valores puros
  worksheet.update(values=data_values, range_name="A2")

  print(f"[SUCCESS] ¡Datos sincronizados en '{sheet_name}' sin alterar la cabecera!")

"""
if __name__ == "__main__":
  simulator = SalesForceSimulator()
  df_panel = simulator.generate_panel_dataset()
  push_clean_data_to_sheets(df_panel)


"""