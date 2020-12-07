from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bagpipemanager",
    version="1.0",
    packages=["bagpipemanager"],
    url="https://github.com/vhte/bagpipemanager",
    license="MIT",
    author="Victor Torres",
    author_email="talk@victortorr.es",
    description="Application to manage Bagpipe Player (.bww) files. Modify tune and sheet properties with few clicks/commands.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pytest"],
    python_requires=">=3.6",
)
