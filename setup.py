import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="manca_queen_voting",
    version="0.0.1",
    author="Subhash Scaria",
    author_email="subhashscaria@gmail.com",
    description="Created for Manca Queen Contest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sscaria/python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
