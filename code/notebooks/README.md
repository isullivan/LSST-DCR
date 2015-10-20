# Experimental notebooks exploring computation of DCR using SEDs #

Tests of code from

1. [chroma](http://darkenergysciencecollaboration.github.io/chroma/) by J. Meyers and
2. [LSST W14 and S14](https://github.com/lsst-dm/S14DCR) reports by A.C. Becker.

Task: compute DCR given:

* an SED
* a bandpass/filter
* zenith distance

`chroma` has self-contained `spec` package containing `Sed` and
`Bandpass` with functions for computing DCR (1st and 2nd moments) for
a given SED. Code seems modelled off of LSST `sims_photUtils` `Sed`
and `Bandpass`.

Notebook index and summary:
---------------------------

1. `chroma_test`: recapitulate Figures 1. and 2. from the Meyers and
   Burchat paper.

2. `chroma_test2`: tweaks of code from `chroma_test` to use the SN
   spectrum that was included in the `chroma` package. Note I am not
   sure exactly what or from where this spectrum comes from.

3. `chroma_test3`: tweaks from `chroma_test2` to compute the temporal
   evolution of DCR as a function of SN epoch, again using the
   ambiguously sourced SN spectrum from the `chroma` package.

4. `chroma_test4`: attempt to compute DCR from a stellar SED and LSST
   bandpass in the LSST `sims_sed_library`, but using `chroma`.

5. `chroma_test5`: attempt to recapitulate results from `chroma_test4`
   but using the LSST `sims_photUtils` codebase, including their `Sed`
   and `Bandpass`. Much of this code is modelled off of the W14 code
   listed above.

Summary of results so far:
--------------------------

Although the DCR calculation functions (as a function of wavelength,
zenith distance, temperature, humidity, pressure) in (4.) and (5.) are
identical, including the default temp./hum./pressure values, the final
integration of DCR over SED * Bandpass result in large differences in
DCR estimation, particularly in *u*.

Is this a problem with the integration? Is there an issue with the use
of fnu vs. flambda? Or is it a result of `sims_photUtils` utilizes the
entire LSST throughput, and not just a bandpass profile? Or perhaps
something as simple as a spectral window/wavelength range difference.

Additional notebooks `chroma_test4-copy` and `chroma_test5-copy` test
the last theory by using a synthetic spectrum with only flux between
650-660nm. There the numbers look pretty close. So let's continue
testing...


