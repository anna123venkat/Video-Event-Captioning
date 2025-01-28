import cv2
import os

def split_video_into_frames(video_path, output_folder, num_frames=80):
    """
    Splits a video into a specified number of frames and saves them in the output folder.

    Parameters:
        video_path (str): Path to the input video file.
        output_folder (str): Path to the folder where frames will be saved.
        num_frames (int): Number of frames to extract from the video (default is 80).
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames < num_frames:
        raise ValueError(f"Video has only {total_frames} frames, fewer than the requested {num_frames}")

    # Determine the step size to evenly extract frames
    step_size = total_frames // num_frames

    frame_count = 0
    current_frame = 0

    while frame_count < num_frames:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break

        # Save every step_size-th frame
        if current_frame % step_size == 0:
            frame_name = f"frame_{frame_count:04d}.png"
            frame_path = os.path.join(output_folder, frame_name)
            cv2.imwrite(frame_path, frame)
            frame_count += 1

        current_frame += 1

    cap.release()
    print(f"Extracted {frame_count} frames from {video_path} into {output_folder}")

if __name__ == "__main__":
    # Example usage
    video_path = "example_video.mp4"
    output_folder = "output_frames"
    split_video_into_frames(video_path, output_folder)
