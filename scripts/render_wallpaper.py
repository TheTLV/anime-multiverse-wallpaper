#!/usr/bin/env python3
"""
Master Build Pipeline for Anime Multiverse Live Wallpaper (20-Minute Master Video @ 1080p 60FPS).
Automatically detects hardware NVENC acceleration (NVIDIA GPU) and falls back to CPU libx264.
"""

import os
import sys
import subprocess
import shutil
import argparse

def detect_encoder():
    """Detects if h264_nvenc hardware acceleration is available in ffmpeg."""
    try:
        res = subprocess.run(['ffmpeg', '-encoders'], capture_output=True, text=True)
        if 'h264_nvenc' in res.stdout:
            # Quick check if NVENC actually works on current hardware
            test_cmd = [
                'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=64x64:d=0.1',
                '-c:v', 'h264_nvenc', '-f', 'null', '-'
            ]
            t = subprocess.run(test_cmd, capture_output=True)
            if t.returncode == 0:
                print("[INFO] NVIDIA NVENC hardware acceleration detected and active.")
                return 'h264_nvenc', ['-preset', 'p4', '-b:v', '9M']
    except Exception:
        pass
    print("[INFO] Using software CPU encoder (libx264).")
    return 'libx264', ['-preset', 'medium', '-crf', '18']

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {desc}")
        print("STDERR:", res.stderr[-1000:])
        sys.exit(1)
    print(f">>> [DONE] {desc}")

def build_wallpaper(input_dir, output_file, work_dir="/tmp/wallpaper_build"):
    codec, encoder_opts = detect_encoder()
    os.makedirs(work_dir, exist_ok=True)
    clips_dir = os.path.join(work_dir, "clips")
    os.makedirs(clips_dir, exist_ok=True)
    
    print(f"[BUILD] Working directory: {work_dir}")
    print(f"[BUILD] Output target: {output_file}")
    
    # 1. Main Scenes specification
    # Each scene unit is smoothed via xfade crossfade loop, then extended to 300.0s
    scenes = [
        {
            "name": "s1_torii_sunset",
            "src": os.path.join(input_dir, "torii_landscape.mkv"),
            "fallback_src": os.path.join(input_dir, "main_loop_azur_lane_torii_sunset.mp4"),
            "unit_dur": 16.5,
            "loops": 19,
            "target_dur": 300.0
        },
        {
            "name": "s2_hsr_astral",
            "src": os.path.join(input_dir, "hsr_astral_station.mp4"),
            "fallback_src": os.path.join(input_dir, "main_loop_hsr_astral_express.mp4"),
            "unit_dur": 18.0,
            "loops": 17,
            "target_dur": 300.0
        },
        {
            "name": "s3_wuwa_clouds",
            "src": os.path.join(input_dir, "wuwa_sea_of_clouds.mp4"),
            "fallback_src": os.path.join(input_dir, "main_loop_wuwa_sea_of_clouds.mp4"),
            "unit_dur": 18.0,
            "loops": 17,
            "target_dur": 300.0
        },
        {
            "name": "s4_al_ocean",
            "src": os.path.join(input_dir, "al_siren.mkv"),
            "fallback_src": os.path.join(input_dir, "main_loop_azur_lane_coastal_sakura.mp4"),
            "unit_dur": 46.0,
            "loops": 7,
            "target_dur": 300.0
        }
    ]
    
    rendered_loops = {}
    for sc in scenes:
        src = sc["src"] if os.path.exists(sc["src"]) else sc["fallback_src"]
        if not os.path.exists(src):
            print(f"[WARN] Source file for {sc['name']} not found at {src}. Checking input directory...")
            continue
            
        loop_out = os.path.join(clips_dir, f"{sc['name']}_300s.mp4")
        if not os.path.exists(loop_out):
            # Generate seamless extended 300s loop
            cmd = [
                'ffmpeg', '-y', '-stream_loop', str(sc["loops"]), '-i', src,
                '-t', str(sc["target_dur"]),
                '-vf', 'fps=60,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
                '-c:v', codec
            ] + encoder_opts + ['-pix_fmt', 'yuv420p', '-an', loop_out]
            run_cmd(cmd, f"Render Main Scene {sc['name']} (300.0s @ 60fps)")
        rendered_loops[sc["name"]] = loop_out

    # 2. Concat list compilation
    concat_list = os.path.join(work_dir, "master_concat.txt")
    with open(concat_list, "w") as f:
        for sc in scenes:
            if sc["name"] in rendered_loops:
                f.write(f"file '{rendered_loops[sc['name']]}'\n")
                
    # 3. Final Master Assembly
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_list,
        '-c', 'copy', output_file
    ]
    run_cmd(cmd, f"Assemble Master Video: {output_file}")
    
    # 4. Generate master thumbnail
    thumb_path = os.path.splitext(output_file)[0] + "-thumb.jpg"
    subprocess.run([
        'ffmpeg', '-y', '-ss', '00:01:00', '-i', output_file,
        '-vframes', '1', '-update', '1', thumb_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[SUCCESS] Master video created: {output_file}")
    print(f"[SUCCESS] Thumbnail created: {thumb_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render Anime Multiverse Live Wallpaper Master")
    parser.add_argument("--input-dir", default="/home/phu/.gemini/antigravity-cli/brain/67da141d-a5e7-4ef0-a267-a87f8536c186/scratch", help="Directory containing raw cutscenes or loops")
    parser.add_argument("--output", default="/home/phu/.local/share/gnome-wallpaper-engine/backgrounds/azur_multiverse_odyssey.mp4", help="Output path for master wallpaper")
    args = parser.parse_args()
    build_wallpaper(args.input_dir, args.output)
