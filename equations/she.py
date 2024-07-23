import numpy as np
from equations.equation import Equation

class SwiftHohenberg(Equation):
    def __init__(self):
        params = {'epsilon': 1.6,
                  'nu': 1.0,
                  'dx': 0.25}
        super().__init__('SwiftHohenberg', params, 200)
    
    def rhs(self, t, u, **params):
        epsilon, nu, dx = params['epsilon'], params['nu'], params['dx']
        
        u_ft = np.fft.fft2(u)
        ks = 2 * np.pi * np.fft.fftfreq(self.N) / dx
        Kx, Ky = np.meshgrid(ks, ks)
        
        # laplacian = np.fft.ifft2(u_ft * (-Kx ** 2 - Ky ** 2)).real
        # bilaplacian = np.fft.ifft2(u_ft * (Kx ** 4 + Ky ** 4)).real
        
        u_ip1 = np.roll(u, -1, axis=0)
        u_im1 = np.roll(u, 1, axis=0)
        u_jp1 = np.roll(u, -1, axis=1)
        u_jm1 = np.roll(u, 1, axis=1)
        laplacian = (u_ip1 + u_im1 + u_jp1 + u_jm1 - 4 * u) / dx ** 2
        bilaplacian = (np.roll(u, 2, axis=0) + np.roll(u, -2, axis=0) \
            + np.roll(u, 2, axis=1) + np.roll(u, -2, axis=1) \
            - 4 * u_ip1 - 4 * u_im1 - 4 * u_jp1 - 4 * u_jm1 + 12 * u) / dx ** 4
    
        return epsilon * u - u * u * u - nu * laplacian - bilaplacian
        