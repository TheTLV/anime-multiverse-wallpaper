#!/usr/bin/env python3
"""
Procedural VFX Assets Generator for Anime Multiverse Live Wallpaper.
Generates:
1. Tactical Naval Radar Sweep HUD (Azur Lane)
2. Sonoro Sphere Acoustic Shockwave (Wuthering Waves)
3. Void Slash / Reality Fracture (Honkai: Star Rail / Acheron style)
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFilter

def generate_radar_frames(output_dir, num_frames=180, width=1920, height=1080):
    """Generates 180 frames (3.0s @ 60fps) of Tactical Naval Radar Sweep HUD."""
    os.makedirs(output_dir, exist_ok=True)
    cx, cy = width // 2, height // 2
    max_radius = 650
    print(f"[VFX] Generating {num_frames} Radar Sweep frames into {output_dir}...")
    
    for frame_idx in range(num_frames):
        t = frame_idx / float(num_frames)
        angle_rad = t * 2 * math.pi - math.pi / 2
        
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # HUD opacity fade-out in last 20%
        hud_alpha = 1.0 if t < 0.8 else max(0.0, 1.0 - (t - 0.8) / 0.2)
        
        # Concentric circles
        for r in [200, 350, 500, max_radius]:
            col = (0, 245, 212, int(140 * hud_alpha))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
        
        # Crosshair axes
        col_axis = (0, 245, 212, int(100 * hud_alpha))
        draw.line([cx - max_radius - 40, cy, cx + max_radius + 40, cy], fill=col_axis, width=1)
        draw.line([cx, cy - max_radius - 40, cx, cy + max_radius + 40], fill=col_axis, width=1)
        
        # Degree tick marks
        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            r1 = max_radius
            r2 = max_radius + (15 if deg % 45 == 0 else 8)
            draw.line(
                [cx + r1 * math.cos(rad), cy + r1 * math.sin(rad),
                 cx + r2 * math.cos(rad), cy + r2 * math.sin(rad)],
                fill=(0, 245, 212, int(180 * hud_alpha)),
                width=2 if deg % 45 == 0 else 1
            )
            
        # Rotating sweep line
        sweep_x = cx + (max_radius + 20) * math.cos(angle_rad)
        sweep_y = cy + (max_radius + 20) * math.sin(angle_rad)
        draw.line([cx, cy, sweep_x, sweep_y], fill=(120, 255, 240, int(230 * hud_alpha)), width=3)
        
        # Sweep beam sector trail (30 degrees trailing)
        trail_steps = 30
        for i in range(trail_steps):
            frac = i / float(trail_steps)
            trail_angle = angle_rad - (1.0 - frac) * math.radians(35)
            alpha_trail = int(60 * frac * hud_alpha)
            tx = cx + max_radius * math.cos(trail_angle)
            ty = cy + max_radius * math.sin(trail_angle)
            draw.line([cx, cy, tx, ty], fill=(0, 245, 212, alpha_trail), width=2)
            
        # Target ping blips
        for bx, by in [(cx + 280, cy - 140), (cx - 320, cy + 220), (cx + 420, cy + 180)]:
            draw.rectangle([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 60, 90, int(220 * hud_alpha)))
            draw.rectangle([bx - 10, by - 10, bx + 10, by + 10], outline=(255, 60, 90, int(140 * hud_alpha)), width=1)
            
        img.save(os.path.join(output_dir, f"f_{frame_idx:03d}.png"))
    print("[VFX] Radar Sweep frames generation completed.")

def generate_sonoro_frames(output_dir, num_frames=180, width=1920, height=1080):
    """Generates 180 frames (3.0s @ 60fps) of Sonoro Sphere Acoustic Shockwave."""
    os.makedirs(output_dir, exist_ok=True)
    cx, cy = width // 2, height // 2
    max_radius = 1200
    print(f"[VFX] Generating {num_frames} Sonoro Sphere frames into {output_dir}...")
    
    for frame_idx in range(num_frames):
        t = frame_idx / float(num_frames)
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Multi-wave propagation
        for wave_offset in [0.0, 0.22, 0.45]:
            local_t = (t - wave_offset)
            if local_t < 0 or local_t > 0.65:
                continue
            prog = local_t / 0.65
            r = int(prog * max_radius)
            alpha = int(180 * math.sin(prog * math.pi))
            col = (255, 230, 140, alpha)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=max(2, int(8 * (1.0 - prog))))
            
            # Sub-harmonic reverberation ring
            r2 = max(0, r - 35)
            col2 = (140, 220, 255, int(alpha * 0.7))
            draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=col2, width=2)
            
        img.save(os.path.join(output_dir, f"f_{frame_idx:03d}.png"))
    print("[VFX] Sonoro Sphere frames generation completed.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frames_dir = os.path.join(base_dir, "..", "assets", "vfx_frames")
    generate_radar_frames(os.path.join(frames_dir, "radar_sweep"))
    generate_sonoro_frames(os.path.join(frames_dir, "sonoro_sphere"))
    print("[VFX] All procedural VFX assets generated successfully!")
