import os
import unittest

from pwperformance.loggers import InfluxHandler
import logging

INFLUX_TOKEN = "INFLUX_TOKEN"

logger = logging.getLogger(__file__)

class TestInfluxHandler(unittest.TestCase):

    def testBasicSend(self):
        # Keys indexed by influx: search and filtering can only be done on this elements

        bucket = "scipion-benchmarks"
        org = "CNB"
        token = os.environ.get(INFLUX_TOKEN, None)

        if token is None:
            # Cancel the test
            logger.warning("Missing credentials to run this test. %s not set" % INFLUX_TOKEN)
            return

        indexed_keys = ["project_name",	"prot_id" ,"prot_name", "step_id"]
        ih = InfluxHandler(token= token, org= org, bucket= bucket, indexed_keys=indexed_keys, measurement="testBasicSend")
        logger.addHandler(ih)
        logger.setLevel(logging.INFO)
        logger.info("Testing sending data", extra=getExtraLogInfo("myproject", "START", prot_id=1, prot_name="ProtClass", step_id=1, duration=3.4))
        logger.info("Testing sending data")

def getExtraLogInfo(project_name, status, prot_id=None, prot_name=None, step_id=None , duration=None):
    # Add TS!! optionally
    return {"project_name": project_name,
            "status": status,
            "prot_id": prot_id,
            "prot_name": prot_name,
            "step_id": step_id,
            "duration": duration
    }