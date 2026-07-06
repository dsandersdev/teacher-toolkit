# Teacher Toolkit Roadmap

Teacher Toolkit will evolve in phases.

The roadmap is organized by user value rather than technical implementation.

---

# Version 0.1 — Foundation

## AI Integration

- [ ] Connect AI SDK
- [ ] Configuration
- [ ] Prompt loading

## Lesson Planning

- [ ] Lesson generator
- [ ] Essential questions
- [ ] Learning objectives

## Output

- [ ] Markdown output
- [ ] Organized workspace

---

# Version 0.2 — Classroom Materials

- [ ] Worksheet generator
- [ ] Quiz generator
- [ ] Exit ticket generator
- [ ] Homework generator

---

# Version 0.3 — Teacher Communication

- [ ] Parent email generator
- [ ] Newsletter generator
- [ ] Report card comments
- [ ] Conference summaries

---

# Version 0.4 — Student Support

- [ ] Differentiation
- [ ] RTI plans
- [ ] Intervention lessons
- [ ] Enrichment activities

---

# Version 0.5 — Classroom AI Assistant

- [ ] Ask questions
- [ ] Brainstorm activities
- [ ] Rewrite text
- [ ] Explain concepts
- [ ] Generate examples

---

# Future Ideas

- PowerPoint generation
- PDF export
- Google Docs export
- Standards databases
- Curriculum mapping
- Classroom calendar
- Year planner
- AI image generation
- Interactive lessons
- Voice assistant

## Future Feature Roadmap: Teacher Uploads, Grading, and Gradebook

### Manual Resource Upload
- Allow teachers to upload their own lessons, worksheets, quizzes, tests, and activities.
- Store uploaded resources in SQLite.
- Make uploaded resources searchable with generated resources.
- Allow uploaded lessons to be used as source material for quizzes, worksheets, or reteach lessons.

### Assignment and Assessment Grading
- Allow teachers to load completed student work from a folder.
- Support grading worksheets, quizzes, and tests using an answer key.
- Store student scores in the database.
- Track scores by student, assessment, topic, and date.

### Excel Gradebook Export
- Export student grades to Excel.
- Support exporting:
  - one quiz/test
  - one worksheet
  - multiple assessments
  - class-wide performance
  - individual student progress
- Include averages, percentages, and performance summaries.

### Intervention and Small Group Tools
- Allow teachers to choose a score threshold, such as below 70%.
- Identify students who need extra support.
- Generate targeted practice worksheets.
- Generate reteach lessons.
- Generate small-group activities.
- Group students by skill gaps or assessment performance.

### Future Database Tables
Planned database additions:

- students
- assessments
- student_scores
- uploaded_resources
- skill_gaps
- intervention_groups
