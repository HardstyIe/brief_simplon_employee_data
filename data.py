import json
import csv
import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Function to load json
def load_json():
    try:
        with open('lib/data/employe_data.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Boot load json
informations = load_json()


@st.cache_data
def load_data(nrows):
    data = pd.read_csv("salaries_export.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

st.title('Gestion des Salaires des Employés (version Collections)')
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


def calc_mensual_salary(informations):
    """
    Function taking the json, parse it to obtain all the name from company + employe detail to obtain mensual salary using hourly rate / contract hours / overtime hours
    
    [Arguments]\n
    informations: Any | List = the json to parse to get the needed data

    [Return]\n
    mensual salary
    """

    # variable initialisation
    max_length_name: int = 0
    max_length_job: int = 0
    filial_data: dict = {}
    company_data: dict = {}
    salary_all_company: list[float] = []
    csv_rows: list[list] = []


    # loop used to define format width used for the console
    for filial in informations:
        for employee in informations[filial]:
            if len(employee['name']) > max_length_name:
                max_length_name = len(employee['name'])

            if len(employee['job']) > max_length_job:
                max_length_job = len(employee['job'])

    # Loop to calculate salary per filial
    for filial in informations:
        filial_salary_list: list[float] = []

        print(f"Filliale : {filial}\n")

        # Loope used tu calculate salary per employee and format output
        for employee in informations[filial]:
            name: str = employee['name']
            job: str = employee['job']
            hourly_rate: float = employee['hourly_rate']
            weekly_hours_worked: float = employee['weekly_hours_worked']
            contract_hours: float = employee['contract_hours']
            overtime_hours: float = weekly_hours_worked - contract_hours

            # condition to modify salary gain from overtime
            if overtime_hours > 0:
                salary_bonus: float = overtime_hours * hourly_rate * 1.5
            else:
                salary_bonus: float = 0
            
            mensual_salary = ((weekly_hours_worked - overtime_hours) * hourly_rate * 4) + salary_bonus
            filial_salary_list.append(mensual_salary)
            salary_all_company.append(mensual_salary)

            print(f"{name:<{max_length_name}} | {job:<{max_length_job}} | Salaire mensuel : {mensual_salary}€")

            # Prepare CSV row
            csv_rows.append([filial, name, job, mensual_salary])

        print()
        print("=" *50)
        print()

        # statistic per branch
        salary_max = max(filial_salary_list)
        salary_min = min(filial_salary_list)
        salary_average = sum(filial_salary_list) / len(filial_salary_list)

        csv_rows.append([filial, "MIN", "", salary_min])
        csv_rows.append([filial, "MAX", "", salary_max])
        csv_rows.append([filial, "AVERAGE", "", salary_average])

        print(f"Statistique des salaires pour la filliale {filial}\nSalaire mini : {salary_min}€ \nSalaire max : {salary_max}€ \nSalaire moyen : {salary_average}€")
        print()

    print()
    print("=" * 50)

    # Global statistic tied to company
    salary_max_global = max(salary_all_company)
    salary_min_global = min(salary_all_company)
    salary_average_global = sum(salary_all_company) / len(salary_all_company)

    print(f"Statistique des salaires pour l'entreprise \nSalaire mini : {salary_min_global}€ \nSalaire max : {salary_max_global}€ \nSalaire moyen : {salary_average_global}€")
    return csv_rows

def export_salaries_to_csv(csv_rows: list[list], filename: str = "salaries_export.csv"):
    """
    Export a list of rows to a CSV file.
    
    [Arguments]
    csv_rows: list[list] - the rows to write to CSV
    filename: str - name of the CSV file to create
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Fillial", "Name", "Job", "Monthly Salary (€)"])
        writer.writerows(csv_rows)
    print(f"CSV file exported: {filename}")

csv_rows = calc_mensual_salary(informations)

export_salaries_to_csv(csv_rows)

