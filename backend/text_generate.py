import os
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from transformers import pipeline
import torchvision.transforms as transforms

class ImageDataset(Dataset):
    """
    A custom dataset for loading images.
    """
    def __init__(self, img_paths, transform=None):
        self.img_paths = img_paths
        self.transform = transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, img_path


def generate_captions(image_folder, query=""):
    """
    Generate captions for images in a folder using a pre-trained image captioning model.

    Parameters:
        image_folder (str): Path to the folder containing images.
        query (str): Optional query to customize captions (not used in this implementation).

    Returns:
        list: A list of generated captions for the images.
    """
    # Define image transformation pipeline
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    # Load image paths
    img_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    if not img_paths:
        raise ValueError(f"No valid image files found in {image_folder}")

    # Initialize dataset and data loader
    dataset = ImageDataset(img_paths, transform=transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=False)

    # Load pre-trained image captioning model
    model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

    captions = []
    for batch_images, batch_paths in dataloader:
        # Generate captions for the batch
        batch_texts = model(batch_images)
        for text, img_path in zip(batch_texts, batch_paths):
            caption = text[0]["generated_text"]
            captions.append((img_path, caption))

    return captions


if __name__ == "__main__":
    # Example usage
    folder_path = "output_frames"
    captions = generate_captions(folder_path)
    for img_path, caption in captions:
        print(f"Image: {img_path} \nCaption: {caption}\n")
