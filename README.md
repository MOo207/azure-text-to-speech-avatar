# Azure Arabic Text-to-Speech Talking Avatar

This project provides a Python script to create a Talking Avatar using Microsoft Azure's Text-to-Speech service. With the avatar synthesis API, you can transform Arabic text input into a spoken avatar video, allowing interactive and engaging voice experiences in Arabic. This example uses Azure’s `ar-SA-HamedNeural` voice for the avatar's speech synthesis.

## Demo
Check out a demo of the talking avatar in action:

[Watch the Demo Video](https://github.com/MOo207/azure-text-to-speech-avatar/raw/master/demo.webm)

## Features
- **Arabic Language Support**: Utilizes the `ar-SA-HamedNeural` voice for natural Arabic speech.
- **Customizable Avatars**: Includes options for custom or pre-built avatar characters and styles.
- **High-Quality Video Output**: Supports MP4 and WebM video formats with various codec options.
- **Azure-Based Authentication**: Integrates Azure Identity for passwordless, secure access to Azure resources.

## Prerequisites
1. **Azure Account**: An active Azure account with access to Azure Speech services.
2. **Azure Speech Service Resource**: Provision a Speech resource in one of the supported regions (*West US 2*, *West Europe*, or *Southeast Asia*).
3. **Environment Configuration**: You’ll need to configure your Azure subscription key and service region.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Azure-Talking-Avatar
   ```
**Install Dependencies**: 
Ensure Python 3.8+ is installed, and then install required packages:

bash
Copy code
pip install azure-identity requests
Set Up Environment Variables: Create a .env file in the project root with your Azure details, or set the environment variables directly in the terminal:

dotenv
Copy code
# .env file
SUBSCRIPTION_KEY=<your_subscription_key>
SERVICE_REGION=<your_service_region>
Supported Regions: The Text-to-Speech avatar feature is only available in West US 2, West Europe, and Southeast Asia. Ensure your Speech Service resource is deployed in one of these regions.

Usage
To run the avatar synthesis job, follow these steps:

Run the Python Script: Execute the script by running:

bash
Copy code
python avatar_synthesis.py
Script Flow:

The script creates a unique job ID and submits an avatar synthesis job using the Arabic ar-SA-HamedNeural voice.
The script polls the job status periodically. Upon completion, it logs the download URL for the generated avatar video.
Configuration Options: Modify the following parameters in the script to customize your avatar:

Voice: Change voice in the synthesisConfig dictionary to use different Azure voices.
Avatar Settings: Modify avatarConfig to customize the avatar’s appearance, style, video format, and background.
Example Code
Here is a quick code overview for the core functionality:

python
Copy code
def submit_synthesis(job_id: str):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    headers = {'Content-Type': 'application/json'}
    headers.update(_authenticate())

    payload = {
        'synthesisConfig': {'voice': 'ar-SA-HamedNeural'},
        'inputKind': 'SSML',
        'inputs': [{'content': '<speak version="1.0" xml:lang="ar-SA"><voice name="ar-SA-HamedNeural">مرحبا, أنا أعربلي, مساعدك الذكي للإعراب</voice></speak>'}],
        'avatarConfig': {
            'talkingAvatarCharacter': 'Harry',
            'talkingAvatarStyle': 'business',
            'videoFormat': 'mp4',
            'subtitleType': 'soft_embedded',
            'backgroundColor': '#FFFFFFFF',
        }
    }

    response = requests.put(url, json=payload, headers=headers)
    if response.status_code < 400:
        logger.info('Job submitted successfully')
    else:
        logger.error(f'Submission failed: {response.text}')
References
Azure Text-to-Speech Avatar Documentation
Troubleshooting
Authentication Issues: Ensure DefaultAzureCredential can locate your Azure account credentials (Azure CLI or Managed Identity).
Region Errors: If you encounter region-related errors, verify your Speech resource is in a supported region (West US 2, West Europe, Southeast Asia).
Debugging: Set logging level to DEBUG in the script for more verbose output:
python
Copy code
logging.basicConfig(level=logging.DEBUG, ...)
License
This project is licensed under the MIT License. See the LICENSE file for details.
