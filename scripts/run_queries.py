import os
import sqlite3
from tabulate import tabulate

DATABASE_PATH = "database/ecommerce.db"
SQL_FOLDER = "sql"
OUTPUT_FOLDER = "output/sample_reports"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def execute_sql_file(conn, sql_file, output_file):

    cursor = conn.cursor()

    with open(sql_file, "r", encoding="utf-8") as file:
        queries = file.read().split(";")

    report = []

    report.append("=" * 70)
    report.append(f"SQL FILE : {os.path.basename(sql_file)}")
    report.append("=" * 70)
    report.append("")

    for index, query in enumerate(queries, start=1):

        query = query.strip()

        if not query:
            continue

        report.append(f"Query {index}")
        report.append("-" * 70)
        report.append(query)
        report.append("")

        try:

            cursor.execute(query)

            if cursor.description:

                rows = cursor.fetchall()
                
                headers = [
                     column[0]
                     for column in cursor.description
                     ]
                
                display_rows = rows[:10]
                table = tabulate(
                     display_rows,
                     headers=headers,
                     tablefmt="grid"
                     )
                print(table)
                report.append(table)
                if len(rows) > 10:
                    print(f"\nShowing first 10 of {len(rows)} rows...\n")
                    report.append(f"\nShowing first 10 of {len(rows)} rows.\n")

            else:

                conn.commit()

                report.append(
                    "Query Executed Successfully."
                )

        except sqlite3.Error as error:

            report.append(f"ERROR : {error}")

        report.append("\n")

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(report))

    print(
        f"Report Saved : {output_file}\n"
    )


def main():

    if not os.path.exists(DATABASE_PATH):

        print("Database not found.")
        print("Run load_database.py first.")
        return

    conn = sqlite3.connect(DATABASE_PATH)

    sql_files = [

        "aggregations.sql",

        "window_functions.sql",

        "cohort_analysis.sql"

    ]

    print("=" * 70)
    print("EXECUTING SQL FILES")
    print("=" * 70)

    for file_name in sql_files:

        sql_path = os.path.join(
            SQL_FOLDER,
            file_name
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file_name.replace(".sql", "_report.txt")
        )

        print(f"\nRunning {file_name}...")

        execute_sql_file(
            conn,
            sql_path,
            output_path
        )

    conn.close()

    print("=" * 70)
    print("ALL SQL FILES EXECUTED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":

    main()