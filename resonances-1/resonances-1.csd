<CsoundSynthesizer>
<CsOptions>
-d -odac1    ; disable displays, send output to speakers
</CsOptions>

<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1


instr 1
    ; Oscillator
    kfreq chnget "freq"        ; control-rate frequency from Python
    aSig vco2 0.3, kfreq       ; square wave oscillator
    
    ; Lowpass Filter        
    kcf  chnget "cutoff"
    kres chnget "res"
    aSig moogladder aSig, kcf, kres


    ; Comb filter
    krvt chnget "combVerbTime"
    ilpt chnget "combLooptime"  
    iskip chnget "combRes"    
    kMix chnget "combMix"
    
    
    aLeft  combinv aSig, krvt, ilpt, iskip
    aRight combinv aSig, krvt, ilpt*.2, iskip
    aLeft = (aSig * (1 - kMix)) + (aLeft * kMix)
    aRight=  (aSig * (1 - kMix)) + (aRight * kMix)    

    outs aLeft, aRight            ; stereo output
endin
</CsInstruments>

<CsScore>
i1 0 500                         ; play forever until stopped
</CsScore>

</CsoundSynthesizer>
