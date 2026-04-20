import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from scipy import stats as scipy_stats
from typing import Dict, Optional


class DistribucionEstadistica(ABC):

    @abstractmethod
    def ajustar(self, datos: pd.Series) -> Dict:
        pass

    @abstractmethod
    def generar(self, n: int = 1) -> float:
        pass

    @abstractmethod
    def pdf(self, x: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def cdf(self, x: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def get_parametros(self) -> Dict:
        pass

    @abstractmethod
    def get_nombre(self) -> str:
        pass


class DistribucionNormal(DistribucionEstadistica):
    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        self.mu = mu
        self.sigma = sigma
        self._ajustado = False

    def ajustar(self, datos: pd.Series) -> Dict:
        mu, sigma = scipy_stats.norm.fit(datos)
        self.mu = mu
        self.sigma = sigma
        self._ajustado = True
        ks_stat, ks_pvalue = scipy_stats.kstest(datos, 'norm', args=(mu, sigma))
        return {
            "distribucion": "Normal",
            "param1": mu,
            "param2": sigma,
            "param3": None,
            "gof_metric": "KS",
            "gof_value": ks_pvalue,
            "notas": f"mu={mu:.4f}, sigma={sigma:.4f}"
        }

    def generar(self, n: int = 1) -> float:
        if not self._ajustado:
            raise RuntimeError("Debe ajustar antes de generar")
        valores = np.random.normal(self.mu, self.sigma, n)
        return valores if n > 1 else valores[0]

    def pdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.norm.pdf(x, self.mu, self.sigma)

    def cdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.norm.cdf(x, self.mu, self.sigma)

    def get_parametros(self) -> Dict:
        return {"mu": self.mu, "sigma": self.sigma}

    def get_nombre(self) -> str:
        return "Normal"


class DistribucionWeibull(DistribucionEstadistica):
    def __init__(self, shape: float = 1.0, scale: float = 1.0, loc: float = 0.0):
        self.shape = shape
        self.scale = scale
        self.loc = loc
        self._ajustado = False

    def ajustar(self, datos: pd.Series) -> Dict:
        shape, loc, scale = scipy_stats.weibull_min.fit(datos, floc=0)
        self.shape = shape
        self.scale = scale
        self.loc = loc
        self._ajustado = True
        ks_stat, ks_pvalue = scipy_stats.kstest(
            datos, 'weibull_min', args=(shape, loc, scale)
        )
        return {
            "distribucion": "Weibull",
            "param1": scale,
            "param2": shape,
            "param3": loc,
            "gof_metric": "KS",
            "gof_value": ks_pvalue,
            "notas": f"forma={shape:.4f}, escala={scale:.4f}"
        }

    def generar(self, n: int = 1) -> float:
        if not self._ajustado:
            raise RuntimeError("Debe ajustar antes de generar")
        valores = scipy_stats.weibull_min.rvs(self.shape, loc=self.loc, scale=self.scale, size=n)
        return valores if n > 1 else valores[0]

    def pdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.weibull_min.pdf(x, self.shape, loc=self.loc, scale=self.scale)

    def cdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.weibull_min.cdf(x, self.shape, loc=self.loc, scale=self.scale)

    def get_parametros(self) -> Dict:
        return {"forma": self.shape, "escala": self.scale, "loc": self.loc}

    def get_nombre(self) -> str:
        return "Weibull"


class DistribucionLogNormal(DistribucionEstadistica):
    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        self.mu = mu
        self.sigma = sigma
        self._ajustado = False

    def ajustar(self, datos: pd.Series) -> Dict:
        mu, sigma = scipy_stats.lognorm.fit(datos, floc=0)
        self.mu = mu
        self.sigma = sigma
        self._ajustado = True
        ks_stat, ks_pvalue = scipy_stats.kstest(
            datos, 'lognorm', args=(mu, 0, sigma)
        )
        return {
            "distribucion": "LogNormal",
            "param1": sigma,
            "param2": mu,
            "param3": None,
            "gof_metric": "KS",
            "gof_value": ks_pvalue,
            "notas": f"mu_log={mu:.4f}, sigma_log={sigma:.4f}"
        }

    def generar(self, n: int = 1) -> float:
        if not self._ajustado:
            raise RuntimeError("Debe ajustar antes de generar")
        valores = scipy_stats.lognorm.rvs(self.mu, loc=0, scale=np.exp(self.sigma), size=n)
        return valores if n > 1 else valores[0]

    def pdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.lognorm.pdf(x, self.mu, loc=0, scale=np.exp(self.sigma))

    def cdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.lognorm.cdf(x, self.mu, loc=0, scale=np.exp(self.sigma))

    def get_parametros(self) -> Dict:
        return {"mu_log": self.mu, "sigma_log": self.sigma}

    def get_nombre(self) -> str:
        return "LogNormal"


class DistribucionGamma(DistribucionEstadistica):
    def __init__(self, shape: float = 1.0, scale: float = 1.0):
        self.shape = shape
        self.scale = scale
        self._ajustado = False

    def ajustar(self, datos: pd.Series) -> Dict:
        shape, loc, scale = scipy_stats.gamma.fit(datos, floc=0)
        self.shape = shape
        self.scale = scale
        self._ajustado = True
        ks_stat, ks_pvalue = scipy_stats.kstest(
            datos, 'gamma', args=(shape, 0, scale)
        )
        return {
            "distribucion": "Gamma",
            "param1": shape,
            "param2": scale,
            "param3": None,
            "gof_metric": "KS",
            "gof_value": ks_pvalue,
            "notas": f"forma={shape:.4f}, escala={scale:.4f}"
        }

    def generar(self, n: int = 1) -> float:
        if not self._ajustado:
            raise RuntimeError("Debe ajustar antes de generar")
        valores = scipy_stats.gamma.rvs(self.shape, loc=0, scale=self.scale, size=n)
        return valores if n > 1 else valores[0]

    def pdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.gamma.pdf(x, self.shape, loc=0, scale=self.scale)

    def cdf(self, x: np.ndarray) -> np.ndarray:
        return scipy_stats.gamma.cdf(x, self.shape, loc=0, scale=self.scale)

    def get_parametros(self) -> Dict:
        return {"forma": self.shape, "escala": self.scale}

    def get_nombre(self) -> str:
        return "Gamma"


FABRICA_DISTRIBUCIONES = {
    "Normal": DistribucionNormal,
    "Weibull": DistribucionWeibull,
    "LogNormal": DistribucionLogNormal,
    "Gamma": DistribucionGamma,
}


def crear_distribucion(nombre: str, **kwargs) -> DistribucionEstadistica:
    if nombre not in FABRICA_DISTRIBUCIONES:
        raise ValueError(f"Distribucion no reconocida: {nombre}")
    return FABRICA_DISTRIBUCIONES[nombre](**kwargs)
