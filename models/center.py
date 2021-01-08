from .institute import Institute
from .university import University


class Center(Institute):
    """Research center that is not a university"""
    __parent_data_points__ = (University,)
