#/eos/user/a/adeiorio/Wprime/nosynch/v15/plot/
#python makedd.py --pathin localhisto/v15/  -y 2017 --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/


python makedd.py --pathin localhisto/v15_nounderflow/  -y 2016 --plotpath plot_28_01 -c muon --pathout localhisto/test_new_nofitrange_v15/ --resetMF #first one resets missing files list 
python makedd.py --pathin localhisto/v15_nounderflow/  -y 2018 --plotpath plot_28_01 -c muon --pathout localhisto/test_new_nofitrange_v15/
python makedd.py --pathin localhisto/v15_nounderflow/  -y 2017 --year_sf 2018 --plotpath plot_28_01 -c muon --pathout localhisto/test_new_nofitrange_v15/

python makedd.py --pathin localhisto/v15_nounderflow/  -y 2016 --plotpath plot_31_01 -c electron --pathout localhisto/test_new_v15/
python makedd.py --pathin localhisto/v15_nounderflow/  -y 2018 --plotpath plot_31_01 -c electron --pathout localhisto/test_new_v15/
python makedd.py --pathin localhisto/v15_nounderflow/  -y 2017 --year_sf 2018 --plotpath plot_31_01 -c electron --pathout localhisto/test_new_v15/

#python makedd.py --pathin localhisto/v15_nounderflow/  -y 2017 --year_sf 2018 --plotpath plot_31_01 -c electron --pathout localhisto/test_new_v15/

#cp -r localhisto/test_new_v15/muon /eos/user/a/adeiorio/Wprime/nosynch/v15/plot_qcdcut/
#cp -r localhisto/test_new_v15/electron /eos/user/a/adeiorio/Wprime/nosynch/v15/plot_qcdcut/
