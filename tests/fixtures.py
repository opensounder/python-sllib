
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

SL2_CORRUPT_PARTLY = os.path.join(BASEDIR, 'sample-data-lowrance',
                                      'other', 'corrupt_partly.sl2')

SL3_V1_A = os.path.join(
    BASEDIR, 'sample-data-lowrance', 'other', 'sonar-log-api-testdata.sl3')

SL3_V2_A = os.path.join(
    BASEDIR, 'sample-data-lowrance', 'other', 'format3_version2.sl3')

SL2 = (
    SL2_SMALL,
    SL2_V1,
    SL2_SOUTHERN1,
    SL2_CORRUPT_PARTLY
)

SL3 = (
    SL3_V1_A,
    SL3_V2_A
)