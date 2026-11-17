# Student Data Analysis Pipeline

A small pandas pipeline that cleans student records, adds study-time groups,
summarizes results by pass status, and exports correlation and summary reports.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A student-data CSV file (not included in this repository)

## Run

Install the project dependencies:

```powershell
uv sync
```

Run the pipeline, replacing the example path with your CSV file:

```powershell
uv run python main.py --data .\student-data.csv
```

The CSV should include a `passed` column and may include `studytime` and
`absences`. By default, reports are written to the `data/` directory. Choose a
different location with `--output-dir`.

The input CSV and generated reports are excluded from Git to avoid publishing
student data or derived records.