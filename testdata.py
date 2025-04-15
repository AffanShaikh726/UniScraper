from openAI import jsonifyDataAI

def base_data(file_path="baseData.txt"):
    text = ""
    # Read the file content
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Process the data using jsonifyDataAI
    return jsonifyDataAI(text)