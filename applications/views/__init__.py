from .govdata import GetPassportInfoFromGov
from .application import ApplicationCreateAPIView, ApplicationListAPIView
from .passport import (
    RegionListAPIView,
    DistrictByRegionAPIView,
    PassportInfoCreateAPIView,
    PassportInfoRetrieveAPIView,
)
from .diplom import (
    DiplomInfoCreateAPIView,
    DiplomInfoRetrieveAPIView,
)

__all__ = [
    "GetPassportInfoFromGov",
    "ApplicationCreateAPIView",
    "ApplicationListAPIView",
    "RegionListAPIView",
    "DistrictByRegionAPIView",
    "PassportInfoCreateAPIView",
    "PassportInfoRetrieveAPIView",

    "DiplomInfoCreateAPIView",
    "DiplomInfoRetrieveAPIView",
]
