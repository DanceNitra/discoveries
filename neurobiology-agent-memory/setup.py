from setuptools import setup, find_packages

setup(
    name="neurobiology_agent_memory",
    version="0.1.0",
    description="5-Tier Agent Memory Architecture — Complementary Learning Systems",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
)
