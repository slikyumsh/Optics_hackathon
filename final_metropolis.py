import copy
import warnings
from numpy import Infinity
import random

from rayoptics.elem.surface import Circular

from calc_parse_loss import calc_loss
isdark = False
warnings.filterwarnings("ignore")
# use standard rayoptics environment
from rayoptics.environment import *

# util functions
from rayoptics.util.misc_math import normalize

last_loss = 0.76
cur_loss = 0.76
best_loss = 0.76

bestX = []
bestY = []
bestY1 = []
bestY2 = []
bestY3 = []
bestY4 = []
bestY5 = []
bestY6 = []
bestY7 = []

X =  [-5.041451686876395e-06, 0.27295602780081735, 0.9889756247531791, 1.652720468979783, 278.4272946995099, 0.12811146661779996, 0.47279856918820895, -0.05038637151844433, 1.0606469721925824, 1.7744648229136246, 174.86476878551773, -0.2682853476452658, 2.085866680706233, 0.8809036797365971, 1.0918422485466275, 1.033235696347449, 1.012130172510614, -4.198357974779292e-05, 0.844387325550726, 1.5286633388122453, 13.272645776434537, 3.356776766389772e-05, 1.259648949738764, 0.9389735015207475, -4.387626221771935e-05, 0.19258910559725959, -4.357148387485064e-05, 1.256345236885694e-05, 3.412211098671522e-05, 0.7044480414345003, 0.9726146028122292]
Y =  [7.767663347150967e-07, 0.006989961312539579, -0.033683299069711355, 0.02057941689533597, -0.00453320377117771, 7.865984390668331e-07, 8.042903376391567e-07, 8.328551788399372e-07]
Y1 =  [7.320720148998173e-07, -0.0023674519745927125, -0.03957578830655727, 0.0040621045400731585, -0.0001521402869230454, 6.601100716436691e-07, 7.70818684774671e-07, 7.080881007493782e-07]
Y2 =  [7.580143111298296e-07, -0.023986860054831947, 0.014584599915953539, -0.0169839977337229, 0.0038655118063765687, 7.679336363395694e-07, 7.770488437620121e-07, 7.293620393009774e-07]
Y3 =  [6.961792649356755e-07, 7.909676471708906e-07, 7.499617289414937e-07, 8.821039405829203e-07, 7.215117433525062e-07, 7.667192557417417e-07, 7.395404284889468e-07, 7.630249593151128e-07]
Y4 =  [7.001690522219228e-07, 8.135823558661861e-07, 6.874045782021986e-07, 7.395876529571839e-07, 7.250741923564933e-07, 7.650328854050125e-07, 7.776297307464449e-07, 8.163429120797157e-07]
Y5 =  [7.012566397008523e-07, 8.102298155581631e-07, 7.687544532332421e-07, 7.25014319834636e-07, 8.384577232717423e-07, 8.254383653609174e-07, 6.731050515009555e-07, 7.05961511175669e-07]
Y6 =  [7.043003560298324e-07, 8.071500939694709e-07, 7.717926499678571e-07, 7.280988312314858e-07, 8.365834546392231e-07, 8.303114594995252e-07, 6.800645768864621e-07, 7.027135339936005e-07]
Y7 =  [8.63382554020186e-07, 9.802417810736698e-07, 7.958309693239886e-07, 7.982645320860086e-07, 9.305154817605681e-07, 8.92194774395753e-07, 7.675760865594337e-07, 7.399624466524545e-07]



def metropolis(lengthX, lengthY, theta=100, treshold = 1e-9):
    global last_loss, cur_loss, bestX, X, Y,Y1, Y2, Y3, bestY, bestY1, bestY2, bestY3, best_loss, Y4, Y5, bestY4, bestY5, bestY6,bestY7,Y6,Y7
    param = random.randint(0, lengthX-1)
    value = random.uniform(-0.01, 0.01)

    prev = copy.deepcopy(X)
    if (abs(X[param] * value)) > treshold:
        X[param] = X[param] * (1. + value)
    else:
        X[param] = X[param] + treshold * np.sign(X[param] *  value  + 1e-7)

    prevY = copy.deepcopy(Y)
    random_params = [random.randint(0, lengthY - 1) for _ in range(lengthY)]
    random_values = [random.uniform(-0.005, 0.005) for _ in range(lengthY)]
    for i in range(0, lengthY):
        if (abs(Y[random_params[i]] * random_values[i])) > treshold:
            Y[random_params[i]] = Y[random_params[i]] * (1. + random_values[i])
        else:
            Y[random_params[i]] = Y[random_params[i]] + treshold * np.sign(Y[random_params[i]] * random_values[i] + 1e-7)
        
    prevY1 = copy.deepcopy(Y1)
    random_params1 = [random.randint(0, lengthY - 1) for _ in range(lengthY)]
    random_values1 = [random.uniform(-0.005, 0.005) for _ in range(lengthY)]
    for i in range(0, lengthY):
        if (abs(Y1[random_params1[i]] * random_values1[i])) > treshold:
            Y1[random_params1[i]] = Y1[random_params1[i]] * (1. + random_values1[i])
        else:
            Y1[random_params1[i]] = Y1[random_params1[i]] + treshold * np.sign(Y1[random_params1[i]] * random_values1[i] + 1e-7)

    prevY2 = copy.deepcopy(Y2)
    random_params2 = [random.randint(0, lengthY - 1) for _ in range(lengthY)]
    random_values2 = [random.uniform(-0.005, 0.005) for _ in range(lengthY)]

    for i in range(0, lengthY):
        if (abs(Y2[random_params2[i]] * random_values2[i])) > treshold:
            Y2[random_params2[i]] = Y2[random_params2[i]] * (1. + random_values2[i])
        else:
            Y2[random_params2[i]] = Y2[random_params2[i]] + treshold * np.sign(Y2[random_params2[i]] * random_values2[i] + 1e-7)

    
    prevY3 = copy.deepcopy(Y3)
    random_params3 = [random.randint(0, lengthY - 1) for _ in range(lengthY)]
    random_values3 = [random.uniform(-0.005, 0.005) for _ in range(lengthY)]
    for i in range(0, lengthY):
        if (abs(Y3[random_params3[i]] * random_values3[i])) > treshold:
            Y3[random_params3[i]] = Y3[random_params3[i]] * (1. + random_values3[i])
        else:
            Y3[random_params3[i]] = Y3[random_params3[i]] + treshold * np.sign(Y3[random_params3[i]] * random_values3[i] + 1e-7)

    prevY4 = copy.deepcopy(Y4)
    random_params4 = [random.randint(0, lengthY - 1) for _ in range(lengthY)]
    random_values4 = [random.uniform(-0.005, 0.005) for _ in range(lengthY)]
    for i in range(0, lengthY):
        if (abs(Y4[random_params4[i]] * random_values4[i])) > treshold:
            Y4[random_params4[i]] = Y4[random_params4[i]] * (1. + random_values4[i])
        else:
            Y4[random_params4[i]] = Y4[random_params4[i]] + treshold * np.sign(Y4[random_params4[i]] * random_values4[i] + 1e-7)

    prevY5 = copy.deepcopy(Y5)
    random_params5 = [random.randint(0, 7) for _ in range(8)]
    random_values5 = [random.uniform(-0.005, 0.005) for _ in range(8)]
    for i in range(0, 8):
        if (abs(Y5[random_params5[i]] * random_values5[i])) > treshold:
            Y5[random_params5[i]] = Y5[random_params5[i]] * (1. + random_values5[i])
        else:
            Y5[random_params5[i]] = Y5[random_params5[i]] + treshold * np.sign(Y5[random_params5[i]] * random_values5[i] + 1e-7)
    prevY6 = copy.deepcopy(Y6)
    random_params6 = [random.randint(0, 7) for _ in range(8)]
    random_values6 = [random.uniform(-0.005, 0.005) for _ in range(8)]
    for i in range(0, 8):
        if (abs(Y6[random_params6[i]] * random_values6[i])) > treshold:
            Y6[random_params6[i]] = Y5[random_params6[i]] * (1. + random_values6[i])
        else:
            Y6[random_params6[i]] = Y6[random_params6[i]] + treshold * np.sign(
                Y6[random_params6[i]] * random_values6[i] + 1e-7)
    prevY7 = copy.deepcopy(Y7)
    random_params7 = [random.randint(0, 7) for _ in range(8)]
    random_values7 = [random.uniform(-0.005, 0.005) for _ in range(8)]
    for i in range(0, 8):
        if (abs(Y7[random_params7[i]] * random_values7[i])) > treshold:
            Y7[random_params7[i]] = Y7[random_params7[i]] * (1. + random_values7[i])
        else:
            Y7[random_params7[i]] = Y7[random_params7[i]] + treshold * np.sign(
                Y7[random_params7[i]] * random_values7[i] + 1e-7)

    try:
        opm = OpticalModel()
        sm = opm['seq_model']
        osp = opm['optical_spec']
        pm = opm['parax_model']
        em = opm['ele_model']
        pt = opm['part_tree']
        opm.system_spec.dimensions = 'mm'
        osp['pupil'] = PupilSpec(osp, key=['object', 'pupil'], value=2.35)
        osp['fov'] = FieldSpec(osp, key=['object', 'angle'], value=0.05, is_relative=True, flds=[0., 5., 10., 15., 20.])
        osp['wvls'] = WvlSpec([(470, 1.0), (650, 1.0)], ref_wl=1)
        osp.defocus = FocusRange(focus_shift=0.)

        opm.radius_mode = False

        sm.gaps[0].thi = 1e10
        sm.add_surface([1. / X[1], X[2], 1.54, 75.0])

        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1. / X[1], ec=X[13],
                                                         coefs=[Y[0], Y[1], Y[2], Y[3], Y[4], Y[5], Y[6], Y[7]])

        # воздух
        sm.add_surface([1. / X[5], X[6]])
        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1. / X[5], ec=X[14],
                                                         coefs=[Y1[0], Y1[1], Y1[2], Y1[3], Y1[4], Y1[5], Y1[6], Y1[7]])

        sm.add_surface([1. / (X[7]), X[8], 1.67, 39.0])
        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1. / (X[7]), ec=X[15],
                                                         coefs=[Y2[0], Y2[1], Y2[2], Y2[3], Y2[4], Y2[5], Y2[6], Y2[7]])

        sm.add_surface([1. / (X[11]), X[12]])
        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1. / (X[11]), ec=X[16],
                                                         coefs=[Y3[0], Y3[1], Y3[2], Y3[3], Y3[4], Y3[5], Y3[6], Y3[7]])

        ap2 = Circular(0.51, x_offset=0.3)
        sm.ifcs[2].clear_apertures = [ap2]

        sm.add_surface([-1. / (X[17]), 0.8582010294386863, 1.54, 75.0])
        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=-1. / (X[17]), ec=3.229133607129681e-05,
                                                         coefs=[Y4[0], Y4[1], Y4[2], Y4[3], Y4[4], Y4[5], Y4[6], Y4[7]])

        sm.add_surface([-1. / (X[21]), 0.511712129719171])
        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=-1. / (X[21]), ec=X[23],
                                                         coefs=[Y5[0], Y5[1], Y5[2], Y5[3], Y5[4], Y5[5], Y5[6], Y5[7]])

        sm.add_surface([-1. / (-4.2352630401005415e-05), 0.2, 1.54, 75.0])
        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=-1. / (-4.2352630401005415e-05), ec=1.229133607129681e-05,
                                                         coefs=[Y6[0], Y6[1], Y6[2], Y6[3], Y6[4], Y6[5], Y6[6], Y6[7]])

        sm.add_surface([-1. / (3.370979820618158e-05), 0.70])
        sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=-1. / (3.370979820618158e-05), ec=X[23],
                                                         coefs=[Y7[0], Y7[1], Y7[2], Y7[3], Y7[4], Y7[5], Y7[6], Y7[7]])

        ap4 = Circular(0.12)
        sm.ifcs[4].clear_apertures = [ap4]

        opm.update_model()

        sm.do_apertures = True
        sm.stop_surface=1
        sm.cur_surface=9

        opm.save_model("test30.roa")
        try:
            loss = calc_loss("test30.roa")
        except Exception as e:
            print("Error")
            
        else:
            cur_loss = loss

            if ((cur_loss < last_loss)):
                last_loss = copy.deepcopy(cur_loss)
                
                print("Potential update ", cur_loss)
                if (cur_loss < best_loss):
                    print("Best value updated ")
                    best_loss = last_loss
                    bestX = copy.deepcopy(X)
                    bestY = copy.deepcopy(Y)
                    bestY1 = copy.deepcopy(Y1)
                    bestY2 = copy.deepcopy(Y2)
                    bestY3 = copy.deepcopy(Y3)
                    bestY4 = copy.deepcopy(Y4)
                    bestY5 = copy.deepcopy(Y5)
                    bestY6 = copy.deepcopy(Y6)
                    bestY7 = copy.deepcopy(Y7)
            else:
                stay_random = random.uniform(0., 1.)
                if stay_random > np.exp(-1. * abs(cur_loss - last_loss) * theta):
                    Y = copy.deepcopy(prevY)
                    X = copy.deepcopy(prev)
                    Y1 = copy.deepcopy(prevY1)
                    Y2 = copy.deepcopy(prevY2)
                    Y3 = copy.deepcopy(prevY3)
                    Y4 = copy.deepcopy(prevY4)
                    Y5 = copy.deepcopy(prevY5)
                    Y6 = copy.deepcopy(prevY6)
                    Y7 = copy.deepcopy(prevY7)
                else:
                    if (str(cur_loss).isnumeric()):
                        last_loss = cur_loss
                        print("Accepted ", cur_loss)
                    else:
                        print("None value found ", cur_loss)
                    

            print(cur_loss)
    except Exception as exception:
        print("Global error ! ")


for i in range(0, 1000):
    metropolis(len(X), len(Y))


print("X = ", bestX)
print("Y = ", bestY)
print("Y1 = ",bestY1)
print("Y2 = ",bestY2)
print("Y3 = ",bestY3)
print("Y4 = ",bestY4)
print("Y5 = ",bestY5)
print("Y6 = ",bestY6)
print("Y7 = ",bestY7)
print(best_loss)