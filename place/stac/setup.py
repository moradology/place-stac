"""stac_fastapi: pgstac module."""

from setuptools import find_namespace_packages, setup

install_requires = [
    "orjson",
    "stac-fastapi.pgstac",
    "stac-fastapi.api",
    "stac-fastapi.types",
    "stac-fastapi.extensions",
    "uvicorn[standard]",
    "pypgstac[psycopg]",
    "pygeoif==0.7",
]

extra_reqs = {
    "dev": [],
    "docs": []
}


setup(
    name="place.stac",
    description="An implementation of STAC API based on the FastAPI framework and using the pgstac backend for PLACE.",
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    install_requires=install_requires,
    packages=find_namespace_packages(exclude=["alembic", "tests", "scripts"]),
    zip_safe=False,
    entry_points={
    },
)