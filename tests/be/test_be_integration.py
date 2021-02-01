#-*- coding: utf-8 -*-
import os, sys, io
import requests
import pytest
import pydicom
import json, time
from common import api_test_util as util

integration = pytest.mark.integration

#@integration
def test_intg_001():
    print("I am running")
    assert 1==2
