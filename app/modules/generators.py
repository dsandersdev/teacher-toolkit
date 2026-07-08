class GeneratorModule:
    def __init__(self, toolkit):
        self.toolkit = toolkit

    def run(self, choice, registry):
        item = registry[choice]
        values = {}

        profile = self.toolkit.teacher_profile

        for field, default in item["fields"].items():

            if field == "curriculum":
                profile_curriculum = getattr(
                    profile,
                    "curriculum",
                    None,
                )

                if profile_curriculum:
                    values[field] = profile_curriculum
                    continue

                default = self.toolkit.settings.default_curriculum

            if field == "grade":
                profile_grades = getattr(
                    profile,
                    "grades",
                    None,
                )

                if profile_grades:
                    default = profile_grades[0]

            label = field.replace("_", " ").title()

            if default:
                value = input(
                    f"{label} [{default}]: "
                ).strip()

                values[field] = value or default

            else:
                values[field] = input(
                    f"{label}: "
                ).strip()

        generator = self.toolkit.generators[choice]

        result = generator.generate(**values)

        metadata = {
            "title": self.toolkit.build_title(values),
            **values,
        }

        self.toolkit.finish(
            result,
            item["prefix"],
            metadata=metadata,
        )