---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
title: About Me
---

<!-- Photo -->
<div class="about-photo-wrapper mb-4">
  <img src="/assets/img/about-photo.png" alt="Fu Qilin" class="about-photo">
</div>

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
    <div class="education-logos">
      <div class="edu-logo-item">
        <img src="/assets/img/suat.svg" alt="SUAT" class="edu-logo">
        <div class="edu-info">
          <p class="exp-title"><strong>Shenzhen University of Advanced Technology</strong></p>
          <p class="exp-period">2025 - 2028</p>
        </div>
      </div>
      <div class="edu-logo-item">
        <img src="/assets/img/南方科技大学-logo.svg" alt="SUSTech" class="edu-logo">
        <div class="edu-info">
          <p class="exp-title"><strong>Southern University of Science and Technology</strong></p>
          <p class="exp-period">2025 - 2028</p>
        </div>
      </div>
      <div class="edu-logo-item">
        <img src="/assets/img/安徽大学-logo.svg" alt="Anhui University" class="edu-logo">
        <div class="edu-info">
          <p class="exp-title"><strong>Anhui University</strong></p>
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
/* Photo */
.about-photo-wrapper {
  text-align: center;
}

.about-photo {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--avatar-border-color, rgb(206 206 206 / 90%));
}

/* Section styling */
.section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  border-bottom: 2px solid var(--main-border-color, #e9ecef);
  padding-bottom: 0.4rem;
  margin-bottom: 1rem;
  color: var(--heading-color);
}

.section-body p {
  margin-bottom: 0.6rem;
  line-height: 1.7;
  color: var(--text-color);
}

/* Card styling — using Chirpy's --card-bg for dark mode */
.card {
  border: 1px solid var(--main-border-color, rgba(128, 128, 128, 0.15));
  border-radius: 8px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.8rem;
  background: var(--card-bg, #fff);
}

/* Experience items */
.exp-title {
  margin-bottom: 0.2rem;
  color: var(--text-color);
}

.exp-detail {
  margin-bottom: 0.15rem;
  color: var(--text-muted-color, #999);
}

.exp-period {
  font-size: 0.85rem;
  color: var(--text-muted-color, #999);
  margin-bottom: 0;
}

/* Timeline items */
.timeline-item {
  position: relative;
  border-left: 3px solid var(--main-border-color, #e9ecef);
  margin-left: 0.5rem;
  padding-left: 1rem;
}

/* Project cards */
.project-card {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--text-color);
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
  color: var(--text-color);
}

/* Education logos */
.education-logos {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.edu-logo-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem 1rem;
  border: 1px solid var(--main-border-color, rgba(128, 128, 128, 0.15));
  border-radius: 8px;
  background: var(--card-bg, #fff);
}

.edu-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  flex-shrink: 0;
}

.edu-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.edu-info .exp-title {
  margin: 0;
}

.edu-info .exp-period {
  margin: 0;
}
</style>
