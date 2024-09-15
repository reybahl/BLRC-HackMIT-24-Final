import requests
import os

# Replace the empty string with your model id below
model_id = "7qkpp7dw"
baseten_api_key = "Us98UpGt.GfMVx8t9i7EN5Tr2oS13ZhtPhtY3uWag"

def get_relevant_objects(objects):
    data = {
        "prompt": f"""You are given a list of objects identified by an image segmentation model. Follow these instructions carefully:

    1. Choose \emphasize{{at least one object}} and \emphasize{{no more than five}} that are not background objects.
    2. The number of selected objects \emphasize{{must be less than or equal to half}} of the total number of objects in the list.
    3. Return the selected objects in a comma-separated list, and enclose them in square brackets.
    4. Do not give explanations or context, and \emphasize{{do not exceed the specified limit.}}
    Here is the list of objects you must predict on:

    {objects}

    Here are some examples:
    input: painting, sky, person, wall, screen
    output: ['person']

    input: animal, person, sky
    output: ['animal', 'person']
    """,
        "stream": True,
        "max_tokens": 1024
    }

    # Call model endpoint
    res = requests.post(
        f"https://model-{model_id}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {baseten_api_key}"},
        json=data,
        stream=True
    )

    generated_string = ""
    # Print the generated tokens as they get streamed
    for content in res.iter_content():
        generated_string += content.decode("utf-8")

    ans = []
    for obj in objects:
        if obj in generated_string:
            ans.append(obj)
    return ans