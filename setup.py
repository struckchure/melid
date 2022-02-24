import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="melid",
    version="0.0.1",
    author="Dev 47 - Mohammed Al Ameen",
    author_email="ameenmohammed2311@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-47/melid",
    project_urls={
        "Bug Tracker": "https://github.com/dev-47/melid/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "melid"},
    packages=setuptools.find_packages(where="melid"),
    python_requires=">=3.6",
)
