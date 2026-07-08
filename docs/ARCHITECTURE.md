# Teacher Toolkit Architecture

Teacher Toolkit is an AI-powered teaching assistant designed to help teachers create instructional resources, manage students, analyze assessments, and generate targeted interventions.

The project is designed with a modular architecture so it can grow into:

- Desktop application
- Web application
- API backend
- Multi-teacher platform

---

# High Level Structure

```text
Teacher-Toolkit
│
├── app/
│   │
│   ├── teacher_toolkit.py
│   │
│   │   Main application controller
│   │   Handles:
│   │   - startup
│   │   - dependency creation
│   │   - menu routing
│   │   - shared save/export workflow
│   │
│   ├── modules/
│   │
│   │   User workflows and features
│   │
│   │   ├── generators.py
│   │   ├── resources.py
│   │   ├── profiles.py
│   │   ├── students.py
│   │   └── gradebook.py
│   │
│   ├── generators/
│   │
│   │   AI content generation layer
│   │
│   │   Examples:
│   │   - Lesson plans
│   │   - Worksheets
│   │   - Quizzes
│   │   - Parent emails
│   │   - Report comments
│   │   - Intervention plans
│   │
│   ├── repositories/
│   │
│   │   Data access layer
│   │
│   │   Handles:
│   │   - Teachers
│   │   - Students
│   │   - Resources
│   │   - Assessments
│   │   - Scores
│   │
│   ├── exporters/
│   │
│   │   Output generation
│   │
│   │   Supports:
│   │   - Markdown
│   │   - DOCX
│   │   - PDF
│   │   - Excel
│   │
│   └── templates/
│
│       AI prompt templates
│
├── database/
├── outputs/
├── docs/
└── tests/
```

---

# Module Layer

Modules contain user workflows.

Modules do not directly create files or talk to AI.

They coordinate:

```text
User input
    ↓
Module
    ↓
Generator / Repository
    ↓
Exporter
```

Current modules:

## Generator Module

Handles:

- Lesson plans
- Worksheets
- Quizzes
- Parent communication
- Report comments


## Resource Module

Handles:

- Saved resource library
- Creating quizzes from lessons
- Creating worksheets from lessons
- Viewing lesson history


## Profile Module

Handles:

- Teacher profiles
- Curriculum preferences
- Grade levels
- Teaching style


## Student Module

Handles:

- Student management
- Student records


## Gradebook Module

Handles:

- Assessments
- Student scores
- Performance analysis
- Intervention workflow

Features:

- Create assessments
- Enter scores
- Analyze results
- Find struggling students
- Export Excel reports
- Generate AI interventions
- Create intervention worksheets
- Create intervention quizzes
- Student progress tracking
- Parent progress updates
- Class performance summaries

---

# Generator Layer

The AI generator layer creates classroom content.

Examples:

```text
modules
   ↓
generators
   ↓
AI model
   ↓
generated resource
```

Generators use templates instead of hard-coded prompts.

---

# Repository Layer

Repositories isolate storage logic.

The rest of the application does not need to know how data is stored.

Current storage can later move to:

- SQLite
- PostgreSQL
- Cloud database

without rewriting modules.

---

# Export Layer

All resources support multiple outputs:

- Markdown
- DOCX
- PDF
- JSON

Gradebook additionally supports:

- Excel

---

# AI Integration

Teacher Toolkit uses AI models through an abstraction layer.

Supported goals:

- Local AI
- RTX GPU acceleration
- Future cloud models

---

# Design Principles

- Keep user workflows separate from AI logic
- Keep storage separate from application logic
- Templates control AI behavior
- Generated resources should be reusable
- Every teacher can have separate settings
- Architecture should support future web conversion

---

# Current Status

Completed:

- Modular refactor
- Teacher profiles
- Student management
- Resource library
- AI generators
- Gradebook
- AI interventions
- Progress tracking
- Export system

Next architecture phase:

- API layer
- Desktop GUI
- Web dashboard