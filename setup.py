from setuptools import find_packages, setup

DEV_REQUIRES = [
    "black",
    "pylint",
    "pre-commit",
    "mypy",
    "sqlalchemy-stubs",
    "pytest",
    "pytest-cov",
    "mkdocs",
]

setup(
    name="app_utils",
    version="0.1",
    author="Sandeep Srinivasa",
    author_email="sss@redcarpetup.com",
    license="MIT",
    description="A starter project to create a standalone TDD project with docker based postgresql fixtures",
    python_requires=">=3.7",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["alembic", "psycopg2-binary", "sqlalchemy", "parse", "pytest", "pydantic", "docker"],
    extras_require={
        "dev": DEV_REQUIRES
    },
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: SQL",
    ],
)
