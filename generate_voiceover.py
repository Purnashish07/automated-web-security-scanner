import asyncio
import os
import subprocess
import edge_tts

VOICE = "en-US-ChristopherNeural"
OUTPUT_DIR = r"d:\Purnashish\automated-web-security-scanner\demo-video"

SECTIONS = [
    {
        "id": "sec1_intro",
        "title": "Title & Welcome",
        "text": "Hello everyone! Today, I am proud to present SecureScan—an automated web security configuration scanner designed to assess and elevate the security posture of modern web applications."
    },
    {
        "id": "sec2_problem",
        "title": "The Security Challenge",
        "text": "In today's interconnected digital landscape, web application security is more critical than ever. Often, severe vulnerabilities stem not from complex code flaws, but from fundamental security misconfigurations—such as absent defense-in-depth headers, unhardened cookies, and permissive CORS policies. SecureScan simplifies this assessment by providing an intuitive, automated platform that passively inspects a target's HTTP response headers, cookie flags, and SSL configurations in real time—delivering immediate actionable insights without intrusive exploitation."
    },
    {
        "id": "sec3_demo",
        "title": "Live Scanner Walkthrough",
        "text": "Here is the live SecureScan application. The interface features a clean, responsive cyber-themed dashboard built with Flask and modern CSS, displaying a live status indicator at the top right. Starting an audit is effortless. Simply input the authorized target URL into the search field. The scanner includes built-in Server-Side Request Forgery safeguards, automatically verifying that the target resolves to a publicly routable IP address and blocking internal network scanning. Once we click 'Run Scan', SecureScan initiates a lightweight, non-destructive audit. It inspects redirects, analyzes SSL implementation, and parses the complete HTTP response structure within seconds."
    },
    {
        "id": "sec4_results",
        "title": "Results & Vulnerability Findings",
        "text": "As the scan finishes, SecureScan immediately organizes the output into a structured security report. At the top, four clear metric cards provide a high-level summary: Total Checks performed, Passed configurations, Warnings requiring remediation, and items categorized for contextual review. Diving into the detailed findings, each issue is classified with clear severity badges. First, HTTPS verification confirms the transport layer is encrypted with a PASS badge. Next, our header audit identifies key missing protections—such as Content-Security-Policy to mitigate Cross-Site Scripting, and HTTP Strict Transport Security to enforce encrypted connections, both flagged as Medium severity with concrete remediation guidance. We also see evaluations for X-Frame-Options against clickjacking, X-Content-Type-Options against MIME sniffing, along with detailed cookie attribute checks and Cross-Origin Resource Sharing reviews. Every scan report can be exported directly as a standardized JSON document with a single click—ideal for automated CI/CD pipelines and security documentation."
    },
    {
        "id": "sec5_outro",
        "title": "Architecture & Summary",
        "text": "SecureScan is architected around three essential security pillars: automated HTTPS and header enforcement, cookie attribute compliance, and cross-origin access verification. By combining lightweight passive scanning, strict SSRF defenses, and a modern, developer-friendly interface, SecureScan empowers developers, security students, and administrators to catch configuration oversights before attackers do. Thank you for watching, and stay secure!"
    }
]

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_list = []
    
    print("Generating voiceover segments with edge-tts...")
    for sec in SECTIONS:
        out_path = os.path.join(OUTPUT_DIR, f"{sec['id']}.mp3")
        communicate = edge_tts.Communicate(sec["text"], VOICE, rate="-2%")
        await communicate.save(out_path)
        print(f"Generated {sec['id']}.mp3 ({len(sec['text'])} chars)")
        file_list.append(out_path)
        
    # Concatenate all into SecureScan_Voiceover.mp3
    concat_txt = os.path.join(OUTPUT_DIR, "concat_audio.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in file_list:
            clean_p = p.replace("\\", "/")
            f.write(f"file '{clean_p}'\n")
            
    final_voiceover = os.path.join(OUTPUT_DIR, "SecureScan_Voiceover.mp3")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c:a", "libmp3lame", "-q:a", "2",
        final_voiceover
    ]
    subprocess.run(cmd, check=True)
    print("Combined voiceover saved to:", final_voiceover)

if __name__ == "__main__":
    asyncio.run(main())
