#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023-2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""
This script checks that the pipfile of the repository meets the requirements.

In particular:
- Avoid the usage of "*"

It is assumed the script is run from the repository root.
"""

import re
import sys
import logging
import itertools
from typing import Any, Dict, List, Tuple, Iterator, Optional, OrderedDict as OrderedDictType, cast
from pathlib import Path
from collections import OrderedDict

import toml
import click
from aea.package_manager.v1 import PackageManagerV1
from aea.package_manager.base import load_configuration
from aea.configurations.data_types import Dependency


ANY_SPECIFIER = "*"


class PathArgument(click.Path):
    """Path parameter for CLI."""

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Optional[Path]:
        """Convert path string to `pathlib.Path`"""
        path_string = super().convert(value, param, ctx)
        return None if path_string is None else Path(path_string)


class Pipfile:
    """Class to represent Pipfile config."""

    ignore = [
        "open-aea-ledger-cosmos",
        "open-aea-ledger-ethereum",
        "open-aea-ledger-fetchai",
        "open-aea-flashbots",
        "open-aea-flashbots",
        "tomte",
    ]

    def __init__(
        self,
        sources: List[str],
        packages: OrderedDictType[str, Dependency],
        dev_packages: OrderedDictType[str, Dependency],
        file: Path,
    ) -> None:
        """Initialize object."""
        self.sources = sources
        self.packages = packages
        self.dev_packages = dev_packages
        self.file = file

    def __iter__(self) -> Iterator[Dependency]:
        """Iterate dependencies as from aea.configurations.data_types.Dependency object."""
        for name, dependency in itertools.chain(
            self.packages.items(), self.dev_packages.items()
        ):
            if name.startswith("comment_") or name in self.ignore:
                continue
            yield dependency

    def update(self, dependency: Dependency) -> None:
        """Update dependency specifier"""
        if dependency.name in self.ignore:
            return
        if dependency.name in self.packages:
            if dependency.version == "":
                return
            self.packages[dependency.name] = dependency
        else:
            self.dev_packages[dependency.name] = dependency

    def check(self, dependency: Dependency) -> Tuple[Optional[str], int]:
        """Check dependency specifier"""
        if dependency.name in self.ignore:
            return None, 0

        if dependency.name in self.packages:
            expected = self.packages[dependency.name]
            if expected != dependency:
                return (
                    f"in Pipfile {expected.get_pip_install_args()[0]}; "
                    f"got {dependency.get_pip_install_args()[0]}"
                ), logging.WARNING
            return None, 0

        if dependency.name not in self.dev_packages:
            return f"{dependency.name} not found in Pipfile", logging.ERROR

        expected = self.dev_packages[dependency.name]
        if expected != dependency:
            return (
                f"in Pipfile {expected.get_pip_install_args()[0]}; "
                f"got {dependency.get_pip_install_args()[0]}"
            ), logging.WARNING

        return None, 0

    @classmethod
    def parse(
        cls, content: str
    ) -> Tuple[List[str], OrderedDictType[str, OrderedDictType[str, Dependency]]]:
        """Parse from string."""
        sources = []
        sections: OrderedDictType = OrderedDict()
        lines = content.split("\n")
        comments = 0
        while len(lines) > 0:
            line = lines.pop(0)
            if "[[source]]" in line:
                source = line + "\n"
                while True:
                    line = lines.pop(0)
                    if line == "":
                        break
                    source += line + "\n"
                sources.append(source)
            if "[dev-packages]" in line or "[packages]" in line:
                section = line
                sections[section] = OrderedDict()
                while len(lines) > 0:
                    line = lines.pop(0).strip()
                    if line == "":
                        break
                    if line.startswith("#"):
                        sections[section][f"comment_{comments}"] = line
                        comments += 1
                    else:
                        dep = Dependency.from_pipfile_string(line)
                        sections[section][dep.name] = dep
        return sources, sections

    def compile(self) -> str:
        """Compile to Pipfile string."""
        content = ""
        for source in self.sources:
            content += source + "\n"

        content += "[packages]\n"
        for package, dep in self.packages.items():
            if package.startswith("comment"):
                content += str(dep) + "\n"
            else:
                content += dep.to_pipfile_string() + "\n"

        content += "\n[dev-packages]\n"
        for package, dep in self.dev_packages.items():
            if package.startswith("comment"):
                content += str(dep) + "\n"
            else:
                content += dep.to_pipfile_string() + "\n"
        return content

    @classmethod
    def load(cls, file: Path) -> "Pipfile":
        """Load from file."""
        sources, sections = cls.parse(
            content=file.read_text(encoding="utf-8"),
        )
        return cls(
            sources=sources,
            packages=sections.get("[packages]", OrderedDict()),
            dev_packages=sections.get("[dev-packages]", OrderedDict()),
            file=file,
        )

    def dump(self) -> None:
        """Write to Pipfile."""
        self.file.write_text(self.compile(), encoding="utf-8")



class PyProjectToml:
    """Class to represent pyproject.toml file."""

    ignore = [
        "python",
    ]

    def __init__(
        self,
        dependencies: OrderedDictType[str, Dependency],
        config: Dict[str, Dict],
        file: Path,
    ) -> None:
        """Initialize object."""
        self.dependencies = dependencies
        self.config = config
        self.file = file

    def __iter__(self) -> Iterator[Dependency]:
        """Iterate dependencies as from aea.configurations.data_types.Dependency object."""
        for dependency in self.dependencies.values():
            if dependency.name not in self.ignore:
                yield dependency

    def update(self, dependency: Dependency) -> None:
        """Update dependency specifier"""
        if dependency.name in self.ignore:
            return
        if dependency.name in self.dependencies and dependency.version == "":
            return
        self.dependencies[dependency.name] = dependency

    def check(self, dependency: Dependency) -> Tuple[Optional[str], int]:
        """Check dependency specifier"""
        if dependency.name in self.ignore:
            return None, 0

        if dependency.name not in self.dependencies:
            return f"{dependency.name} not found in pyproject.toml", logging.ERROR

        expected = self.dependencies[dependency.name]
        if expected.name != dependency.name and expected.version != dependency.version:
            return (
                f"in pyproject.toml {expected.get_pip_install_args()[0]}; "
                f"got {dependency.get_pip_install_args()[0]}"
            ), logging.WARNING

        return None, 0

    @classmethod
    def load(cls, pyproject_path: Path) -> Optional["PyProjectToml"]:
        """Load pyproject.yaml dependencies"""
        config = toml.load(pyproject_path)
        dependencies = OrderedDict()
        try:
            config["tool"]["poetry"]["dependencies"]
        except KeyError:
            return None
        for name, version in config["tool"]["poetry"]["dependencies"].items():
            if isinstance(version, str):
                dependencies[name] = Dependency(
                    name=name,
                    version=version.replace("^", "==") if version != "*" else "",
                )
                continue
            data = cast(Dict, version)
            if "extras" in data:
                version = data["version"]
                if re.match(r"^\d", version):
                    version = f"=={version}"
                dependencies[name] = Dependency(
                    name=name,
                    version=version,
                    extras=data["extras"],
                )
                continue

        return cls(
            dependencies=dependencies,
            config=config,
            file=pyproject_path,
        )

    def dump(self) -> None:
        """Dump to file."""
        update = ""
        content = self.file.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if " = " not in line:
                update += f"{line}\n"
                continue
            package, *_ = line.split(" = ")
            dep = self.dependencies.get(package)
            if dep is None:
                update += f"{line}\n"
                continue
            update += f"{dep.to_pipfile_string()}\n"
        self.file.write_text(update[:-1], encoding="utf-8")


def load_packages_dependencies(packages_dir: Path) -> List[Dependency]:
    """Returns a list of package dependencies."""
    package_manager = PackageManagerV1.from_dir(packages_dir=packages_dir)
    dependencies: Dict[str, Dependency] = {}
    for package in package_manager.iter_dependency_tree():
        if package.package_type.value == "service":
            continue
        _dependencies = load_configuration(  # type: ignore
            package_type=package.package_type,
            package_path=package_manager.package_path_from_package_id(
                package_id=package
            ),
        ).dependencies
        for key, value in _dependencies.items():
            if key not in dependencies:
                dependencies[key] = value
            else:
                print(f"Processing {key} {value} vs {dependencies[key]}")
                if value.version == "":
                    continue
                if dependencies[key].version == "":
                    dependencies[key] = value
                if value == dependencies[key]:
                    continue
                print(
                    f"Non-matching dependency versions for {key}: {value} vs {dependencies[key]}"
                )

    return list(dependencies.values())


def _update(
    packages_dependencies: List[Dependency],
    pipfile: Optional[Pipfile] = None,
    pyproject: Optional[PyProjectToml] = None,
) -> None:
    """Update dependencies."""

    if pipfile is not None:
        for dependency in packages_dependencies:
            pipfile.update(dependency=dependency)


        pipfile.dump()

    if pyproject is not None:
        for dependency in packages_dependencies:
            pyproject.update(dependency=dependency)


        pyproject.dump()



def _check(
    packages_dependencies: List[Dependency],
    pipfile: Optional[Pipfile] = None,
    pyproject: Optional[PyProjectToml] = None,
) -> None:
    """Update dependencies."""

    fail_check = 0

    if pipfile is not None:
        print("Comparing dependencies from Pipfile and packages")
        for dependency in packages_dependencies:
            error, level = pipfile.check(dependency=dependency)
            if error is not None:
                logging.log(level=level, msg=error)
                fail_check = level or fail_check


    if pyproject is not None:
        print("Comparing dependencies from pyproject.toml and packages")
        for dependency in packages_dependencies:
            error, level = pyproject.check(dependency=dependency)
            if error is not None:
                logging.log(level=level, msg=error)
                fail_check = level or fail_check

        print("Comparing dependencies from pyproject.toml and tox")

        print("Comparing dependencies from tox and pyproject.toml")

    print("Comparing dependencies from tox and packages")
    if fail_check == logging.ERROR:
        print("Dependencies check failed")
        sys.exit(1)

    if fail_check == logging.WARNING:
        print("Please address warnings to avoid errors")
        sys.exit(0)

    print("No issues found")


@click.command(name="dm")
@click.option(
    "--check",
    is_flag=True,
    help="Perform dependency checks.",
)
@click.option(
    "--packages",
    "packages_dir",
    type=PathArgument(
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    help="Path of the packages directory.",
)
@click.option(
    "--pipfile",
    "pipfile_path",
    type=PathArgument(
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    help="Pipfile path.",
)
@click.option(
    "--pyproject",
    "pyproject_path",
    type=PathArgument(
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    help="Pipfile path.",
)
def main(
    check: bool = False,
    packages_dir: Optional[Path] = None,
    pipfile_path: Optional[Path] = None,
    pyproject_path: Optional[Path] = None,
) -> None:
    """Check dependencies across packages, tox.ini, pyproject.toml and setup.py"""

    logging.basicConfig(format="- %(levelname)s: %(message)s")

    pipfile_path = pipfile_path or Path.cwd() / "Pipfile"
    pipfile = Pipfile.load(pipfile_path) if pipfile_path.exists() else None

    pyproject_path = pyproject_path or Path.cwd() / "pyproject.toml"
    pyproject = PyProjectToml.load(pyproject_path) if pyproject_path.exists() else None

    packages_dir = packages_dir or Path.cwd() / "packages"
    packages_dependencies = load_packages_dependencies(packages_dir=packages_dir)

    if check:
        return _check(
            pipfile=pipfile,
            pyproject=pyproject,
            packages_dependencies=packages_dependencies,
        )

    return _update(
        pipfile=pipfile,
        pyproject=pyproject,
        packages_dependencies=packages_dependencies,
    )


if __name__ == "__main__":
    main()
