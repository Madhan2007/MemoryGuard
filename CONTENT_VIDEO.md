# MemoryGuard — Video Content Deliverable

---

## 🎬 Video Specifications

| Spec | Requirement |
|------|-------------|
| **Duration** | 3-5 minutes (hackathon demo) + 60s short version |
| **Format** | MP4, 1080p, 30fps |
| **Audio** | Clear narration + background music (optional) |
| **Captions** | Required (accessibility) |
| **Platform** | YouTube, LinkedIn, Twitter/X, Hackathon submission portal |

---

## 📋 Video Structure (3-5 min Main Demo)

### 1. Hook & Problem (0:00-0:45)
| Time | Visual | Audio/Narration |
|------|--------|-----------------|
| 0:00-0:10 | Split screen: "Typical AI" (forgets) vs "MemoryGuard" (remembers) | "Most AI agents have amnesia. They forget every conversation." |
| 0:10-0:25 | Sales rep frustrated, flipping through CRM notes | "Sales reps lose context across 10-15 calls over 90-day cycles." |
| 0:25-0:45 | Architecture diagram: Hindsight + MemoryGuard | "We built MemoryGuard: Hindsight for memory + 4-gate verification for truth." |

### 2. Architecture Overview (0:45-1:30)
| Time | Visual | Audio |
|------|--------|-------|
| 0:45-1:00 | Animated diagram: User → Agent Loop → Hindsight Recall → LLM → MemoryGuard → Hindsight Retain | "Two layers: Hindsight Cloud for persistent vector memory, MemoryGuard for governance." |
| 1:00-1:15 | 4 gates animation: Admission → Contamination → Consolidation → Scope | "Every memory passes 4 gates. The hero is Contamination — verifier LLM checks grounding." |
| 1:15-1:30 | Two banks: Project (deal) + Common (rep) | "Project bank for deal context, Common bank for rep preferences. Never mix." |

### 3. Live Demo: Hero Moments (1:30-3:30)

#### Moment 1: Consolidation (ACME) — 1:30-2:15
| Action | Screen | Narration |
|--------|--------|-----------|
| Select "Acme Corp" | Streamlit sidebar | "First scenario: ACME Corp — consolidation." |
| Click "I prefer email..." | Quick action button | "Turn 1: Customer states email preference." |
| Show decision card | Memory panel | "RETAIN. Frequency 1." |
| Click "Also prefer email..." | Quick action button | "Turn 4: Same preference again." |
| Show MERGE card | Memory panel | "MERGE. Frequency now 3. Three source quotes. One memory." |
| Show recalled context | Recalled context expander | "Next turn recalls it automatically." |

#### Moment 2: Contamination Rejection (NORTHWIND) — 2:15-2:55
| Action | Screen | Narration |
|--------|--------|-----------|
| Select "Northwind Health" | Sidebar | "NORTHWIND — contamination rejection." |
| Click "Evaluating SOC2..." | Quick action | "Customer says 'evaluating SOC2'." |
| Show two decision cards | Memory panel | "Verifier extracts TWO candidates. One grounded, one hallucinated." |
| Highlight REJECT card | Memory panel (red badge) | "REJECTED: 'SOC2 mandatory' — UNSUPPORTED. Source says 'evaluating'." |
| Highlight RETAIN card | Memory panel (green badge) | "RETAIN: 'Evaluating SOC2' — SUPPORTED." |

#### Moment 3: Scope Isolation (GLOBEX) — 2:55-3:30
| Action | Screen | Narration |
|--------|--------|-----------|
| Select "Globex Inc" | Sidebar | "GLOBEX — scope isolation." |
| Click "Evaluating Gong..." | Quick action | "Competitor mentions go to PROJECT bank." |
| Click "Prefer email..." | Quick action | "Rep preference goes to COMMON bank." |
| Show memory panel | Two memories with 📁 and 👤 icons | "Competitors stay in project. Rep prefs in common. Zero leakage." |

### 4. Ablation Proof (3:30-4:00)
| Visual | Narration |
|--------|-----------|
| Ablation table slide | "We ran 5 configs. Only Full MemoryGuard catches the hallucination." |
| Highlight row: Full=1, others=0 | "No-Contamination accepts the hallucination. Raw Hindsight accepts it. MemoryGuard is the difference." |

### 5. Close & Links (4:00-4:30)
| Visual | Narration |
|--------|-----------|
| GitHub repo + Architecture diagram | "Open source. Built for HackWithHyderabad 3.0." |
| QR code + URLs | "github.com/yourusername/memoryguard — try it yourself." |
| Team photo/logo | "MemoryGuard: Verified memory for deal intelligence agents." |

---

## 🎬 60-Second Short Version (TikTok/Reels/Shorts)

| Time | Visual | Audio |
|------|--------|-------|
| 0-3s | Split: "AI with amnesia" vs "MemoryGuard learns" | "Your AI forgets. Ours learns." |
| 3-10s | Sales rep pain | "Reps lose context across 15 calls. AI starts fresh every time." |
| 10-25s | Architecture speed-run | "Hindsight for memory. MemoryGuard for truth." |
| 25-40s | Contamination demo | "Source: 'evaluating SOC2' → Hallucination: 'SOC2 mandatory' → REJECTED." |
| 40-50s | Consolidation freq=3 | "Remembers. Merges. Learns your preferences." |
| 50-60s | GitHub QR + "Built for HackWithHyderabad 3.0" | "github.com/yourusername/memoryguard" |

---

## 🎥 Recording Checklist

### Pre-Recording
- [ ] Clean desktop (hide sensitive info)
- [ ] Set screen resolution to 1920x1080
- [ ] Test microphone (Blue Yeti / Rode NT-USB / good headset)
- [ ] Close unnecessary apps (Slack, email, etc.)
- [ ] Have browser tabs ready: Streamlit, GitHub, ablation JSON
- [ ] Disable notifications (Windows Focus Assist / Mac Do Not Disturb)

### Recording Software Options
| Tool | Platform | Notes |
|------|----------|-------|
| **OBS Studio** | Win/Mac/Linux | Free, pro features, 1080p60 |
| **ScreenFlow** | Mac | Paid, excellent editing |
| **Camtasia** | Win/Mac | Paid, built-in editor |
| **Loom** | Browser | Free tier, quick share |
| **Xbox Game Bar** | Win | Win+G, simple |

### During Recording
- [ ] Record in one take (or few segments)
- [ ] Speak clearly, moderate pace
- [ ] Pause 2s between sections for editing
- [ ] Show mouse clicks (enable "highlight cursor" in OBS)
- [ ] Record 2-3 takes of each section

### Post-Production
- [ ] Trim dead space
- [ ] Add captions (required for accessibility)
- [ ] Add title cards for each section
- [ ] Add GitHub URL watermark (bottom-right)
- [ ] Add background music (low volume, royalty-free)
- [ ] Export: MP4, H.264, 1080p, 30fps, <500MB

---

## 🎨 Assets Needed

### Screenshots (for B-roll)
- [ ] Streamlit login page
- [ ] Streamlit main demo (chat + memory panel)
- [ ] Memory decision cards (green/blue/red badges)
- [ ] Recalled context expander
- [ ] Ablation results table
- [ ] GitHub repo README

### Graphics
- [ ] MemoryGuard logo (use 🧠 emoji or create simple logo)
- [ ] Architecture diagram (export from docs/ARCHITECTURE.md)
- [ ] Ablation results chart (bar chart from eval/results/)
- [ ] QR code for GitHub repo (use qr-code-generator.com)

### Music (Royalty-Free)
- YouTube Audio Library
- Epidemic Sound (if subscription)
- Incompetech (Kevin MacLeod)

---

## 📤 Distribution Checklist

### YouTube
- [ ] Title: "MemoryGuard: Verified Memory for Deal Intelligence Agents | HackWithHyderabad 3.0"
- [ ] Description: Links to GitHub, Hindsight, Hackathon
- [ ] Tags: AI, Agents, Hindsight, SalesTech, Hackathon, MachineLearning
- [ ] Thumbnail: Custom (MemoryGuard logo + "Verified Memory")
- [ ] Playlist: "Hackathon Demos" / "AI Agents"
- [ ] End screen: Subscribe + GitHub link

### LinkedIn
- [ ] Native video upload (better reach than YouTube link)
- [ ] Tag: @Vectorize, @GroqInc, @HackWithHyd
- [ ] Hashtags: #AI #Agents #Hindsight #SalesTech #Hackathon

### Twitter/X
- [ ] Native video (better than link)
- [ ] Thread with key moments (see CONTENT_SOCIAL.md)
- [ ] Tag: @vectorize_io @GroqInc @HackWithHyd

### Hackathon Submission Portal
- [ ] Upload video file or YouTube link
- [ ] Include GitHub repo URL
- [ ] Include live demo URL (if deployed)

---

## 📁 File Organization for Video Production

```
video-production/
├── raw-footage/
│   ├── take-1-architecture.mp4
│   ├── take-2-acme-demo.mp4
│   ├── take-3-northwind-demo.mp4
│   ├── take-4-globex-demo.mp4
│   └── take-5-ablation.mp4
├── assets/
│   ├── logo.png
│   ├── architecture-diagram.png
│   ├── ablation-chart.png
│   └── github-qr.png
├── audio/
│   ├── narration.wav
│   └── background-music.mp3
├── project/
│   ├── memoryguard-demo.prproj  (Premiere)
│   └── memoryguard-demo.davinci  (DaVinci Resolve)
└── exports/
    ├── memoryguard-demo-main.mp4      (3-5 min)
    └── memoryguard-demo-short.mp4     (60 sec)
```

---

## 🚀 Quick Recording Command (OBS)

```bash
# Start Streamlit
streamlit run src/ui/main.py --server.port=8501

# In OBS:
# 1. Add "Window Capture" → Streamlit browser window
# 2. Add "Audio Input Capture" → Microphone
# 3. Settings → Output → Recording → MP4, 1080p, 30fps, CBR 8000 Kbps
# 4. Hotkeys: Start/Stop Recording (Ctrl+Shift+R)
```

---

## ✅ Final Verification Before Submit

- [ ] Video plays without errors
- [ ] Audio clear, no background noise
- [ ] Captions accurate (auto-generated + manual fix)
- [ ] All demo moments visible and clear
- [ ] GitHub URL visible and clickable
- [ ] Duration: 3-5 min (main) + 60s (short)
- [ ] File size < 500MB each
- [ ] Uploaded to YouTube (unlisted or public)
- [ ] Links added to hackathon submission form

---

*Ready to record. All demo scenarios tested and working.*