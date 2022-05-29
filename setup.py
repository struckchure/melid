import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="melid",
    version="0.1-b",
    author="Dev 47 - Mohammed Al Ameen",
    author_email="ameenmohammed2311@gmail.com",
    description="A PyQt5 desktop application framework with simple and powerful features.",
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
    packages=setuptools.find_namespace_packages(include=["melid.*"]),
    namespace_packages=["melid"],
    python_requires=">=3.6",
    install_requires=[
        "PyQt5==5.15.6",
        "QtAwesome==1.1.1",
    ],
)
