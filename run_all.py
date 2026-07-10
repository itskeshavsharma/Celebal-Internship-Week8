import subprocess
import sys

def run_script(script_path, args=None):
    """
    Runs a python script using subprocess and handles any errors.
    """
    print("\n" + "=" * 70)
    print(f"RUNNING: python {script_path}")
    print("=" * 70)
    
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
        
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Occurred while running {script_path}")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

def main():
    print("=" * 70)
    print("      E-COMMERCE ORDER ANALYTICS PIPELINE (AUTOMATED RUN)")
    print("=" * 70)

    # Step 1: Generate Raw Data
    run_script("scripts/generate_data.py")

    # Step 2: Clean Data
    run_script("scripts/clean_data.py")

    # Step 3: Load SQLite Database
    run_script("scripts/load_database.py")

    # Step 4: Run SQL Queries & Save Reports
    run_script("scripts/run_queries.py")

    # Step 5: Run Tests
    run_script("scripts/run_tests.py")

    print("\n" + "=" * 70)
    print("Success: Pipeline executed successfully!")
    print("All datasets generated, cleaned, loaded, queried, and verified.")
    print("=" * 70)
    print("\nInfo: To run the interactive CLI Dashboard, use this command:")
    print("   python scripts/report_cli.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
