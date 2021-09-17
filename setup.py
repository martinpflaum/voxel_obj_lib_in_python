import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "voxelobj",
    version = "0.0.1",
    install_requires=["numpy"],
    author = "Martin Pflaum",
    author_email = "martin.pflaum.09.03.1999@gmail.com",
    description = "simple voxel library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/martinpflaum/voxel_obj_lib_in_python",
    keywords=["python","voxel","obj","3D"],
    project_urls={
        "Bug Tracker": "https://github.com/martinpflaum/voxel_obj_lib_in_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.6",
)