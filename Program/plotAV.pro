pro plotAV

readcol, 'randomAV.txt', c, n, e, s, w
random_AV=fltarr(7,n_elements(c))
for i=0, n_elements(c)-1 do random_AV[*,i]=[c[i],n[i],e[i],s[i],w[i], mean([c[i],n[i],e[i],s[i],w[i]]), stddev([c[i],n[i],e[i],s[i],w[i]])]

readcol, 'cepheidGals.txt', c, n, e, s, w
cepheid_AV=fltarr(7,n_elements(c))
for i=0, n_elements(c)-1 do cepheid_AV[*,i]=[c[i],n[i],e[i],s[i],w[i], mean([c[i],n[i],e[i],s[i],w[i]]), stddev([c[i],n[i],e[i],s[i],w[i]])]
readcol, 'riceGals.txt', c, n, e, s, w
rice_AV=fltarr(7,n_elements(c))
for i=0, n_elements(c)-1 do rice_AV[*,i]=[c[i],n[i],e[i],s[i],w[i], mean([c[i],n[i],e[i],s[i],w[i]]), stddev([c[i],n[i],e[i],s[i],w[i]])]

readcol, 'SwiftAV.txt', c, n, e, s, w
swift_AV=fltarr(7,n_elements(c))
for i=0, n_elements(c)-1 do swift_AV[*,i]=[c[i],n[i],e[i],s[i],w[i], mean([c[i],n[i],e[i],s[i],w[i]]), stddev([c[i],n[i],e[i],s[i],w[i]])]


plot, random_AV[0,*], random_AV[1,*], psym=4, xlog=1, ylog=1
oplot, random_AV[0,*], random_AV[2,*], psym=4
oplot, random_AV[0,*], random_AV[3,*], psym=4
oplot, random_AV[0,*], random_AV[4,*], psym=4

cgoplot, rice_AV[0,*], rice_AV[1,*], psym=4, color='blue'
cgoplot, rice_AV[0,*], rice_AV[2,*], psym=4, color='blue'
cgoplot, rice_AV[0,*], rice_AV[3,*], psym=4, color='blue'
cgoplot, rice_AV[0,*], rice_AV[4,*], psym=4, color='blue'

plot, random_AV[5,*], random_AV[0,*], psym=4, /ylog, /xlog
oplot, [0.0001, 5], [0.0001, 5]
cgoplot, rice_AV[5,*], rice_AV[0,*], psym=5, color='blue'
cgoplot, cepheid_AV[5,*], cepheid_AV[0,*], psym=5, color='red'
cgoplot, swift_AV[5,*], swift_AV[0,*], psym=5, color='green'



nplots=1
; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
; the default size is given in centimeters
; 8.8 is made to match a journal column width
xsize = 8.8
wall = 0.03
margin=0.12
a = xsize/8.8 - (margin + wall)
b = a * 2d / (1 + sqrt(5))
xrange=[-20,30]
yrange=[5,25]
ysize = (margin + nplots*(b + wall ) )*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/ysize
y2 = y1 + b*8.8/ysize

figurename='avplot.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
plot, xrange, yrange, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle="Mean AV at 20'", charsize=1.0, /xlog, /ylog, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0.01,10], ytitle='AV at Galaxy Center', yticks=nxticks, ystyle=1, xrange=[0.01,10], xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, ytickv=ytickvalues

cgoplot, random_AV[5,*], random_AV[0,*], psym=4, color='grey'
cgoplot, [0.0001, 5], [0.0001, 5]
cgoplot, rice_AV[5,*], rice_AV[0,*], psym=5, color='blue'
cgoplot, cepheid_AV[5,*], cepheid_AV[0,*], psym=5, color='red'
cgoplot, swift_AV[5,*], swift_AV[0,*], psym=5, color='green'


;al_legend, ['SN2017erp','SN2005cf','SN2011fe'], psym=[46, 15, 4], position=[12,23], color=['red','orange','blue'], symsize=[1,0.5,0.5], box=0

device, /close
SET_PLOT, 'X'
spawn, 'open avplot.eps' 


figurename='avplotflat.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
cgplot, xrange, yrange, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle="Mean A$_V$ at 20'", charsize=1.0, /xlog,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[-99,99], ytitle='% Change in A$_V$ at Center', yticks=nxticks, ystyle=1, xrange=[0.01,10], xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, ytickv=ytickvalues

cgoplot, random_AV[5,*], 100.0*(random_AV[0,*]-random_AV[5,*])/random_AV[5,*], psym=4, color='grey'
cgoplot, rice_AV[5,*], 100.0*(rice_AV[0,*]-rice_AV[5,*])/rice_AV[5,*], psym=5, color='blue'
cgoplot, cepheid_AV[5,*], 100.0*(cepheid_AV[0,*]-cepheid_AV[5,*])/cepheid_AV[5,*], psym=5, color='red'
cgoplot, swift_AV[5,*], 100.0*(swift_AV[0,*]-swift_AV[5,*])/swift_AV[5,*], psym=5, color='green'


;al_legend, ['SN2017erp','SN2005cf','SN2011fe'], psym=[46, 15, 4], position=[12,23], color=['red','orange','blue'], symsize=[1,0.5,0.5], box=0

device, /close
SET_PLOT, 'X'
spawn, 'open avplotflat.eps' 

print, 'rice '
print, rice_AV[0,where(abs(100.0*(rice_AV[0,*]-rice_AV[5,*])/rice_AV[5,*]) gt 22.0)]

print, 'Cepheid '
print, cepheid_AV[0,where(abs(100.0*(cepheid_AV[0,*]-cepheid_AV[5,*])/cepheid_AV[5,*]) gt 22.0)]

print, 'swift '
print, swift_AV[0,where(abs(100.0*(swift_AV[0,*]-swift_AV[5,*])/swift_AV[5,*]) gt 22.0)]

print, 'random '
print, random_AV[0,where(abs(100.0*(random_AV[0,*]-random_AV[5,*])/random_AV[5,*]) gt 22.0)]


print, 'rice '
print, rice_AV[0,where((100.0*(rice_AV[0,*]-rice_AV[5,*])/rice_AV[5,*]) lt -42.0)]

print, 'Cepheid '
print, cepheid_AV[0,where((100.0*(cepheid_AV[0,*]-cepheid_AV[5,*])/cepheid_AV[5,*]) lt -22.0)]


print, 'final stop'
stop
end