import torch
from transformers import ResNetForImageClassification
from torchvision import transforms
from PIL import Image

# Load the state dictionary
model_path = 'final_model_resnet_50.pt'
state_dict = torch.load(model_path, map_location=torch.device('cpu'))

# Initialize the ResNet model using transformers
model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")
# Modify the classifier layer to match the training script
model.classifier[1] = torch.nn.Linear(in_features=2048, out_features=2, bias=True)

# Load the state dictionary into the model
model.load_state_dict(state_dict)
model.eval()

# Define the preprocessing steps
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load an image for testing
image_path = 'auguste_test.png'  # Replace with your test image path
image = Image.open(image_path)

# Preprocess the image
input_tensor = preprocess(image)
input_batch = input_tensor.unsqueeze(0)

# Make predictions
with torch.no_grad():
    output = model(input_batch)

# Interpret the output (assuming binary classification)
_, predicted_class = torch.max(output.logits, 1)
print(f'Predicted Class: {predicted_class.item()}')
