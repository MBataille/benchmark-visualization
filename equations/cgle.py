import numpy as np
from equations.equation import Equation

class ComplexGinzburgLandau(Equation):
    def __init__(self):
        params = {'b': 0.2,
                  'c': 1,
                  'dx': 0.5}
        super().__init__('ComplexGinzburgLandau', params, 300,
                         field_names=['Re A', 'Im A'])
    
    def rhs(self, t, Re, Im, **params):
        b, c, dx = params['b'], params['c'], params['dx']
        A = Re + 1j * Im
        
        A_ip1 = np.roll(A, -1, axis=0)
        A_im1 = np.roll(A, 1, axis=0)
        A_jp1 = np.roll(A, -1, axis=1)
        A_jm1 = np.roll(A, 1, axis=1)
        laplacian = (A_ip1 + A_im1 + A_jp1 + A_jm1 - 4 * A) / dx ** 2
    
        dA = A + (1 + 1j * b) * laplacian - (1 + 1j * c) * A * (Re * Re + Im * Im)
        return dA.real, dA.imag
        