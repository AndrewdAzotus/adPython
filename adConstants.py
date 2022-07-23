#!/usr/bin/python3
import os

HostName = os.uname()[1]

SQLSrvr = "192.168.136.110"
if HostName == "london":
  SQLSrvr = "localhost"

dbAccessDetails = {
  "CanopyUser" : "Canopy",
  "CanopyPswd" : "Shelter",
  "PrimesUser" : "PrimesCalc",
  "PrimesPswd" : "Eratos"
}
