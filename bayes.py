from numpy import Infinity
from calc_parse_loss import calc_loss
isdark = False
# use standard rayoptics environment
from rayoptics.environment import *
from bayes_opt import BayesianOptimization
# util functions
from rayoptics.util.misc_math import normalize

#, r1, thi1, n1, v1, r2, thi2, r3, thi3, n3, v3, r4, thi4, ec1, ec2, ec3
def function(thi1,thi2, thi3, thi4):
    opm = OpticalModel()
    sm = opm['seq_model']
    osp = opm['optical_spec']
    pm = opm['parax_model']
    em = opm['ele_model']
    pt = opm['part_tree']

    opm.system_spec.dimensions = 'mm'
    osp['pupil'] = PupilSpec(osp, key=['object', 'pupil'], value=2.5)
    osp['fov'] = FieldSpec(osp, key=['object', 'angle'],  value=0.05, is_relative=True, flds=[0., 5., 10., 15., 20.])
    osp['wvls'] = WvlSpec([(470, 1.0), (650, 1.0)], ref_wl=1)


    osp.defocus = FocusRange(focus_shift=-0.01737)

    opm.radius_mode = False

    sm.gaps[0].thi=1e10

    sm.add_surface([1./0.2747823174694503, thi1, 1.54, 58.])
    sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1./0.2747823174694503, ec=0.979069624564, coefs=[0., 0.009109298409282469, -0.03374649200850791, 0.01797256809388843,  -0.0050513483804677005, 0.0, 0.0, 0.0])

    #воздух
    sm.add_surface([1./0.13556582944950138, thi2])
    sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=1./0.13556582944950138, ec=0.9,
                            coefs=[0., -0.002874728268075267, -0.03373322938525211, 0.004205227876537139, -0.0001705765222318475, 0., 0., 0.])


    sm.add_surface([-1./(0.055209803982245384), thi3, 1.67, 49.])
    sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=-1./(0.055209803982245384), ec=1.1,
                            coefs=[0.0, -0.0231369463217776, 0.011956554928461116,-0.017782670650182023,0.004077846642272649, 0.0, 0.0, 0.0])

    sm.add_surface([1./(-0.2548888474926888), thi4])
    sm.ifcs[sm.cur_surface].profile = Spherical(r=1./(-0.2548888474926888))

    opm.update_model()
    
    sm.do_apertures = True
    sm.stop_surface=1
    sm.cur_surface=5

    opm.save_model("test30.roa")
    try:
        loss = calc_loss("test30.roa")
    except Exception as e:
        print("Ошибка")
    else:
        print(loss)
        return -1. * loss


param_space = {
    'thi1': (0.9, 1.1),
    'thi2': (0.5, 0.55),
    'thi3': (0.9, 1.1),
    'thi4': (4.0, 4.5)
}


optimizer = BayesianOptimization(
    f=function,
    pbounds=param_space,
    random_state=42
)

# Выполните оптимизацию
optimizer.maximize(init_points=10, n_iter=100)  # Задайте количество начальных точек и итераций

# Получите лучшие параметры и значение целевой функции
best_params = optimizer.max['params']
best_value = optimizer.max['target']

print("Лучшие параметры:", best_params)
print("Лучшее значение целевой функции:", best_value)
print("Best loss ", -1.*best_value)