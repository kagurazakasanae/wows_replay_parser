import json, os, sys
items = json.load(open(sys.path[0]+'/db/data.json', 'r'))
ships = json.load(open(sys.path[0]+'/db/ship.json', 'r'))
crew = json.load(open(sys.path[0]+'/db/crew.json', 'r'))
flags = [
 [
  'IDS_PCEF016_NE7_SIGNALFLAG', 'NE7', ','],
 [
  'IDS_PCEF012_MY6_SIGNALFLAG', 'MY6', ','],
 [
  'IDS_PCEF018_IX_SIGNALFLAG', 'IX', ','],
 [
  'IDS_PCEF019_JW1_SIGNALFLAG', 'JW1', ','],
 [
  'IDS_PCEF017_VL_SIGNALFLAG', 'VL', ','],
 [
  'IDS_PCEF006_HY_SIGNALFLAG', 'HY', ';'],
 [
  'IDS_PCEF014_NF_SIGNALFLAG', 'NF', ','],
 [
  'IDS_PCEF005_SM_SIGNALFLAG', 'SM', ','],
 [
  'IDS_PCEF007_ID_SIGNALFLAG', 'ID', ','],
 [
  'IDS_PCEF009_JY2_SIGNALFLAG', 'JY2', ','],
 [
  'IDS_PCEF008_IY_SIGNALFLAG', 'IY', ','],
 [
  'IDS_PCEF010_JC_SIGNALFLAG', 'JC', ';'],
 [
  'IDS_PCEF001_ZULU_SIGNALFLAG', 'Zulu', ','],
 [
  'IDS_PCEF011_IB3_SIGNALFLAG', 'IB3', ','],
 [
  'IDS_PCEF003_EQUALSPEED_SIGNALFLAG', 'EqSp', ','],
 [
  'IDS_PCEF015_ZH_SIGNALFLAG', 'ZH', ','],
 [
  'IDS_PCEF013_PP_SIGNALFLAG', 'PP', ';'],
 [
  'IDS_PCEF021_WYVERN_FLAG', 'Wyvern', ','],
 [
  'IDS_PCEF022_RED_DRAGON_FLAG', 'Red Dragon', ','],
 [
  'IDS_PCEF020_BLUE_DRAGON_FLAG', 'Blue Dragon', ','],
 [
  'IDS_PCEF023_OUROBOROS_FLAG', 'Ouroboros', ','],
 [
  'IDS_PCEF024_HYDRA_FLAG', 'Hydra', ','],
 [
  'IDS_PCEF027_LEVIATHAN_FLAG', 'Leviathan', ','],
 [
  'IDS_PCEF026_SCYLLA_FLAG', 'Scylla', ','],
 [
  'IDS_PCEF025_BASILISK_FLAG', 'Basilisk', '.']]

