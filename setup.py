from setuptools import setup

with open("readme.md", encoding="utf-8") as fr:
    long_description = fr.read()

setup(
    author="Dobatymo",
    name="rbtv-api",
    version="0.0.8",
    url="https://github.com/Dobatymo/rbtv-api",
    description="Simple Python wrapper for the JSON Rocket Beans TV API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=["rbtv"],
    python_requires=">=3.6",
    install_requires=["requests", "genutility"],
    extras_require={"all": ["unidecode"]},
    use_2to3=False,
)
