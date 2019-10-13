import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onelab",
    author="Jack Kennedy",
    author_email="jackbkennedy@gmail.com",
    description="A python package to use gmsh and ONELAB via their original python APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackbkennedy/onelab",
    download_url = 'https://github.com/jackbkennedy/onelab/releases/tag/v0.1',
    packages=setuptools.find_packages(),
    license="GPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'pandas']
)
