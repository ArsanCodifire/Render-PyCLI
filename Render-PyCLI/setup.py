from setuptools import setup, find_packages

setup(
    name="renderpy",
    version="0.5.0",
    description="Render CLI in Python",
    long_description=open("ReadMe.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Arsan Codifire",
    url="https://github.com/ArsanCodifire/Render-PyCLI",  # replace with your repo link
    packages=find_packages(),
    install_requires=[
        "typer",
        "httpx",
        "rich",
        "textual"
    ],
    entry_points={
        "console_scripts": [
            "renderpy=renderpy.cli:app"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
