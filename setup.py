import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="10-closest-films", # Replace with your own username
    version="0.0.1",
    author="Bohdan Mahometa",
    author_email="bohdan.mahometa@ucu.edu.ua",
    description="A project for finding 10 closest locations of films",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bogdanmagometa/10-closest-films",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
