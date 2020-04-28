from setuptools import setup
from io import open

with open("readme.md", "r", encoding="utf-8") as fr:
	long_description = fr.read()

setup(
	name="rbtv-api",
	version="0.0.1",
	py_modules=["rbtv"],
	long_description=long_description,
	install_requires=["requests"]
)
