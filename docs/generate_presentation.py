#!/usr/bin/env python3
"""
Generate a 12-slide Hackathon-SEE presentation for Cloud Service Provider (CloudGuard).
Alliance University • Department of Information Technology • Linux System Administration (E1ITA307)
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette ──
BG_DARK = RGBColor(10, 17, 40)          # #0A1128
NAVY_PRIMARY = RGBColor(15, 23, 42)      # #0F172A
NAVY_DEEP = RGBColor(30, 58, 138)        # #1E3A8A
BLUE_ACCENT = RGBColor(37, 99, 235)      # #2563EB
CYAN_ACCENT = RGBColor(2, 132, 199)      # #0284C7
CYAN_LIGHT = RGBColor(56, 189, 248)      # #38BDF8
BG_LIGHT = RGBColor(248, 250, 252)       # #F8FAFC
CARD_BG = RGBColor(255, 255, 255)        # #FFFFFF
CARD_BG_TINT = RGBColor(241, 245, 249)   # #F1F5F9
CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0
TEXT_PRIMARY = RGBColor(15, 23, 42)      # #0F172A
TEXT_SECONDARY = RGBColor(71, 85, 105)   # #475569
TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B
GREEN_SUCCESS = RGBColor(5, 150, 105)    # #059669
GREEN_TINT = RGBColor(236, 253, 245)     # #ECFDF5
AMBER_ACCENT = RGBColor(217, 119, 6)     # #D97706
LINE_COLOR = RGBColor(203, 213, 225)     # #CBD5E1

FONT_HEADING = "Trebuchet MS"
FONT_BODY = "Calibri"
FONT_MONO = "Consolas"

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title, subtitle, slide_num):
    # Breadcrumb
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(9.5), Inches(0.3))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = "CLOUD SERVICE PROVIDER  •  HACKATHON-SEE  |  LINUX SYSTEM ADMINISTRATION"
    p_cat.font.name = FONT_HEADING
    p_cat.font.size = Pt(8.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE_ACCENT

    # Title & Subtitle
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.62), Inches(10.5), Inches(0.7))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

    p_sub = tf_title.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_SECONDARY
    p_sub.space_before = Pt(2)

    # University Seal top-right
    seal_path = "assets/logos/img-002.png"
    if os.path.exists(seal_path):
        slide.shapes.add_picture(seal_path, Inches(11.95), Inches(0.35), width=Inches(0.62), height=Inches(0.62))

    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.36), Inches(11.733), Pt(1))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE_COLOR
    line.line.fill.background()

def add_footer(slide, slide_num, total_slides=12):
    # Bottom divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Pt(1))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE_COLOR
    line.line.fill.background()

    # Footer text
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.35))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "Alliance School of Advanced Computing  •  Department of Information Technology  |  CloudGuard Platform"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED

    # Slide number on right
    tb_num = slide.shapes.add_textbox(Inches(11.0), Inches(7.02), Inches(1.533), Inches(0.35))
    tf_num = tb_num.text_frame
    tf_num.word_wrap = True
    tf_num.margin_left = tf_num.margin_right = tf_num.margin_top = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"Slide {slide_num} of {total_slides}"
    p_num.font.name = FONT_BODY
    p_num.font.size = Pt(9)
    p_num.font.bold = True
    p_num.font.color.rgb = BLUE_ACCENT

def add_card(slide, left, top, width, height, title, items, bg_color=CARD_BG, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.10)

    # Title paragraph
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(11.5)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY
    p_title.space_after = Pt(3)

    # Bullet items
    for item in items:
        p = tf.add_paragraph()
        p.space_after = Pt(2.5)
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        
        # If item has a bold lead prefix (format: "KEYWORD: Rest of text")
        if ":" in item:
            parts = item.split(":", 1)
            run1 = p.add_run()
            run1.text = "•  " + parts[0] + ":"
            run1.font.bold = True
            run1.font.color.rgb = NAVY_PRIMARY
            
            run2 = p.add_run()
            run2.text = parts[1]
            run2.font.bold = False
            run2.font.color.rgb = TEXT_SECONDARY
        else:
            run = p.add_run()
            run.text = "•  " + item
            run.font.color.rgb = TEXT_SECONDARY
    return card

def add_image_card(slide, left, top, width, height, img_path, caption):
    # Outer container card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1)

    caption_h = Inches(0.38)
    padding = Inches(0.12)
    img_box_w = width - (padding * 2)
    img_box_h = height - caption_h - (padding * 2)

    if os.path.exists(img_path):
        im = Image.open(img_path)
        orig_w, orig_h = im.size
        aspect = orig_w / orig_h
        box_aspect = img_box_w / img_box_h

        if aspect > box_aspect:
            final_w = img_box_w
            final_h = img_box_w / aspect
            final_l = left + padding
            final_t = top + padding + (img_box_h - final_h) / 2
        else:
            final_h = img_box_h
            final_w = img_box_h * aspect
            final_l = left + padding + (img_box_w - final_w) / 2
            final_t = top + padding

        # Image
        pic = slide.shapes.add_picture(img_path, final_l, final_t, width=final_w, height=final_h)
        pic.line.color.rgb = RGBColor(203, 213, 225)
        pic.line.width = Pt(0.75)

    # Caption box at bottom
    cap_top = top + height - caption_h - Inches(0.04)
    tb_cap = slide.shapes.add_textbox(left + padding, cap_top, width - (padding * 2), caption_h)
    tf_cap = tb_cap.text_frame
    tf_cap.word_wrap = True
    tf_cap.margin_left = tf_cap.margin_right = tf_cap.margin_top = tf_cap.margin_bottom = 0
    p_cap = tf_cap.paragraphs[0]
    p_cap.alignment = PP_ALIGN.CENTER
    p_cap.text = caption
    p_cap.font.name = FONT_BODY
    p_cap.font.size = Pt(8.5)
    p_cap.font.bold = True
    p_cap.font.color.rgb = NAVY_PRIMARY

# ── Main Presentation Generator ──

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: Title Slide (Dark Theme)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_DARK)

    # Alliance Banner Logo top-center
    banner_path = "assets/logos/img-000.png"
    if os.path.exists(banner_path):
        s1.shapes.add_picture(banner_path, Inches(0.8), Inches(0.6), width=Inches(3.8))

    # University Seal top-right
    seal_path = "assets/logos/img-002.png"
    if os.path.exists(seal_path):
        s1.shapes.add_picture(seal_path, Inches(11.4), Inches(0.5), width=Inches(1.1), height=Inches(1.1))

    # Sub-header category tag
    tb_tag = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.4))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "LINUX SYSTEM ADMINISTRATION (E1ITA307)  •  HACKATHON-SEE PROJECT REPORT"
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = CYAN_LIGHT

    # Main Project Title
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.733), Inches(1.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_main = tf_title.paragraphs[0]
    p_main.text = "CLOUD SERVICE PROVIDER"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(36)
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(255, 255, 255)

    p_sub = tf_title.add_paragraph()
    p_sub.text = "CloudGuard: Enterprise Multi-Tenant Linux Infrastructure & Administration Platform"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)
    p_sub.space_before = Pt(4)

    # Accent decorative line
    line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.6), Inches(11.733), Pt(2))
    line.fill.solid()
    line.fill.fore_color.rgb = BLUE_ACCENT
    line.line.fill.background()

    # Team Card (Left)
    card_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.9), Inches(5.6), Inches(2.8))
    card_team.fill.solid()
    card_team.fill.fore_color.rgb = RGBColor(15, 23, 42)
    card_team.line.color.rgb = RGBColor(51, 65, 85)
    card_team.line.width = Pt(1)

    tf_ct = card_team.text_frame
    tf_ct.word_wrap = True
    tf_ct.margin_left = tf_ct.margin_right = Inches(0.25)
    tf_ct.margin_top = Inches(0.2)
    p_ct_t = tf_ct.paragraphs[0]
    p_ct_t.text = "PROJECT TEAM"
    p_ct_t.font.name = FONT_HEADING
    p_ct_t.font.size = Pt(12)
    p_ct_t.font.bold = True
    p_ct_t.font.color.rgb = CYAN_LIGHT
    p_ct_t.space_after = Pt(6)

    team_members = [
        "SHOBITH I K  (2411021061604)",
        "ALLEN CHRIST A  (2411021061266)",
        "SRIKANTH C  (2411021061560)",
        "ANASUYA K ANIL  (L2411021061702)"
    ]
    for tm in team_members:
        p_m = tf_ct.add_paragraph()
        p_m.text = "•  " + tm
        p_m.font.name = FONT_BODY
        p_m.font.size = Pt(10)
        p_m.font.bold = True
        p_m.font.color.rgb = RGBColor(241, 245, 249)
        p_m.space_after = Pt(2)

    p_deg = tf_ct.add_paragraph()
    p_deg.text = "Bachelor of Technology in Information Technology"
    p_deg.font.name = FONT_BODY
    p_deg.font.size = Pt(9)
    p_deg.font.color.rgb = RGBColor(148, 163, 184)
    p_deg.space_before = Pt(4)

    # Faculty & Institution Card (Right)
    card_fac = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(3.9), Inches(5.6), Inches(2.8))
    card_fac.fill.solid()
    card_fac.fill.fore_color.rgb = RGBColor(15, 23, 42)
    card_fac.line.color.rgb = RGBColor(51, 65, 85)
    card_fac.line.width = Pt(1)

    tf_cf = card_fac.text_frame
    tf_cf.word_wrap = True
    tf_cf.margin_left = tf_cf.margin_right = Inches(0.25)
    tf_cf.margin_top = Inches(0.2)
    p_cf_t = tf_cf.paragraphs[0]
    p_cf_t.text = "SUPERVISION & INSTITUTION"
    p_cf_t.font.name = FONT_HEADING
    p_cf_t.font.size = Pt(12)
    p_cf_t.font.bold = True
    p_cf_t.font.color.rgb = CYAN_LIGHT
    p_cf_t.space_after = Pt(6)

    fac_info = [
        ("Under the Supervision of:", "Prof. Ananthanagu U"),
        ("Designation:", "Assistant Professor, Dept. of Information Technology"),
        ("Faculty Leadership:", "Dr. Shekhar R, Professor & HoD"),
        ("Institution:", "Alliance School of Advanced Computing"),
        ("University:", "Alliance University, Bengaluru"),
        ("Academic Submission:", "November 2026  •  Academic Year 2026–2027")
    ]
    for lbl, val in fac_info:
        p_f = tf_cf.add_paragraph()
        run_l = p_f.add_run()
        run_l.text = lbl + " "
        run_l.font.bold = True
        run_l.font.name = FONT_BODY
        run_l.font.size = Pt(9.5)
        run_l.font.color.rgb = RGBColor(148, 163, 184)
        run_v = p_f.add_run()
        run_v.text = val
        run_v.font.name = FONT_BODY
        run_v.font.size = Pt(9.5)
        run_v.font.color.rgb = RGBColor(241, 245, 249)
        p_f.space_after = Pt(2)

    print("Slide 1 built")

    # ==========================================
    # SLIDE 2: Introduction & Project Overview
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, BG_LIGHT)
    add_header(s2, "1. Introduction & Project Overview", "Engineering an isolated, resilient, and observable Linux multi-tenant hosting platform", 2)
    add_footer(s2, 2)

    col_w = Inches(5.5)
    add_card(s2, Inches(0.8), Inches(1.5), col_w, Inches(1.65), "Platform Foundation (CloudGuard)", [
        "System Scope: Production-style Cloud Service Provider (CSP) implemented natively on Ubuntu Server 26.04.1 LTS.",
        "Zero Cloud Vendor Lock-In: 100% built with open-source core utilities (LVM2, Nginx, UFW, OpenSSH, Systemd, Bash, Flask).",
        "Target Architecture: Multi-tenant virtual hosting with hard resource boundaries, defense-in-depth security, and real-time observability."
    ])

    add_card(s2, Inches(0.8), Inches(3.25), col_w, Inches(1.85), "Core Engineering Capabilities", [
        "Storage Isolation: Dynamic LVM2 volume quotas preventing noisy-neighbor filesystem exhaustion.",
        "Access Security: Zero-trust POSIX permissions (2750), nologin customer shells, and Ed25519 SSH keys.",
        "Resilience & Telemetry: Automated 7-generation rsync backup rotation and authenticated web dashboard.",
        "Service Hardening: Systemd unit sandboxing with ProtectSystem=strict and NoNewPrivileges."
    ])

    add_card(s2, Inches(0.8), Inches(5.2), col_w, Inches(1.5), "Academic Alignment", [
        "Curriculum Focus: Validates core competencies from Linux System Administration (E1ITA307).",
        "Demonstrated Skills: Kernel partition tables, volume groups, POSIX DAC, network routing, and automation scripting."
    ])

    add_image_card(s2, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "assets/diagrams/arch_overview.png", "Figure 1.1: Complete CloudGuard Architectural Hierarchy across 5 core operational layers.")
    print("Slide 2 built")

    # ==========================================
    # SLIDE 3: Problem Statement & Objectives
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, BG_LIGHT)
    add_header(s3, "2. Problem Statement & Core Objectives", "Overcoming security vulnerabilities and operational risks in shared multi-tenant hosting", 3)
    add_footer(s3, 3)

    half_w = Inches(5.7)
    add_card(s3, Inches(0.8), Inches(1.5), half_w, Inches(1.65), "The Shared Hosting Dilemma: Storage Contention", [
        "Unbounded Directory Growth: Standard directory sharing allows a single runaway tenant to fill the entire root filesystem.",
        "Noisy-Neighbor Failure: Global disk exhaustion causes database corruption, system logging failures, and kernel panics."
    ])

    add_card(s3, Inches(0.8), Inches(3.25), half_w, Inches(1.75), "Security Threat: Cross-Tenant Privilege Traversal", [
        "Permissive Default Permissions: Default Linux umask (022) results in 0755 permissions, making web trees world-readable.",
        "Confidentiality Breach: In shared environments, one tenant can inspect proprietary code and databases of another tenant.",
        "Interactive Shell Exploitation: Shell access enables unprivileged local privilege escalation attempts."
    ])

    add_card(s3, Inches(0.8), Inches(5.1), half_w, Inches(1.6), "Operational Risks: Blind Spots & Data Loss", [
        "Lack of Central Telemetry: Administrators cannot detect runaway processes or disk threshold violations in real time.",
        "Manual Backup Failure: Ad-hoc backup routines lack strict retention limits, leading to storage exhaustion or stale archives."
    ])

    # Right side: Strategic Objectives (4 Pillars)
    add_card(s3, Inches(6.8), Inches(1.5), half_w, Inches(1.25), "Pillar 1: Hardware-Like Storage Quotas (LVM2)", [
        "Provision dedicated physical partitions and logical volumes (client1_lv, client2_lv, backup_lv) to eliminate neighbor spillover."
    ], bg_color=CARD_BG_TINT)

    add_card(s3, Inches(6.8), Inches(2.85), half_w, Inches(1.25), "Pillar 2: Zero-Trust Tenant Isolation", [
        "Enforce nologin shells and locked passwords; lock customer web directories to mode 2750 (drwxr-s---) with setgid group inheritance."
    ], bg_color=CARD_BG_TINT)

    add_card(s3, Inches(6.8), Inches(4.2), half_w, Inches(1.25), "Pillar 3: Layered Perimeter Defense", [
        "Bind administrative and web services strictly to private host-only subnet (192.168.56.0/24); enforce Ed25519 SSH keys."
    ], bg_color=CARD_BG_TINT)

    add_card(s3, Inches(6.8), Inches(5.55), half_w, Inches(1.25), "Pillar 4: Automated Lifecycle & Management", [
        "Deploy daily cron backups with 7-generation FIFO retention and a sandboxed, authenticated Flask administrative dashboard."
    ], bg_color=CARD_BG_TINT)
    print("Slide 3 built")

    # ==========================================
    # SLIDE 4: System Architecture
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, BG_LIGHT)
    add_header(s4, "3. System & Network Architecture", "Dual-homed network topology, hypervisor abstraction, and interface isolation", 4)
    add_footer(s4, 4)

    add_card(s4, Inches(0.8), Inches(1.5), col_w, Inches(1.65), "Host & Virtual Machine Environment", [
        "Host Workstation: EndeavourOS Linux (Rolling Release, Kernel 6.x) providing host management tools and Ed25519 client.",
        "Type-2 Hypervisor: Oracle VM VirtualBox 7.x with dual virtual network adapters and secondary dedicated virtual disk.",
        "Server Virtual Machine: Ubuntu Server 26.04.1 LTS (x86_64, 4 vCPUs, 4 GiB RAM, 25 GiB system root + 25 GiB data disk)."
    ])

    add_card(s4, Inches(0.8), Inches(3.25), col_w, Inches(2.0), "Dual-Adapter Network Strategy", [
        "Adapter 1 (NAT - enp0s3): Dynamic DHCP IP; strictly dedicated to outbound internet connectivity for APT packages and NTP time sync. All inbound external traffic rejected.",
        "Adapter 2 (Host-Only - enp0s8): Static IP 192.168.56.103/24; isolated internal management plane for SSH, HTTP web hosting, and Flask telemetry. No external routing.",
        "Interface Segmentation: Guarantees server management is fully decoupled from public internet exposure."
    ])

    add_card(s4, Inches(0.8), Inches(5.35), col_w, Inches(1.35), "Name Resolution & Host Configuration", [
        "Host /etc/hosts Aliases: client1.cloudguard.local and client2.cloudguard.local mapped to 192.168.56.103.",
        "SSH Client Config: ~/.ssh/config alias cloudguard configured with Ed25519 identity."
    ])

    add_image_card(s4, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "assets/diagrams/network_topology.png", "Figure 3.1: Dual-adapter network topology separating internet egress from private management traffic.")
    print("Slide 4 built")

    # ==========================================
    # SLIDE 5: Server Provisioning & Storage (LVM)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, BG_LIGHT)
    add_header(s5, "4. Server Provisioning & Storage (LVM)", "Secondary block device partitioning, LVM2 volume pooling, and persistent fstab mounts", 5)
    add_footer(s5, 5)

    add_card(s5, Inches(0.8), Inches(1.5), col_w, Inches(1.75), "Secondary Storage Abstraction", [
        "Dedicated Storage Device: 25 GiB secondary virtual disk (/dev/sdb) separate from the OS root partition (/dev/sda).",
        "GPT Partition Table: Created GUID Partition Table with partition /dev/sdb1 flagged as Linux LVM (type 8e00 / 0FC63DAF).",
        "Physical Volume (PV): Initialized via pvcreate /dev/sdb1, providing 25.00 GiB of managed raw storage capacity."
    ])

    add_card(s5, Inches(0.8), Inches(3.35), col_w, Inches(1.85), "Volume Group & Logical Volume Allocation", [
        "Volume Group (VG): cloudguard_vg initialized with 25.00 GiB total capacity.",
        "Dynamic Capacity Reserve: 20.00 GiB carved into logical volumes; 5.00 GiB unallocated reserve kept for live online expansion.",
        "client1_lv: 8.00 GiB ext4 mounted persistently at /srv/client1 (Customer 1).",
        "client2_lv: 8.00 GiB ext4 mounted persistently at /srv/client2 (Customer 2).",
        "backup_lv: 4.00 GiB ext4 mounted persistently at /srv/backups (Backup Vault)."
    ])

    add_card(s5, Inches(0.8), Inches(5.3), col_w, Inches(1.4), "Persistent Mounting via UUIDs", [
        "fstab Reliability: Mounts mapped via immutable filesystem UUIDs preventing drive letter reordering errors across reboots.",
        "ext4 Journaling: Standard ordered data journaling guarantees metadata integrity during unexpected power loss."
    ])

    add_image_card(s5, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "CloudGuard_Evidence/screenshots/02_lvm_storage_configuration.png", "Figure 4.1: Terminal output verifying LVM PVs, VGs, LVs, and persistent mountpoints via lsblk.")
    print("Slide 5 built")

    # ==========================================
    # SLIDE 6: Customer Management & Isolation
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, BG_LIGHT)
    add_header(s6, "5. Customer Account Management & Isolation", "Least-privilege account provisioning, disabled shells, and POSIX setgid directory barriers", 6)
    add_footer(s6, 6)

    add_card(s6, Inches(0.8), Inches(1.5), col_w, Inches(1.75), "Least-Privilege User Provisioning", [
        "Dedicated System Accounts: client1 (UID 1001) and client2 (UID 1002) provisioned with primary groups matching usernames.",
        "Interactive Shell Prohibited: Configured with -s /usr/sbin/nologin; blocks interactive console, SSH sessions, and sudo escalation.",
        "Password Field Locked: passwd -l locks password hash in /etc/shadow, preventing credential brute-force attacks."
    ])

    add_card(s6, Inches(0.8), Inches(3.35), col_w, Inches(1.85), "Directory Ownership & POSIX Permissions", [
        "Document Roots: /srv/client1/public and /srv/client2/public.",
        "Dual Ownership Model: Chowned to clientN:www-data ensuring mutual access between customer owner and Nginx web server.",
        "Strict Permission Mode: Locked to 2750 (drwxr-s---).",
        "SetGID Bit (2): Guarantees that any new files or subdirectories created automatically inherit group ownership www-data."
    ])

    add_card(s6, Inches(0.8), Inches(5.3), col_w, Inches(1.4), "Cross-Tenant Traversal Validation", [
        "Zero-Trust Proof: Executing sudo -u client1 ls /srv/client2/public strictly triggers Permission Denied at kernel VFS level.",
        "Complete Privacy: Competitor tenants cannot list files, read code, or traverse directories across volume boundaries."
    ])

    add_image_card(s6, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "CloudGuard_Evidence/screenshots/03_customer_account_isolation.png", "Figure 5.1: Proof of customer account parameters, locked shells, and cross-tenant traversal refusal.")
    print("Slide 6 built")

    # ==========================================
    # SLIDE 7: Web Hosting & Virtual Hosts
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, BG_LIGHT)
    add_header(s7, "6. Multi-Tenant Web Hosting with Nginx", "Name-based virtual host routing, independent document roots, and audit logging", 7)
    add_footer(s7, 7)

    add_card(s7, Inches(0.8), Inches(1.5), col_w, Inches(1.7), "Nginx Web Engine Architecture", [
        "High-Performance Reverse Proxy: Deployed Nginx 1.24+ running under systemd with worker processes bound to group www-data.",
        "Default Site Deactivation: Removed /etc/nginx/sites-enabled/default to eliminate server fingerprinting and default welcome leakage.",
        "Syntax Validation: Every configuration change verified using nginx -t prior to graceful reload."
    ])

    add_card(s7, Inches(0.8), Inches(3.3), col_w, Inches(1.9), "Name-Based Virtual Host Configuration", [
        "Virtual Host 1: client1.cloudguard.local -> Document Root: /srv/client1/public (index.html with Alpha Enterprises branding).",
        "Virtual Host 2: client2.cloudguard.local -> Document Root: /srv/client2/public (index.html with Beta Solutions branding).",
        "HTTP Header Inspection: Nginx evaluates incoming Host header and serves exclusively from the tenant's isolated storage volume."
    ])

    add_card(s7, Inches(0.8), Inches(5.3), col_w, Inches(1.4), "Dedicated Logging & Verification", [
        "Per-Tenant Log Segregation: Independent access and error logs stored in /var/log/nginx/clientN_access.log.",
        "Host Curl Validation: Executed curl -I against both hostnames; both return HTTP 200 OK with accurate payload delivery."
    ])

    add_image_card(s7, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "CloudGuard_Evidence/screenshots/04_customer_websites.png", "Figure 6.1: Nginx virtual hosts serving distinct customer homepages with HTTP 200 validation.")
    print("Slide 7 built")

    # ==========================================
    # SLIDE 8: Security Implementation
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, BG_LIGHT)
    add_header(s8, "7. Multi-Layered Security Hardening", "Subnet-restricted UFW firewall, Ed25519 cryptographic SSH, and root lockdown", 8)
    add_footer(s8, 8)

    add_card(s8, Inches(0.8), Inches(1.5), col_w, Inches(1.85), "Subnet-Restricted Perimeter Firewall (UFW)", [
        "Default Traffic Policy: Incoming traffic DENIED by default; outgoing traffic ALLOWED.",
        "Strict Interface & Subnet Binding: Inbound traffic permitted ONLY on Host-Only interface (enp0s8) from host subnet 192.168.56.0/24:",
        "  • TCP 22: SSH Administrative Access",
        "  • TCP 80: Nginx Customer Websites",
        "  • TCP 5000: CloudGuard Dashboard UI",
        "Public Interface Rejection: External NAT interface (enp0s3) drops all incoming packets, preventing internet scans."
    ])

    add_card(s8, Inches(0.8), Inches(3.45), col_w, Inches(1.9), "OpenSSH Cryptographic Hardening", [
        "Hardened Drop-in: /etc/ssh/sshd_config.d/99-cloudguard.conf.",
        "PasswordAuthentication no: Passwords completely rejected at protocol handshake level.",
        "PermitRootLogin no: Direct root logins blocked; requires unprivileged user + sudo.",
        "PubkeyAuthentication yes: Enforces 256-bit elliptic-curve Ed25519 key authentication (~/.ssh/cloudguard_ed25519)."
    ])

    add_card(s8, Inches(0.8), Inches(5.45), col_w, Inches(1.25), "Runtime Security Validation", [
        "Effective Config Audit: Verified via sshd -T; confirmed effective runtime configuration matches security policy."
    ])

    add_image_card(s8, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "CloudGuard_Evidence/screenshots/05_firewall_and_ssh_security.png", "Figure 7.1: Active UFW firewall rules and OpenSSH cryptographic runtime configuration.")
    print("Slide 8 built")

    # ==========================================
    # SLIDE 9: Backup & Disaster Recovery
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, BG_LIGHT)
    add_header(s9, "8. Automated Backup & Disaster Recovery", "Atomic rsync snapshots, automated 7-generation retention, and restoration drill", 9)
    add_footer(s9, 9)

    add_card(s9, Inches(0.8), Inches(1.5), col_w, Inches(1.8), "Production Backup Script Engineering", [
        "Strict Shell Mode: /usr/local/sbin/cloudguard-backup.sh authored with set -Eeuo pipefail and umask 077.",
        "Atomic Snapshot Creation: rsync -a creates timestamped archives in isolated backup volume /srv/backups/cloudguard/<timestamp>/.",
        "Comprehensive Audit Log: Every run records start time, transferred directory trees, and exit code in /var/log/cloudguard-backup.log."
    ])

    add_card(s9, Inches(0.8), Inches(3.4), col_w, Inches(1.8), "7-Generation FIFO Retention Algorithm", [
        "Storage Capacity Safeguard: Script dynamically counts existing timestamped backup directories.",
        "Automated Pruning: When count exceeds 7, the oldest snapshots are pruned via rm -rf.",
        "Zero Disk Exhaustion: Guarantees that the dedicated backup volume (backup_lv, 4 GiB) never fills up or impacts customer storage."
    ])

    add_card(s9, Inches(0.8), Inches(5.3), col_w, Inches(1.4), "Cron Scheduling & Restoration Drill", [
        "Automated Daily Execution: Scheduled at 02:00 IST via /etc/cron.d/cloudguard-backup.",
        "Restoration Verification Drill: Simulated accidental web file deletion; successfully restored from backup snapshot with 100% md5 match."
    ])

    add_image_card(s9, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "CloudGuard_Evidence/screenshots/06_backup_history_and_logs.png", "Figure 8.1: Timestamped snapshot archives, automated retention logs, and cron scheduling.")
    print("Slide 9 built")

    # ==========================================
    # SLIDE 10: Monitoring & Dashboard
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, BG_LIGHT)
    add_header(s10, "9. System Monitoring & Administration Dashboard", "Automated cron telemetry, Flask web interface, and systemd sandboxing", 10)
    add_footer(s10, 10)

    add_card(s10, Inches(0.8), Inches(1.5), col_w, Inches(1.7), "Hourly Health Telemetry Daemon", [
        "Monitoring Script: /usr/local/sbin/cloudguard-monitor.sh executes hourly via /etc/cron.d/cloudguard-monitor.",
        "Tracked Metrics: CPU uptime, RAM consumption (with 80% threshold warning), filesystem usage on /srv/*, LVM volume health, and daemon status (nginx, ssh, cron).",
        "Persistent Log: Structured output appended to /var/log/cloudguard-monitor.log."
    ])

    add_card(s10, Inches(0.8), Inches(3.3), col_w, Inches(1.9), "CloudGuard Web Administration UI", [
        "Application Stack: Python 3 / Flask served through production Gunicorn WSGI bound strictly to 192.168.56.103:5000.",
        "Secure Authentication: HTTP Basic Authentication using constant-time hash comparison (hmac.compare_digest) preventing timing attacks.",
        "Unified Visibility: Real-time gauges for CPU/RAM, LVM storage pool allocation, customer public directories, and backup history."
    ])

    add_card(s10, Inches(0.8), Inches(5.3), col_w, Inches(1.4), "Systemd Daemon Sandboxing", [
        "Unprivileged Service Account: Runs as dedicated system user cloudguard-dashboard without sudo privileges.",
        "Security Directives: ProtectSystem=strict, ProtectHome=true, PrivateTmp=true, NoNewPrivileges=true."
    ])

    add_image_card(s10, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "CloudGuard_Evidence/screenshots/01a_cloudguard_dashboard_overview.png", "Figure 9.1: Live CloudGuard Dashboard showing system metrics, storage gauges, and service health.")
    print("Slide 10 built")

    # ==========================================
    # SLIDE 11: Testing & Results
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, BG_LIGHT)
    add_header(s11, "10. Testing, Validation & Acceptance Matrix", "100% verification pass rate across storage, security, hosting, and backup criteria", 11)
    add_footer(s11, 11)

    add_card(s11, Inches(0.8), Inches(1.5), col_w, Inches(3.6), "System Acceptance Testing Matrix", [
        "Storage & LVM: 3/3 Logical volumes online; persistent fstab UUID mounts; zero leakage between filesystems. [STATUS: PASS]",
        "Tenant Security: Customer 1 denied traversal of Customer 2 root; nologin shell active; password locked. [STATUS: PASS]",
        "Web Delivery: HTTP 200 OK across both virtual hosts; distinct tenant payloads delivered. [STATUS: PASS]",
        "Firewall & SSH: Password login rejected; root login blocked; UFW subnet binding active. [STATUS: PASS]",
        "Backup & Retention: Daily cron operational; 7-generation rotation verified; restore drill OK. [STATUS: PASS]",
        "Dashboard Hardening: Gunicorn active; systemd sandboxing enforced; REST API authenticated. [STATUS: PASS]"
    ])

    add_card(s11, Inches(0.8), Inches(5.2), col_w, Inches(1.5), "Quantitative Verification Metrics", [
        "Core Functional Test Cases: 11 of 11 Executed and Passed (100% Success Rate).",
        "Dashboard REST API Endpoints: 12 of 12 Validated with Basic Auth (100% Pass).",
        "Zero Unhandled Exceptions: Error logs audited clean across Nginx, SSH, and Gunicorn."
    ], bg_color=GREEN_TINT, border_color=RGBColor(167, 243, 208))

    add_image_card(s11, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2), "CloudGuard_Evidence/screenshots/01b_cloudguard_dashboard_storage_backups.png", "Figure 10.1: Dashboard Storage Pool and Backup History audit showing real-time system metrics.")
    print("Slide 11 built")

    # ==========================================
    # SLIDE 12: Conclusion & Future Scope
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, BG_LIGHT)
    add_header(s12, "11. Conclusion & Future Enhancements", "Project achievements, operational boundaries, and technical expansion roadmap", 12)
    add_footer(s12, 12)

    add_card(s12, Inches(0.8), Inches(1.5), half_w, Inches(2.6), "Summary of Project Achievements", [
        "Fully Functional Cloud Platform: Engineered a complete, multi-tenant Linux Cloud Service Provider entirely using native Linux utilities and systemd daemons.",
        "Hardware-Enforced Multi-Tenancy: Combined LVM storage quotas, POSIX permissions (2750), and UFW packet filtering to establish zero-trust customer boundaries.",
        "Automated Resilience: Engineered zero-touch backup rotation (7-generation FIFO) and hourly health telemetry ensuring rapid disaster recovery.",
        "Centralized Observability: Deployed a hardened, sandboxed web dashboard providing unified visibility into host metrics and tenant resources."
    ])

    add_card(s12, Inches(0.8), Inches(4.2), half_w, Inches(2.5), "Current Operational Limitations", [
        "Plaintext HTTP Delivery: Websites and dashboard operate over HTTP without automated TLS/HTTPS encryption.",
        "Single-Node Architecture: Operates within a single virtual machine without multi-node clustering or high-availability failover.",
        "Manual Customer Onboarding: Provisioning new tenants requires administrative script execution rather than a self-service customer portal."
    ])

    # Right side: Next-Generation Roadmap
    add_card(s12, Inches(6.8), Inches(1.5), half_w, Inches(1.25), "Roadmap 1: Automated TLS/HTTPS Provisioning", [
        "Integrate Let's Encrypt / Certbot to automate ACME SSL/TLS certificate issuance, renewal, and HTTPS redirection for all virtual hosts."
    ], bg_color=CARD_BG_TINT)

    add_card(s12, Inches(6.8), Inches(2.85), half_w, Inches(1.25), "Roadmap 2: Containerized Customer Runtimes", [
        "Migrate customer web trees to rootless Docker / Podman containers to enforce kernel namespace and cgroup CPU/memory limits per tenant."
    ], bg_color=CARD_BG_TINT)

    add_card(s12, Inches(6.8), Inches(4.2), half_w, Inches(1.25), "Roadmap 3: High Availability & Clustered Storage", [
        "Deploy Ceph or GlusterFS distributed storage across multiple server nodes with HAProxy load balancing for zero-downtime failover."
    ], bg_color=CARD_BG_TINT)

    add_card(s12, Inches(6.8), Inches(5.55), half_w, Inches(1.25), "Roadmap 4: Self-Service Customer API & Billing", [
        "Build a RESTful self-service provisioning API with automated quota billing, custom DNS configuration, and automated invoice generation."
    ], bg_color=CARD_BG_TINT)
    print("Slide 12 built")

    # Save presentation
    output_path = "Cloud_Service_Provider_Hackathon_SEE_Presentation.pptx"
    prs.save(output_path)
    print(f"\nPresentation successfully created: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == "__main__":
    build_presentation()
