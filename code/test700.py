def chromatic_biases_700():
    zeniths = [10, 20, 30, 40, 50]
    waves = np.arange(300, 1101, 1, dtype=np.float64)

    fig = plt.figure(figsize=(8,5))
    #ax = fig.add_subplot(111)
    ax = fig.add_axes([0.14, 0.13, 0.76, 0.78])
    ax.set_xlabel('Wavelength (nm)', fontsize=18)
    ax.set_xlim(300, 1200)
    ax.set_ylabel('Relative refraction (arcsec)', fontsize=18)
    ax.set_ylim(-0.5, 1.)

    for zenith in zeniths:
        # chroma expects angles in radians, so need to convert deg to radians
        refrac_angle = dcr.get_refraction(waves, zenith * np.pi/180)
        refrac_ref = refrac_angle[np.argmin(abs(waves - 700))]
        # chroma output is also in radians, so convert to arcsec here
        ax.plot(waves, (refrac_angle - refrac_ref) * 206265, label=str(zenith)+' deg')

    # 350nm wide Euclid filter.
    # ax.fill_between([0., 550., 550., 900., 900., 1200.], [-1, -1, 0.25, 0.25, -1, -1], -1,
    #                 color='black', alpha=0.15)

    colors = ['purple', 'blue', 'green', 'gold', 'magenta', 'red']
    for i, filter_ in enumerate('ugrizy'):
        # filters are stored in two columns: wavelength (nm), and throughput
        fdata = spec.Bandpass(datadir+'filters/LSST_{}.dat'.format(filter_))
        fwave, throughput = fdata.wave_list, fdata(fdata.wave_list)
        ax.fill_between(fwave, throughput * 2.0 - 0.5, -0.5, color=colors[i], alpha=0.3)
    # Add in lambda^(-2/5) for chromatic seeing comparison integrand comparison
    ax2 = ax.twinx()
    ys = (waves/700.0)**(-2./5)
    ax2.plot(waves, ys, 'k', lw=3, label='$\lambda^{-2/5}$')
    ax.legend(fontsize=11, title='zenith angle')
    ax2.legend(fontsize=11, title='chromatic seeing', loc='upper right', bbox_to_anchor = (0.78, 1))
    ax2.set_xlim(300, 1100)
    ax2.set_ylim(0.8, 1.4)
    ax2.set_ylabel('Relative $r^2_\mathrm{PSF}$', fontsize=18)

    ax.text(350.0, -0.4, 'u', fontsize=18)
    ax.text(460.0, -0.4, 'g', fontsize=18)
    ax.text(618.0, -0.4, 'r', fontsize=18)
    ax.text(750.0, -0.4, 'i', fontsize=18)
    ax.text(867.0, -0.4, 'z', fontsize=18)
    ax.text(967.0, -0.4, 'y', fontsize=18)

    for label in ax.get_xticklabels():
        label.set_fontsize(18)
    for label in ax.get_yticklabels():
        label.set_fontsize(18)
    for label in ax2.get_yticklabels():
        label.set_fontsize(18)

    if not os.path.isdir('output/'):
        os.mkdir('output/')
    fig.savefig('output/chromatic_biases_700.png', dpi=220)
    fig.savefig('output/chromatic_biases_700.pdf')
    #return fig
    
chromatic_biases_700()
