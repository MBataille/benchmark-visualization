import numpy as np
from equations.equation import Equation

class SwiftHohenberg(Equation):
    def __init__(self):
        params = {'epsilon': .02,
                  'nu': 1.0,
                  'dx': 0.5}
        super().__init__('SwiftHohenberg', params, 200)
    
    def rhs(self, t, u, **params):
        epsilon, nu, dx = params['epsilon'], params['nu'], params['dx']
        
        # u_ft = np.fft.fft2(u)
        # ks = 2 * np.pi * np.fft.fftfreq(self.N) / dx
        # Kx, Ky = np.meshgrid(ks, ks)
        
        
        
        u_ip1 = np.roll(u, -1, axis=0)
        u_im1 = np.roll(u, 1, axis=0)
        u_jp1 = np.roll(u, -1, axis=1)
        u_jm1 = np.roll(u, 1, axis=1)
        laplacian = (u_ip1 + u_im1 + u_jp1 + u_jm1 - 4 * u) / dx ** 2
        # bilaplacian = (np.roll(u, 2, axis=0) + np.roll(u, -2, axis=0) \
        #     + np.roll(u, 2, axis=1) + np.roll(u, -2, axis=1) \
        #     - 4 * u_ip1 - 4 * u_im1 - 4 * u_jp1 - 4 * u_jm1 + 12 * u) / dx ** 4
    
        # 13-point stencil
        bilaplacian = (np.roll(u, 2, axis=0) + np.roll(u, -2, axis=0) \
            + np.roll(u, 2, axis=1) + np.roll(u, -2, axis=1) \
            + 2 * np.roll(u_ip1, -1, axis=1) + 2 * np.roll(u_ip1, 1, axis=1) \
            + 2 * np.roll(u_im1, -1, axis=1) + 2 * np.roll(u_im1, 1, axis=1) \
            - 8 * u_ip1 - 8 * u_im1 - 8 * u_jp1 - 8 * u_jm1 + 20 * u) / dx ** 4

        return epsilon * u - u * u * u - nu * laplacian - bilaplacian
        