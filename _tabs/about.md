---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
title: About
---

<!-- Photo -->
<div class="about-photo-wrapper mb-4">
  <div class="about-photo" role="img" aria-label="Fu Qilin"></div>
</div>

<!-- About Me -->
<div class="section" id="about-me">
  <h3 class="section-title">About Me</h3>
  <div class="section-body">
    <p>Hi, my name is <strong>Fu Qilin</strong>. I am a tech enthusiast and creator based in Shenzhen, China. My interests focus on programming, tools, and continuous growth.</p>
    <p>I enjoy building projects, automating workflows, and sharing what I learn. I believe in learning by doing — every project is a chance to level up.</p>
    <p><strong><a href="https://github.com/70asunflower" target="_blank" rel="noopener">View my GitHub →</a></strong></p>
  </div>
</div>

<!-- Education -->
<div class="section" id="education">
  <h3 class="section-title">Education</h3>
  <div class="section-body">

    <div class="card">
      <div class="experience-item">
        <div class="institution-logo logo-suat" title="Shenzhen University of Advanced Technology"></div>
        <div class="experience-content">
          <p class="exp-title"><strong>Shenzhen University of Advanced Technology</strong></p>
          <p class="exp-detail">Master of Engineering in Electronic Information</p>
          <p class="exp-period">2025 - Present</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="experience-item">
        <div class="institution-logo logo-sustech" title="Southern University of Science and Technology"></div>
        <div class="experience-content">
          <p class="exp-title"><strong>Southern University of Science and Technology</strong></p>
          <p class="exp-detail">Master of Engineering in Electronic Information</p>
          <p class="exp-period">2025 - Present</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="experience-item">
        <div class="institution-logo logo-ahu" title="Anhui University"></div>
        <div class="experience-content">
          <p class="exp-title"><strong>Anhui University</strong></p>
          <p class="exp-detail">Bachelor of Engineering in Electronic Science and Technology</p>
          <p class="exp-period">2020 - 2024</p>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- Experience -->
<div class="section" id="experience">
  <h3 class="section-title">Experience</h3>
  <div class="section-body">
    <div class="card timeline-item">
      <div class="experience-item">
        <div class="experience-content">
          <p class="exp-title"><strong>Freelance Developer</strong></p>
          <p class="exp-detail">Full-stack development & automation</p>
          <p class="exp-period">2024 - Present</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Projects -->
<div class="section" id="projects">
  <h3 class="section-title">Projects</h3>
  <div class="section-body">
    <div class="project-card"><a href="https://github.com/70asunflower/ai-learning-journey" class="project-name">AI Learning Journey</a> <a href="https://github.com/70asunflower/ai-learning-journey" target="_blank" class="project-badge"><img src="https://img.shields.io/github/stars/70asunflower/ai-learning-journey?style=social&amp;logo=github" alt="GitHub stars"></a>: A curated knowledge base for AI/LLM learning, covering fine-tuning (LoRA/QLoRA/SFT/DPO), quantization, inference, and deployment with structured resources and notes.</div>
    <div class="project-card"><a href="https://github.com/70asunflower/ic-chip-design-learning" class="project-name">IC Chip Design Learning</a> <a href="https://github.com/70asunflower/ic-chip-design-learning" target="_blank" class="project-badge"><img src="https://img.shields.io/github/stars/70asunflower/ic-chip-design-learning?style=social&amp;logo=github" alt="GitHub stars"></a>: A structured learning path for IC chip design, from RTL design and verification to physical design and tapeout, covering digital/analog design, UVM, and EDA flows.</div>
  </div>
</div>


<style>
/* ===== Luka-style About Me Page ===== */

/* Accent color — warm brown-orange, adapts to dark mode */
:root {
  --about-accent: #c2714f;
  --about-accent-rgb: 194, 113, 79;
  --about-secondary: #8c8577;
}

[data-theme="dark"] {
  --about-accent: #e28a67;
  --about-accent-rgb: 226, 138, 103;
  --about-secondary: #9b9488;
}

/* Photo */
.about-photo-wrapper {
  text-align: center;
}

.about-photo {
  display: inline-block;
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background-image: url("/assets/img/about-photo.png");
  background-size: cover;
  background-position: center;
  border: 3px solid rgba(var(--about-accent-rgb), 0.3);
  transition: border-color 0.3s;
  cursor: default;
}

.about-photo:hover {
  border-color: var(--about-accent);
}

/* Section */
.section {
  margin-bottom: 2rem;
}

.section-title {
  display: inline-block;
  margin: 0 0 18px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--about-accent);
  color: var(--about-accent);
  font-size: 19px;
  font-weight: 600;
}

.section-body p {
  margin: 0 0 14px;
  line-height: 1.75;
  color: var(--text-color);
}

/* Card — Luka style: transparent, no background */
.card {
  background: transparent;
  padding: 0;
  box-shadow: none;
  border: none;
  border-radius: 0;
  margin-bottom: 0;
  cursor: default;
}

/* Experience items */
.experience-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.institution-logo {
  width: 52px;
  height: 52px;
  flex-shrink: 0;
  border-radius: 6px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: default;
}

.logo-suat { background-image: url("/assets/img/suat.svg"); }
.logo-sustech { background-image: url("/assets/img/sustech-logo.svg"); }
.logo-ahu { background-image: url("/assets/img/ahu-logo.svg"); }

.experience-content {
  flex: 1;
}

.experience-content p {
  margin: 0 0 2px;
}

.exp-title {
  font-size: 15px;
  color: var(--text-color);
}

.exp-detail {
  font-size: 14px;
  color: var(--about-secondary);
}

.exp-period {
  font-size: 13px;
  color: var(--about-accent);
  font-weight: 500;
  margin-bottom: 0;
}

/* Timeline — Luka style with gradient line + dot */
.timeline-item {
  position: relative;
  margin-left: 20px;
  padding-left: 8px;
  padding-bottom: 20px;
}

.timeline-item::before {
  content: "";
  position: absolute;
  left: -20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--about-accent), rgba(var(--about-accent-rgb), 0.12));
}

.timeline-item:last-child::before {
  bottom: 50%;
}

.timeline-item::after {
  content: "";
  position: absolute;
  left: -25px;
  top: 22px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--about-accent);
  border: 2px solid var(--card-bg, #fff);
}

/* Project cards */
.project-card {
  font-size: 16px;
  line-height: 1.7;
  padding: 0 0 14px;
  color: var(--text-color);
}

.project-name {
  font-weight: 600;
  font-size: 16px;
}

.project-badge {
  text-decoration: none;
  margin-left: 8px;
}

.project-badge img {
  vertical-align: middle;
}

.project-card + .project-card {
  padding-top: 8px;
  border-top: 1px dashed rgba(var(--about-accent-rgb), 0.25);
}

/* Awards */
.awards-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.award-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 0;
}

.award-icon {
  flex-shrink: 0;
  font-size: 20px;
}

.award-text {
  color: var(--text-color);
  font-size: 14px;
  margin: 0;
}

/* Links in about page */
.section-body a {
  color: var(--about-accent);
  text-decoration: none;
  border-bottom: 1px solid rgba(var(--about-accent-rgb), 0.3);
  transition: border-color 0.2s;
}

.section-body a:hover {
  border-bottom-color: var(--about-accent);
}

/* Responsive */
@media (max-width: 640px) {
  .experience-item {
    gap: 12px;
  }
  .institution-logo {
    width: 44px;
    height: 44px;
  }
  .section-title {
    font-size: 18px;
  }
}
</style>




