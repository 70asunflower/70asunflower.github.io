---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
title: About Me
---

<!-- About Me -->
<div class="section" id="about-me">
  <h3 class="section-title">About Me</h3>
  <div class="section-body">
    <p>Hi, my name is <strong>Fu Qilin</strong>. I am a tech enthusiast and creator based in Shenzhen, China. My interests focus on programming, tools, and continuous growth.</p>
    <p>I enjoy building projects, automating workflows, and sharing what I learn. I believe in learning by doing — every project is a chance to level up.</p>
    <p><strong><a href="#">Download my CV</a></strong> (Updated: April 2026)</p>
  </div>
</div>

<!-- Education -->
<div class="section" id="education">
  <h3 class="section-title">Education</h3>
  <div class="section-body">
    <div class="card">
      <div class="experience-content">
        <p class="exp-title"><strong>Shenzhen University</strong></p>
        <p class="exp-detail">Bachelor of Computer Science</p>
        <p class="exp-period">2022 - 2026</p>
      </div>
    </div>
  </div>
</div>

<!-- Experience -->
<div class="section" id="experience">
  <h3 class="section-title">Experience</h3>
  <div class="section-body">
    <div class="card timeline-item">
      <div class="experience-content">
        <p class="exp-title"><strong>Freelance Developer</strong></p>
        <p class="exp-detail">Full-stack development & automation</p>
        <p class="exp-period">2024 - Present</p>
      </div>
    </div>
  </div>
</div>

<!-- Projects -->
<div class="section" id="projects">
  <h3 class="section-title">Projects</h3>
  <div class="section-body">
    <div class="card project-card">
      <a href="https://70asunflower.github.io" style="font-weight: 500">Personal Homepage</a> <a href="https://github.com/70asunflower/70asunflower.github.io" target="_blank" style="text-decoration: none; margin-left: 8px;"><i class="fab fa-github"></i></a>: A personal homepage built with Jekyll & Chirpy theme, hosted on GitHub Pages.
    </div>
    <div class="card project-card">
      <a href="#" style="font-weight: 500">Notion IM Helper</a> <a href="https://github.com/70asunflower/my-skills" target="_blank" style="text-decoration: none; margin-left: 8px;"><i class="fab fa-github"></i></a>: Sync IM messages to Notion via Notion API.
    </div>
  </div>
</div>

<!-- Awards -->
<div class="section" id="awards">
  <h3 class="section-title">Awards</h3>
  <div class="section-body">
    <div class="awards-grid">
      <div class="award-item">
        <span class="award-icon">🏅</span>
        <div class="award-text"><strong>Placeholder Award</strong></div>
      </div>
    </div>
  </div>
</div>

<style>
/* Section styling - matching Luka template style */
.section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  border-bottom: 2px solid var(--sidebar-border-color, #e9ecef);
  padding-bottom: 0.4rem;
  margin-bottom: 1rem;
}

.section-body p {
  margin-bottom: 0.6rem;
  line-height: 1.7;
}

/* Card styling */
.card {
  border: 1px solid var(--card-border-color, rgba(0, 0, 0, 0.08));
  border-radius: 8px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.8rem;
  background: var(--card-bg, #fff);
}

/* Experience items */
.exp-title {
  margin-bottom: 0.2rem;
}

.exp-detail {
  margin-bottom: 0.15rem;
  color: var(--text-muted, #6c757d);
}

.exp-period {
  font-size: 0.85rem;
  color: var(--text-muted, #6c757d);
  margin-bottom: 0;
}

/* Timeline items */
.timeline-item {
  position: relative;
  border-left: 3px solid var(--sidebar-border-color, #e9ecef);
  margin-left: 0.5rem;
  padding-left: 1rem;
}

/* Project cards */
.project-card {
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Awards */
.awards-grid {
  display: grid;
  gap: 0.6rem;
}

.award-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.award-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.award-text {
  margin: 0;
}
</style>
