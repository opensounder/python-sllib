
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))


SL2_SMALL = os.path.join(BASEDIR,
                         'sample-data-lowrance',
                         'Elite_4_Chirp', 'small.sl2')
SL2_V1 = os.path.join(BASEDIR,
                      'sample-data-lowrance', 'Elite_4_Chirp',
                      'Chart 05_11_2018 [0].sl2')

SL2_SOUTHERN1 = os.path.join(BASEDIR, 'sample-data-lowrance',
                                      'HDS5', 'southern1.sl2')

SL3_FIRST = os.path.join(BASEDIR,
                         'sample-data-lowrance', 'unknown',
                         'sonar-log-api-testdata.sl3')
