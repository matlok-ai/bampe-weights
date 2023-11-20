from setuptools import setup


long_description = open("README.md").read()
requirements = []
with open("./requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name="bampe-weights",
    packages=[
        "bw",
        "bw.converter",
        "bw.diff",
        "bw.st",
    ],
    scripts=[],
    version="0.0.3",
    license="Apache 2.0",
    description=(
        "An alternative approach to "
        "building Generative AI models"
    ),
    author="matlok-ops",
    author_email="hello@matlok.ai",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/matlok-ai/bampe-weights",
    keywords=[
        "artificial intelligence",
        "deep learning",
        "transformers",
    ],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
