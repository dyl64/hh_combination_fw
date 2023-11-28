from ROOT import TFile
import pandas as pd
import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import sys
sys.path.append('./recomendationsrealewksinglet/')
from Singlet import Singlet

bbbbfacecolor='deepskyblue'
bbbbedgecolor='blue'
bbyyfacecolor='lightcoral'
bbyyedgecolor='red'
bbtautaufacecolor='lightgreen'
bbtautauedgecolor='green'
combfacecolor='#FDC536'
combedgecolor='black'
invalidcolor='gray'

do_2ch_over_2p = True

plot_single_ch = False

plot_paperstyle = True

draw_hcoupling = False

mH=500.

def interp_limit(mSvalue,mSset,xsec_set):
    interp_xsec=0
    for i in range(0,len(mSset)-1):
        if(mSvalue>=mSset[i] and mSvalue<=mSset[i+1]):
            interp_xsec=(xsec_set[i+1]-xsec_set[i])/(mSset[i+1]-mSset[i])*(mSvalue-mSset[i])+xsec_set[i]
    return interp_xsec

data=pd.read_csv("../scripts/hh_limits_summary0913.txt",sep=",")

x=data["mass"]
y=data["r_br_yy_bb"]
z_exp=data["exp_limit"]
z_obs=data["obs_limit"]


# f_exp=interpolate.LinearNDInterpolator(list(zip(np.log(x),np.log(y))), z_exp, fill_value=0)
# f_obs=interpolate.LinearNDInterpolator(list(zip(np.log(x),np.log(y))), z_obs, fill_value=0)
f_exp=interpolate.LinearNDInterpolator(list(zip(x,y)), z_exp, fill_value=0)
f_obs=interpolate.LinearNDInterpolator(list(zip(x,y)), z_obs, fill_value=0)

hh_limit_bbbb=pd.read_csv("hh_limits_bbbb_230711.txt",sep=",")
hh_limit_bbyy=pd.read_csv("hh_limits_bbyy_230711.txt",sep=",")
hh_limit_bbtautau=pd.read_csv("hh_limits_bbtautau_230711.txt",sep=",")
br_h_bb_sm=5.809e-1
br_h_tautau_sm=6.3e-2
br_h_yy_sm=2.270e-3

xmin=-1
xmax=1
ymin=0.1
ymax=10

# fhMSSM=TFile.Open("../../LHCHWG_ROOT/hMSSM.root","r")
# f_mH=fhMSSM.Get("m_H")
# f_widthH=fhMSSM.Get("width_H")
# f_ggFH=fhMSSM.Get("xs_gg_H")
# f_H_hh=fhMSSM.Get("br_H_hh")
# f_hyy=fhMSSM.Get("br_h_gamgam")
# f_hbb=fhMSSM.Get("br_h_bb")
# f_htautau=fhMSSM.Get("br_h_tautau")

singlet=Singlet()

BSMpred=pd.read_csv("./recomendationsrealewksinglet/output_sHDECAY_mH"+str(int(mH))+".csv",sep=",",header=None)
# xsina=BSMpred[2]
# ytanB=BSMpred[3]
# zbrhh=BSMpred[17]
# f_brhh=interpolate.interp2d(xsina,ytanB,zbrhh,kind="cubic")
# print(f_brhh(0.87,7.5))

# sinarange=np.linspace(xmin,xmax,101)
# tanBrange=np.linspace(ymin,ymax,100)

sinarange=BSMpred[3].drop_duplicates()
tanBrange=BSMpred[2].drop_duplicates()

X,Y = np.meshgrid(sinarange,tanBrange)
# Z will be the limit divided by the theory predicted value
Z_obs=np.array(X)
Z_exp=np.array(X)
Z_obs_bbbb=np.array(X)
Z_exp_bbbb=np.array(X)
Z_obs_bbyy=np.array(X)
Z_exp_bbyy=np.array(X)
Z_obs_bbtautau=np.array(X)
Z_exp_bbtautau=np.array(X)
mH_grid=np.array(X)
widthHovermH_grid=np.array(X)
[nsina,ntanB]=X.shape
for i in range(nsina):
    # sinaround=round(sinarange[i],2)
    # # print(sinaround)
    # zbrhhslice=BSMpred[17][BSMpred[3]==sinaround]
    # ytanBslice=BSMpred[2][BSMpred[3]==sinaround]
    # # print(ytanBslice)
    # # print(zbrhhslice)
    # f_brhh=interpolate.interp1d(ytanBslice,zbrhhslice,kind='cubic')
    # print(f_brhh(7.3))
    for j in range(ntanB):
        # sina=X[i,j]
        # tanB=Y[i,j]
        sina=round(X[i,j],2)
        tanB=round(Y[i,j],1)
        # mH=f_mH.Interpolate(sina,tanB)
        # widthH=f_widthH.Interpolate(sina,tanB)
        # mH_grid[i,j]=mH
        # widthHovermH_grid[i,j]=widthH/mH
        # ggFH=f_ggFH.Interpolate(sina,tanB)
        # br_H_hh=f_H_hh.Interpolate(sina,tanB)
        # br_h_bb=f_hbb.Interpolate(sina,tanB)
        # br_h_tautau=f_htautau.Interpolate(sina,tanB)
        # br_h_yy=f_hyy.Interpolate(sina,tanB)
        widthH=singlet.getGamma_H2(mH,sina,tanB)
        mH_grid[i,j]=mH
        widthHovermH_grid[i,j]=widthH/mH
        # if(widthH<0):
        #     print(sina,tanB,widthH)
        ggFH=singlet.getXsecGGF_H2(mH,sina,'QuarkLoopInduced')
        br_H_hh=singlet.getBR_H2(mH, 'hh', sina, tanB)
        # if(br_H_hh<0):
        #     print(sina,tanB,br_H_hh)
        br_h_bb=0.5809
        br_h_tautau=6.3e-2
        br_h_yy=2.270e-3
        if(br_H_hh== None):
            print(sina,tanB)
            br_H_hh=1e-8
        xsec_theory=ggFH*br_H_hh
        r_br_yy_bb=br_h_yy/br_h_bb
        if(do_2ch_over_2p):
            if(widthHovermH_grid[i,j]>0.02):
                r_br_yy_bb=0
        if(mH>=251):
            # xsec_limit_exp=f_exp(np.log(mH),np.log(r_br_yy_bb))*(0.5809*0.5809)/(br_h_bb*br_h_bb)
            # xsec_limit_obs=f_obs(np.log(mH),np.log(r_br_yy_bb))*(0.5809*0.5809)/(br_h_bb*br_h_bb)
            xsec_limit_exp=f_exp(mH,r_br_yy_bb)*(0.5809*0.5809)/(br_h_bb*br_h_bb)
            xsec_limit_obs=f_obs(mH,r_br_yy_bb)*(0.5809*0.5809)/(br_h_bb*br_h_bb)
            Z_exp[i,j]=xsec_theory/xsec_limit_exp
            Z_obs[i,j]=xsec_theory/xsec_limit_obs
        else:
            Z_exp[i,j]=0
            Z_obs[i,j]=0
        if(np.isnan(Z_exp[i,j])):Z_exp[i,j]=Z_obs[i,j]=0

        if (br_H_hh<=0): br_H_hh=1e-8
        if (ggFH<=0): ggFH=1e-8
        Z_exp_bbbb[i,j]=interp_limit(mH,hh_limit_bbbb["mH[GeV]"],hh_limit_bbbb["Expected[fb]"])*0.001*br_h_bb_sm*br_h_bb_sm/(ggFH*br_H_hh*br_h_bb*br_h_bb)
        Z_obs_bbbb[i,j]=interp_limit(mH,hh_limit_bbbb["mH[GeV]"],hh_limit_bbbb["Observed[fb]"])*0.001*br_h_bb_sm*br_h_bb_sm/(ggFH*br_H_hh*br_h_bb*br_h_bb)
        Z_exp_bbtautau[i,j]=interp_limit(mH,hh_limit_bbtautau["mH[GeV]"],hh_limit_bbtautau["Expected[fb]"])*0.001*br_h_bb_sm*br_h_tautau_sm/(ggFH*br_H_hh*br_h_bb*br_h_tautau)
        Z_obs_bbtautau[i,j]=interp_limit(mH,hh_limit_bbtautau["mH[GeV]"],hh_limit_bbtautau["Observed[fb]"])*0.001*br_h_bb_sm*br_h_tautau_sm/(ggFH*br_H_hh*br_h_bb*br_h_tautau)
        Z_exp_bbyy[i,j]=interp_limit(mH,hh_limit_bbyy["mH[GeV]"],hh_limit_bbyy["Expected[fb]"])*0.001*br_h_bb_sm*br_h_yy_sm/(ggFH*br_H_hh*br_h_bb*br_h_yy)
        Z_obs_bbyy[i,j]=interp_limit(mH,hh_limit_bbyy["mH[GeV]"],hh_limit_bbyy["Observed[fb]"])*0.001*br_h_bb_sm*br_h_yy_sm/(ggFH*br_H_hh*br_h_bb*br_h_yy)
        if(Z_exp_bbbb[i,j]!=0):
            Z_exp_bbbb[i,j]=1/Z_exp_bbbb[i,j]
            Z_obs_bbbb[i,j]=1/Z_obs_bbbb[i,j]
        else:
            Z_obs_bbbb[i,j]=0
            Z_exp_bbbb[i,j]=0
        if(Z_exp_bbtautau[i,j]!=0):
            Z_exp_bbtautau[i,j]=1/Z_exp_bbtautau[i,j]
            Z_obs_bbtautau[i,j]=1/Z_obs_bbtautau[i,j]
        else:
            Z_obs_bbtautau[i,j]=0
            Z_exp_bbtautau[i,j]=0
        if(Z_exp_bbyy[i,j]!=0):
            Z_exp_bbyy[i,j]=1/Z_exp_bbyy[i,j]
            Z_obs_bbyy[i,j]=1/Z_obs_bbyy[i,j]
        else:
            Z_obs_bbyy[i,j]=0
            Z_exp_bbyy[i,j]=0
        if(np.isnan(Z_obs_bbbb[i,j])):Z_obs_bbbb[i,j]=0
        if(np.isnan(Z_exp_bbbb[i,j])):Z_exp_bbbb[i,j]=0
        if(np.isnan(Z_obs_bbyy[i,j])):Z_obs_bbyy[i,j]=0
        if(np.isnan(Z_exp_bbyy[i,j])):Z_exp_bbyy[i,j]=0
        if(np.isnan(Z_obs_bbtautau[i,j])):Z_obs_bbtautau[i,j]=0
        if(np.isnan(Z_exp_bbtautau[i,j])):Z_exp_bbtautau[i,j]=0

        if(widthHovermH_grid[i,j]>0.02):
            if(i>=1 and mH==275.):
                k=(widthHovermH_grid[i,j]-widthHovermH_grid[i-1,j])/(tanB-Y[i-1,j])#Gradient of the width grid
                if(k!=0 and Z_exp_bbyy[i,j] > 1 and widthHovermH_grid[i-1,j]<0.02): #Only care about the points near the contours
                    cross=tanB-(widthHovermH_grid[i,j]-0.02)/k #Points where the width=0.02
                    k2=(1-Z_exp_bbyy[i-1,j])/(cross-Y[i-1,j]) #Gradient of Z_exp_bbyy in order to get the same cross points as width
                    Z_exp_bbyy[i,j]=Z_exp_bbyy[i-1,j]+k2*(tanB-Y[i-1,j]) # Apply the gradient to the Z_exp_bbyy
                    if(Z_exp_bbyy[i,j]>1): #If in some case the Z_exp_bbyy is still > 1, set it to 0
                        Z_exp_bbyy[i,j]=0
                else:
                    Z_exp_bbyy[i,j]=0
            else:
                Z_exp_bbyy[i,j]=0

fig=plt.figure()
ax=plt.axes([0.1,0.1,0.8,0.8])
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymin+(ymax-ymin)/0.55*0.8)
plt.minorticks_on()
ax.tick_params(which='both',direction="in",top=True,right=True)
plt.rcParams["font.sans-serif"] = ["Helvetica"]
cs1=ax.contour(X, Y, Z_exp,[1],linewidths=2, colors=combedgecolor,linestyles='solid')
# cs2=ax.contour(X,Y,Z_obs,[1],linewidths=2, colors=combedgecolor,linestyles='solid')
# cs3=ax.contour(X, Y, mH_grid,[251,260,280,300,350,400,500,600,700,800,900,1000],linewidths=1, colors=invalidcolor,linestyles='dotted')
# plt.clabel(cs3,colors=invalidcolor,fmt='%3g')
csf1=ax.contourf(X,Y,Z_obs,[1,1e9],colors=[combfacecolor])

if plot_single_ch:
    csfbbtautau=ax.contourf(X,Y,Z_obs_bbtautau,[1,1e9],colors=[bbtautaufacecolor])
    csfbbyy=ax.contourf(X,Y,Z_obs_bbyy,[1,1e9],colors=[bbyyfacecolor])
    csfbbbb=ax.contourf(X,Y,Z_obs_bbbb,[1,1e9],colors=[bbbbfacecolor])

    csbbbbexp=ax.contour(X, Y, Z_exp_bbbb,[1],linewidths=2, colors=bbbbedgecolor,linestyles='dashed')
    csbbbbobs=ax.contour(X,Y,Z_obs_bbbb,[1],linewidths=2, colors=bbbbedgecolor,linestyles='solid')

    csbbyyexp=ax.contour(X, Y, Z_exp_bbyy,[1],linewidths=2, colors=bbyyedgecolor,linestyles='dashed')
    
    csbbyyobs=ax.contour(X,Y,Z_obs_bbyy,[1],linewidths=2, colors=bbyyedgecolor,linestyles='solid')

    csbbtautauexp=ax.contour(X, Y, Z_exp_bbtautau,[1],linewidths=2, colors=bbtautauedgecolor,linestyles='dashed')
    csbbtautauobs=ax.contour(X,Y,Z_obs_bbtautau,[1],linewidths=2, colors=bbtautauedgecolor,linestyles='solid')
elif plot_paperstyle:
    csbbbbexp=ax.contour(X, Y, Z_exp_bbbb,[1],linewidths=2, colors=bbbbedgecolor,linestyles='-.')
    csbbyyexp=ax.contour(X, Y, Z_exp_bbyy,[1],linewidths=2, colors=bbyyedgecolor,linestyles='dashed')
    # csbbyyexp=ax.contour(X2, Y2, f_Zexpbby(X2,Y2),[1],linewidths=2, colors=bbyyedgecolor,linestyles='dashed')
    # csbbyyexp=ax.contour(X2, Y2, Z_exp_bbyy2,[1],linewidths=2, colors=bbyyedgecolor,linestyles='dashed')
    csbbtautauexp=ax.contour(X, Y, Z_exp_bbtautau,[1],linewidths=2, colors=bbtautauedgecolor,linestyles='dotted')
    # print(csbbyyexp.collections[0].get_paths())

if draw_hcoupling:
    ax.vlines(0.26,ymin,ymax,colors='purple',zorder=2.5)
    ax.vlines(-0.26,ymin,ymax,colors='purple',zorder=2.5)
    ax.vlines(0.34,ymin,ymax,linestyles='dashed',colors='purple',zorder=2.5)
    ax.vlines(-0.34,ymin,ymax,linestyles='dashed',colors='purple',zorder=2.5)
    ax.text(-0.132,2,r"$sin(\alpha)$<0.26(0.34)",size='9',color='purple')
    ax.text(-0.132,1.5,r"from SM coupling",size='9',color='purple')

ax.set_xlabel(r'm$_A$ [GeV]', loc='right',size='15',family='Helvetica')
ax.set_ylabel(r'tan$\mathrm{\beta}$', loc='top',size='15',family='Helvetica')
ax.tick_params(axis='both', labelsize=12)

ax2=plt.axes([0.1,0.65,0.8,0.25])
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_facecolor('none')
plt.rcParams['ps.useafm'] = True
ax2.text(0.03,0.75,'ATLAS',weight='bold',family='Helvetica',style='italic',size='13')
ax2.text(0.03,0.55,r'$\sqrt{\mathrm{s}}$ = 13 TeV, 126'+u'\u2014'+r'139 fb$^{-1}$',family='Helvetica',size='13')
ax2.text(0.03,0.35,r'$H \to hh$, EWK-singlet'+f', m$_H = {int(mH)} $GeV',family='Helvetica',size='13')
# ax2.text(0.32,0.5,,family='Helvetica',size='13')
ax2.text(0.03,0.15,r'95% CL upper limits',family='Helvetica',size='13')
#ax.scatter(interp_X,interp_Y,Z_obs_interp)


bbtautaunm=mpatches.Patch(color=bbtautaufacecolor,alpha=1,linewidth=2)
bbtautaunm.set_edgecolor(bbtautauedgecolor)
bbyynm=mpatches.Patch(color=bbyyfacecolor,alpha=1,linewidth=2)
bbyynm.set_edgecolor(bbyyedgecolor)
bbbbnm=mpatches.Patch(color=bbbbfacecolor,alpha=1,linewidth=2)
bbbbnm.set_edgecolor(bbbbedgecolor)
combnm=mpatches.Patch(color=combfacecolor,alpha=1,linewidth=0)
combnm.set_edgecolor(combedgecolor)
widthnm=mpatches.Patch(color=invalidcolor,alpha=1,linewidth=0)
#obsnm.set_hatch('//')

obsnm=mlines.Line2D([],[],color=combedgecolor,linewidth=0)
expnm=mlines.Line2D([],[],linestyle='solid',color=combedgecolor,linewidth=2)
mHnm=mlines.Line2D([],[],linestyle='dotted',color=invalidcolor,linewidth=1)
csfmH=ax.contourf(X,Y,widthHovermH_grid,[0.05,100],colors=['gray'],zorder=2)
# ax.scatter(X,Y,Z_exp_bbyy)
ax.set_axisbelow(False) 

if plot_single_ch:
    legendnm=[bbbbnm,bbyynm,bbtautaunm,combnm]
    labels=[r'bbbb',r'bb$\gamma\gamma$',r'bb$\tau\tau$',r'combined']
    legend2=[obsnm,expnm,widthnm]
    labels2=['Observed','Expected',r'$\Gamma_H/m_H>5$%']
    leg=ax2.legend([i for i in legendnm],labels ,loc='center left',bbox_to_anchor=(0.4,0.55),frameon=False,prop={'size': 10})
    leg2=ax2.legend([i for i in legend2], labels2, loc='center left',bbox_to_anchor=(0.65,0.55),frameon=False,prop={'size': 10})
    plt.gca().add_artist(leg)
elif plot_paperstyle:
    bbbbexpnm=mlines.Line2D([],[],linestyle='-.',color=bbbbedgecolor,linewidth=2)
    bbtautauexpnm=mlines.Line2D([],[],linestyle='dotted',color=bbtautauedgecolor,linewidth=2)
    bbyyexpnm=mlines.Line2D([],[],linestyle='dashed',color=bbyyedgecolor,linewidth=2)
    legendnm=[combnm,expnm,bbtautauexpnm,bbbbexpnm,bbyyexpnm]
    labels=[r'Obs. combined',r'Exp. combined',r'Exp. $b\bar{b}\tau\tau$',r'Exp. $b\bar{b}b\bar{b}$',r'Exp. $b\bar{b}\gamma\gamma$']
    legend2=[widthnm]
    labels2=[r'$\mathrm{\Gamma}_H/\mathrm{m}_H>5$%']
    leg=ax2.legend([i for i in legendnm],labels ,loc='center left',bbox_to_anchor=(0.69,0.5),frameon=False,prop={'size': 9.5, 'family':'Helvetica'},handlelength=3)
    leg2=ax2.legend([i for i in legend2], labels2, loc='center left',bbox_to_anchor=(0.4,0.15),frameon=False,prop={'size': 9.5})
    plt.gca().add_artist(leg)
else:
    legpaper=[combnm,expnm,widthnm]
    labelspaper=['Observed','Expected',r'$\Gamma_H/m_H>5$%']
    legpaper=ax2.legend([i for i in legpaper], labelspaper, loc='center left',bbox_to_anchor=(0.65,0.55),frameon=False,prop={'size': 10})

# plt.show()
plt.savefig("singlet_mS"+str(int(mH))+".pdf")


