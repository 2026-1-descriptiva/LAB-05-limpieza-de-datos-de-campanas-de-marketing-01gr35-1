"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import os
import zipfile
import pandas as pd


def clean_campaign_data():
    """
    Limpieza de datos de campaña de marketing
    """

    # Crear carpeta output
    os.makedirs("files/output", exist_ok=True)
    
    dfs = []
    
    # Leer los 10 archivos zip
    for i in range(10):
        zip_path = f"files/input/bank-marketing-campaing-{i}.csv.zip"
        
        if not os.path.exists(zip_path):
            continue
            
        with zipfile.ZipFile(zip_path, 'r') as z:
            archivos = z.namelist()
            csv_name = [a for a in archivos if a.endswith('.csv')][0]
            
            with z.open(csv_name) as f:
                df = pd.read_csv(f)
                dfs.append(df)
    
    # Combinar todos los datos
    df = pd.concat(dfs, ignore_index=True)
    print(f"Total de registros: {len(df)}")
    
    # ========== client.csv ==========
    client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    
    # Limpiar job
    client['job'] = client['job'].str.replace('.', '', regex=False)
    client['job'] = client['job'].str.replace('-', '_', regex=False)
    
    # Limpiar education
    client['education'] = client['education'].str.replace('.', '_', regex=False)
    client['education'] = client['education'].replace('unknown', pd.NA)
    
    # Convertir credit_default
    client['credit_default'] = (client['credit_default'] == 'yes').astype(int)
    
    # Convertir mortgage
    client['mortgage'] = (client['mortgage'] == 'yes').astype(int)
    
    # Guardar
    client.to_csv("files/output/client.csv", index=False)
    print("✓ client.csv generado")
    
    # ========== campaign.csv ==========
    campaign = df[['client_id', 'number_contacts', 'contact_duration', 
                   'previous_campaign_contacts', 'previous_outcome', 
                   'campaign_outcome', 'day', 'month']].copy()
    
    # Convertir previous_outcome
    campaign['previous_outcome'] = (campaign['previous_outcome'] == 'success').astype(int)
    
    # Convertir campaign_outcome
    campaign['campaign_outcome'] = (campaign['campaign_outcome'] == 'yes').astype(int)
    
    # Crear fecha
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    campaign['month_num'] = campaign['month'].map(month_map)
    campaign['last_contact_date'] = '2022-' + campaign['month_num'] + '-' + campaign['day'].astype(str).str.zfill(2)
    
    # Seleccionar las columnas finales
    campaign = campaign[['client_id', 'number_contacts', 'contact_duration', 
                         'previous_campaign_contacts', 'previous_outcome', 
                         'campaign_outcome', 'last_contact_date']]
    
    # Guardar
    campaign.to_csv("files/output/campaign.csv", index=False)
    print("✓ campaign.csv generado")
    
    # ========== economics.csv ==========
    economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
    
    # CORREGIDO: usar 'euribor_three_months' (con 'i', no 'o')
    economics.columns = ['client_id', 'cons_price_idx', 'euribor_three_months']
    
    # Guardar
    economics.to_csv("files/output/economics.csv", index=False)
    print("✓ economics.csv generado")
    
    print("\n✅ ¡Proceso completado exitosamente!")


if __name__ == "__main__":
    clean_campaign_data()