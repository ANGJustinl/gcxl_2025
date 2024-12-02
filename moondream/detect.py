from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

model_id = "./moondream/moondream2"

model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)

image = Image.open("yolo_train/datasets/rubbish_classification/images/test/fimg_74.jpg")
enc_image = model.encode_image(image)
print(
    model.answer_question(
        enc_image,
        "CLASSIFY the object(s) in the image (recyclable waste, hazardous waste, kitchen waste, other waste)",
        tokenizer,
    )
)
