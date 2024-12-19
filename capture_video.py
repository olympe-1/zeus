import subprocess
import os

def capture_video(output_path="video.h264", duration=10, resolution="1920x1080", bitrate="10M", framerate=30):
    """
    Captures a video using libcamera-vid.
    """
    try:
        # Command to capture video with specified resolution, bitrate, and framerate
        subprocess.run(
            [
                "libcamera-vid",
                "-o", output_path,
                "-t", str(duration * 1000),
                "--width", resolution.split("x")[0],
                "--height", resolution.split("x")[1],
                "--bitrate", bitrate,
                "--framerate", str(framerate)
            ],
            check=True
        )
        print(f"Video captured: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error capturing video: {e}")

def convert_to_mp4(input_file="video.h264", output_file="video.mp4", quality=23):
    """
    Converts a video from H.264 to MP4 using ffmpeg.
    """
    try:
        # Command to convert video with specified quality (lower is better quality)
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_file,
                "-c:v", "libx264",  # Use H.264 codec
                "-preset", "slow",  # Balance between encoding speed and compression
                "-crf", str(quality),  # Quality parameter (lower value = higher quality)
                output_file
            ],
            check=True
        )
        print(f"Video converted to MP4: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    # Create a folder for videos if it doesn't exist
    if not os.path.exists("captures"):
        os.makedirs("captures")

    # Capture a video with improved quality
    capture_video("captures/video.h264", duration=10, resolution="1920x1080", bitrate="10M", framerate=30)

    # Convert the video to MP4 with better quality
    convert_to_mp4("captures/video.h264", "captures/video.mp4", quality=23)
