
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="magictranslator",
    version="0.1.0",
    author="c_rainbow",
    author_email="c.rainbow.678@example.com",
    description="Wrapper library for multiple translation APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c-rainbow/magictranslator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

