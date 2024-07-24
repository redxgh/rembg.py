from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rembg-pro",
    version="0.1.0",
    author="Marwen Trabelsi",
    author_email="marwen.trabelsi@relayr.io",
    description="A simple, FREE AI background removal tool for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your_project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "requests-toolbelt",
    ],
    extras_require={
        "dev": [
            "pytest",
            "mock",
        ],
    },
)