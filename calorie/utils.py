from PIL import Image
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os
from calorie.models import Food


def getContent(file_name):
    file = Food.objects.get(name=file_name)  # type: ignore
    image_path = file.image.path
    img = Image.open(image_path)
    img_format = img.format

    im_x, im_y = img.size

    width_needed = 240

    if im_x > width_needed:
        resize_factor = im_x / width_needed

        res_img = img.resize((int(im_x / resize_factor), int(im_y / resize_factor)))
        res_img.format = img_format

    res_img.save("temp.jpg")
    res_img

    import io
    import PIL

    def input_image_setup(pil_image):
        """Converts a PIL image to a list of dictionaries suitable for Gemini input.
        Args:
            pil_image: A PIL Image object.
        Returns:
            A list of dictionaries, each containing mime_type and data for the image.
        """

        if not isinstance(pil_image, PIL.Image.Image):  # type:ignore
            raise ValueError("Input must be a PIL Image object.")

        image_format = pil_image.format

        with io.BytesIO() as output:
            pil_image.save(output, format=image_format)
            bytes_data = output.getvalue()

        image_parts = [
            {"mime_type": f"image/{image_format.lower()}", "data": bytes_data}
        ]

        return image_parts

    im_bytes = input_image_setup(res_img)

    img.format

    load_dotenv("key.env")

    API_KEY = os.getenv("API")
    genai.configure(api_key=API_KEY)

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

        model = genai.GenerativeModel(
            model_name=name, generation_config=generation_config
        )  # type: ignore

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
            return None  # Or return an empty string or default value

    response = get_gemini_response(im_bytes)

    j = json.loads(response.text)  # type: ignore
    return j
