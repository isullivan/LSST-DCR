# Summary of References on DCR #

1. Filippenko (1982).
    * Seminal paper on atmospheric DCR on spectrophotometry
    * Uses the refractive index of dry air from (Edlén 1953;
      Coleman, Bozman, and Meggers 1960). Corrects for ambient temperature and
      atmospheric pressure using (Barrell 1951).

2. C.Y. Hohenkerk and A.T. Sinclair, The Computation of Angular
   Atmospheric Refraction at Large Zenith Angles.
    * Good background.
    * Uses a different implementation, "the method recommended by Auer
      and Standish".
    * This is the function implemented in `pypal` which is used by
      some (but not all?) code in the `sims` stack.
    * Uses a model atmosphere with temperature and pressure gradients,
      integrated to the surface.  This I believe is different from
      (1.) which assumes a single refractive surface.

1. [Report on Summer 2014 Production: Analysis of DCR (Andy Becker)](https://github.com/lsst-dm/S14DCR/blob/master/report/S14report_V0-00.pdf)

    * Estimated DCR effects directly for LSST using catSim's stellar
	  SEDs.
    * Appears to use the formulae given in Filippenko (1982) for DCR estimation.
    * Investigated only airmass effects (no temperature,
	  etc. dependence).
    * Utilized 5 mas threshold for "good" DCR corrections based on
      estimated accuracy required for difference imaging (no dipoles).
    * Summmary of DCR estimates:
        - For *g* and *r*, nearly all stars will exhibit differential DCR
	      of > 5 mas at parallactic angle differences > 20 deg. or airmass
	      differences of > 0.15.
	    - For *i*, similar effects for parallactic angle differences > 25
	      deg. or airmass differences > 0.2, mostly for M-dwarf stars.
	    - For *z*, only very large differences in parallactic angle or
          airmass lead to DCR > 5 mas.
	* DCR corrections tested based on modeling using colors and airmass
      terms.
	    - Random forest regression models provided most accurate
          modeling of DCR and refraction.
		- *u* and *g* models worked but would be degraded by 10% color
          errors (*u*) or 2.5% color errors (*g*).
		- *riz* models could correct all but 10<sup>-5</sup> stars to
          < 5 mas residuals.
	* **Recommendations**:
	    - Code from the
		  [S14DCR analysis](https://github.com/lsst-dm/S14DCR) should
		  be updated to use latest version of sims_photUtils and
		  include estimates for galaxies and SNe.
 		- Potentially merge capabilities of SED and Bandpass in
          sims_photUtils with those from
          [chroma](https://github.com/DarkEnergyScienceCollaboration/chroma/);
          see below.
		- Incorporate DCR calcs into sims pipeline to enable effects
          of DCR corrections on image coadds and differences (see also
          [W14ImageDifferencing](https://github.com/lsst-dm/W14ImageDifferencing)).

2. Meyers and Burchat (2015).

    * Estimates of DCR on weak lensing measurements.
    * Uses the formulae given in Filippenko (1982) for DCR estimation. 
	* Source code for analysis is [available](https://github.com/DarkEnergyScienceCollaboration/chroma/).
	* Primarily measured effects of DCR on shape measurements (2nd
      moments); code can be used to estimate 1st moments for a given
      SED. [Preliminary code](https://github.com/isullivan/LSST-DCR/tree/master/code/notebooks).
    * Investigated means for correction/mitigation/prediction based on
      colors using Extra Trees Regression (ETR, claimed to be better than
      Random Forests regression which is what the `S14` report (above)
      used).
    * Estimation is that the DCR offset is not a problem, but only
      shown (in figures) for *ri* bands. ETR improves this prediction.

3. Chambers (2007).

    * Updated summary of (more accurate?) astrometric transformations
      including DCR.
    * Estimated astrometric accuracy in Pann-STARRS of 1 mas. This
      assumes accurate atmospheric characterization for each field
      from sky probes (atmospheric absorption).
	* **Recommendations**:
      - Understand these transformations. Suggestion is that C code
        exits somewhere in the Pan-STARRS codebase, but I could not
        find it.
