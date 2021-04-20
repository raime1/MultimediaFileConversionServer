import ffmpeg
import os

video_exts = [".avi", ".gif", ".mov", ".mp4", ".rawvideo", ".webm"]
audio_exts = [".aac",".ac3", ".flac", ".mp4", ".wav"]

def convert_file(input_file, output_file):
    input_name, input_ext = os.path.splitext(input_file)
    output_name,  output_ext = os.path.splitext(output_file)

    if not can_convert(input_ext, output_ext):
        return
    
    try:
        print(input_file)
        print(output_file)
        ffmpeg.input(input_file).output(output_file).run(capture_stdout= False,capture_stderr=True, overwrite_output=True)

        #out, err = ffmpeg.input(input_file).output('pipe:', format = 'mp4').run(capture_stdout= True, capture_stderr=True))

    except Exception as e:
        print(f"Error in the conversion process: {e}")

def can_convert(og_ext, to_ext):
    if og_ext == to_ext:
        print("The conversion extension is the same as the one in the specified file. No conversion to be made")
        return False
    #exts = None
    #if og_ext in video_exts:
    #    exts = video_exts
    #elif og_ext in audio_exts:
    #    exts = audio_exts
    #else:
    if og_ext not in video_exts and og_ext not in audio_exts:
        print(f"The file extension {og_ext} of the input file is not supported")
        return False
    
    if to_ext not in video_exts and to_ext not in audio_exts:
        print(f"The file extension {to_ext} of the output file is not supported")
        return False
    
    #if to_ext not in exts:
    #    print(f"Conversion from {og_ext} to {to_ext} is not supported!!!")
    #    return False
    return (True)

convert_file("test2.webm", "test2.mp4")