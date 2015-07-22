'''Module containing only the DataSet class'''
from django.db import models
from StatsModel import StatsModel
from Reaction import Reaction

class DataSet(models.Model):
  '''The DataSet class describes the relationship between a statistical model and
  the reactions used to either build or test that model.
  '''

  class Meta:
    app_label='DRP'

  reaction=models.ForeignKey(Reaction)
  model=models.ForeignKey(StatsModel)
  isTestSet=models.BooleanField()
  isTrainingSet=models.BooleanField()
