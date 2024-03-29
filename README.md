# SOPRO Project
As it is mentioned in [SOPRO](http://sopro.web.ua.pt/project) website:
> particles have major impacts on climate and are the most serious air pollution health risk, having been classified as carcinogens. While stringent policies have led to ample reductions in particle exhaust emissions, currently traffic non-exhaust emissions, together with cooking, are unabated. `SOPRO` seeks to develop hitherto unavailable Luso-Brazilian chemical and toxicological emission profiles for major urban sources, to improve our ability to accurately apportion their contributions to pollution levels and to model air quality under different activity patterns, climate and mitigation scenarios. The results can be useful to update emission inventories, review environmental standards, support air quality plans and identify strategies to reduce pollution levels and the associated health risks.

> To accomplish with the proposed, `SOPRO` is divided into 4 Work Packages:
* Emission factors/Source profiles;
* Source apportionment and updated inventories;
* Toxicology;
* Chemical transport modelling.

> `SOPRO` outcomes will help us achieve better communication with stakeholders from relevant sectors in a media-driven society. The results can be used for updating emission inventories, reviewing environmental standards, support air quality plans and policies and identifying regional abatement measures to reduce PM-related air pollution and the associated health risks. In addition, through the longstanding involvement of some partners in the IPCC process and other international assessments, `SOPRO` will ensure that results will have impact beyond Europe, which is essential in the climate policy arena.

> `SOPRO` (Chemical and toxicological **SO**urce **PRO**filing of particulate matter in urban air) is a joint proposal of the University of Aveiro/CESAM and the University of São Paulo, but has the support of various centres of excellence from different countries, generating a transcontinental and multidisciplinary initiative.
The `SOPRO` project aims to:
* Provide scientific support on the peculiarities of Portuguese and Brazilian urban areas causing the PM2.5/PM10 target values to be widely surpassed, accurately determine source contributions, and identify those responsible for the exceedances;
* Link physico-chemical properties of emissions to health risks;
* Propose source-oriented mitigation strategies.

As part the `SOPRO` project, we are going to analyze through the WRF-CMAQ model the atmospheric chemical transport of particles and its secondary formation. Also, a source profiles will be analyzed (speciation), including cooking as a source.

## Preliminar work to propose a PhD project to the IAG (USP)
The tasks are describing as following:

- [ ] Run the WRF model for Portugal
   - [x] Review the article *[Modelling air quality levels of regulated metals: limitations and challenges](https://link.springer.com/article/10.1007/s11356-020-09645-9)* to obtain coordinates for WRF and details to reproduce the experiment.
   - [x] Use of NCEP GDAS/FNL 0.25 Degree Global Tropospheric Analyses and Forecast Grids [ds083.3](https://rda.ucar.edu/datasets/ds083.3/)
   - [x] Geogrid model configuration
   - [x] Cam-Chem as chemical IC/BC
   - [X] Biomass burning from FINN
   - [x] Anthropogenic emissions from EDGARv5 (2015)
   - [x] MOZCART mechanism (aerosol + gases)
   - [ ] EDGARv6
   - [ ] Europe model as chemical IC/BC

Porto
<img width="486" alt="image" src="https://user-images.githubusercontent.com/52834007/166975364-d3896803-b309-456e-9867-cc3c00b0914d.png">


Lisboa
<img width="484" alt="image" src="https://user-images.githubusercontent.com/52834007/166976566-e0980b7e-9503-4774-a8fa-eee184fc679e.png">

   - [x] ERA Interim
      - [x] Explore these websites: [Conor](https://conorsweeneyucd.blogspot.com/2015/01/download-era-interim-data.html), [dreambooker](https://dreambooker.site/2018/04/20/Initializing-the-WRF-model-with-ERA5/) about how download and automatize this process for initializing WRF-ARW.
      - [x] Explore [ERA Interim](https://rda.ucar.edu/datasets/ds627.0/) as meteorological initial and boundary conditions at 6 h and 0.75º temporal and spatial resolution, respectively.
      - [x] Download ERA Interim and run the WRF-ARW.
   - [ ] Sep - Dec 2017. Resolution of 3 km, according to the agrreement in the meeting.
      - [x] NCEP GDAS/FNL 0.25 degree
      - [x] Era Interim
   - [ ] Sep - Dec 2017. Resolution of 1 km, according to the agrreement in the meeting.
      - [ ] NCEP GDAS/FNL 0.25 degree
   - [ ] Evaluate the meteorological simulations for Portugal against the observations for three or more meteorological stations using Python.
      - [x] NCEP GDAS/FNL 0.25 degree
      - [x] Era Interim 
- [x] Review meteorological observations inside the modeling domain area.
- [x] Write a Thesis Proposal for the PhD. This proposal will useful to be admitted to the IAG (USP) as part of the program of PhD studies.
  - [x] Review articles about aerosol speciation, sources, CMAQ, urban issues about air quality risk over human health.
  - [x] Write a justification and motivation.
  - [x] Objectives for the PhD research.
  - [x] Methodology
  - [x] Schedule for the PhD research.
- [ ] CMAQ
  - [ ] Introduction of CMAQ. Review tutorial videos in YouTube of **[`NQualiAr`](https://www.youtube.com/channel/UCIc6KMeWteIZ55VIMiQI-5w)**.
  - [ ] Review guidelines about model install and running. After that, review articles about CMAQ for aerosols for urban areas.
  - [x] Modeling practice with CMAQ. Use a tutorial as an example to run CMAQ.
  - [ ] Run CMAQ for Portugal and for the modeling domain of interest for the SOPRO Project, using WRF simulations. Evaluate results about aerosol formation and source profiles.

My email is <aperalta@usp.br> if you want to get in touch.
