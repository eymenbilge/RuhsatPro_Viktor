from .core import *
from .errors import *
from .geometry import *
from .parametrization import *
from .result import *
from .utils import *
from .views import *
from .__version__ import __version__ as __version__

from viktor import (
    api_v1 as api_v1,
    external as external,
    geo as geo,
    testing as testing,
)

from .external import (
    idea_rcs as idea_rcs,
    scia as scia,
    axisvm as axisvm,
    dfoundations as dfoundations,
    dgeostability as dgeostability,
    dsettlement as dsettlement,
    dsheetpiling as dsheetpiling,
    dstability as dstability,
    dynamo as dynamo,
    excel as excel,
    grasshopper as grasshopper,
    grlweap as grlweap,
    rfem as rfem,
    robot as robot,
    spreadsheet as spreadsheet,
    word as word,
)
