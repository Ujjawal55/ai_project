#!/usr/bin/env python
# coding: utf-8

# ## Take image input:

# In[37]:


from PIL import Image

# image_path = "./fruit.jpg"
image_path = "./food2.jpg"
img = Image.open(image_path)
img_format = img.format

print(img.size)
im_x, im_y = img.size

width_needed = 240
if im_x > width_needed:
    resize_factor = im_x / width_needed

    res_img = img.resize((int(im_x / resize_factor), int(im_y / resize_factor)))
    res_img.format = img_format

print(res_img.size)
res_img.save("temp.jpg")
# img.save("temp.jpg", format=img_format)
res_img


# ## Convert to bytes:

# In[38]:

import io
import PIL


def input_image_setup(pil_image):
    """Converts a PIL image to a list of dictionaries suitable for Gemini input.
    Args:
        pil_image: A PIL Image object.
    Returns:
        A list of dictionaries, each containing mime_type and data for the image.
    """

    if not isinstance(pil_image, PIL.Image.Image):
        raise ValueError("Input must be a PIL Image object.")

    # Choose the appropriate format based on your model's requirements
    # image_format = "JPEG"  # Adjust if needed for PNG, etc.
    image_format = pil_image.format

    with io.BytesIO() as output:
        pil_image.save(output, format=image_format)
        bytes_data = output.getvalue()

    print()
    image_parts = [{"mime_type": f"image/{image_format.lower()}", "data": bytes_data}]

    return image_parts


# Open the image using PIL
# img = Image.open("./temp.jpg")
im_bytes = input_image_setup(res_img)


# In[39]:


img.format


# In[40]:


# im_bytes
# dat = im_bytes[0]['data']


# # Gemini API:

# In[41]:


import json
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os


# In[42]:


# import os
# print("yes") if 'API' in list(os.environ) else "nope"


# In[43]:


# API = "your_key"
load_dotenv("key.env")

API_KEY = os.getenv("API")
genai.configure(api_key=API_KEY)


# In[44]:


def get_gemini_response(image_data):
    """
    Image data parameter is `not PIL Image`, it is `io image`.
    """

    # name = 'gemini-1.5-pro'
    name = "gemini-1.5-flash"

    generation_config = {
        "temperature": 1.5,  # accurate 0 to 2 creative
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        # "response_mime_type": "text/plain",
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(model_name=name, generation_config=generation_config)

    output_type = "application/json"

    system_instr = """
        You are an expert nutritionist. Analyze the food items in the image and calculate the total calories. Get me the calories details from the image.
        You Never respond with errors or 'sorry not possible' type of responses. If nothing is possible or there is some ambiguity, then just assume things and make up an approximate response.
        At any cost, dont go out of output format. Just keep one main assumption and don't make multiple cases under it. Go with one of the cases when needed.
    """

    output_format = """
    [
        {
            "item1": string (item name),
            "calories": string (60 calories etc.)
            "no_of_instances": integer
        },
        {
            "item2": string (item name),
            "calories": string (45 calories etc.)
            "no_of_instances": integer
        },
        ...,
        {
            "total_cal" : string (total cal of all things together)
            "assumptions_made": string (maximum 30 words.)
        }
    ]
    """

    main_prompt = """
        Provide the details of each food item and its calorie count.
        Dont go out of output's json format asked!
    """

    # Combine input and prompt into a single string
    combined_prompt = f"""
        System Instruction:
            {system_instr}        
        \n\n\n
        Output Type:
            {output_type}
        \n\n\n
        Output Format:
            {output_format}
        \n\n\n
        Prompt:
            {main_prompt}
        \n\n\n
        Image Data:
            {image_data[0]}
    """

    try:
        response = model.generate_content(contents=(combined_prompt, image_data[0]))
        return response

    except (TypeError, ValueError) as e:
        # Handle potential errors gracefully, e.g., log the error or provide informative feedback
        error_message = f"Error generating response: {e}"
        return None  # Or return an empty string or default value


# In[45]:


import time

t1 = time.time()
response = get_gemini_response(im_bytes)
t2 = time.time()


print(f"Generated response in {round(t2-t1, 2)} secs")
response


# In[46]:


print(f"Generated response in {round(t2-t1, 2)} secs")


# In[50]:


import json

j = json.loads(response.text)
j


# In[25]:


# import json
# j = [{'item1': 'apple', 'calories': '100 calories', 'no_of_instances': 4},
#      {'item2': 'banana', 'calories': '105 calories', 'no_of_instances': 1},
#      {'total_cal': '920 calories',
#      'assumptions_made': 'Assuming all fruits are medium size.'}]

print(json.dumps(j, indent=4))


# In[31]:


print("\n" * 2)
print("\033[94m" + "-" * 80 + "\033[0m")
print("\n" * 2)
for ind, item in enumerate(j):
    print(f"Item Number {ind}: ", end="")
    print(json.dumps(item, indent=4))
    print()


# In[ ]:


# In[ ]:


# In[ ]:


# In[48]:


# Combine input and prompt into a single string
# import sys
# combined_prompt = f"""generate 500 word essay on porsche"""

# resp = model.generate_content(contents=(combined_prompt), stream=True)

# for chunk in resp:
#     sys.stdout.write(chunk.text)
#     sys.stdout.write("\n")
#     sys.stdout.flush()

# import IPython.display
# display.Markdown(item)
