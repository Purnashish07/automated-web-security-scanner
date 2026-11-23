import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORKDIR = r"d:\Purnashish\automated-web-security-scanner\demo-video"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

f_title = get_font(FONT_BOLD, 38)
f_sub = get_font(FONT_REG, 24)
f_badge = get_font(FONT_BOLD, 18)
f_meta = get_font(FONT_MONO, 16)
f_big_hero = get_font(FONT_BOLD, 56)

def decorate_frame(base_img_path, badge_text, title_text, desc_text, out_path, is_thumbnail=False):
    base = Image.open(base_img_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    
    # Create overlay canvas
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Top banner bar
    draw.rectangle([(0, 0), (1920, 54)], fill=(11, 17, 32, 235))
    draw.line([(0, 54), (1920, 54)], fill=(0, 255, 204, 80), width=1)
    
    # Brand logo on top left
    draw.ellipse([(35, 17), (51, 33)], fill=(16, 185, 129, 255))
    draw.text((62, 14), "SecureScan", font=f_badge, fill=(0, 255, 204, 255))
    draw.text((165, 15), "|  Automated Web Security Scanner", font=f_meta, fill=(156, 163, 175, 255))
    
    # Top right pill: SYSTEM AUDIT ACTIVE
    draw.rounded_rectangle([(1650, 12), (1885, 42)], radius=15, fill=(31, 41, 55, 200), outline=(16, 185, 129, 180), width=1)
    draw.ellipse([(1665, 23), (1673, 31)], fill=(16, 185, 129, 255))
    draw.text((1685, 17), "1080p FULL HD DEMO", font=f_meta, fill=(229, 231, 235, 255))
    
    # Bottom glassmorphism lower-third container
    lh_top = 890
    draw.rectangle([(0, lh_top), (1920, 1080)], fill=(8, 14, 26, 245))
    draw.line([(0, lh_top), (1920, lh_top)], fill=(0, 255, 204, 180), width=2)
    
    # Accent color block on left
    draw.rectangle([(0, lh_top), (8, 1080)], fill=(0, 255, 204, 255))
    
    # Category Badge
    badge_w = 340
    draw.rounded_rectangle([(45, lh_top + 20), (45 + badge_w, lh_top + 52)], radius=6, fill=(17, 24, 39, 255), outline=(0, 255, 204, 150), width=1)
    draw.text((62, lh_top + 25), badge_text, font=f_badge, fill=(0, 255, 204, 255))
    
    # Main Headline
    draw.text((45 + badge_w + 30, lh_top + 20), title_text, font=f_title, fill=(243, 244, 246, 255))
    
    # Secondary Description
    draw.text((45, lh_top + 70), desc_text, font=f_sub, fill=(156, 163, 175, 255))
    
    # Watermark on right of lower third
    draw.text((1560, lh_top + 80), "IBM SkillsBuild 2026", font=f_meta, fill=(107, 114, 128, 200))
    
    final_img = Image.alpha_composite(base, overlay).convert("RGB")
    final_img.save(out_path, quality=95)
    print(f"Generated slide: {os.path.basename(out_path)}")

def create_cards_slide(title, subtitle, items, out_path):
    img = Image.new("RGB", (1920, 1080), (11, 17, 32))
    draw = ImageDraw.Draw(img)
    
    # Subtle cyber grid background lines
    for x in range(0, 1920, 60):
        draw.line([(x, 0), (x, 1080)], fill=(17, 24, 39, 100), width=1)
    for y in range(0, 1080, 60):
        draw.line([(0, y), (1920, y)], fill=(17, 24, 39, 100), width=1)
        
    # Top banner bar
    draw.rectangle([(0, 0), (1920, 60)], fill=(15, 23, 42))
    draw.line([(0, 60), (1920, 60)], fill=(0, 255, 204, 100), width=1)
    draw.ellipse([(40, 22), (56, 38)], fill=(16, 185, 129))
    draw.text((68, 18), "SecureScan", font=f_badge, fill=(0, 255, 204))
    draw.text((180, 20), "|  Automated Web Security Architecture", font=f_meta, fill=(156, 163, 175))
    
    # Center Header
    draw.text((120, 120), title, font=f_big_hero, fill=(243, 244, 246))
    draw.text((120, 195), subtitle, font=f_sub, fill=(156, 163, 175))
    
    # Render 3 Feature/Insight Cards
    card_w = 520
    card_h = 480
    start_y = 280
    gap = 40
    start_x = (1920 - (3 * card_w + 2 * gap)) // 2
    
    colors = [(16, 185, 129), (245, 158, 11), (6, 182, 212)]
    
    for i, itm in enumerate(items):
        cx = start_x + i * (card_w + gap)
        accent = colors[i % len(colors)]
        
        # Card Box
        draw.rounded_rectangle([(cx, start_y), (cx + card_w, start_y + card_h)], radius=16, fill=(17, 24, 39), outline=(55, 65, 81), width=1)
        
        # Top glowing accent line on card
        draw.rounded_rectangle([(cx, start_y), (cx + card_w, start_y + 6)], radius=3, fill=accent)
        
        # Icon / Badge Tag
        draw.rounded_rectangle([(cx + 35, start_y + 40), (cx + 180, start_y + 75)], radius=6, fill=(31, 41, 55), outline=accent, width=1)
        draw.text((cx + 48, start_y + 46), itm["tag"], font=f_meta, fill=accent)
        
        # Card Heading
        draw.text((cx + 35, start_y + 105), itm["heading"], font=f_title, fill=(243, 244, 246))
        
        # Card Text (multiple lines)
        lines = itm["text"].split("\n")
        cur_y = start_y + 175
        for l in lines:
            draw.text((cx + 35, cur_y), l, font=f_sub, fill=(156, 163, 175))
            cur_y += 38
            
    # Bottom Lower Third
    draw.rectangle([(0, 930), (1920, 1080)], fill=(8, 14, 26))
    draw.line([(0, 930), (1920, 930)], fill=(0, 255, 204, 180), width=2)
    draw.rectangle([(0, 930), (8, 1080)], fill=(0, 255, 204))
    draw.text((60, 955), "PASSIVE CONFIGURATION SCANNER", font=f_badge, fill=(0, 255, 204))
    draw.text((60, 995), "Non-invasive HTTP, SSL, and Header Inspection Engine — Safe for Production Testing", font=f_sub, fill=(229, 231, 235))
    
    img.save(out_path, quality=95)
    print(f"Generated cards slide: {os.path.basename(out_path)}")

def create_outro_slide(out_path):
    img = Image.new("RGB", (1920, 1080), (11, 17, 32))
    draw = ImageDraw.Draw(img)
    
    for x in range(0, 1920, 60):
        draw.line([(x, 0), (x, 1080)], fill=(17, 24, 39, 100), width=1)
    for y in range(0, 1080, 60):
        draw.line([(0, y), (1920, y)], fill=(17, 24, 39, 100), width=1)
        
    draw.rectangle([(0, 0), (1920, 60)], fill=(15, 23, 42))
    draw.line([(0, 60), (1920, 60)], fill=(0, 255, 204, 100), width=1)
    draw.ellipse([(40, 22), (56, 38)], fill=(16, 185, 129))
    draw.text((68, 18), "SecureScan", font=f_badge, fill=(0, 255, 204))
    draw.text((180, 20), "|  Project Demonstration Summary", font=f_meta, fill=(156, 163, 175))
    
    draw.text((150, 180), "SecureScan", font=f_big_hero, fill=(0, 255, 204))
    draw.text((150, 260), "Automated Web Security Configuration Scanner", font=f_title, fill=(243, 244, 246))
    draw.text((150, 320), "A production-ready passive audit framework for modern web applications.", font=f_sub, fill=(156, 163, 175))
    
    # Info Box
    box_x = 150
    box_y = 400
    draw.rounded_rectangle([(box_x, box_y), (box_x + 1620, box_y + 360)], radius=16, fill=(17, 24, 39), outline=(55, 65, 81), width=1)
    
    details = [
        ("PROJECT ARCHITECTURE", "Python 3.12 · Flask REST API · Tailwind CSS · Vanilla JS · Vercel Serverless"),
        ("AUTHOR & RESEARCHER", "Purnashish Atroliya · Madhav Institute of Technology and Science (MITS), Gwalior"),
        ("CURRICULUM / BOOTCAMP", "IBM SkillsBuild Cyber Security BootCamp 2026"),
        ("GITHUB REPOSITORY", "https://github.com/Purnashish07/automated-web-security-scanner"),
        ("LIVE APPLICATION", "https://automated-web-security-scanner-abxd.vercel.app/")
    ]
    
    dy = box_y + 40
    for label, val in details:
        draw.text((box_x + 50, dy), label, font=f_badge, fill=(16, 185, 129))
        draw.text((box_x + 380, dy), val, font=f_sub, fill=(243, 244, 246))
        dy += 60
        
    draw.rectangle([(0, 930), (1920, 1080)], fill=(8, 14, 26))
    draw.line([(0, 930), (1920, 930)], fill=(0, 255, 204, 180), width=2)
    draw.text((60, 955), "SECURE BY DESIGN", font=f_badge, fill=(0, 255, 204))
    draw.text((60, 995), "Thank you for watching — audit your application security posture with SecureScan!", font=f_sub, fill=(229, 231, 235))
    
    img.save(out_path, quality=95)
    print(f"Generated outro slide: {os.path.basename(out_path)}")

def main():
    print("Step 1: Preparing all visual slides...")
    
    # Slide 01: Title Card
    decorate_frame(
        os.path.join(WORKDIR, "SecureScan_Thumbnail.png"),
        "01 · PROJECT DEMO",
        "SecureScan — Automated Web Security Scanner",
        "A lightweight, passive cybersecurity configuration audit framework for modern web applications.",
        os.path.join(WORKDIR, "slide_01_title.png"),
        is_thumbnail=True
    )
    
    # Slide 02: Architecture & Threat Landscape
    threat_items = [
        {
            "tag": "THREAT VECTOR",
            "heading": "Header Oversights",
            "text": "• Missing Content-Security-Policy\n• Absent Strict-Transport-Security\n• Unprotected X-Frame-Options\n• Allows XSS & Clickjacking"
        },
        {
            "tag": "RISK FACTOR",
            "heading": "Cookie Vulnerabilities",
            "text": "• Missing Secure flag\n• Omitted HttpOnly attribute\n• Weak SameSite configuration\n• Enables session hijacking"
        },
        {
            "tag": "PASSIVE AUDIT",
            "heading": "CORS & SSRF Guard",
            "text": "• Evaluates Wildcard Origins\n• Prevents Credential Leakage\n• Built-in SSRF IP validation\n• Safe non-invasive testing"
        }
    ]
    create_cards_slide(
        "Why Automated Web Security Scanning Matters",
        "Addressing critical web application misconfigurations before they are exploited in production.",
        threat_items,
        os.path.join(WORKDIR, "slide_02_threats.png")
    )
    
    # Slide 03: Live Hero View
    decorate_frame(
        os.path.join(WORKDIR, "raw_frame_01_hero.png"),
        "02 · SYSTEM OVERVIEW",
        "Interactive Cybersecurity Dashboard",
        "Sleek dark-mode interface with live system readiness and responsive target input.",
        os.path.join(WORKDIR, "slide_03_hero.png")
    )
    
    # Slide 04: Target Input & SSRF
    decorate_frame(
        os.path.join(WORKDIR, "raw_frame_02_input.png"),
        "03 · INPUT VALIDATION",
        "Target URL Entry & SSRF Safeguards",
        "Automatic public IP DNS resolution check rejects localhost, private subnets, and loopback attacks.",
        os.path.join(WORKDIR, "slide_04_input.png")
    )
    
    # Slide 05: Scanning in Progress
    decorate_frame(
        os.path.join(WORKDIR, "raw_frame_03_scanning.png"),
        "04 · SCAN EXECUTION",
        "Initiating Non-Destructive Passive Audit",
        "Dispatches lightweight HTTP/HTTPS probes, inspecting SSL certificates, redirects, and header trees.",
        os.path.join(WORKDIR, "slide_05_scanning.png")
    )
    
    # Slide 06: Summary Metrics Top
    decorate_frame(
        os.path.join(WORKDIR, "raw_frame_04_results_top.png"),
        "05 · AUDIT SUMMARY",
        "Executive Finding Overview & Status Codes",
        "Total Checks: 8  |  Passed: 1  |  Warnings: 5  |  Needs Review: 2  |  HTTP 200 OK",
        os.path.join(WORKDIR, "slide_06_results_summary.png")
    )
    
    # Slide 07: Detailed Findings (HTTPS, CSP, HSTS)
    decorate_frame(
        os.path.join(WORKDIR, "raw_frame_05_findings_mid.png"),
        "06 · VULNERABILITY AUDIT",
        "Header Analysis: CSP, HSTS & Transport Security",
        "Categorized severity badges with actionable remediation advice for development teams.",
        os.path.join(WORKDIR, "slide_07_findings_mid.png")
    )
    
    # Slide 08: Cookie & CORS Findings + JSON Export
    decorate_frame(
        os.path.join(WORKDIR, "raw_frame_06_findings_bottom.png"),
        "07 · COOKIE & CORS CHECKS",
        "Cookie Security Flags & Automated JSON Export",
        "Validates Secure, HttpOnly, and SameSite attributes, plus one-click standardized JSON export.",
        os.path.join(WORKDIR, "slide_08_findings_bottom.png")
    )
    
    # Slide 09: Three Feature Pillars Grid
    decorate_frame(
        os.path.join(WORKDIR, "raw_frame_07_features.png"),
        "08 · CORE CAPABILITIES",
        "Three Specialized Security Pillars",
        "Dedicated verification modules for HTTPS & Headers, Cookie Attributes, and Cross-Origin Resource Sharing.",
        os.path.join(WORKDIR, "slide_09_features.png")
    )
    
    # Slide 10: Outro & Summary
    create_outro_slide(os.path.join(WORKDIR, "slide_10_outro.png"))
    
    print("\nStep 2: Compiling video segments with audio sync...")
    
    # Define video segment timeline mapped to audio files
    # Section 1: 12.96s (slide_01_title)
    # Section 2: 37.61s (slide_02_threats: 18.0s, slide_03_hero: 19.61s)
    # Section 3: 47.30s (slide_04_input: 24.0s, slide_05_scanning: 23.30s)
    # Section 4: 72.43s (slide_06_results_summary: 22.0s, slide_07_findings_mid: 28.0s, slide_08_findings_bottom: 22.43s)
    # Section 5: 30.72s (slide_09_features: 15.0s, slide_10_outro: 15.72s)
    
    segments = [
        {
            "id": "part1",
            "audio": "sec1_intro.mp3",
            "slides": [("slide_01_title.png", 12.96)]
        },
        {
            "id": "part2",
            "audio": "sec2_problem.mp3",
            "slides": [("slide_02_threats.png", 18.0), ("slide_03_hero.png", 19.61)]
        },
        {
            "id": "part3",
            "audio": "sec3_demo.mp3",
            "slides": [("slide_04_input.png", 24.0), ("slide_05_scanning.png", 23.30)]
        },
        {
            "id": "part4",
            "audio": "sec4_results.mp3",
            "slides": [
                ("slide_06_results_summary.png", 22.0),
                ("slide_07_findings_mid.png", 28.0),
                ("slide_08_findings_bottom.png", 22.43)
            ]
        },
        {
            "id": "part5",
            "audio": "sec5_outro.mp3",
            "slides": [("slide_09_features.png", 15.0), ("slide_10_outro.png", 15.72)]
        }
    ]
    
    part_files = []
    
    for seg in segments:
        part_id = seg["id"]
        audio_file = os.path.join(WORKDIR, seg["audio"])
        part_out = os.path.join(WORKDIR, f"{part_id}.mp4")
        
        # Build concat list for this segment's slides
        slide_list_file = os.path.join(WORKDIR, f"list_{part_id}.txt")
        with open(slide_list_file, "w", encoding="utf-8") as f:
            for s_img, s_dur in seg["slides"]:
                clean_img = os.path.join(WORKDIR, s_img).replace("\\", "/")
                f.write(f"file '{clean_img}'\n")
                f.write(f"duration {s_dur}\n")
            # Repeat last file for ffmpeg concat requirement
            last_img = os.path.join(WORKDIR, seg["slides"][-1][0]).replace("\\", "/")
            f.write(f"file '{last_img}'\n")
            
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", slide_list_file,
            "-i", audio_file,
            "-vf", "scale=1920:1080,format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            part_out
        ]
        print(f"Encoding {part_id}.mp4...")
        subprocess.run(cmd, check=True)
        part_files.append(part_out)
        
    print("\nStep 3: Merging all video segments...")
    master_list = os.path.join(WORKDIR, "master_list.txt")
    with open(master_list, "w", encoding="utf-8") as f:
        for p in part_files:
            clean_p = p.replace("\\", "/")
            f.write(f"file '{clean_p}'\n")
            
    merged_raw = os.path.join(WORKDIR, "merged_raw.mp4")
    cmd_merge = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", master_list,
        "-c", "copy",
        merged_raw
    ]
    subprocess.run(cmd_merge, check=True)
    print("Merged raw video created.")
    
    print("\nStep 4: Mixing background music with master video...")
    final_output = os.path.join(WORKDIR, "SecureScan_Demo_1080p.mp4")
    bgm_file = os.path.join(WORKDIR, "bgm.mp3")
    
    # Mix voiceover with subtle background music (-26dB volume)
    cmd_final = [
        "ffmpeg", "-y",
        "-i", merged_raw,
        "-i", bgm_file,
        "-filter_complex", "[1:a]volume=0.08[bgm]; [0:a][bgm]amix=inputs=2:duration=first:dropout_transition=3[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        final_output
    ]
    subprocess.run(cmd_final, check=True)
    print(f"\nSUCCESS! Final video created at: {final_output}")

if __name__ == "__main__":
    main()
