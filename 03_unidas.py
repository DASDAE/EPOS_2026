# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "epos-2026 @ git+https://github.com/DASDAE/epos_2026@main",
#     "dascore @ git+https://github.com/DASDAE/dascore@dev",
#     "marimo>=0.24",
#     "matplotlib>=3.10",
#     "numba",
#     "unidas>=0.1.6",
#     "xdas>=0.2.9",
#     "daspy-toolbox>=1.2.7",
# ]
# ///
import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Moving between DAS libraries with UniDAS

    [UniDAS](https://github.com/DASDAE/unidas) converts between the data structures used by DAS libraries. Start with a small DASCore example patch, convert it to Xdas and DASPy, then bring it back.
    """)
    return


@app.cell
def _():
    import dascore as dc
    import unidas

    return dc, unidas


@app.cell
def _(dc):
    patch = dc.get_example_patch()
    patch
    return (patch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Xdas

    Pass the target class name to `unidas.convert`. Xdas uses a `DataArray`.
    """)
    return


@app.cell
def _(patch, unidas):
    xdas_array = unidas.convert(patch, to="xdas.DataArray")
    xdas_array
    return (xdas_array,)


@app.cell
def _(unidas, xdas_array):
    # Convert back to a DASCore Patch.
    patch_from_xdas = unidas.convert(xdas_array, to="dascore.Patch")
    patch_from_xdas
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## DASPy

    The same call gives us a DASPy `Section`. Its time and distance coordinates must be evenly sampled, with an absolute start time, as in this example.
    """)
    return


@app.cell
def _(patch, unidas):
    section = unidas.convert(patch, to="daspy.Section")
    section
    return (section,)


@app.cell
def _(section, unidas):
    patch_from_daspy = unidas.convert(section, to="dascore.Patch")
    patch_from_daspy
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The conversion changes the container so you can use another library's methods. Check the metadata you need when moving between libraries; they do not all represent it in the same way.
    """)
    return


if __name__ == "__main__":
    app.run()
