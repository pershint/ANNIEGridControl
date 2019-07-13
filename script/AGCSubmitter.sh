source /cvmfs/annie.opensciencegrid.org/setup_annie.sh
#FILEDIR=/pnfs/annie/persistent/users/moflaher/wcsim/multipmt/tankonly/wcsim_25_04_19_ANNIEp2v6_nodigit_BNB_Water_10k_22-05-17/
FILEDIR=/pnfs/annie/persistent/users/moflaher/wcsim/multipmt/tankonly/wcsim_04-07-19_ANNIEp2v6_nodigint_longlappds_BNB_Water_10k_22-05-17/
echo $FILEDIR
python main.py -S TOOLANALYSISRECO -s INPUT_FILE_PMT $FILEDIR INPUT_FILE_LAPPD $FILEDIR OUTPUT_FILE_TREE -M 800
