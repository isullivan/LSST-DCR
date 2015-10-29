# Experimental notebooks exploring computation of DCR using SEDs #

Tests of code from

1. [chroma](http://darkenergysciencecollaboration.github.io/chroma/) by J. Meyers and
2. [LSST W14 and S14](https://github.com/lsst-dm/S14DCR) reports by A.C. Becker.
3. [palpy](https://github.com/Starlink/pal/blob/master/palRefro.c) which is used by the simulations.

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

5. `s14_test4`: attempt to recapitulate results from `chroma_test4`
   but using the LSST `sims_photUtils` codebase, including their `Sed`
   and `Bandpass`. Much of this code is modelled off of the W14 code
   listed above.
   
6. `sims_coordUtils_test`: apparently the simulations use the `palpy` 
   library to project objects through the atmosphere. This is different
   than estimating DCR given an observed location, but `palpy` has a
   function for doing that too. This notebook explores DCR predictions
   using `palpy` and compares them to `s14_test4` and `chroma_test4`.

Summary of results so far:
--------------------------

After fixing differences in bandpasses and slight differences in default
values of temperature, humidity and pressure, the `S14` and `chroma` 
DCR estimates for the stellar SED basically agree (to within $$10^{-5}$$ 
arcsec, or so - at a zd of 70 deg.).

The estimates from `S14` are significantly faster (about 15x), so now that we 
have them in agreement, we'll continue on, using the `S14` methods.

The `palpy` library estimates DCR differently than `chroma`
or `S14` (which do it the same way and get the same results). Thus
at high zd, the estimates from `palpy` are significantly different.
Which function should we use. This is to be explored now.

