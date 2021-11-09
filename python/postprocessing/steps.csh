set outdir = $1
set version = v17
echo $outdir
set nstep=$2

echo $nstep
if ($nstep == 0) then
    echo "nsteps is 0, doing nothing"
endif

if ($nstep > 3) then
    echo "nsteps > 3, running makeplot"
    nohup python doplot.py -m fitsrcr -v $version -o $outdir -y 2016,2017,2018 --parallel 10
endif

if ($nstep > 2) then
    echo "nsteps > 2, running merge"
    nohup python mergeyears.py -v $version -i $outdir -o $outdir --parallel 10 > $outdir/$version/merge.log  
endif

if ($nstep > 1) then
    echo "nsteps > 1, running makedd"
    nohup python makedd.py --pathin $outdir/$version/plot_merged -y 2020 --plotpath plot_$outdir -c electron --pathout $outdir/$version/plot_explin --runoptions N --resetMF > & $outdir/$version/makedd.log #first one resets missing files list 
    nohup python makedd.py --pathin $outdir/$version/plot_merged -y 2020 --plotpath plot_$outdir -c muon --pathout $outdir/$version/plot_explin --runoptions N --resetMF > & $outdir/$version/makedd.log #first one resets missing files list 
    nohup python makedd.py --pathin $outdir/$version/plot_merged -y 2020 --plotpath plot_$outdir -c electron --pathout $outdir/$version/plot_explin --runoptions B --resetMF > & $outdir/$version/makedd.log #first one resets missing files list 
    nohup python makedd.py --pathin $outdir/$version/plot_merged -y 2020 --plotpath plot_$outdir -c muon --pathout $outdir/$version/plot_explin --runoptions B --resetMF > & $outdir/$version/makedd.log #first one resets missing files list 
    cp $outdir/$version/plot_merged/muon/* $outdir/$version/plot_explin/muon/
    cp $outdir/$version/plot_merged/electronon/* $outdir/$version/plot_explin/electron/
endif

if ($nstep > 0) then
    echo "nsteps > 0, running preparefit"
    python preparefit.py -m "sum symmetrize smooth" -i $outdir/$version/plot_explin -o $outdir/$version/plot_explin_fit 
endif
