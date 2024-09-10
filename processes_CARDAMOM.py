def compile_CARDAMOM(dircardamom):
    import subprocess
    exitcode_forward = subprocess.run(["gcc",
                                  "-std=c99",
                                   dircardamom + "C/projects/CARDAMOM_GENERAL/CARDAMOM_RUN_MODEL.c",
                                   "-o",
                                   dircardamom + "C/projects/CARDAMOM_GENERAL/CARDAMOM_RUN_MODEL.exe",
                                   "-lm"])

    exitcode_assim = subprocess.run(["gcc",
                                 "-std=c99",
                                 dircardamom + "C/projects/CARDAMOM_MDF/CARDAMOM_MDF.c",
                                 "-o",
                                 dircardamom + "C/projects/CARDAMOM_MDF/CARDAMOM_MDF.exe",
                                 "-lm"])

# As long as the exit code == 0, you now have a compiled version of CARDAMOM ready to run.
    print("The exit code was: %d" % exitcode_forward.returncode)
    return print("The exit code was: %d" % exitcode_assim.returncode)

def run_CARDAMOM(dircardamom, cardamom_cbf, cardamom_cbr, number_iterations = "10000000"):
    import subprocess
    executable_assim = dircardamom + "C/projects/CARDAMOM_MDF/CARDAMOM_MDF.exe"
    printrate = "0" #
    samplerate = "1000" # Number of output parameters = number_iterations/samplerate, generally use between 500 and 1000 output parameters
    minimum_step_size = ".001" # Relates to MCMC, standard is currently .001
    mcmcid = "119" # Current default MCMC method is 119
    nadapt = "1000" # MCMC setting, standard is 1000

# Run assimilation
    cmdline_submit_assim = [executable_assim,
                        cardamom_cbf,
                        cardamom_cbr,
                        number_iterations,
                        printrate,
                        samplerate,
                        minimum_step_size,
                        mcmcid,
                        nadapt]


    exitcode_assim = subprocess.run(cmdline_submit_assim)
    return print("The exit code was: %d" % exitcode_assim.returncode)


def forward_run(dircardamom, dir_output, dir_cbr, cardamom_cbf, cardamom_cbr, chain ):
    import subprocess
    import readwritebinary as rwbin

    executable_forward = dircardamom + "C/projects/CARDAMOM_GENERAL/CARDAMOM_RUN_MODEL.exe"

    name = cardamom_cbr.split(dir_cbr,1)[1].split('.cbr',1)[0]
    basename = name[0:6]
    locpoint = name[6:]
    chain_number = chain
    cardamom_output_flux = "{}_{}_{}_{}_{}.{}".format(dir_output,'fluxfile',basename,locpoint,chain_number, "bin")
    cardamom_output_pool = "{}_{}_{}_{}_{}.{}".format(dir_output,'poolfile',basename,locpoint,chain_number, "bin")
    cardamom_output_edcd = "{}_{}_{}_{}_{}.{}".format(dir_output,'edcdfile',basename,locpoint,chain_number, "bin")
    cardamom_output_prob = "{}_{}_{}_{}_{}.{}".format(dir_output,'probfile',basename,locpoint,chain_number, "bin")


    cmdline_submit_forward = [executable_forward,
                          cardamom_cbf,
                          cardamom_cbr,
                          cardamom_output_flux,
                          cardamom_output_pool,
                          cardamom_output_edcd,
                          cardamom_output_prob]


    exitcode_forward = subprocess.run(cmdline_submit_forward)
    print("The exit code was: %d" % exitcode_forward.returncode)

    CBR = rwbin.CARDAMOM_READ_OUTPUT(cardamom_cbf,cardamom_cbr,cardamom_output_flux, cardamom_output_pool)
    #print(type(CBR))
    return CBR

def forward_run2(dircardamom, dir_output, dir_cbr, cardamom_cbf, cardamom_cbr, chain ):
    import subprocess
    import readwritebinary as rwbin
    import netCDF4
    executable_forward = dircardamom + "C/projects/CARDAMOM_GENERAL/CARDAMOM_RUN_MODEL.exe"

    name = cardamom_cbr.split(dir_cbr,1)[1].split('.cbr',1)[0]
    basename = name[0:6]
    locpoint = name[6:]
    chain_number = chain
    cardamom_output_flux = "{}_{}_{}_{}_{}.{}".format(dir_output,'outputfile',basename,locpoint,chain_number, "nc")


    cmdline_submit_forward = [executable_forward,
                          cardamom_cbf,
                          cardamom_cbr,
                          cardamom_output_flux]


    exitcode_forward = subprocess.run(cmdline_submit_forward)
    print("The exit code was: %d" % exitcode_forward.returncode)

    CBR = netCDF4.Dataset(cardamom_output_flux)
    #print(type(CBR))
    return CBR










def compile_CARDAMOM_2(dircardamom):
    import subprocess
    exitcode_forward = subprocess.run(["gcc",   "-std=c99","-L/usr/local/Cellar/netcdf/4.8.0_1/lib","-lnetcdf",
                                   dircardamom + "C/projects/CARDAMOM_GENERAL/CARDAMOM_RUN_MODEL.c",
                                   "-o",
                                   dircardamom + "C/projects/CARDAMOM_GENERAL/CARDAMOM_RUN_MODEL.exe",
                                   "-lm"])

    exitcode_assim = subprocess.run(["gcc",
                                 "-std=c99","-L/usr/local/Cellar/netcdf/4.8.0_1/lib","-lnetcdf",
                                 dircardamom + "C/projects/CARDAMOM_MDF/CARDAMOM_MDF.c",
                                 "-o",
                                 dircardamom + "C/projects/CARDAMOM_MDF/CARDAMOM_MDF.exe",
                                 "-lm"])


    # As long as the exit code == 0, you now have a compiled version of CARDAMOM ready to run.
    print("The exit code was: %d" % exitcode_forward.returncode)
    return print("The exit code was: %d" % exitcode_assim.returncode)


def run_CARDAMOM_2(dircardamom, cardamom_cbf, cardamom_cbr, number_iterations = "10000000"):
    import subprocess
    executable_assim = dircardamom + "C/projects/CARDAMOM_MDF/CARDAMOM_MDF.exe"
    printrate = "0" #
    samplerate = "1000" # Number of output parameters = number_iterations/samplerate, generally use between 500 and 1000 output parameters
    minimum_step_size = ".001" # Relates to MCMC, standard is currently .001
    mcmcid = "119" # Current default MCMC method is 119
    nadapt = "1000" # MCMC setting, standard is 1000

# Run assimilation
    cmdline_submit_assim = [executable_assim,
                        cardamom_cbf,
                        cardamom_cbr,
                        number_iterations,
                        printrate,
                        samplerate,
                        minimum_step_size,
                        mcmcid,
                        nadapt]


    exitcode_assim = subprocess.run(cmdline_submit_assim)
    return print("The exit code was: %d" % exitcode_assim.returncode)
