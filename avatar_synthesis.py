import json
import logging
import os
import sys
import time
import uuid
import requests
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

class SpeechServiceClient:
    def __init__(self, speech_endpoint=None, subscription_key=None, passwordless_authentication=False):
        self.speech_endpoint = speech_endpoint or os.environ.get('SPEECH_ENDPOINT')
        self.subscription_key = subscription_key or os.environ.get('SPEECH_KEY')
        self.api_version = "2024-08-01"
        self.passwordless_authentication = passwordless_authentication

    def _authenticate(self):
        if self.passwordless_authentication:
            token = DefaultAzureCredential().get_token('https://cognitiveservices.azure.com/.default')
            return {'Authorization': f'Bearer {token.token}'}
        return {'Ocp-Apim-Subscription-Key': self.subscription_key}

    def _create_job_id(self):
        return str(uuid.uuid4())

    def submit_synthesis(self, job_id, ssml_content, voice="ar-SA-HamedNeural"):
        url = f'{self.speech_endpoint}/avatar/batchsyntheses/{job_id}?api-version={self.api_version}'
        headers = {**self._authenticate(), 'Content-Type': 'application/json'}
        payload = {
            'synthesisConfig': {"voice": voice},
            "inputKind": "SSML",
            "inputs": [{"content": ssml_content}],
            "avatarConfig": {"customized": False, "talkingAvatarCharacter": 'Harry', "talkingAvatarStyle": 'business', "videoFormat": "mp4", "videoCodec": "h264", "subtitleType": "soft_embedded", "backgroundColor": "#FFFFFFFF"}
        }

        response = requests.put(url, json=payload, headers=headers)
        if response.status_code < 400:
            logger.info(f'Job submitted successfully, Job ID: {response.json()["id"]}')
            return True
        logger.error(f'Failed to submit job: [{response.status_code}] {response.text}')
        return False

    def get_synthesis(self, job_id):
        url = f'{self.speech_endpoint}/avatar/batchsyntheses/{job_id}?api-version={self.api_version}'
        headers = self._authenticate()
        response = requests.get(url, headers=headers)

        if response.status_code < 400:
            job_status = response.json().get('status')
            if job_status == 'Succeeded':
                result_url = response.json().get("outputs", {}).get("result")
                logger.info(f'Succeeded with download URL: {result_url}')
                return 'Succeeded', result_url
            return job_status, None
        logger.error(f'Failed to get job status: {response.text}')
        return 'Failed', None

def run_batch_synthesis():
    client = SpeechServiceClient()
    job_id = client._create_job_id()
    ssml_content = "<speak version=\"1.0\" xml:lang=\"ar-SA\"><voice name=\"ar-SA-HamedNeural\">مرحبا, أنا أعربلي, مساعدك الذكي للإعراب</voice></speak>"

    if client.submit_synthesis(job_id, ssml_content):
        while True:
            status, result = client.get_synthesis(job_id)
            if status == 'Succeeded':
                logger.info('Batch avatar synthesis job succeeded')
                return result
            elif status == 'Failed':
                logger.error('Batch avatar synthesis job failed')
                return None
            else:
                logger.info(f'Job still running, status: {status}')
                time.sleep(3)

if __name__ == '__main__':
    url = run_batch_synthesis()
    print(f'Avatar synthesis result URL: {url}')
