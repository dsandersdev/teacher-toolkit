# Teacher Toolkit Architecture

Teacher Toolkit is built on top of AI-SDK.

The application follows a modular architecture organized by functional domains.

```
Teacher Toolkit
│
├── app/
│   ├── main.py
│   ├── teacher_toolkit.py
│   │
│   ├── planning/
│   ├── classroom/
│   ├── communication/
│   ├── students/
│   ├── ai/
│   ├── services/
│   └── models/
│
├── prompts/
├── outputs/
├── docs/
└── tests/
```

---

## Planning

Responsible for instructional planning.

Examples:

- Lesson plans
- Unit plans
- Standards alignment
- Scope and sequence

---

## Classroom

Responsible for creating classroom materials.

Examples:

- Worksheets
- Assessments
- Exit tickets
- Homework
- Slideshows
- Classroom games

---

## Communication

Responsible for teacher communication.

Examples:

- Parent emails
- Newsletters
- Report card comments
- Conference notes

---

## Students

Responsible for instructional support.

Examples:

- Intervention
- RTI
- Differentiation
- Extension activities

---

## AI

Coordinates prompts and AI interactions using AI-SDK.

---

## Services

Shared application services.

Examples:

- Configuration
- File export
- Document generation
- Templates

---

## Design Principles

- Each module has a single responsibility.
- AI prompts are stored separately from code.
- Output should always be classroom-ready.
- All generated content should be reproducible.
- Teacher Toolkit extends AI-SDK rather than duplicating SDK functionality.
