import subprocess
import os

def capture_image(output_path="image.jpg"):
    try:
        # Commande pour capturer une image avec libcamera
        subprocess.run(
            ["libcamera-jpeg", "-o", output_path],
            check=True
        )
        print(f"Image capturée : {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la capture : {e}")

if __name__ == "__main__":
    # Crée un dossier pour les images si nécessaire
    if not os.path.exists("captures"):
        os.makedirs("captures")

    # Capture l'image
    capture_image("captures/image.jpg")
