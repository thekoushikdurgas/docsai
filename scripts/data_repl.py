"""Interactive data ingestion REPL (S3/local CSV, email patterns, optional generator/CSV dual-write).

Run from ``docs/``:

- ``python cli.py data ingest-local``
- Or: ``python -m scripts.data_repl`` with ``docs/`` on ``PYTHONPATH``.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_DOCS = _SCRIPTS.parent
for _p in (_DOCS, _SCRIPTS):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from scripts.config import get_all_defaults, get_default, reset_defaults, set_default
from scripts.ingestion.local import (
    ingest_companies_from_local,
    ingest_contacts_from_local,
    ingest_email_patterns_from_local,
)
from scripts.ingestion.s3 import ingest_companies_from_s3, ingest_contacts_from_s3
from scripts.utils import ingest_utils
from scripts.utils.s3_client import get_s3_bucket_name, get_s3_client

list_csv_files = ingest_utils.list_csv_files
split_companies_contacts = ingest_utils.split_companies_contacts
list_s3_csv_objects = ingest_utils.list_s3_csv_objects
classify_csv = ingest_utils.classify_csv


def input_int(prompt: str, default: int) -> int:
    try:
        raw = input(f"{prompt} [{default}]: ").strip()
        return int(raw) if raw else default
    except Exception:
        return default


def input_str(prompt: str, default: str) -> str:
    raw = input(f"{prompt} [{default}]: ").strip()
    return raw if raw else default


def _after_ingest_errors(before_path: str | None, before_count: int | None, label: str) -> None:
    after_path, after_count = ingest_utils.get_error_log_info()
    if after_count and before_count is not None and after_count > before_count and after_path:
        print(f"\nLogged {after_count - before_count} error(s) during {label}. See: {after_path}")


def run_companies_from_s3(batch_size: int, max_threads: int) -> None:
    print("Listing CSVs in S3 bucket...")
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()
    keys = list_s3_csv_objects(s3_client, bucket_name)
    if not keys:
        print("No CSV objects found in S3 bucket.")
        return
    for i, k in enumerate(keys, 1):
        print(f"{i}. {k}")
    try:
        idx = int(input("Select CSV to ingest: ").strip())
        if idx < 1 or idx > len(keys):
            print("Invalid selection.")
            return
    except Exception:
        print("Invalid input.")
        return
    key = keys[idx - 1]
    print(f"Starting Companies import from S3 object: {key}")
    before_path, before_count = ingest_utils.get_error_log_info()
    ingest_companies_from_s3(batch_size=batch_size, max_threads=max_threads, object_key=key)
    _after_ingest_errors(before_path, before_count, "companies S3 ingestion")


def run_contacts_from_s3(batch_size: int, max_threads: int) -> None:
    print("Listing CSVs in S3 bucket...")
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()
    keys = list_s3_csv_objects(s3_client, bucket_name)
    if not keys:
        print("No CSV objects found in S3 bucket.")
        return
    for i, k in enumerate(keys, 1):
        print(f"{i}. {k}")
    try:
        idx = int(input("Select CSV to ingest: ").strip())
        if idx < 1 or idx > len(keys):
            print("Invalid selection.")
            return
    except Exception:
        print("Invalid input.")
        return
    key = keys[idx - 1]
    print(f"Starting Contacts import from S3 object: {key}")
    before_path, before_count = ingest_utils.get_error_log_info()
    ingest_contacts_from_s3(batch_size=batch_size, max_threads=max_threads, object_key=key)
    _after_ingest_errors(before_path, before_count, "contacts S3 ingestion")


def run_companies_from_local(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    companies, _, unknowns = split_companies_contacts(paths)
    if not companies:
        print("No company CSVs detected under data/data/")
        if unknowns:
            print(f"{len(unknowns)} unknown CSV(s) skipped.")
        return
    for i, p in enumerate(companies, 1):
        print(f"{i}. {p}")
    try:
        idx = int(input("Select CSV to ingest: ").strip())
        if idx < 1 or idx > len(companies):
            print("Invalid selection.")
            return
    except Exception:
        print("Invalid input.")
        return
    p = companies[idx - 1]
    print(f"Ingesting company CSV: {p}")
    before_path, before_count = ingest_utils.get_error_log_info()
    ingest_companies_from_local(p, batch_size=batch_size, max_threads=max_threads)
    _after_ingest_errors(before_path, before_count, "company ingestion")


def run_contacts_from_local(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    _, contacts, unknowns = split_companies_contacts(paths)
    if not contacts:
        print("No contact CSVs detected under data/data/")
        if unknowns:
            print(f"{len(unknowns)} unknown CSV(s) skipped.")
        return
    for i, p in enumerate(contacts, 1):
        print(f"{i}. {p}")
    try:
        idx = int(input("Select CSV to ingest: ").strip())
        if idx < 1 or idx > len(contacts):
            print("Invalid selection.")
            return
    except Exception:
        print("Invalid input.")
        return
    p = contacts[idx - 1]
    print(f"Ingesting contact CSV: {p}")
    before_path, before_count = ingest_utils.get_error_log_info()
    ingest_contacts_from_local(p, batch_size=batch_size, max_threads=max_threads)
    _after_ingest_errors(before_path, before_count, "contact ingestion")


def run_both_from_local_single(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    both_csvs = [p for p in paths if "company" in classify_csv(p) and "contact" in classify_csv(p)]
    if not both_csvs:
        print("No CSVs with both company and contact columns detected under data/data/")
        return
    print("CSVs with both company and contact columns:")
    for i, p in enumerate(both_csvs, 1):
        print(f"{i}. {os.path.basename(p)}")
    try:
        idx = int(input("Select CSV to ingest: ").strip())
        if idx < 1 or idx > len(both_csvs):
            print("Invalid selection.")
            return
    except Exception:
        print("Invalid input.")
        return
    p = both_csvs[idx - 1]
    print(f"\n=== Processing {os.path.basename(p)} ===")
    before_path, before_count = ingest_utils.get_error_log_info()
    print("Step 1/2: Ingesting companies...")
    ingest_companies_from_local(p, batch_size=batch_size, max_threads=max_threads)
    print("\nStep 2/2: Ingesting contacts...")
    ingest_contacts_from_local(p, batch_size=batch_size, max_threads=max_threads)
    _after_ingest_errors(before_path, before_count, f"processing {os.path.basename(p)}")
    print(f"\n=== Completed processing {os.path.basename(p)} ===")


def run_both_from_local_all(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    both_csvs = [p for p in paths if "company" in classify_csv(p) and "contact" in classify_csv(p)]
    if not both_csvs:
        print("No CSVs with both company and contact columns detected under data/data/")
        return
    print(f"\nFound {len(both_csvs)} CSV(s) with both company and contact columns:")
    for i, p in enumerate(both_csvs, 1):
        print(f"{i}. {os.path.basename(p)}")
    confirm = input(f"\nProcess all {len(both_csvs)} files? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Operation cancelled.")
        return
    batch_before_path, batch_before_count = ingest_utils.get_error_log_info()
    for i, p in enumerate(both_csvs, 1):
        print(f"\n--- File {i}/{len(both_csvs)}: {os.path.basename(p)} ---")
        ingest_companies_from_local(p, batch_size=batch_size, max_threads=max_threads)
        ingest_contacts_from_local(p, batch_size=batch_size, max_threads=max_threads)
    batch_after_path, batch_after_count = ingest_utils.get_error_log_info()
    if batch_after_count and batch_before_count is not None and batch_after_count > batch_before_count and batch_after_path:
        print(f"\nLogged {batch_after_count - batch_before_count} error(s). See: {batch_after_path}")
    print(f"\n=== All {len(both_csvs)} files processed ===")


def run_all_companies_from_local(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    companies, _, _ = split_companies_contacts(paths)
    if not companies:
        print("No company CSVs detected under data/data/")
        return
    if input(f"\nProcess all {len(companies)} company files? (yes/no): ").strip().lower() != "yes":
        return
    b0, c0 = ingest_utils.get_error_log_info()
    for i, p in enumerate(companies, 1):
        print(f"\n--- {i}/{len(companies)}: {os.path.basename(p)} ---")
        ingest_companies_from_local(p, batch_size=batch_size, max_threads=max_threads)
    _after_ingest_errors(b0, c0, "all company files")


def run_all_contacts_from_local(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    _, contacts, _ = split_companies_contacts(paths)
    if not contacts:
        print("No contact CSVs detected under data/data/")
        return
    if input(f"\nProcess all {len(contacts)} contact files? (yes/no): ").strip().lower() != "yes":
        return
    b0, c0 = ingest_utils.get_error_log_info()
    for i, p in enumerate(contacts, 1):
        print(f"\n--- {i}/{len(contacts)}: {os.path.basename(p)} ---")
        ingest_contacts_from_local(p, batch_size=batch_size, max_threads=max_threads)
    _after_ingest_errors(b0, c0, "all contact files")


def run_email_patterns_from_local(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    if not paths:
        print("No CSV files found under data/data/")
        return
    for i, p in enumerate(paths, 1):
        print(f"{i}. {os.path.basename(p)}")
    try:
        idx = int(input("\nSelect CSV for email patterns: ").strip())
        if idx < 1 or idx > len(paths):
            print("Invalid selection.")
            return
    except Exception:
        print("Invalid input.")
        return
    p = paths[idx - 1]
    b0, c0 = ingest_utils.get_error_log_info()
    ingest_email_patterns_from_local(p, batch_size=batch_size, max_threads=max_threads)
    _after_ingest_errors(b0, c0, "email pattern import")


def run_all_email_patterns_from_local(batch_size: int, max_threads: int) -> None:
    paths = list_csv_files()
    if not paths:
        print("No CSV files found under data/data/")
        return
    if input(f"\nProcess all {len(paths)} files for email patterns? (yes/no): ").strip().lower() != "yes":
        return
    b0, c0 = ingest_utils.get_error_log_info()
    for i, p in enumerate(paths, 1):
        print(f"\n--- {i}/{len(paths)}: {os.path.basename(p)} ---")
        ingest_email_patterns_from_local(p, batch_size=batch_size, max_threads=max_threads)
    _after_ingest_errors(b0, c0, "all email pattern files")


def show_postgres_settings() -> None:
    while True:
        print("\n=== PostgreSQL Settings ===")
        print(f"1) User (current: {get_default('postgres.user')})")
        print(f"2) Password (current: {'*' * len(get_default('postgres.password', '') or '')})")
        print(f"3) Host (current: {get_default('postgres.host')})")
        print(f"4) Port (current: {get_default('postgres.port')})")
        print(f"5) Database (current: {get_default('postgres.database')})")
        print("6) Back")
        choice = input("Select an option: ").strip()
        if choice == "1":
            set_default("postgres.user", input_str("PostgreSQL User", get_default("postgres.user")))
        elif choice == "2":
            set_default("postgres.password", input_str("PostgreSQL Password", get_default("postgres.password")))
        elif choice == "3":
            set_default("postgres.host", input_str("PostgreSQL Host", get_default("postgres.host")))
        elif choice == "4":
            set_default("postgres.port", input_int("PostgreSQL Port", int(get_default("postgres.port") or 5432)))
        elif choice == "5":
            set_default("postgres.database", input_str("PostgreSQL Database", get_default("postgres.database")))
        elif choice == "6":
            break


def show_s3_settings() -> None:
    while True:
        ak = get_default("s3.access_key") or ""
        print("\n=== S3 Settings ===")
        print(f"1) Access Key (current: {ak[:10]}...)" if len(ak) > 10 else f"1) Access Key (current: {ak or '(empty)'})")
        print("2) Secret Key (current: ***)")
        print(f"3) Region (current: {get_default('s3.region')})")
        print(f"4) Bucket Name (current: {get_default('s3.bucket_name')})")
        print("5) Back")
        choice = input("Select an option: ").strip()
        if choice == "1":
            set_default("s3.access_key", input_str("S3 Access Key", ak))
        elif choice == "2":
            set_default("s3.secret_key", input_str("S3 Secret Key", get_default("s3.secret_key")))
        elif choice == "3":
            set_default("s3.region", input_str("S3 Region", get_default("s3.region")))
        elif choice == "4":
            set_default("s3.bucket_name", input_str("S3 Bucket Name", get_default("s3.bucket_name")))
        elif choice == "5":
            break


def show_generator_settings() -> None:
    while True:
        defaults = get_all_defaults()
        config = defaults.get("generation", {})
        es_config = config.get("elasticsearch", {})
        print("\n=== Synthetic Data Generator Settings ===")
        print(f"1) Total Companies (current: {config.get('total_companies', 1_000_000):,})")
        print(f"2) Contacts per Company (current: {config.get('contacts_per_company', 5)})")
        print("… (3–13) batch/process/ES host-port-user-password/index names — use config.json or extend here")
        print("13) Back")
        choice = input("Select an option: ").strip()
        if choice == "1":
            set_default("generation.total_companies", input_int("Total Companies", int(config.get("total_companies", 1_000_000))))
        elif choice == "2":
            set_default("generation.contacts_per_company", input_int("Contacts per Company", int(config.get("contacts_per_company", 5))))
        elif choice == "13":
            break


def show_all_settings() -> None:
    defaults = get_all_defaults()
    print("\n=== All Current Settings ===")
    print(defaults)
    input("\nPress Enter to continue...")


def show_settings_menu() -> None:
    while True:
        print("\n=== Settings Menu ===")
        d = get_all_defaults()
        print(f"1) Batch Size ({d.get('batch_size', 1000)})  2) Max Threads ({d.get('max_threads', 3)})")
        print("3) PostgreSQL  4) S3  5) Generator  6) View all  7) Reset  8) Back")
        choice = input("Select an option: ").strip()
        if choice == "1":
            set_default("batch_size", input_int("Batch Size", int(d.get("batch_size", 1000))))
        elif choice == "2":
            set_default("max_threads", input_int("Max Threads", int(d.get("max_threads", 3))))
        elif choice == "3":
            show_postgres_settings()
        elif choice == "4":
            show_s3_settings()
        elif choice == "5":
            show_generator_settings()
        elif choice == "6":
            show_all_settings()
        elif choice == "7":
            if input("Reset all settings to defaults? (yes/no): ").strip().lower() == "yes":
                reset_defaults()
                print("Reset.")
        elif choice == "8":
            break


def run_csv_processor() -> None:
    try:
        from scripts.generation.csv_orchestrator import CSVOrchestrator
        from scripts.generation.config import load_generator_config
    except ImportError as e:
        print(f"Import error: {e}")
        return
    csv_files = list_csv_files()
    if not csv_files:
        print("No CSV files found in data/data/")
        return
    for i, f in enumerate(csv_files, 1):
        print(f"{i}. {os.path.basename(f)}")
    try:
        idx = int(input("\nSelect CSV file: ").strip())
        csv_path = csv_files[idx - 1]
    except Exception:
        print("Invalid selection.")
        return
    try:
        config = load_generator_config()
    except Exception as e:
        print(f"Config error: {e}")
        return
    if input("\nStart processing? (yes/no): ").strip().lower() != "yes":
        return
    try:
        CSVOrchestrator(config).run(csv_path)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Error: {e}")


def run_synthetic_data_generator() -> None:
    try:
        from scripts.generation.orchestrator import GeneratorOrchestrator
        from scripts.generation.config import load_generator_config
    except ImportError as e:
        print(f"Import error: {e}")
        return
    try:
        config = load_generator_config()
    except Exception as e:
        print(f"Config error: {e}")
        return
    if input("\nStart generation? (yes/no): ").strip().lower() != "yes":
        return
    try:
        GeneratorOrchestrator(config).run()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Error: {e}")


def main() -> None:
    batch_size = get_default("batch_size", 1000)
    max_threads = get_default("max_threads", 3)
    while True:
        print("\n=== Data Ingestion CLI ===")
        print("1) Companies from S3   2) Contacts from S3")
        print("3) Companies from Local   4) Contacts from Local")
        print("5) Companies & Contacts (one CSV)   6) Both (all local CSVs)")
        print("7) All companies local   8) All contacts local")
        print("9) Email patterns (one CSV)   10) Email patterns (all CSVs)")
        print("11) Synthetic data generator   12) CSV dual-write (PG+ES)")
        print("13) Settings   14) Exit")
        choice = input("Select an option: ").strip()
        batch_size = get_default("batch_size", 1000)
        max_threads = get_default("max_threads", 3)
        actions = {
            "1": lambda: run_companies_from_s3(batch_size, max_threads),
            "2": lambda: run_contacts_from_s3(batch_size, max_threads),
            "3": lambda: run_companies_from_local(batch_size, max_threads),
            "4": lambda: run_contacts_from_local(batch_size, max_threads),
            "5": lambda: run_both_from_local_single(batch_size, max_threads),
            "6": lambda: run_both_from_local_all(batch_size, max_threads),
            "7": lambda: run_all_companies_from_local(batch_size, max_threads),
            "8": lambda: run_all_contacts_from_local(batch_size, max_threads),
            "9": lambda: run_email_patterns_from_local(batch_size, max_threads),
            "10": lambda: run_all_email_patterns_from_local(batch_size, max_threads),
            "11": run_synthetic_data_generator,
            "12": run_csv_processor,
            "13": show_settings_menu,
        }
        if choice == "14":
            print("Goodbye.")
            break
        fn = actions.get(choice)
        if fn:
            fn()
        else:
            print("Invalid choice. Select 1-14.")


if __name__ == "__main__":
    main()
