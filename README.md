# course-db
CLI util for managing the database of the course (aka all the Google Sheets)


```bash
my_app/
├── cli/          # Entry points — argument parsing, command definitions (Click/Typer)
├── services/     # Business logic — what the commands actually do
├── models/       # Data models/schemas (Pydantic, dataclasses)
├── repository/   # Data access — reading/writing files, DB, APIs
└── utils/        # Shared helpers
```