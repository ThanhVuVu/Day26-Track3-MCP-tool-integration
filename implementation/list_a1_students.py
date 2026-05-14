from db import execute_query

def list_students_in_cohort(cohort_name: str):
    query = "SELECT name FROM students WHERE cohort = ?;"
    results = execute_query(query, (cohort_name,))
    for row in results:
        print(row['name'])

if __name__ == "__main__":
    list_students_in_cohort("A1")
