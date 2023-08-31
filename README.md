[![Linting](https://github.com/cnangel/build-rpm-action/actions/workflows/lint.yml/badge.svg)](https://github.com/cnangel/build-rpm-action/actions/workflows/lint.yml)
[![Testing](https://github.com/cnangel/build-rpm-action/actions/workflows/test.yml/badge.svg)](https://github.com/cnangel/build-rpm-action/actions/workflows/test.yml)

# Build RPM Packages GitHub Action

This action builds RPM packages in a clean, flexible environment.

It is mainly a shell wrapper around `rpmbuild`, using a configurable
Docker image to install build dependencies in and build packages. Resulting
.rpm files and other build artifacts are moved to a specified place.


## Usage
### Basic Example
```yaml
on: push

jobs:
  build-rpms:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: cnangel/build-rpm-action@v1
        env:
          RPM_BUILD_OPTIONS: nodebuginfo
        with:
          rpmbuild_opts: -bb
```

### Inputs
All inputs have a default value or are optional.

#### `dnf_opts`
Extra options to be passed to `dnf` or `yum` when installing build dependencies and
extra packages.

Optional and empty by default.

#### `artifacts_dir`
Directory relative to the workspace where the built packages and other
artifacts will be moved to.

Defaults to `rpmbuild/RPMS` in the workspace.

#### `before_build_hook`
Shell command(s) to be executed after installing the build dependencies and right
before `rpmbuild` is executed. A single or multiple commands can be
given, same as for a
[`run` step](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsrun)
in a workflow.

The hook is executed with `sh -c` as the root user *inside* the build container.
The package contents from the build dependencies and
[`extra_build_deps`](#extra_build_deps) are available.

Optional and empty by default.

Example use case:
```yaml
- uses: cnangel/build-rpm-action@v1
  with:
    before_build_hook: ./autogen.sh
    extra_build_deps: gcc-c++ jo jq git
```

#### `rpmbuild_opts`
Options to be passed to `rpmbuild`. See `man rpmbuild`.

Optional and empty by default.

#### `docker_image`
Name of a (Redhat-based) Docker image to build packages inside or path of a
Dockerfile in GITHUB_WORKSPACE to build a container from.

Defaults to `cnangel:centos9`.

#### `extra_build_deps`
Extra packages to be installed as “build dependencies”. *This should rarely be
used, build dependencies should be specified in the `*.spec` file.*

By default, these packages are built with the "-ba" option, which will build 
the source code package (src.rpm) and the normal application architecture 
packages (rpm)

Optional and empty by default.

#### `extra_docker_args`
Additional command-line arguments passed to `docker run` when the build
container is started. This might be needed if specific volumes or network
settings are required.

Optional and empty by default.

#### `host_arch`
The architecture packages are built for `noarch`, `i386`, `x86_64`

Optional and defaults to the architecture the action is run on (likely x86_64).

Basic example for cross-compilation:
```yaml
- uses: cnangel/build-rpm-action@v1
  with:
    host_arch: i386
```

#### `source_dir`
Directory relative to the workspace that contains the package sources,
especially the `rpmbuild/SOURCES` subdirectory.

Defaults to the workspace.

### Outputs
#### `rpm_dir_names`
The compiled product supports multiple files.

#### `rpm_dir_path`
Compiled product path.

### Environment Variables
Environment variables work as you would expect. So you can use e.g. the
`RPM_BUILD_OPTIONS` variable:
```yaml
- uses: cnangel/build-rpm-action@v1
  env:
    RPM_BUILD_OPTIONS: nodebuginfo
```

## Motivation
There are other GitHub actions that wrap `rpmbuild`. At the time of
writing, all of them had one or multiple limitations:
 * Hard-coding too specific options,
 * hard-coding one specific distribution as build environment,
 * installing unnecessary packages as build dependencies,
 * or expecting only exactly one .rpm file.

This action’s goal is to not have any of these limitations.
