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

`S14` and `chroma` use the same DCR estimation - based upon 
formulae given by Allens Astrophysical Quantities (Cox et al. 2001), including effects
due to `pressure`, `temperature`, and the partial pressure of water vapor: `H2O_pressure`.
For `chroma`, default values for `pressure`, `temperature`, and `H2O_pressure` are taken 
from LSST PhoSim defaults. Defaults from `S14` are roughly the same but differed 
slightly due to pressure conversion factors. After those effects are corrected,
`S14` and `chroma` give the same DCR estimates (including integration over a test
stellar SED).

The `palpy` library estimates DCR differently than `chroma`
or `S14`. Thus at high zd, the estimates from `palpy` are 
significantly different. `palpy.refro()` estimates are based upon:
```
- The routine computes the refraction for zenith distances up
*     to and a little beyond 90 deg using the method of Hohenkerk
*     and Sinclair (NAO Technical Notes 59 and 63, subsequently adopted
*     in the Explanatory Supplement, 1992 edition - see section 3.281).
```
This reference is [here](http://astro.ukho.gov.uk/data/tn/naotn63.pdf) and
probably is worth reading!!! Other relevant notes are 
[here](https://github.com/Starlink/pal/blob/master/palRefro.c).

Which function should we use? This is to be explored now.

Note there are also significant (up to 10'') differences in total diffraction
(up to 0.3'' in differential chromatic diffraction) depending on if we use the 
default LSST `Site` parameters vs. the defaults used in the `S14` code! 
This amounts to altitude, temp., pressure, others.

*Update:* I am not sure which model phoSim uses. I found the part of their code
where they seem to do atmospheric refraction, and there is a function that 
does what `chroma` and `S14` do. In `raytrace/photonmanipulate.cpp`. So it may
actually just be a difference in atmospheric parameters used...
```
int Image::atmosphericDispersion (Vector *angle) {
    double dx, dy, adcx = 0.0, adcy = 0.0;

    if (atmosphericdispcenter) {
        dx = zenith*sin(shiftedAngle);
        dy = zenith*cos(shiftedAngle);
        adcx = tan(sqrt(dx*dx + dy*dy))*dx/sqrt(dx*dx + dy*dy)*air.air_refraction_adc/1e6;
        adcy = tan(sqrt(dx*dx + dy*dy))*dy/sqrt(dx*dx + dy*dy)*air.air_refraction_adc/1e6;
        if (zenith==0.0) {
            adcx = 0.0;
            adcy = 0.0;
        }
    }
    if (atmospheric_dispersion) {
        dx = -angle->x + zenith*sin(shiftedAngle);
        dy = -angle->y + zenith*cos(shiftedAngle);
        angle->x = angle->x + tan(sqrt(dx*dx + dy*dy))*dx/sqrt(dx*dx + dy*dy)*airRefraction/1e6;
        angle->y = angle->y + tan(sqrt(dx*dx + dy*dy))*dy/sqrt(dx*dx + dy*dy)*airRefraction/1e6;
        if (atmosphericdispcenter) {
            angle->x = angle->x - adcx;
            angle->y = angle->y - adcy;
        }
        angle->z = smallAnglePupilNormalize(angle->x,angle->y);
    }
    return(0);

}
```
where `air_refraction_adc` is computed as follows (in `raytrace/atmospheresetup.cpp`):
```
   air.air_refraction_adc=64.328+29498.1/(146-1/central_wavelength/central_wavelength)+255.4/(41 -1/central_wavelength/central_wavelength);
    air.air_refraction_adc=air.air_refraction_adc*pressure*(1+(1.049-0.0157*temperature)*1e -6*pressure)/720.883/(1+0.003661*temperature);
    air.air_refraction_adc=air.air_refraction_adc-((0.0624-0.000680/central_wavelength/central_wavelength)/(1+0.003661*temperature)*water_pressure);
```
and there is also (in `raytrace/photonmanipulate.cpp`):
```
double Image::airIndexRefraction() {
    double airRefraction = 64.328 + 29498.1/(146-1/wavelength/wavelength) + 255.4/(41-1/wavelength/wavelength);
    airRefraction = airRefraction*pressure*(1 + (1.049-0.0157*temperature)*1e-6*pressure)/720.883/(1 + 0.003661*temperature);
    airRefraction = airRefraction - ((0.0624-0.000680/wavelength/wavelength)/(1 + 0.003661*temperature)*water_pressure);
    if (airrefraction) return(airRefraction); else return(0.0);
}
```
