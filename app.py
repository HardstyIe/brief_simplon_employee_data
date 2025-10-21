import json
import csv
import streamlit as st
import pandas as pd

# -------------------------
# 1️⃣ Charger le JSON
# -------------------------
def load_json(path: str) -> dict:
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
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {path}")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Erreur de format JSON dans {path}")
        return {}

informations = load_json("lib/data/employe_data_test.json")


# -------------------------
# 2️⃣ Calcul des salaires
# -------------------------
def calc_monthly_salary(informations: dict) -> tuple[list, dict, float, float, float, list, list]:
    """
    Function taking the json, parse it to obtain all the name from company + employe detail to obtain monthly salary using hourly rate / contract hours / overtime hours
    
    [Arguments]\n
    informations: any | dict = the json to parse to get the needed data

    [Return]\n
    monthly salary\n
    min/max/average salary per branch\n
    min/max/average company\n
    preparation ground for csv export (csv_rows)
    """
    max_length_name = max_length_job = 0
    salary_all_company = []
    csv_rows = []
    csv_stats_global = []
    csv_stats_fillial = []
    branch_stats = {} 

    # Trouver les largeurs pour l'affichage console
    for branch in informations:
        for employee in informations[branch]:
            max_length_name = max(max_length_name, len(employee['name']))
            max_length_job = max(max_length_job, len(employee['job']))

    # Calculs
    for branch in informations:
        branch_salary_list = []
        rows = []

        print(f"\nFilliale : {branch}\n")

        for employee in informations[branch]:
            name = employee['name']
            job = employee['job']
            hourly_rate = employee['hourly_rate']
            weekly_hours_worked = employee['weekly_hours_worked']
            contract_hours = employee['contract_hours']
            overtime_hours = weekly_hours_worked - contract_hours


            # Calcul du salaire mensuel :
            # - On multiplie par 4 semaines pour obtenir un montant mensuel approximatif
            # - Les heures sup sont majorées à 1,5x le taux horaire (conformément au brief)
            # Salaire de base mensuel (heures normales)
            base_monthly_salary = contract_hours * hourly_rate * 4

            # Bonus heures sup mensuel (si applicable)
            if overtime_hours > 0:
                monthly_overtime_bonus = overtime_hours * hourly_rate * 1.5 * 4
            else:
                monthly_overtime_bonus = 0

            # Salaire total mensuel
            monthly_salary = base_monthly_salary + monthly_overtime_bonus

            branch_salary_list.append(monthly_salary)
            salary_all_company.append(monthly_salary)
            csv_rows.append([branch, name, job, monthly_salary, overtime_hours])
            rows.append({
                "name":name,
                "job":job,
                "hourly_rate":hourly_rate,
                "weekly_hours_worked":weekly_hours_worked,
                "contract_hours":contract_hours,
                "overtime_hours":overtime_hours,
                "monthly_salary":round(monthly_salary,2)
            })

            print(f"{name:<{max_length_name}} | {job:<{max_length_job}} | Salaire mensuel : {monthly_salary:.2f}€")
        branch_stats[branch] = pd.DataFrame(rows)

        # Statistiques de la branche
        if branch_salary_list:
            salary_min = min(branch_salary_list)
            salary_max = max(branch_salary_list)
            salary_avg = sum(branch_salary_list) / len(branch_salary_list)
        else:
            salary_min = salary_max = salary_avg = 0
        
        # ajout des données branche dans le csv
        csv_stats_global.append([branch,salary_min,salary_max,round(salary_avg, 2)]
                                )
        print("\n" + "=" * 50)
        print(f"Statistiques des salaires pour {branch}")
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

    csv_stats_fillial.append(["Entreprise (global)",salary_min_global,salary_max_global,round(salary_avg_global, 2)])

    print("=" * 50)
    print("Statistiques globales :")
    print(f"Salaire mini : {salary_min_global:.2f}€")
    print(f"Salaire max  : {salary_max_global:.2f}€")
    print(f"Salaire moyen: {salary_avg_global:.2f}€\n")

    return csv_rows, branch_stats, salary_min_global, salary_max_global, salary_avg_global, csv_stats_fillial, csv_stats_global


# -------------------------
# 3️⃣ Export CSV
# -------------------------
def export_salaries_to_csv(csv_rows: list, csv_stats_global: list, csv_stats_fillial: list, filename: str = "salaries_export.csv") -> None:
    """
    This function is used to create a csv file using data collected

    [Arguments]\n
    csv_rows: list = data collected previously to import in the csv\n
    csv_stats_filia = data collected previously to import in the csv\n
    csv_stats_fillial = data collected previously to import in the csv
    filename: str = the name of the file you want to create (default="salaries_export.csv")

    [Return]\n
    create a csv file with the collected data
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # --- Section employés ---
        writer.writerow(["--- Détails employés ---"])
        writer.writerow(["branche", "Name", "Job", "monthly Salary (€)", "Overtime Hours"])
        writer.writerows(csv_rows)
        writer.writerow([])

        writer.writerow(["--- Statistiques globales ---"])
        # --- Section statistiques globales ---
        writer.writerow(["branche", "Salaire minimum (€)", "Salaire maximum (€)", "Salaire moyen (€)"])
        writer.writerows(csv_stats_global)
        writer.writerow([])

        # --- Section statistiques branches ---
        writer.writerow(["--- Statistiques par branche ---"])
        writer.writerow(["Zone", "Salaire minimum (€)", "Salaire maximum (€)", "Salaire moyen (€)"])
        writer.writerows(csv_stats_fillial)

    print(f"✅ CSV file exported: {filename}")


# -------------------------
# 4️⃣ Affichage Streamlit
# -------------------------
def show_data_tabs(branch_stats: dict) -> None:
    """
    Function for streamlit app to display data

    [Arguments]\n
    branch_stats: dict = data returned by calc_monthly_salary()
    """
    if not branch_stats:
        st.warning("Aucune branche à afficher.")
        return

    tabs = st.tabs(list(branch_stats.keys()))
    for i, branch in enumerate(branch_stats.keys()):
        with tabs[i]:
            df = branch_stats[branch]
            if df.empty:
                st.info("Aucun employé.")
                continue

            # Slider pour le salaire (double poignée)
            min_sal = int(df["monthly_salary"].min())
            max_sal = int(df["monthly_salary"].max())
            salary_range = st.slider(
                f"Filtrer salaire ({branch})",
                min_sal, max_sal, (min_sal, max_sal), step=10, key=f"salary_{branch}"
            )

            # Filtre par poste (multiselect)
            jobs = ["Tous"] + sorted(df["job"].unique().tolist())
            job_sel = st.selectbox("Filtrer par poste", jobs, key=f"job_{branch}")

            filtered = df[
                (df["monthly_salary"] >= salary_range[0]) &
                (df["monthly_salary"] <= salary_range[1])
            ]
            if job_sel != "Tous":
                filtered = filtered[filtered["job"] == job_sel]

            st.dataframe(filtered, width="stretch")

            # Statistiques de la branche
            st.write(f"### Statistiques de {branch}")
            st.table(pd.DataFrame([{
                "Salaire minimum": f"{min_sal:.2f}€",
                "Salaire maximum": f"{max_sal:.2f}€",
                "Salaire moyen": f"{round(filtered["monthly_salary"].mean(), 2):.2f}€"
            }]))
            st.metric("Employés visibles", len(filtered))

# -------------------------
# 5️⃣ Programme principal
# -------------------------
csv_rows, branch_stats, salary_min_g, salary_max_g, salary_avg_g, csv_stats_fillial, csv_stats_global = calc_monthly_salary(informations)
export_salaries_to_csv(csv_rows,csv_stats_global,csv_stats_fillial)

with open("salaries_export.csv", "rb") as f:
    st.download_button("Télécharger le CSV", f, file_name="salaries_export.csv", mime="text/csv")

show_data_tabs(branch_stats)

# Affichage des stats global de l'entreprise
st.divider()
st.write("### Statistiques globales")
st.table(pd.DataFrame([{
        "Salaire minimum global": f"{salary_min_g:.2f}€",
        "Salaire maximum global": f"{salary_max_g:.2f}€",
        "Salaire moyen global": f"{salary_avg_g:.2f}€"
    }]))
