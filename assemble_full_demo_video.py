#!/usr/bin/env python3
"""
Full Automated Demo Video Assembly Script.
Assembles:
1. 8s Cinematic AI Hook (scaled to 1080p)
2. 16s Messy Document Problem (with smooth cinematic push-in)
3. 21s Fast Terminal Batch Execution (with smooth zoom)
4. 27s Live Formula Excel Master Register (with formula inspection zoom)
5. 19.2s Commercial Offer & Outro (with smooth drift)
Slices and mixes with the 91.2s voiceover track into a final 1080p MP4.
"""

import subprocess
from pathlib import Path


def run_cmd(cmd, desc):
    print(f"🎬 {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Error in {desc}:\n{res.stderr[-500:]}")
        raise RuntimeError(f"FFmpeg failed: {desc}")
    print(f"  ✓ {desc} complete.")


def main():
    print("=" * 65)
    print("🚀 AUTOMATED 1080P DEMO VIDEO COMPOSITOR (OPTION 2)")
    print("=" * 65)

    temp_dir = Path("temp_segments")
    temp_dir.mkdir(parents=True, exist_ok=True)

    # 1. Segment 0: Cinematic Intro (8 seconds, 1080p 30fps)
    intro_mp4 = Path("intro_clip.mp4")
    seg0 = temp_dir / "seg0_intro.mp4"
    if intro_mp4.exists():
        cmd0 = [
            "ffmpeg", "-y",
            "-ss", "0", "-t", "8",
            "-i", str(intro_mp4),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
            "-an", str(seg0)
        ]
        run_cmd(cmd0, "Normalizing Cinematic AI Intro (8s)")
    else:
        print("⚠️ intro_clip.mp4 not found, using scene 1 for intro.")

    # 2. Segment 1: Messy Input Document (16 seconds, zoompan)
    seg1 = temp_dir / "seg1_messy.mp4"
    cmd1 = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", "temp_frames/scene1_messy_invoice.png",
        "-vf", "zoompan=z='min(zoom+0.0005,1.06)':d=480:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
        "-t", "16",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        str(seg1)
    ]
    run_cmd(cmd1, "Rendering Scene 1: Messy Document Walkthrough (16s)")

    # 3. Segment 2: Terminal Execution (21 seconds, zoompan)
    seg2 = temp_dir / "seg2_terminal.mp4"
    cmd2 = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", "temp_frames/scene2_terminal_run.png",
        "-vf", "zoompan=z='min(zoom+0.0004,1.05)':d=630:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
        "-t", "21",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        str(seg2)
    ]
    run_cmd(cmd2, "Rendering Scene 2: Batch Terminal Pipeline (21s)")

    # 4. Segment 3: Excel Master Deliverable with Live Formulas (27 seconds, zoompan)
    seg3 = temp_dir / "seg3_excel.mp4"
    cmd3 = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", "temp_frames/scene3_excel_master.png",
        "-vf", "zoompan=z='min(zoom+0.0006,1.08)':d=810:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
        "-t", "27",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        str(seg3)
    ]
    run_cmd(cmd3, "Rendering Scene 3: Live Formula Excel Inspection (27s)")

    # 5. Segment 4: Commercial Offer & Outro (19.2 seconds)
    seg4 = temp_dir / "seg4_outro.mp4"
    cmd4 = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", "temp_frames/scene4_commercial_outro.png",
        "-vf", "zoompan=z='min(zoom+0.0003,1.04)':d=576:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
        "-t", "19.2",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        str(seg4)
    ]
    run_cmd(cmd4, "Rendering Scene 4: Commercial Offer & Outro (19.2s)")

    # 6. Concat list
    concat_txt = temp_dir / "concat_list.txt"
    with open(concat_txt, "w") as f:
        f.write(f"file '{seg0.resolve().as_posix()}'\n")
        f.write(f"file '{seg1.resolve().as_posix()}'\n")
        f.write(f"file '{seg2.resolve().as_posix()}'\n")
        f.write(f"file '{seg3.resolve().as_posix()}'\n")
        f.write(f"file '{seg4.resolve().as_posix()}'\n")

    video_only = temp_dir / "stitched_video.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(video_only)
    ]
    run_cmd(cmd_concat, "Concatenating 5 Video Segments")

    # 7. Final Merge with Voiceover Audio
    final_output = Path("final_ai_data_toolkit_demo.mp4")
    voiceover_path = Path("voiceover.mp3")

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(video_only),
        "-i", str(voiceover_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_output)
    ]
    run_cmd(cmd_final, "Merging Voiceover Audio & Exporting Final MP4")

    print("\n" + "=" * 65)
    print("🎉 FINAL DEMO VIDEO CREATION COMPLETE (10/10 STANDARD)!")
    print("=" * 65)
    print(f"📁 Deliverable: {final_output.resolve()}")
    print("=" * 65)


if __name__ == "__main__":
    main()
