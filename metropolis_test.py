import warnings
warnings.filterwarnings("ignore")
from rayoptics.environment import *
from rayoptics.elem.surface import Aperture, Circular, Elliptical
# util functions
from rayoptics.util.misc_math import normalize
from calc_parse_loss import calc_loss
import copy
import warnings
from numpy import Infinity
import random
from calc_parse_loss import calc_loss
isdark = False
warnings.filterwarnings("ignore")
# use standard rayoptics environment
from rayoptics.environment import *

# util functions
from rayoptics.util.misc_math import normalize


X = [-4.845975138071575e-06, 0.27289072893926297, 0.979089500550259, 1.562143699995668, 286.3268143342434, 0.12757292966898365, 0.4976985868016406, -0.0499097527859659, 1.0283887913015086, 1.7618702671740445, 167.42958289489502, -0.26845338739126257, 2.109240114869494, 0.8853029221687085, 1.1074608493634126, 1.0355730283207585, 0.9784668076430673, -4.1651625541166444e-05, 0.8570563331142012, 1.5912412986742466, 12.31488715184438, 3.198186366543512e-05, 1.311712129719171, 0.9688476182807819]
Y = [5.0511370269849e-07, 0.009593576315131715, -0.033923210086491656, 0.017530258062542353, -0.005557733254536261, 4.835553239645145e-07, 4.754739084440438e-07, 4.762290622956345e-07]
Y1 = [4.116660259406584e-07, -0.002724306218671618, -0.03686917860915836, 0.0036263466321055874, -0.00016183332938758536, 4.4888499212262214e-07, 4.633218369929322e-07, 4.623414152981795e-07]
Y2 = [4.663945970957146e-07, -0.02496923378014343, 0.012252469223041872, -0.01928358384373149, 0.004130244149262994, 4.78747539570957e-07, 4.588331046879918e-07, 4.703430147215058e-07] 
Y3 = [4.716019559967116e-07, 4.789807465025439e-07, 4.5434495703220897e-07, 4.815958528872e-07, 4.5441354257390504e-07, 4.877423381488874e-07, 4.711291729407197e-07, 4.4865478126454545e-07]
Y4 = [4.5994640829817283e-07, 4.815984847007885e-07, 4.242316217819082e-07, 4.597569097928876e-07, 5.113180977873441e-07, 4.65694158789167e-07, 4.633552521213859e-07, 4.386671928781448e-07]
Y5 = [5.008822077652336e-07, 4.64744188726496e-07, 4.297533556826988e-07, 4.572963134221159e-07, 4.663830615637756e-07, 4.3441192081450457e-07, 4.801042565203454e-07, 4.855599965919782e-07]

opm = OpticalModel()
sm = opm['seq_model']
osp = opm['optical_spec']
pm = opm['parax_model']
em = opm['ele_model']
pt = opm['part_tree']
opm.system_spec.dimensions = 'mm'
osp['pupil'] = PupilSpec(osp, key=['object', 'pupil'], value=2.35)
osp['fov'] = FieldSpec(osp, key=['object', 'angle'],  value=0.056, is_relative=True, flds=[0., 5., 10., 15., 20.])
osp['wvls'] = WvlSpec([(470, 1.0), (650, 1.0)], ref_wl=1)
osp.defocus = FocusRange(focus_shift=X[0])  

opm.radius_mode = False

sm.gaps[0].thi=1e10
sm.add_surface([1./X[1], X[2], 1.54, 75.0])

sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1./X[1], ec=X[13], 
               coefs=[ Y[0], Y[1], Y[2],  Y[3],  Y[4], Y[5], Y[6],  Y[7]])

#воздух
sm.add_surface([1./X[5], X[6]])
sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1./X[5], ec=X[14],
                         coefs=[Y1[0], Y1[1], Y1[2],  Y1[3],Y1[4], Y1[5], Y1[6],  Y1[7]])

#1.67, 39.0 - пластик2
#1.54, 75.0 - пластик1
sm.add_surface([1./(X[7]), X[8], 1.67, 39.0])
sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1./(X[7]), ec=X[15],
                         coefs=[Y2[0], Y2[1], Y2[2],  Y2[3], Y2[4], Y2[5], Y2[6],  Y2[7]])

sm.add_surface([1./(X[11]), X[12]])
sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1./(X[11]), ec = X[16],
                                                  coefs= [Y3[0], Y3[1], Y3[2],  Y3[3], Y3[4], Y3[5], Y3[6],  Y3[7] ])

sm.add_surface([-1./(X[17]), X[18], 1.54, 75.0])
sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=-1./(X[17]), ec=X[21], 
                                                  coefs=[ Y4[0],Y4[1], Y4[2], Y4[3], Y4[4],Y4[5], Y4[6], Y4[7]])
ap2 = Circular(0.4)
sm.ifcs[2].clear_apertures = [ap2]

ap2 = Circular(0.2)
sm.ifcs[4].clear_apertures = [ap2]

sm.add_surface([-1./(X[21]), X[22]])
sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=-1./(X[21]), ec=X[23],
                                                  coefs=[Y5[0], Y5[1], Y5[2], Y5[3], Y5[4], Y5[5], Y5[6], Y5[7]])

opm.update_model()

sm.do_apertures = True
sm.stop_surface = 1
sm.cur_surface = 7

opm.save_model("test30.roa")
try:
     loss = calc_loss("test30.roa")
except Exception as e:
     print("Ошибка")
print(loss)
     



