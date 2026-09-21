# EPOS workshop tutorial

**[dasdae.github.io/epos_2026](https://dasdae.github.io/epos_2026/)** -- the rendered site, with the slides and this page.

Data and code for the EPOS 2026 workshop (based on the [Galileo_2026](https://github.com/dasdae/galileo_2026) material).

- The [intro slides](https://dasdae.github.io/epos_2026/intro.html) set the session up
- the [conclusion slides](https://dasdae.github.io/epos_2026/conclusions.html) close it.

# Learning objectives

1. **`Patch` and `Spool`** -- Manage and visualize data sources, perform simple processing. 
2. **`Inventory`** -- Manage deployment metadata and integrate it into processing. 

# Contents

We will primarily cover 2 notebooks that explain DASCore using a real research dataset.

| Notebook | Topic | molab |
| --- | --- | --- |
| `01_patch_and_spool.py` | The `Patch`: filtering, transforms and plots | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/DASDAE/epos_2026/blob/main/01_patch_and_spool.py) |
| `02_the_inventory.py` | The observing system, with `Inventory` | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/DASDAE/epos_2026/blob/main/02_the_inventory.py) |

# Background

The data comes from an underground hardrock mine in Europe, where two types of sensing cable are grouted into 14 boreholes above the planned extraction volume, to watch how the rockmass holds up as extraction proceeds. See the [borehole geometry](epos_2026/data/docs/geometry.html) and the [optical paths](epos_2026/data/docs/optical_topo.pdf).

Four kinds of fiber data ship with it, along with the metadata that describes them: DSS from a Febus G1 BOTDR, low frequency and 2 kHz DAS from a Sintela Onyx Peta (the interrogator samples at 20 kHz, but everything it writes out is decimated), and OTDR traces from a Tempo Communications OFL100. Later notebooks study a mine blast that went off at **2026-08-06T10:13:27** UTC.

# Setup

The notebooks are [marimo](https://marimo.io) notebooks: plain python files that name their own dependencies, so there is no environment to build by hand. You will need **python 3.12 or newer**, and familiarity with numpy, pandas and matplotlib.

# License

Code is MIT, data is CC BY 4.0. See [LICENSING.md](LICENSING.md).

# AI usage

Claude Code and Codex were used to help prepare and edit this material.
