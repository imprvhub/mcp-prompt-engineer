from setuptools import setup, find_packages

setup(
    name="mcp-prompt-engineer",
    version="0.1.0",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ivan Luna",
    author_email="contact@ivanluna.dev",
    url="https://github.com/imprvhub/mcp-prompt-engineer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "mcp[cli]>=1.3.0",
        "aiohttp>=3.11.13",
    ],
    entry_points={
        "console_scripts": [
            "mcp-prompt-engineer=mcp_prompt_engineer.main:mcp.run",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
