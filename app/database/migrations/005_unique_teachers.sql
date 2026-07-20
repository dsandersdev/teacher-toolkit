CREATE UNIQUE INDEX IF NOT EXISTS idx_teachers_unique_profile
ON teachers (
    name,
    school
);