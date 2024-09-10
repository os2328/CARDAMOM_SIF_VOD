# CARDAMOM_SIF_VOD
Data and scripts for "Constraining respiration flux and carbon pools in a simple ecosystem carbon model"


The work uses CARDAMOM v.1 (https://github.com/CARDAMOM-framework/CARDAMOM/)

The base DALEC is DALEC 813. The new DALEC is called DALEC 895

Copy /C/projects/CARDAMOM_MODELS/DALEC/DALEC_813, and rename /C/projects/CARDAMOM_MODELS/DALEC/DALEC_895

Model parameters modification:
open MODEL_INFO_895.c, Line 18: 
DALECmodel.nopars=36;

Add parameters so called “long names” and min max values in PARS_INFO_.c 

/*SIF linear coefficient*/
CARDADATA->parmin[33]=0.01; 
CARDADATA->parmax[33]=0.15; 

/*VOD wood linear coefficient a*/
CARDADATA->parmin[34]=0.000001; 
CARDADATA->parmax[34]=0.0008; 
    
/*VOD leaves linear coefficient b*/
CARDADATA->parmin[35]=0.0001; 
CARDADATA->parmax[35]=0.01; 

And in readwritebinary.py
  PARS = read_cbr_file(inputfilename_cbr,INFO = {'nopars':36,'latterhalf':0})


Note: This file contains all the parameters used by this DALEC. Order is important – the parameters are referenced in many other files by their index. The name is used too. As soon as new parameters are created, this change should be reflected in library_cbr.py: in a dictionary of Long to short names to units there, “short names” and units should be added. 

             'SIF linear coefficient':('sif_c', 'SIFunits/GPPunits'),
             'VOD wood linear coefficient a':('vod_a', 'vod/biomass'),
             'VOD leaves linear coefficient b':('vod_b', 'vod/biomass'),


Add all the necessary variable’s quantities to /C/projects/CARDAMOM_GENERAL/CARDAMOM_DATA_STRUCTURE.c (e.g. follow “GPP” entry as example)

		double *SIF; /*observations themselves*/ 
		int *sifpts;
		int nsif; /* Number of non-empty points in observation*/
		double *M_SIF; /*SIF values CALCULATED BY THE MODEL*/
		double sif_annual_unc; /* needed for DALEC_LIKELIHOOD_SIF.c NOT always calculated*/
		double sif_obs_unc; /* can be calculated as observations’ std  – not implemented*/
		double sif_obs_threshold; /* needed for DALEC_LIKELIHOOD_SIF.c */


Provide the information on how the new data was included in .cbf file. Add to CARDAMOM_READ_BINARY_DATA.c
This is just for printout while running

		printf("Number of SIF obs. = %d\n",CDATA->nsif);
  
Currently, uncertainty is hard coded rather than calculated. Also, not sure about statdat indexing

		DATA->sif_obs_unc=statdat[27];if (statdat[27]<0){DATA->sif_obs_unc=0.6;}

Memory allocation for the new data, calculated by the model and observed. Then freeing the space

		DATA->M_SIF=calloc(DATA->nodays,sizeof(double));
		if (DATA->SIF==0){DATA->SIF=calloc(DATA->nodays,sizeof(double));}
		if (DATA->nsif>0){DATA->sifpts=calloc(DATA->nsif,sizeof(int));} 

		if (DATA.nsif>0){free(DATA.sifpts);} 
		free(DATA.SIF);
		free(DATA.M_SIF);

Repeat for VOD

Reading and adding non-empty observations
		
  		DATA->nsif=0;
    
Then, in a loop

		if (DATA->noobs>11){DATA->SIF[n]=obsline[11];
      		if (obsline[11]>-9998){DATA->nsif=DATA->nsif+1;}}   /*this should correspond to a new field; SIF added after CH4 in write binary.m */

IMPORTANT NOTE: in DALEC 813, there was an option for CH4 and NEE and they where the observation number 11. However, they are absent in the corresponding .cbf files AND mre importantly, in obsnames in readwritebinary.py. Hence, if a new observation is added – it becomes the 11th observation. For that reason, the CH4 lines were commented in the code above. Same is true for the lines 

		if (DATA->noobs>11){c=0;for (n=0;n<DATA->nodays;n++){if (DATA->SIF[n]>-9998){DATA->sifpts[c]=n;c=c+1;}}} 

Data initialization 

		CDATA->SIF=0; 

Changing the actual model.

Changing the model means adding to the DALEC_895.c.  In my case, inside the last loop,

		double *SIF=DATA.M_SIF;

    		/*SIF model*/
    		SIF[n] = FLUXES[f+0]*pars[33];

		/*VOD */
		double c = 0.0;
		VOD[n]=  pars[34]*POOLS[p+3] + pars[35]*POOLS[p+1]+c;

Pars[33], [34], and [35] correspond to the newly defined model parameters from step 2 (as mentioned, the order is important, the parameters are called by their indices in the code). 


Adding new cost function. 

In this new model, a new observation is included for DA. Hence, a new cost function is needed. In my case, the new cost function is DALEC_LIKELIHOOD_SIF.c and DALEC_LIKELIHOOD_VOD.c  in /C/projects/DALEC_CODE/MODEL_LIKELIHOOD_FUNCTIONS/
and add to all likelihoods
  
	#include "DALEC_LIKELIHOOD_SIF.c"
	#include "DALEC_LIKELIHOOD_VOD.c"

The cost function basically repeats NEE function, though decoupling seasonal from interannual variations is not implemented. 

		for (n=0;n<D.nsif;n++){dn=D.sifpts[n];tot_exp+=pow((D.M_SIF[dn]-D.SIF[dn])/sif_obs_unc,2);}
		P=P-0.5*tot_exp;
		return P;

Same is repeated for VOD: 

		for (n=0;n<D.nvod;n++){dn=D.vodpts[n];tot_exp+=pow((D.M_VOD[dn]-D.VOD[dn])/vod_obs_unc,2);}
		P=P-0.5*tot_exp;
		return P;

Then, in DALEC_ALL_LIKELIHOOD.c

	if (D.ID==895){
	P=P+DALEC_LIKELIHOOD_SIF(D);//
	P=P+DALEC_LIKELIHOOD_VOD(D);//
 	}


Changes made to readwritebinary.py and CARDAMOM_WRITE_BINARY_FILEFORMAT.m files. 
Adding new SIF and VOD observation (everywhere in the file where obsnames are mentioned)

	obsnames=['GPP','LAI','NBE','ABGB','ET','EWT','BAND1','BAND2','BAND3','BAND4','SOM', 'SIF', 'VOD']   

