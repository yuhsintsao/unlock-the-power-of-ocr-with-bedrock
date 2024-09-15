import os
import sys
import logging
from typing import Dict, Tuple
import boto3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the new package root to the system path
NEW_PACKAGE_ROOT = '/opt/ml/processing/script'
sys.path.insert(0, os.path.abspath(NEW_PACKAGE_ROOT))


def find_suitable_image_size(page) -> Tuple[int, int]:
    """
    Determine the suitable image size for a PDF page.
    
    Args:
        page: The PDF page object.
    
    Returns:
        A tuple containing the suitable width and height.
    """
    page_width, page_height = page.width, page.height
    logger.debug(f"PDF page dimensions: {page_width:.2f} x {page_height:.2f}")
    aspect_ratio = page_width / page_height
    
    # Define the accepted aspect ratios and corresponding image sizes
    accepted_ratios: Dict[Tuple[int, int], Tuple[int, int]] = {
        (1, 1): (1092, 1092),
        (3, 4): (951, 1268),
        (2, 3): (896, 1344),
        (9, 16): (819, 1456),
        (1, 2): (784, 1568)
    }
    
    # Find the most suitable aspect ratio
    closest_ratio = min(accepted_ratios.keys(), key=lambda x: abs(aspect_ratio - (x[0] / x[1])))
    suitable_width, suitable_height = accepted_ratios[closest_ratio]
    dpi = min(suitable_width / page_width * 72, suitable_height / page_height * 72)
    logger.debug(f"Calculated DPI: {dpi:.2f}")
    
    # Convert the page to an image
    image = page.to_image(resolution=int(dpi))
    image.save('output_image.png')
    
    return suitable_width, suitable_height

def generate_conversation(
    bedrock_client: boto3.client,
    model_id: str,
    system_text: str,
    input_text_pre: str,
    input_text_post: str,
    input_image: str
) -> Dict:
    """
    Generate a conversation using the Bedrock model.
    
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id: The model ID to use.
        system_text: The system message.
        input_text_pre: The input text before the image.
        input_text_post: The input text after the image.
        input_image: The path to the input image file.
    
    Returns:
        The conversation that the model generated.
    """
    logger.debug(f"Generating message with model {model_id}")
    with open(input_image, "rb") as f:
        image_data = f.read()
    
    inference_config = {"temperature": 0.5}
    additional_model_fields = {"top_k": 3}
    message = {
        "role": "user",
        "content": [
            {"text": input_text_pre},
            {"image": {"format": 'png', "source": {"bytes": image_data}}},
            {"text": input_text_post}
        ]
    }
    
    response = bedrock_client.converse(
        modelId=model_id,
        system=[{"text": system_text}],
        messages=[message],
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields
    )
    
    logger.debug(f"Model response: {response}")
    return response

