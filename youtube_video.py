import yt_dlp
import os
import imageio

# Set the YouTube video URL and directories
video_url = 'https://www.youtube.com/watch?v=rfscVS0vtbw'  # Replace with another URL
data_root = 'C:/Users/Vishal R/OneDrive/Desktop/esophageal/data/'  # Replace with the correct path
video_dir = 'surgical_video_src'
output_dir = 'surgical_video_frames'

# Check if the root path exists
if not os.path.exists(data_root):
    print(f"The path {data_root} does not exist. Please check the path.")
    exit()

# Create directories for video and output frames if they don't exist
video_path = os.path.join(data_root, video_dir)
output_path = os.path.join(data_root, output_dir)

if not os.path.exists(video_path):
    os.makedirs(video_path)

if not os.path.exists(output_path):
    os.makedirs(output_path)

# Download the video using yt-dlp
ydl_opts = {
    'outtmpl': os.path.join(video_path, '%(id)s.%(ext)s'),  # Set the output file name
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(video_url, download=True)
    filename = ydl.prepare_filename(info_dict)

# Read the video using imageio
vid = imageio.get_reader(filename, 'ffmpeg')

# Define the start and end frames for extraction
start_frame = 340
end_frame = 500

# Loop through the frames and save them as images
for frame in range(start_frame, end_frame):
    image = vid.get_data(frame)
    output_filename = os.path.join(output_path, f"frame_{frame - start_frame:04d}.png")
    imageio.imwrite(output_filename, image)
    print(f"Saved: {output_filename}")

print("Video frames extracted successfully.")



