from sdk.ai import Application

app = Application("Teacher Toolkit")

response = app.ai.chat(
            "Create a Grade 2 math lesson about fractions."
            )

app.outputs.write_text("lesson.md", response)

print("Done!")
