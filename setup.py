from setuptools import setup


long_description = open("README.md").read()
requirements = []
with open("./requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name="bampe-weights",
    packages=[
        "bw",
        "bw.bl",
        "bw.converter",
        "bw.diff",
        "bw.np",
        "bw.sk",
        "bw.st",
    ],
    scripts=[],
    version="0.1.0",
    license="MIT",
    description=(
        "An alternative approach to "
        "building foundational generative "
        "AI models "
        "with visualizations using Blender"
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
