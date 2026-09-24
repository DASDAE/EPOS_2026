# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "epos-2026 @ git+https://github.com/DASDAE/epos_2026@main",
#     "dascore @ git+https://github.com/DASDAE/dascore@dev",
#     "marimo>=0.24",
#     "matplotlib>=3.10",
#     "numba",
#     "unidas>=0.1.2",
#     "xdas>=0.2.9",
#     "daspy-toolbox>=1.2.7",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Managing and Visualizing Data Archives

    This notebook provides a gentle introduction to DASCore's `Patch` and `Spool` objects for managing data archives.

    /// note | Important Note
    The DASCore version used here is from the development branch. It will probably be released towards the end of 2026.

    To install it outside of this notebook:

    ```bash
    pip install git+github.com/dasdae/dascore::dev
    ```
    ///
    """)
    return


@app.cell
def _():
    import dascore as dc
    import matplotlib.pyplot as plt
    import numpy as np

    from epos_2026 import get_data_path

    # Define optical distances for boreholes of interest on DAS recording.
    borehole_distances = {
        "N180": (1577.9, 1634.7),
        "N160": (1486.0, 1544.4),
        "N140": (1399.0, 1459.4),
        "N120": (1306.0, 1365.0),
        "N100": (1216.3, 1274.2),
    }

    # Zoomed in times around the blast
    blast_time_zoom_0 = ("2026-08-06T10:13:26.5", "2026-08-06T10:13:28.7")
    blast_time_zoom_1 = ("2026-08-06T10:13:26.6", "2026-08-06T10:13:27")
    blast_time_zoom_2 = ("2026-08-06T10:13:26.79", "2026-08-06T10:13:26.86")

    # Set default mpl figuresize to better suit the notebook width
    plt.rcParams["figure.figsize"] = (10, 6)  # width, height in inches


    def get_downgoing(patch, hole):
        """Trim th patch to only include downgoing leg for specific borehole."""
        _d1, _d2 = borehole_distances[hole]
        # The borehole is a U, so the fiber runs down one leg and back up the other.
        _downgoing = (_d1, (_d1 + _d2) / 2)
        return patch.select(distance=_downgoing)


    return (
        blast_time_zoom_0,
        blast_time_zoom_2,
        dc,
        get_data_path,
        get_downgoing,
        np,
        plt,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Spool
    To open a data archive we use `dascore.spool`. This will create an index of the folder contents and enable fast data access and visualizations.
    """)
    return


@app.cell
def _(get_data_path):
    # First get a path to our data directory.
    data_path = get_data_path()
    return (data_path,)


@app.cell
def _(get_data_path, mo):
    # Look at the directory structure.
    mo.ui.file_browser(initial_path=get_data_path())
    return


@app.cell
def _(data_path, dc):
    # Next create the spool and make sure it is up-to-date, and select our DAS file.
    spool = dc.spool(data_path).update()
    return (spool,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Inspecting the data archive

    Spool has several ways to help visualize its contents.
    """)
    return


@app.cell
def _(spool):
    spool  # The str/repr is helpful.
    return


@app.cell
def _(spool):
    spool.select(time=("2026-08-06T10", "2026-08-06T11")).viz.coverage()
    return


@app.cell
def _(spool):
    spool.select(tag="DSS").viz.calendar()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here we have DSS (distribued strain sensing), DAS (distributed acoustic sensing), and DAS_LF (DAS low-frequency) all managed in the same spool.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Selecting and shaping content

    We use `select` a `chunk` to control the spool contents and shapes.

    For example to get spools which select only DAS and LF_DAS data:
    """)
    return


@app.cell
def _(spool):
    das_spool = spool.select(tag="DAS")
    das_lf_spool = spool.select(tag="DAS_LF")
    return das_lf_spool, das_spool


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The DAS Spool now has one patch (data array with metdata)
    """)
    return


@app.cell
def _(das_spool):
    das_spool
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But the lf_das spool has more. To merge these arrays together, so when we eventually load them, we use `chunk`.
    """)
    return


@app.cell
def _(das_lf_spool):
    das_lf_spool
    return


@app.cell
def _(das_lf_spool):
    das_lf_spool_chunked = das_lf_spool.chunk(time=..., tolerance=10)
    return (das_lf_spool_chunked,)


@app.cell
def _(das_lf_spool_chunked):
    das_lf_spool_chunked
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Excercise 1.1**

    1) Use select to create a spool with all das-like tags.

    2) Use select to trim 2 seconds from the start and end of each patch.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Extracting Patches

    A spool is a metadata index; the `Patch` holds the data. Patches are extracted (loaded) only when you ask for them.
    """)
    return


@app.cell
def _(das_spool):
    # Get the first patch in the spool and convert from phase angle to strain.
    das_patch = (
        das_spool[0]
        .radians_to_strain()
    )
    return (das_patch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The patch is based on [xarray's](https://docs.xarray.dev/en/stable/) [data array](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html). It has several parts:

    - dims : a tuple[str] of dimension names
    - data : the array
    - coords : a dict-like container for coordinates (which label each axis)
    - attrs : a dict-like container for scalar metadata

    We can look at a patch's summary by printing it.
    """)
    return


@app.cell
def _(das_patch):
    das_patch
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The parts of the patch are accessed as follows:
    """)
    return


@app.cell
def _(das_patch):
    _dims = das_patch.dims  # tuple of dimension names

    _coords = das_patch.coords  # dict-like container for coordinates

    _attrs = das_patch.attrs  # dict-like container for attributes

    _data = das_patch.data  # Data Array
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _(spool):
    from dascore.units import seconds

    spool.select(time=(2, -2), relative=True )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plotting and Selecting
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As with all other DASCore objects, the Patch has a namespace dedicated to visualizations called `viz`. Using this we can see the blast clearly (the other line enables interactivity).
    """)
    return


@app.cell
def _(das_patch, mo):
    _ax = das_patch.viz.waterfall()
    mo.mpl.interactive(_ax.figure)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `select` is used to trim patches in either dimension.
    """)
    return


@app.cell
def _(blast_time_zoom_2, das_patch, mo):
    # Select part of time
    zoomed_in_patch = das_patch.select(time=blast_time_zoom_2)

    _ax = zoomed_in_patch.viz.waterfall()
    mo.mpl.interactive(_ax.figure)
    return


@app.cell
def _(blast_time_zoom_2, das_patch, get_downgoing, mo):
    # Select the down-going part of N180. 
    n180_das_patch = get_downgoing(das_patch, "N180")
    _ax = n180_das_patch.select(time=blast_time_zoom_2).viz.waterfall()
    mo.mpl.interactive(_ax.figure)
    return (n180_das_patch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The wiggle plot is also helpful; in this case it accentuates the post-blast offsets.
    """)
    return


@app.cell
def _(blast_time_zoom_2, mo, n180_das_patch):
    # The wiggle plot is also helpful
    _ax = n180_das_patch.select(time=blast_time_zoom_2).viz.wiggle(scale=0.5)
    mo.mpl.interactive(_ax.figure)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using the whole record and selecting the channel at the bottom of the hole, we see all the charges clearly. Notice how each charge adds its own step to the strain record, ratcheting it up charge by charge.
    """)
    return


@app.cell
def _(n180_das_patch):
    n180_das_patch.select(distance=-1, samples=True).viz.wiggle()
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Observations**

    **1) There is significant offset caused by the blast.**

    The blast might have caused permanent deformation to the ground, that is the point of blasting in a mine, but the dynamic response of the instrument could have been exceeded in these near-field recordings.


    **2) The strain dissipates post-blast**

    From second 28.25 or so, the background strain level begins to return to normal. This could indicate strain dissipation and [afterslip](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=afterslip+earthquake&btnG=), or perhaps it's something else?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Patch Processing

    Let's set aside the strain offset questions for now and focus on the charge waveforms. To do this, it will be convinient to remove the offsets.

    Let's test two approaches. The `Patch.pass_filter` is a standard Butterworth filter, and a simple time derivative.
    """)
    return


@app.cell
def _(blast_time_zoom_0, n180_das_patch):
    # Use select again to trim the patch. 
    n180_first_blast_das = n180_das_patch.select(
        time=blast_time_zoom_0  # trim distance coordiante
    )
    return (n180_first_blast_das,)


@app.cell
def _(mo, n180_first_blast_das, plt):
    # Apply the pass filter.
    n180_blast_filtered = n180_first_blast_das.pass_filter(time=(5, 200))

    # versus a temporal deriviative
    n180_blast_derivative = n180_first_blast_das.differentiate("time")


    # Setup and display both wiggle plots side by side.
    # Wiggle trace spacing depends on amplitude, so keep the y axes independent.
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 6), sharex=True)
    n180_blast_derivative.viz.wiggle(ax=_axes[0], scale=0.5)
    n180_blast_filtered.viz.wiggle(ax=_axes[1], scale=0.5)
    _axes[0].set_title("strain raite")
    _axes[1].set_title("bandpass 5 to 200 Hz")
    mo.mpl.interactive(_fig)
    return (n180_blast_derivative,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The derivative has far fewer visual artifacts. Taking the envelope and the mean along the distance axis:
    """)
    return


@app.cell
def _(n180_blast_derivative):
    das_envelope_full = n180_blast_derivative.envelope("time")
    das_envelope = das_envelope_full.mean("distance").squeeze()

    das_envelope.viz.wiggle()
    return (das_envelope,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Counting the charges

    Assuming the moveout over the array isn't large enough to smear the peaks from different charges together when stacking, averaging the envelope over the leg gives a single trace where each charge should have a peak. We can use `find_peaks` to count them.
    """)
    return


@app.cell
def _(das_envelope, dc, plt):
    from scipy.signal import find_peaks

    # Get the time array in seconds from the start of the window.
    _time_coord = das_envelope.get_array("time")
    _time = dc.to_float(_time_coord - _time_coord[0])
    _step = dc.to_float(das_envelope.get_coord("time").step)

    # We assume a peak is a charge if:
    # 1) it is at least 10% of the amplitude of the highest peak.
    # 2) it occurs at least 30 ms after the previous charge
    _peaks, _ = find_peaks(
        das_envelope.data,
        height=0.1 * das_envelope.data.max(),
        distance=int(0.03 / _step),
    )

    peak_times = _time[_peaks]
    _peak_values = das_envelope.data[_peaks]

    # plot the results
    _fig, _ax = plt.subplots(figsize=(10, 4))
    _ax.plot(_time, das_envelope.data)
    _ax.plot(peak_times, _peak_values, "rv")
    _ax.set_xlabel("seconds from window start")
    _ax.set_ylabel("mean envelope of strain rate")
    _ax.set_title(f"{len(_peaks)} peaks")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One peak on its own, then a train of them 0.6 s later, spaced 50 and 100 ms apart, is consistent with delay detonators.

    ### The spectrum

    `dft` transforms along a dimension and replaces it with a frequency coordinate, labeled `ft_{dim}` (e.g. `ft_time`). The amplitude spectrum averaged over the leg shows where the energy is, and the roll-off towards the 1 kHz Nyquist frequency is the anti-alias low-pass filter.
    """)
    return


@app.cell
def _(blast_time_zoom_0, n180_blast_derivative):
    # Get the average amplitude spectrum
    n180_spectrum = (
        n180_blast_derivative.select(time=blast_time_zoom_0)
        .dft("time", real=True)
        .abs()
        .mean("distance")
        .squeeze()
    )

    # A log axis cannot show the zero-frequency bin, so skip it explicitly.
    _nonzero = n180_spectrum.select(ft_time=(1, ...), samples=True)
    _ax = _nonzero.viz.wiggle()
    _ax.set_xscale("log")
    _ax.set_yscale("log")
    _ax
    return (n180_spectrum,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There is also a distinct frequency comb, which is more apparent when making the same plot on a linear scale.
    """)
    return


@app.cell
def _(n180_spectrum):
    # Select before plotting so the vertical scale fits this band too.
    n180_spectrum.select(ft_time=(100, 300)).viz.wiggle()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Excersise 1.2

    Why is there such a strong frequency comb? Can you show it with peak_times?
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Apparent velocity

    The blast front sweeps along the leg, so each channel records it at a slightly different time. Cross-correlating every channel against the first turns that shift into a lag we can measure, and the slope of lag against distance is one over the apparent velocity.
    """)
    return


@app.cell
def _(blast_time_zoom_2, n180_blast_derivative):
    from dascore.units import ms

    cc = (
        # Zoom in around the first charge
        n180_blast_derivative.select(time=blast_time_zoom_2)
        # taper the window we are about to transform
        .taper(time=10 * ms)
        # correlate all channels against the first channel
        .correlate(distance=0, samples=True)
        # drop the length-1 source dimension
        .squeeze()
        # Select lag times around reasonable velocities
        .select(lag_time=(-0.05, 0.05))
    )

    cc.viz.waterfall()
    return (cc,)


@app.cell
def _(cc, dc, np):
    # Get the values for the distance axis.
    distance = cc.get_array("distance")

    # Get the values for the lag times.
    _lag = dc.to_float(cc.get_array("lag_time"))

    # Find the lag time of the peak correlation for each channel.
    _peak_indices = cc.data.argmax(axis=cc.get_axis("lag_time"))
    _picks = _lag[_peak_indices]
    slope, intercept = np.polyfit(distance, _picks, 1)

    # The slope is negative: the front reaches the deep end of the leg first and
    # travels back up it, so the absolute value keeps speed and drops direction.
    print(f"apparent velocity: {abs(1 / slope):.0f} m/s")
    return distance, intercept, slope


@app.cell
def _(cc, distance, intercept, slope):
    # Plot, return the MPL axis
    _ax = cc.viz.waterfall(show=False, cmap="seismic", scale=0.3)

    # Reuse MPL axis to plot intercept
    _ = _ax.plot(
        distance, slope * distance + intercept, "--", color="0.5", lw=4
    )
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Exercise (1.3)**:

    Make a plot of the low-frequency DAS patch, starting after the last blast. Do you notice any permanent offset?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Points
    - `Spool` is used to manage archives and extract `Patch`es (arrays with metadata)
    - `Patch` has many processing/transformation methods. Often the dimension is used as the first argument or keyword.
    - `get_array`, `get_coord` and `.data` hand the result to NumPy and SciPy where DASCore stops.

    Next, `02_the_inventory.py` attaches the observing system to these patches.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
