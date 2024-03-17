* Encoding: UTF-8.
* Syntax by Rianne on 14-04-2021
* Merge Peil and HBSC for 2003 t/m 2009

add files 
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2003.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2007.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2011.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2015.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2019.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\HBSC2005.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\HBSC2009.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\HBSC2013.sav'
/file=    'C:\Users\20200059\Documents\Data\HBSC\Data\HBSC2017.sav'
/by = meting
/map.
execute.

fre meting.

save 
/outfile= 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019.sav'
/keep = all.

dataset close all.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019.sav'.

* we will process the data variable by variable
* starting with sekse

fre sekse.
recode sekse (1=0) (2=1) .
val labels sekse 0'Jongen' 1'Meisje' .
fre sekse.
crosstabs meting by sekse.

* lft

fre lft.
crosstabs meting by lft.

* schnivo

fre schnivo.
crosstabs meting by schnivo.

* leerjaar

fre leerjaar.
crosstabs meting by leerjaar.

* etngroep3

fre etngroep3.
crosstabs meting by etngroep3.

* stedgem

fre stedgem.
crosstabs meting by stedgem.

* vollgezin

fre vollgezin.
crosstabs meting by vollgezin.

* vaderbaan

fre vaderbaan.
crosstabs meting by vaderbaan.

* moederbaan

fre moederbaan.
crosstabs meting by moederbaan.

* spijbel

fre spijbel.
crosstabs meting by spijbel
/cells count.
recode spijbel (9=SYSMIS) (99=SYSMIS).
fre spijbel.
crosstabs meting by spijbel
/cells count.

*recode spijbel (1=0) (2=1) (3=2) (4=3.5) (5=5.5) (6=7) into spijbel_scale.
*crosstabs meting by spijbel_scale
*/cells=count row.

* cijferleven

fre cijferleven.
crosstabs meting by cijferleven.
recode cijferleven (99=SYSMIS).
fre cijferleven.
crosstabs meting by cijferleven.

* set variable level

variable level sekse etngroep3 vollgezin vaderbaan moederbaan (nominal).
variable level lft cijferleven (scale).
variable level schnivo leerjaar stedgem spijbel (ordinal).

save 
/outfile= 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019.sav'
/keep = all.

* alcohol variables
* first we check whether the merge of the datasets has gone well

crosstabs meting by aant_alcooit1 aant_alcooit2 aant_alc4wk1 aant_alc4wk2 aant_dronkooit1 aant_dronkooit2 aant_dronkooit3 aant_dronk4wk1 aant_dronk4wk2 aant_dronk4wk3.
dataset close all.

* compare with original files

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2003.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2007.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2011.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2015.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\Peil2019.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\HBSC2005.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

* aant_dronk4wk mist for hbsc2005

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\Data\HBSC2009.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\HBSC2013.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\HBSC2017.sav'.
fre aant_alcooit1. 
fre aant_alcooit2. 
fre aant_alc4wk1.
fre aant_alc4wk2. 
fre aant_dronkooit1. 
fre aant_dronkooit2.
fre aant_dronkooit3.
fre aant_dronk4wk1.
fre aant_dronk4wk2.
fre aant_dronk4wk3.

* freqs correct

dataset close all.

* second we check if the values for prevalence are consistent with the values for the alcohol variables

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019.sav'.

variable level aant_alcooit1 aant_alcooit2 aant_alc4wk1 aant_alc4wk2 aant_dronkooit1 aant_dronkooit2 aant_dronkooit3 aant_dronk4wk1 aant_dronk4wk2 aant_dronk4wk3 (ordinal).
fre aant_alcooit1.
recode aant_alcooit1 aant_alcooit2 aant_alc4wk1 aant_alc4wk2 aant_dronkooit1 aant_dronkooit2 aant_dronkooit3 aant_dronk4wk1 aant_dronk4wk2 aant_dronk4wk3 (99 = SYSMIS) (else=copy).
fre aant_alcooit1.

crosstabs meting by aant_alcooit1 aant_alcooit2 by lpalc.
* 103 and 155 have lpalc = 1 while alcohol use is 0/nooit

* we don't do this because the lpalc and similar measures are corrected for non-logical answers in the original datasets already
*recode aant_alcooit1 (0=0) (SYSMIS=SYSMIS) (else=1) into true_lpalc.
*do if NOT(SYSMIS(aant_alcooit2)).
*recode aant_alcooit2 (1=0) (else=1) into true_lpalc.
*end if.
*crosstabs meting by aant_alcooit1 aant_alcooit2 by true_lpalc.
*fre true_lpalc.

crosstabs meting by aant_alc4wk1 aant_alc4wk2 by mpalc.
fre mpalc.
*compute true_mpalc = mpalc.
*fre true_mpalc.
* correct

crosstabs meting by aant_dronkooit1 aant_dronkooit2 aant_dronkooit3 by lpdronk.
* correct for aant_dronkooit3 but not for the other 2

*recode aant_dronkooit1 (0=0) (SYSMIS=SYSMIS) (else=1) into true_lpdronk.
*do if NOT(SYSMIS(aant_dronkooit2)).
*recode aant_dronkooit2 (1=0) (else=1) into true_lpdronk.
*end if.
*do if NOT(SYSMIS(aant_dronkooit3)).
*recode aant_dronkooit3 (1=0) (else=1) into true_lpdronk.
*end if.
*crosstabs meting by aant_dronkooit1 aant_dronkooit2 aant_dronkooit3 by true_lpdronk.
*fre true_lpdronk.

crosstabs meting by aant_dronk4wk1 aant_dronk4wk2 aant_dronk4wk3 by mpdronk.
* correct for aant_dronk4wk3 but not for the other 2

*recode aant_dronk4wk1 (0=0) (SYSMIS=SYSMIS) (else=1) into true_mpdronk.
*do if NOT(SYSMIS(aant_dronk4wk2)).
*recode aant_dronk4wk2 (1=0) (else=1) into true_mpdronk.
*end if.
*do if NOT(SYSMIS(aant_dronk4wk3)).
*recode aant_dronk4wk3 (1=0) (else=1) into true_mpdronk.
*end if.
*crosstabs meting by aant_dronk4wk1 aant_dronk4wk2 aant_dronk4wk3 by true_mpdronk.
*fre true_mpdronk.

*crosstabs lpalc by true_lpalc.
*crosstabs mpalc by true_mpalc.
*crosstabs lpdronk by true_lpdronk.
*crosstabs mpdronk by true_mpdronk.

*variable level true_lpalc true_mpalc true_lpdronk true_mpdronk (scale).

fre lpalc.
fre mpalc.
fre lpdronk.
fre mpdronk.

* binge drinking

fre aant_binge.
crosstabs meting by aant_binge.
crosstabs meting by aant_binge by mpbinge.
* klopt niet
* same situation as described above. Just use mpbinge from the dataset.

*recode aant_binge (1=0) (2 thru hi=1) into true_mpbinge.

*variable level true_mpbinge (scale).

save 
/outfile= 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019.sav'
/keep = all.

dataset close all.

*focus on MPALC

get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019.sav'.
fre meting.
crosstabs meting by sekse schnivo leerjaar etngroep3 stedgem vaderbaan moederbaan vollgezin spijbel
/cells=count row.

MEANS TABLES=lft cijferleven spijbel BY meting
  /CELLS=MEAN COUNT STDDEV SEMEAN MIN MAX MEDIAN.

fre mpalc.

* remove cases with missing values on mpalc
* remove variables leerjaar
* remove cases with age < 12 and age > 16

SELECT IF NOT (SYSMIS(mpalc)).
fre mpalc.

FREQUENCIES VARIABLES=lft
  /ORDER=ANALYSIS.

SELECT IF NOT (lft < 12 OR lft > 16).

save 
/outfile= 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019_MPALC_incomplete.sav'
/keep = meting sekse lft schnivo etngroep3 stedgem vaderbaan moederbaan vollgezin spijbel cijferleven mpalc.

dataset close all.

*we also create a version with complete data
    
get /file = 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019.sav'.
    
USE ALL.
MVA VARIABLES=lft cijferleven sekse schnivo etngroep3 stedgem vaderbaan moederbaan mpalc 
    vollgezin spijbel
  /MAXCAT=25
  /CATEGORICAL=sekse schnivo etngroep3 stedgem vaderbaan moederbaan vollgezin spijbel mpalc
  /MISMATCH PERCENT=0
  /TPATTERN PERCENT=0.
* there are no clear patterns
* mpalc has 1121 missing values. These are mostly standalone missing values without a pattern.
* if we omit all cases with missing values, we are left with 51766 out of 55362 cases
* we thus drop 3586 which is 6.5% of the cases
* this is acceptable

SELECT IF NOT (SYSMIS(meting)) AND NOT (SYSMIS(sekse)) AND NOT (SYSMIS(lft)) AND NOT (SYSMIS(schnivo)).
SELECT IF NOT (SYSMIS(etngroep3)) AND NOT (SYSMIS(stedgem)) AND NOT (SYSMIS(vaderbaan)) AND NOT (SYSMIS(moederbaan)) AND NOT (SYSMIS(vollgezin)).
SELECT IF NOT (SYSMIS(spijbel)) AND NOT (SYSMIS(cijferleven)).
SELECT IF NOT (SYSMIS(mpalc)).

save 
/outfile= 'C:\Users\20200059\Documents\Data\HBSC\Data\AlcoholTrends_HBSCDNSSSU_EMM\PeilHBSC20032019_MPALC_complete.sav'
/keep = meting sekse lft schnivo leerjaar etngroep3 stedgem vaderbaan moederbaan vollgezin spijbel cijferleven mpalc.

dataset close all.


