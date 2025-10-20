import json
import csv
import streamlit as st
import pandas as pd

# -------------------------
# 1️⃣ Charger le JSON
# -------------------------
def load_json(path) -> list:
    """
    This function is used to load data

    [Arguments]\n
    path: str = The path to the json to load

    [Return]\n
    a list containing all data
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}

informations = load_json("lib/data/employe_data_test.json")


# -------------------------
# 2️⃣ Calcul des salaires
# -------------------------
def calc_mensual_salary(informations:list):
    """
    Function taking the json, parse it to obtain all the name from company + employe detail to obtain mensual salary using hourly rate / contract hours / overtime hours
    
    [Arguments]\n
    informations: any | list = the json to parse to get the needed data

    [Return]\n
    mensual salary\n
    min/max/average salary per branch\n
    min/max/average company\n
    preparation ground for csv export (csv_rows)
    """
    max_length_name = max_length_job = 0
    salary_all_company = []
    csv_rows = []
    filial_stats = {} 

    # Trouver les largeurs pour l'affichage console
    for filial in informations:
        for employee in informations[filial]:
            max_length_name = max(max_length_name, len(employee['name']))
            max_length_job = max(max_length_job, len(employee['job']))

    # Calculs
    for filial in informations:
        filial_salary_list = []

        print(f"\nFilliale : {filial}\n")

        for employee in informations[filial]:
            name = employee['name']
            job = employee['job']
            hourly_rate = employee['hourly_rate']
            weekly_hours_worked = employee['weekly_hours_worked']
            contract_hours = employee['contract_hours']
            overtime_hours = weekly_hours_worked - contract_hours

            if overtime_hours > 0:
                salary_bonus = overtime_hours * hourly_rate * 1.5
            else:
                salary_bonus = 0

            mensual_salary = ((weekly_hours_worked - overtime_hours) * hourly_rate * 4) + salary_bonus

            filial_salary_list.append(mensual_salary)
            salary_all_company.append(mensual_salary)
            csv_rows.append([filial, name, job, mensual_salary])

            print(f"{name:<{max_length_name}} | {job:<{max_length_job}} | Salaire mensuel : {mensual_salary:.2f}€")

        # Statistiques de la filiale
        if filial_salary_list:
            salary_min = min(filial_salary_list)
            salary_max = max(filial_salary_list)
            salary_avg = sum(filial_salary_list) / len(filial_salary_list)
        else:
            salary_min = salary_max = salary_avg = 0

        filial_stats[filial] = {
            "Salaire minimum": salary_min,
            "Salaire maximum": salary_max,
            "Salaire moyen": salary_avg
        }

        print("\n" + "=" * 50)
        print(f"Statistiques des salaires pour {filial}")
        print(f"Salaire mini : {salary_min:.2f}€")
        print(f"Salaire max  : {salary_max:.2f}€")
        print(f"Salaire moyen: {salary_avg:.2f}€\n")

    # Statistiques globales
    if salary_all_company:
        salary_min_global = min(salary_all_company)
        salary_max_global = max(salary_all_company)
        salary_avg_global = sum(salary_all_company) / len(salary_all_company)
    else:
        salary_min_global = salary_max_global = salary_avg_global = 0

    print("=" * 50)
    print("Statistiques globales :")
    print(f"Salaire mini : {salary_min_global:.2f}€")
    print(f"Salaire max  : {salary_max_global:.2f}€")
    print(f"Salaire moyen: {salary_avg_global:.2f}€\n")

    return csv_rows, filial_stats, salary_min_global, salary_max_global, salary_avg_global


# -------------------------
# 3️⃣ Export CSV
# -------------------------
def export_salaries_to_csv(csv_rows:list, filename="salaries_export.csv"):
    """
    This function is used to create a csv file using data collected

    [Arguments]\n
    csv_rows: list = data collected previously to import in the csv\n
    filename: str = the name of the file you want to create

    [Return]\n
    create a csv file with the collected data
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filiale", "Name", "Job", "Monthly Salary (€)"])
        writer.writerows(csv_rows)
    print(f"✅ CSV file exported: {filename}")


# -------------------------
# 4️⃣ Affichage Streamlit
# -------------------------
def show_data_tabs(informations:list, filial_stats:dict):
    """
    Function for streamlit app to display data

    [Arguments]\n
    informations: list = the data loading from json\n
    filial_stats: dict = data returned by calc_mensual_salary()
    """
    tabs = st.tabs(list(informations.keys()))

    for tab, filial in zip(tabs, informations.keys()):
        with tab:
            st.subheader(filial)

            # Détails des employés
            df = pd.DataFrame(informations[filial])
            df = df.convert_dtypes()
            st.dataframe(df)

            # Statistiques de la filiale
            stats = filial_stats.get(filial, {})
            st.write("### Statistiques")
            st.table(pd.DataFrame([stats]))


# -------------------------
# 5️⃣ Programme principal
# -------------------------
csv_rows, filial_stats, salary_min_g, salary_max_g, salary_avg_g = calc_mensual_salary(informations)
if st.button("Télécharger CSV"):
    export_salaries_to_csv(csv_rows)


show_data_tabs(informations, filial_stats)
st.divider()
st.write("### Statistiques globales")
st.table(pd.DataFrame([{
        "Salaire minimum global": salary_min_g,
        "Salaire maximum global": salary_max_g,
        "Salaire moyen global": salary_avg_g
    }]))
