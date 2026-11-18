# 🎥 Technical Screen Recording & Setup Guide

This guide ensures your 90-second portfolio demo is crisp, professional, and effortless to record in **one take**.

---

## 🛠️ Recommended Free Recording Tools

### Option A: Loom (Fastest & Best for Client Proposals)
* **Website:** [loom.com](https://www.loom.com/) (Free plan gives you 25 videos up to 5 minutes each).
* **Why it's great:** Once you finish recording, it instantly generates a shareable web link (e.g. `https://www.loom.com/share/abc123xyz`). You can drop this link directly into Reddit DMs, Upwork proposals, or emails without uploading large video files.
* **Camera Bubble:** Loom can put your face in a friendly circular bubble in the bottom corner (great for building client trust).

### Option B: OBS Studio (Maximum Control & Quality)
* **Website:** [obsproject.com](https://obsproject.com/) (100% free & open-source).
* **Settings:** Set Base (Canvas) Resolution to `1920x1080`, 30 FPS, and Output Format to `MP4`.
* **Upload:** Upload to unlisted YouTube or Google Drive to share with clients.

### Option C: Windows Game Bar (Zero Install)
* Press **`Win + Alt + R`** to start/stop recording any active application.
* Video is saved to your `Videos/Captures` folder.

---

## 📋 5-Minute Pre-Recording Checklist

- [ ] **Screen Cleanliness:** Close unnecessary browser tabs, personal messengers (WhatsApp, Telegram, Discord), and messy desktop icons.
- [ ] **Zoom in Terminal & Editor:** Press **`Ctrl + +`** (125% to 150% zoom). Mobile and laptop viewers need large, easily readable text.
- [ ] **Have Files Ready:**
  1. Have `samples/raw_invoice_1.txt` open in your text editor.
  2. Have your terminal open in the `ai-data-toolkit/` directory.
- [ ] **Audio Check:** Do a quick 5-second test recording to confirm your microphone volume is clear and free of fan noise or heavy breathing.

---

## 🚀 One-Take Recording Flow (Step-by-Step)

1. **Start Recording:** Click Record on Loom or OBS.
2. **0:00 – 0:15:** Point at `samples/raw_invoice_1.txt`. Speak **Scene 1** from [docs/DEMO_SCRIPT.md](DEMO_SCRIPT.md).
3. **0:15 – 0:35:** Switch to your terminal and run:
   ```bash
   python demo_launcher.py
   ```
   *(Select `1` and press Enter).*
4. **0:35 – 1:05:** `demo_launcher.py` will run the batch extraction and **automatically open `Master_Invoice_Register.xlsx`** on your screen.
   - Point your cursor to the KPI cards at the top.
   - Click on cell `E13` to show the dynamic formula `=C13*D13`.
   - Speak **Scene 3** from [docs/DEMO_SCRIPT.md](DEMO_SCRIPT.md).
5. **1:05 – 1:30:** Switch to your GitHub repository or contact slide. Deliver **Scene 4** (The 24h turnaround offer + free 1-sample test guarantee).
6. **Stop Recording!**

---

## 🔗 Where to Use Your Demo Video URL

Once your video is generated (e.g. `https://www.loom.com/share/...`):

1. **GitHub README:** Add a video badge or clickable thumbnail banner right under the hero section:
   ```markdown
   [![Watch the 90-Second Demo](https://img.shields.io/badge/Demo-Watch%2090s%20Walkthrough-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](YOUR_LOOM_URL_HERE)
   ```
2. **Upwork & Reddit Proposals:** Paste your Loom link in sentence #2 of every bid:
   > *"I recorded a 90-second video demonstrating this exact extraction pipeline with live formula outputs: [Loom Link]"*
   Clients consistently click video links over reading long text walls!
