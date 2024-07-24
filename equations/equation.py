from abc import ABC, abstractmethod
import numpy as np
from scipy.integrate import RK45
from typing import Iterable

class Equation:
    def __init__(self, name: str, params: dict[str, float], N: int, dim: int = 2, field_names: list[str] = ['u'],
                 solver_class = RK45):
        self.name = name
        self.params = params
        self.N = N
        self.dim = dim
        self.n_fields = len(field_names)
        self.field_names = field_names
        self.set_intial_condition_zero()
        self.solver_class = solver_class
        self.initialize_solver()
        
    @abstractmethod
    def rhs(self, t, *fields, **params):
        pass
    
    def initialize_solver(self):
        self.solver = self.solver_class(
            self.wrapper_rhs, 0, self.pack_fields(self.initial_fields), 
            1_000, max_step=1e-1)
    
    def wrapper_rhs(self, t, Y):
        rhs = self.rhs(t, *self.unpack_fields(Y), **self.params)
        return self.pack_fields(rhs)
    
    def pack_fields(self, fields):
        N2 = self.N * self.N
        if type(fields) == np.ndarray:
            return fields.ravel()
        
        packed_fields = np.empty(N2 * self.n_fields)
        for k, field in enumerate(fields):
            packed_fields[k * N2:(k+1) * N2] = field.ravel()
        return packed_fields
    
    def unpack_fields(self, packed_fields):
        N2 = self.N * self.N
        return [packed_fields[k * N2:(k+1) * N2].reshape(self.N, self.N)\
            for k in range(self.n_fields)]
    
    def step(self):
        self.solver.step()
        
    def get_current_state(self):
        return self.unpack_fields(self.solver.y)
    
    def get_current_time(self):
        return self.solver.t
    
    def set_params(self, params):
        self.params = params
        
    def set_initial_condition(self, initial_condition):
        self.initial_fields = initial_condition
        self.initialize_solver()
        # self.initial_fields = initial_condition
        # self.solver.y = self.pack_fields(initial_condition)

    def set_intial_condition_zero(self):
        # ## change this
        # x = np.linspace(-5, 5, self.N)
        # X, Y = np.meshgrid(x, x)
        # self.initial_fields = np.random.normal(size=(self.N, self.N)) * np.exp(-X*X-Y*Y)
        N = self.N
        xs = np.arange(N)
        X, Y = np.meshgrid(xs, xs)
        self.initial_fields = [0.1 * np.random.normal(size=(N,N))\
            for k in range(self.n_fields)]
        
    def get_initial_condition(self):
        return self.initial_fields

    def get_params(self):
        return self.params
    
    def get_ik(self):
        """Returns the vector corresponding to ik and shifted"""
        return 2j * np.pi / (self.params['dx'] * self.N) * np.fft.fftfreq(self.N)\
                * self.N 

    def get_k(self):
        return 2 * np.pi / (self.params['dx'] * self.N) * np.fft.fftfreq(self.N) * self.N

    def spectral_deriv(self, u_ft, order, real=False, axis=0):
        """Returns the spectral derivative of the specified order
        of a given array u_ft (already in fourier space)"""
        ik = self.get_ik() ** order
        R = np.fft.ifft(ik * u_ft, axis=axis)

        if real:
            return R.real
        return R
        