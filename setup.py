import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onelab_api-jackbkennedy",
    version="0.0.1",
    author="Jack Kennedy",
    author_email="jackbkennedy@gmail.com",
    description="A python package to use gmsh and ONELAB via their original python APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackbkennedy/onelab_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)