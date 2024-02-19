from django.contrib import admin

from .models import *


admin.site.register([
    NLPEventModel,
    NLPEvents,
    NLPModels,
    NLPInputTexts,
    NLPCacheTexts,
    NLPTrainReservation,
    NLPTrainData,
    NLPConfig,
])
