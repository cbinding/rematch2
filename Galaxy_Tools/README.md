# Galaxy Tool Wrappers

In an attempt to foster re-use and to make the tools in this repository more widely available we have produced a number of Galaxy tool wrappers that make available specific configurations of `rematch2`

The idea for each tool is to produce a minimal, self-contained directory that could be installed into any Galaxy instance. To do this the directories contain the Galaxy specific files and symlink in the original files from the root of the repository. Note this works fine on Linux but has not been checked on macOS or Windows.

## ATRIUM_T4_1_2_IE

As the name implies this tool uses `rematch2` to implement the IE step of the task 4.1.2 workflow from the ATRIUM project. See the [README](./ATRIUM_T4_1_2_IE/README.md) for more details.