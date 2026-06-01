<template>
  <div class="land" ref="landRef">

    <!-- ══ NAVBAR ══ -->
    <header :class="['nav', { 'nav--scrolled': scrolled }]" ref="navRef">
      <div class="nav__inner">
        <RouterLink to="/" class="nav__logo">
          <AppLogo :icon-size="32" :font-size="18" :gap="9" />
        </RouterLink>

        <nav class="nav__links" ref="navLinksRef">
          <a href="#features" @click.prevent="scrollTo('#features')">Fonctionnalités</a>
          <a href="#sectors" @click.prevent="scrollTo('#sectors')">Secteurs</a>
          <a href="#testimonials" @click.prevent="scrollTo('#testimonials')">Témoignages</a>
          <a href="#faq" @click.prevent="scrollTo('#faq')">FAQ</a>
        </nav>

        <div class="nav__cta">
          <RouterLink to="/login" class="nav__login">Se connecter</RouterLink>
          <RouterLink to="/dashboard" class="btn-primary btn-sm">Demander une démo</RouterLink>
        </div>

        <button class="nav__burger" @click="mobileOpen = !mobileOpen" aria-label="Menu">
          <span :class="['burger-line', { open: mobileOpen }]"></span>
          <span :class="['burger-line', { open: mobileOpen }]"></span>
          <span :class="['burger-line', { open: mobileOpen }]"></span>
        </button>
      </div>

      <Transition name="mobile">
        <div v-if="mobileOpen" class="nav__mobile">
          <a href="#features" @click="mobileOpen=false; scrollTo('#features')">Fonctionnalités</a>
          <a href="#sectors" @click="mobileOpen=false; scrollTo('#sectors')">Secteurs</a>
          <a href="#testimonials" @click="mobileOpen=false; scrollTo('#testimonials')">Témoignages</a>
          <a href="#faq" @click="mobileOpen=false; scrollTo('#faq')">FAQ</a>
          <div class="nav__mobile-cta">
            <RouterLink to="/login" class="btn-ghost btn-full" @click="mobileOpen=false">Se connecter</RouterLink>
            <RouterLink to="/dashboard" class="btn-primary btn-full" @click="mobileOpen=false">Essai gratuit</RouterLink>
          </div>
        </div>
      </Transition>
    </header>

    <!-- ══ HERO ══ -->
    <section class="hero" ref="heroRef">
      <!-- Animated blobs -->
      <div class="hero__blobs" aria-hidden="true">
        <div class="blob blob--1"></div>
        <div class="blob blob--2"></div>
        <div class="blob blob--3"></div>
      </div>
      <!-- Noise texture -->
      <div class="hero__noise" aria-hidden="true"></div>

      <div class="hero__container">
        <!-- Left: copy -->
        <div class="hero__copy" ref="heroCopyRef">
          <div class="hero__badge">
            <span class="badge__dot"></span>
            Solution RH des équipes de terrain
          </div>

          <h1 class="hero__title">
            La gestion RH
            <br>
            <span class="hero__title-gradient">qui fait vraiment<br>la différence</span>
          </h1>

          <div class="hero__features" aria-live="polite">
            <TransitionGroup name="feature-slide" tag="div" class="hero__features-inner">
              <div
                v-for="(feat, i) in heroFeatures"
                v-show="activeFeature === i"
                :key="i"
                class="hero__feature-item"
              >
                <div class="hero__feature-icon" :style="{ background: feat.bg }">
                  <v-icon size="16" :color="feat.iconColor">{{ feat.icon }}</v-icon>
                </div>
                {{ feat.text }}
              </div>
            </TransitionGroup>
          </div>

          <p class="hero__sub">
            Planification, suivi des temps, paie et admin RH — réunis dans une interface que vos équipes adorent vraiment utiliser.
          </p>

          <div class="hero__actions">
            <RouterLink to="/dashboard" class="btn-primary btn-hero">
              Démarrer gratuitement
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </RouterLink>
            <RouterLink to="/dashboard" class="btn-video">
              <div class="btn-video__play">
                <svg width="12" height="14" viewBox="0 0 12 14" fill="none"><path d="M1 1l10 6L1 13V1z" fill="currentColor"/></svg>
              </div>
              Voir la démo
            </RouterLink>
          </div>

          <div class="hero__trust">
            <div class="trust-avatars">
              <img v-for="n in 4" :key="n" :src="`https://i.pravatar.cc/32?img=${n+10}`" class="trust-avatar" alt="utilisateur" loading="lazy">
            </div>
            <div class="trust-text">
              <div class="trust-stars">
                <svg v-for="n in 5" :key="n" width="14" height="14" viewBox="0 0 24 24" fill="#F59E0B"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              </div>
              <span>4,5/5 · <strong>+2 000 avis</strong></span>
            </div>
          </div>
        </div>

        <!-- Right: 3D mockup card -->
        <div class="hero__visual" ref="heroVisualRef" @mousemove="tiltCard" @mouseleave="resetTilt">
          <div class="hero__card" ref="heroCardRef">
            <!-- App bar -->
            <div class="app-bar">
              <div class="app-bar__dots">
                <span class="dot dot--red"></span>
                <span class="dot dot--yellow"></span>
                <span class="dot dot--green"></span>
              </div>
              <div class="app-bar__title">Planning — Semaine 19</div>
              <div class="app-bar__actions">
                <div class="app-bar__btn">Publier</div>
              </div>
            </div>

            <!-- Days header -->
            <div class="schedule-header">
              <div class="emp-col"></div>
              <div v-for="day in days" :key="day" class="day-col">{{ day }}</div>
            </div>

            <!-- Rows -->
            <div class="schedule-body">
              <div v-for="emp in scheduleData" :key="emp.name" class="schedule-row">
                <div class="emp-info">
                  <div class="emp-avatar" :style="{ background: emp.color }">{{ emp.initials }}</div>
                  <div>
                    <div class="emp-name">{{ emp.name }}</div>
                    <div class="emp-role">{{ emp.role }}</div>
                  </div>
                </div>
                <div class="emp-grid">
                  <div
                    v-for="(shift, di) in emp.week"
                    :key="di"
                    :class="['shift', shift ? `shift--${shift.type}` : 'shift--empty']"
                  >
                    <span v-if="shift">{{ shift.label }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Stats footer -->
            <div class="card-footer">
              <div v-for="stat in cardStats" :key="stat.label" class="card-stat">
                <span class="card-stat__val">{{ stat.val }}</span>
                <span class="card-stat__label">{{ stat.label }}</span>
              </div>
            </div>
          </div>

          <!-- Floating chips -->
          <div class="float-chip float-chip--tl" v-motion :initial="{ opacity: 0, y: 20 }" :enter="{ opacity: 1, y: 0, transition: { delay: 600 } }">
            <div class="chip-icon chip-icon--green">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <div>
              <div class="chip-val">-22%</div>
              <div class="chip-label">Heures supp.</div>
            </div>
          </div>
          <div class="float-chip float-chip--br" v-motion :initial="{ opacity: 0, y: 20 }" :enter="{ opacity: 1, y: 0, transition: { delay: 800 } }">
            <div class="chip-icon chip-icon--blue">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="9" cy="7" r="4" stroke="white" stroke-width="2"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>
            </div>
            <div>
              <div class="chip-val">98%</div>
              <div class="chip-label">Satisfaction</div>
            </div>
          </div>
          <div class="float-chip float-chip--ml">
            <div class="chip-icon chip-icon--purple">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="white"/></svg>
            </div>
            <div>
              <div class="chip-val">4,5 / 5</div>
              <div class="chip-label">Note moyenne</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="hero__scroll">
        <div class="scroll-pill">
          <div class="scroll-ball"></div>
        </div>
        <span>Découvrir</span>
      </div>
    </section>

    <!-- ══ LOGOS ══ -->
    <section class="logos-section">
      <!-- Header -->
      <div class="section-wrap logos-header">
        <div class="logos-stat-pill">
          <div class="logos-stat-pill__dot"></div>
          <span><strong>25 000+</strong> équipes · <strong>600 000+</strong> salariés planifiés chaque semaine</span>
        </div>
        <h3 class="logos-headline">Des marques que vous connaissez, qui font confiance à TimeApp</h3>
        <p class="logos-sub">De la brasserie de quartier aux groupes internationaux, dans tous les secteurs.</p>
      </div>

      <!-- Une seule rangée défilante -->
      <div class="logos-rail">
        <div class="logos-fade logos-fade--l"></div>
        <div class="logos-fade logos-fade--r"></div>
        <div class="logos-track logos-track--fwd">
          <div
            v-for="(c, i) in [...logosAll, ...logosAll]"
            :key="`logo-${i}`"
            class="logo-card"
            :style="{ background: c.bg }"
          >
            <img
              :src="`https://cdn.simpleicons.org/${c.slug}`"
              :alt="c.name"
              class="logo-si-img"
              loading="lazy"
              @error="handleLogoError"
            >
            <span class="logo-brand-name" :style="{ color: c.color }">{{ c.name }}</span>
          </div>
        </div>
      </div>

      <!-- Trusted by note -->
      <div class="section-wrap logos-footer-note">
        <div class="logos-footer-note__inner">
          <div v-for="n in trustNotes" :key="n.text" class="trust-note">
            <v-icon size="15" :color="n.color">{{ n.icon }}</v-icon>
            <span>{{ n.text }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ STATS ══ -->
    <section class="stats-section" ref="statsRef">
      <div class="section-wrap">
        <div class="stats-grid">
          <div v-for="(s, i) in stats" :key="i" class="stat-card">
            <div class="stat-card__icon" :style="{ background: s.bg }">
              <v-icon size="22" :color="s.color">{{ s.icon }}</v-icon>
            </div>
            <div class="stat-card__val" :ref="el => statEls[i] = el">0</div>
            <div class="stat-card__label">{{ s.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ FEATURES ══ -->
    <section class="features-section" id="features" ref="featuresRef">
      <div class="section-wrap">
        <div class="section-eyebrow">Fonctionnalités</div>
        <h2 class="section-title">Tout ce dont vous avez besoin,<br>enfin réuni</h2>
        <p class="section-body">Fini les outils éparpillés. TimeApp centralise planning, temps, paie et RH dans une interface qui s'adapte à votre métier.</p>

        <!-- Tabs -->
        <div class="feat-tabs">
          <button
            v-for="(tab, i) in featureTabs"
            :key="i"
            :class="['feat-tab', { active: activeTab === i }]"
            @click="activeTab = i"
          >
            <div class="feat-tab__icon" :style="activeTab === i ? { background: tab.color } : {}">
              <v-icon size="16" :color="activeTab === i ? 'white' : 'grey-darken-2'">{{ tab.icon }}</v-icon>
            </div>
            {{ tab.label }}
          </button>
        </div>

        <!-- Feature content -->
        <div class="feat-content">
          <div class="feat-text">
            <h3>{{ featureTabs[activeTab].title }}</h3>
            <ul class="feat-list">
              <li v-for="p in featureTabs[activeTab].points" :key="p">
                <div class="feat-check">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                {{ p }}
              </li>
            </ul>
            <div class="feat-metrics">
              <div v-for="m in featureTabs[activeTab].metrics" :key="m.label" class="feat-metric">
                <span class="feat-metric__val">{{ m.val }}</span>
                <span class="feat-metric__label">{{ m.label }}</span>
              </div>
            </div>
            <RouterLink to="/dashboard" class="btn-primary btn-inline">
              Explorer cette fonctionnalité
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </RouterLink>
          </div>

          <div class="feat-visual">
            <img
              :src="featureTabs[activeTab].img"
              :alt="featureTabs[activeTab].label"
              class="feat-photo"
              loading="lazy"
            >
            <div class="feat-visual__overlay">
              <div class="feat-badge">
                <v-icon size="14" color="white">{{ featureTabs[activeTab].icon }}</v-icon>
                {{ featureTabs[activeTab].label }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ SECTORS ══ -->
    <section class="sectors-section" id="sectors">
      <div class="section-wrap">
        <div class="section-eyebrow">Secteurs</div>
        <h2 class="section-title">Fait pour votre métier,<br>pas pour un métier générique</h2>

        <div class="sectors-grid">
          <div
            v-for="(s, i) in sectors"
            :key="i"
            class="sector-card"
            @mouseenter="hoveredSector = i"
            @mouseleave="hoveredSector = null"
          >
            <div class="sector-card__top">
              <div class="sector-icon" :style="{ background: s.bg }">
                <v-icon size="22" :color="s.color">{{ s.icon }}</v-icon>
              </div>
              <div :class="['sector-arrow', { visible: hoveredSector === i }]">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M12 5l7 7-7 7" stroke="#4F46E5" stroke-width="2" stroke-linecap="round"/></svg>
              </div>
            </div>
            <h4 class="sector-card__title">{{ s.name }}</h4>
            <p class="sector-card__desc">{{ s.desc }}</p>
            <div class="sector-card__tag">{{ s.tag }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ AI SECTION ══ -->
    <section class="ai-section">
      <div class="ai-section__inner">
        <div class="section-wrap ai-grid">
          <div class="ai-text">
            <div class="section-eyebrow section-eyebrow--light">Intelligence Artificielle</div>
            <h2 class="section-title section-title--light">Votre assistant RH<br>disponible 24h/24</h2>
            <p class="section-body section-body--light">
              L'assistant TimeApp IA analyse vos données en temps réel, optimise vos plannings et trouve des remplaçants en quelques secondes.
            </p>
            <ul class="feat-list feat-list--light">
              <li v-for="p in aiPoints" :key="p">
                <div class="feat-check feat-check--light">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="#4F46E5" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                {{ p }}
              </li>
            </ul>
            <RouterLink to="/dashboard" class="btn-white-outline btn-inline">
              Découvrir l'IA TimeApp
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </RouterLink>
          </div>

          <div class="ai-visual">
            <!-- Chat interface -->
            <div class="ai-chat">
              <div class="ai-chat__header">
                <div class="ai-avatar">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" fill="white"/></svg>
                </div>
                <div>
                  <div class="ai-chat__name">Assistant TimeApp</div>
                  <div class="ai-chat__status">
                    <span class="status-dot"></span> En ligne
                  </div>
                </div>
                <div class="ai-chat__badge">IA</div>
              </div>

              <div class="ai-chat__body">
                <div class="chat-msg chat-msg--bot">
                  <div class="chat-msg__bubble">
                    Bonjour Sophie 👋 Le planning de la semaine prochaine est prêt. J'ai détecté un conflit mardi matin.
                  </div>
                  <span class="chat-msg__time">09:14</span>
                </div>

                <div class="chat-msg chat-msg--user">
                  <div class="chat-msg__bubble">
                    Trouve-moi un remplaçant pour Thomas mardi 8h-16h
                  </div>
                  <span class="chat-msg__time">09:15</span>
                </div>

                <div class="chat-msg chat-msg--bot">
                  <div class="chat-msg__bubble">
                    ✅ J'ai trouvé <strong>3 disponibilités</strong> compatibles avec les contraintes légales :
                  </div>
                  <span class="chat-msg__time">09:15</span>
                </div>

                <div class="chat-suggestions">
                  <div v-for="s in aiSuggestions" :key="s.name" class="chat-suggestion">
                    <div class="chat-sugg__avatar" :style="{ background: s.color }">{{ s.init }}</div>
                    <div class="chat-sugg__info">
                      <div class="chat-sugg__name">{{ s.name }}</div>
                      <div class="chat-sugg__hours">{{ s.hours }}</div>
                    </div>
                    <button class="chat-sugg__btn">Assigner</button>
                  </div>
                </div>

                <div class="chat-typing">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>

            <!-- Stat chips floating -->
            <div class="ai-stat ai-stat--1">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M22 12h-4l-3 9L9 3l-3 9H2" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>+47% de temps gagné</span>
            </div>
            <div class="ai-stat ai-stat--2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#F59E0B" stroke-width="2"/><path d="M12 6v6l4 2" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/></svg>
              <span>2 min pour trouver un remplaçant</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ TESTIMONIALS ══ -->
    <section class="testi-section" id="testimonials">
      <div class="section-wrap">
        <div class="section-eyebrow">Témoignages</div>
        <div class="testi-header">
          <h2 class="section-title">Leurs équipes adorent TimeApp.<br><em>Les managers aussi.</em></h2>
          <div class="testi-nav">
            <button class="testi-nav__btn" @click="testiScroll(-1)" aria-label="Précédent">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            </button>
            <button class="testi-nav__btn" @click="testiScroll(1)" aria-label="Suivant">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            </button>
          </div>
        </div>

        <div class="testi-track" ref="testiTrackRef">
          <div v-for="(t, i) in testimonials" :key="i" class="testi-card">
            <div class="testi-card__top">
              <div class="testi-card__quote">
                <svg width="24" height="18" viewBox="0 0 24 18" fill="none"><path d="M0 18V10.8C0 7.2 1.2 4.3 3.6 2.1 6 0 9.2-0.1 13.2 0.5L12 3.3C10 3 8.3 3.5 7 4.7 5.7 5.9 5 7.2 5 8.6H10V18H0ZM14 18V10.8C14 7.2 15.2 4.3 17.6 2.1 20-0.1 23.2-0.1 27.2 0.5L26 3.3C24 3 22.3 3.5 21 4.7 19.7 5.9 19 7.2 19 8.6H24V18H14Z" fill="#E5E7EB"/></svg>
              </div>
              <div class="testi-card__stars">
                <svg v-for="n in 5" :key="n" width="14" height="14" viewBox="0 0 24 24" fill="#F59E0B"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              </div>
            </div>
            <p class="testi-card__text">{{ t.text }}</p>
            <div class="testi-card__author">
              <img :src="t.photo" :alt="t.name" class="testi-avatar" loading="lazy">
              <div>
                <div class="testi-name">{{ t.name }}</div>
                <div class="testi-role">{{ t.role }}</div>
              </div>
              <div class="testi-tag">{{ t.sector }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ PRICING CTA ══ -->
    <section class="cta-section">
      <div class="cta-section__inner">
        <div class="cta-glow cta-glow--1"></div>
        <div class="cta-glow cta-glow--2"></div>
        <div class="section-wrap cta-content">
          <div class="cta-badge">
            <span>✦</span> 14 jours d'essai gratuits
          </div>
          <h2 class="cta-title">Prêt à transformer<br>la gestion de vos équipes ?</h2>
          <p class="cta-sub">Sans engagement. Sans carte de crédit. Annulable à tout moment.</p>
          <div class="cta-actions">
            <RouterLink to="/dashboard" class="btn-primary btn-xl">
              Commencer gratuitement
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </RouterLink>
            <RouterLink to="/dashboard" class="btn-outline-white btn-xl">
              Voir une démo
            </RouterLink>
          </div>
          <div class="cta-logos">
            <div v-for="c in ctaLogos" :key="c" class="cta-logo-item">{{ c }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ FAQ ══ -->
    <section class="faq-section" id="faq">
      <div class="section-wrap faq-inner">
        <div class="faq-left">
          <div class="section-eyebrow">FAQ</div>
          <h2 class="section-title">Des questions ?<br>On a les réponses.</h2>
          <p class="section-body">Vous ne trouvez pas votre réponse ? <a href="#" class="faq-contact">Contactez notre équipe →</a></p>
        </div>
        <div class="faq-list">
          <div
            v-for="(item, i) in faqItems"
            :key="i"
            :class="['faq-item', { 'faq-item--open': openFaq === i }]"
            @click="openFaq = openFaq === i ? null : i"
          >
            <div class="faq-item__q">
              {{ item.q }}
              <div :class="['faq-item__icon', { rotated: openFaq === i }]">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </div>
            </div>
            <Transition name="faq-expand">
              <div v-if="openFaq === i" class="faq-item__a">{{ item.a }}</div>
            </Transition>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ FOOTER ══ -->
    <footer class="site-footer">
      <div class="section-wrap">
        <div class="footer-top">
          <div class="footer-brand">
            <AppLogo :icon-size="32" :font-size="17" :gap="9" text-color="white" />
            <p>La solution RH intelligente des équipes de terrain.</p>
            <div class="footer-social">
              <a href="#" aria-label="LinkedIn"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg></a>
              <a href="#" aria-label="Twitter"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/></svg></a>
              <a href="#" aria-label="Instagram"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/></svg></a>
            </div>
          </div>

          <div v-for="col in footerCols" :key="col.title" class="footer-col">
            <h5>{{ col.title }}</h5>
            <ul>
              <li v-for="link in col.links" :key="link"><a href="#">{{ link }}</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom">
          <span>© {{ new Date().getFullYear() }} TimeApp SAS · Tous droits réservés</span>
          <div class="footer-legal">
            <a href="#">CGU</a>
            <a href="#">Confidentialité</a>
            <a href="#">Mentions légales</a>
          </div>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { RouterLink } from 'vue-router'
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import AppLogo from './AppLogo.vue'

gsap.registerPlugin(ScrollTrigger)

// ─── Navbar scroll ───
const scrolled = ref(false)
const mobileOpen = ref(false)
const navRef = ref(null)
let scrollHandler = () => { scrolled.value = window.scrollY > 40 }
onMounted(() => window.addEventListener('scroll', scrollHandler, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', scrollHandler))

const scrollTo = (selector) => {
  const el = document.querySelector(selector)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

// ─── Hero rotating feature ───
const activeFeature = ref(0)
const heroFeatures = [
  { icon: 'mdi-calendar-month-outline', text: 'Créez vos plannings intelligemment', bg: '#EEF2FF', iconColor: '#4F46E5' },
  { icon: 'mdi-clock-time-four-outline', text: 'Suivez les temps et présences', bg: '#ECFDF5', iconColor: '#10B981' },
  { icon: 'mdi-cash-multiple', text: 'Préparez la paie sans erreur', bg: '#FFF7ED', iconColor: '#F97316' },
  { icon: 'mdi-account-cog-outline', text: 'Gérez vos RH de A à Z', bg: '#FDF4FF', iconColor: '#A855F7' },
]
let featureInterval
onMounted(() => {
  featureInterval = setInterval(() => {
    activeFeature.value = (activeFeature.value + 1) % heroFeatures.length
  }, 2500)
})
onUnmounted(() => clearInterval(featureInterval))

// ─── 3D card tilt ───
const heroCardRef = ref(null)
const tiltCard = (e) => {
  const card = heroCardRef.value
  if (!card) return
  const rect = card.getBoundingClientRect()
  const x = (e.clientX - rect.left) / rect.width - 0.5
  const y = (e.clientY - rect.top) / rect.height - 0.5
  gsap.to(card, { rotateY: x * 12, rotateX: -y * 10, duration: 0.4, ease: 'power2.out', transformPerspective: 1000 })
}
const resetTilt = () => {
  gsap.to(heroCardRef.value, { rotateY: 0, rotateX: 0, duration: 0.6, ease: 'elastic.out(1, 0.75)' })
}

// ─── Schedule demo data ───
const days = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
const scheduleData = [
  { name: 'Marie Dupont', role: 'Responsable', initials: 'MD', color: '#4F46E5', week: [{ type: 'morning', label: '8-16h' }, { type: 'morning', label: '8-16h' }, null, { type: 'evening', label: '14-22h' }, { type: 'evening', label: '14-22h' }, null, null] },
  { name: 'Thomas R.', role: 'Serveur', initials: 'TR', color: '#10B981', week: [null, { type: 'day', label: '9-17h' }, { type: 'day', label: '9-17h' }, { type: 'day', label: '9-17h' }, null, { type: 'morning', label: '8-16h' }, null] },
  { name: 'Léa Martin', role: 'Caissière', initials: 'LM', color: '#A855F7', week: [{ type: 'morning', label: '8-16h' }, null, { type: 'evening', label: '14-22h' }, null, { type: 'day', label: '9-17h' }, { type: 'evening', label: '14-22h' }, null] },
  { name: 'Hugo Blanc', role: 'Manager', initials: 'HB', color: '#F97316', week: [{ type: 'day', label: '9-18h' }, { type: 'day', label: '9-18h' }, { type: 'day', label: '9-18h' }, null, { type: 'day', label: '9-18h' }, null, null] },
]
const cardStats = [
  { val: '32h', label: 'Moy/semaine' },
  { val: '94%', label: 'Couverture' },
  { val: '2', label: 'Conflits résolus' },
  { val: '↑12%', label: 'Efficacité' },
]

// ─── Logos Simple Icons CDN – slugs confirmés, une seule rangée ───
const logosAll = [
  { name: "McDonald's",    slug: 'mcdonalds',     color: '#FFC72C', bg: '#FFFBEB' },
  { name: 'Starbucks',     slug: 'starbucks',     color: '#00704A', bg: '#F0FAF4' },
  { name: 'Burger King',   slug: 'burgerking',    color: '#D62300', bg: '#FFF2F0' },
  { name: 'KFC',           slug: 'kfc',           color: '#F40027', bg: '#FFF0F0' },
  { name: 'Air France',    slug: 'airfrance',     color: '#002157', bg: '#EFF3FF' },
  { name: 'SNCF',          slug: 'sncf',          color: '#E2001A', bg: '#FFF0F1' },
  { name: 'Renault',       slug: 'renault',       color: '#111111', bg: '#F4F4F4' },
  { name: 'TotalEnergies', slug: 'totalenergies', color: '#C8102E', bg: '#FFF0F2' },
  { name: 'Orange',        slug: 'orange',        color: '#FF6600', bg: '#FFF5F0' },
  { name: 'IKEA',          slug: 'ikea',          color: '#0058A3', bg: '#F0F6FF' },
  { name: 'Amazon',        slug: 'amazon',        color: '#FF9900', bg: '#FFF8F0' },
  { name: 'Deliveroo',     slug: 'deliveroo',     color: '#00CCBC', bg: '#F0FFFE' },
  { name: 'Uber',          slug: 'uber',          color: '#000000', bg: '#F5F5F5' },
  { name: 'H&M',           slug: 'hm',            color: '#E50010', bg: '#FFF0F1' },
  { name: 'AXA',           slug: 'axa',           color: '#00008F', bg: '#F0F0FF' },
  { name: 'Zara',          slug: 'zara',          color: '#111111', bg: '#F4F4F4' },
]

// Supprime la carte si le logo ne charge pas
const handleLogoError = (e) => {
  const card = e.target.closest('.logo-card')
  if (card) card.style.display = 'none'
}

const trustNotes = [
  { icon: 'mdi-shield-check-outline', color: '#10B981', text: 'Données hébergées en Europe (RGPD)' },
  { icon: 'mdi-lock-outline', color: '#4F46E5', text: 'Certifié ISO 27001' },
  { icon: 'mdi-star-outline', color: '#F59E0B', text: '4,5/5 sur +2 000 avis vérifiés' },
  { icon: 'mdi-headset', color: '#F97316', text: 'Support dédié 7j/7' },
]

// ─── Stats with animated counters ───
const statsRef = ref(null)
const statEls = ref([])
const stats = [
  { val: 25000, suffix: '+', label: 'Équipes de terrain', icon: 'mdi-account-group-outline', color: '#4F46E5', bg: '#EEF2FF' },
  { val: 600000, suffix: '+', label: 'Salariés planifiés', icon: 'mdi-briefcase-outline', color: '#10B981', bg: '#ECFDF5' },
  { val: 2000, suffix: '+', label: 'Avis clients', icon: 'mdi-star-outline', color: '#F59E0B', bg: '#FFFBEB' },
  { val: 47, suffix: '%', label: 'De temps gagné en moyenne', icon: 'mdi-trending-up', color: '#F97316', bg: '#FFF7ED' },
]
onMounted(() => {
  nextTick(() => {
    if (!statsRef.value) return
    ScrollTrigger.create({
      trigger: statsRef.value,
      start: 'top 80%',
      once: true,
      onEnter: () => {
        stats.forEach((s, i) => {
          const el = statEls.value[i]
          if (!el) return
          gsap.fromTo({ n: 0 }, { n: s.val }, {
            duration: 2,
            ease: 'power2.out',
            onUpdate() {
              const v = Math.round(this.targets()[0].n)
              el.textContent = v >= 1000 ? (v / 1000).toFixed(v >= 100000 ? 0 : 1).replace('.', ',') + 'k' + s.suffix : v + s.suffix
            },
            onComplete() { el.textContent = s.val >= 1000 ? (s.val / 1000).toFixed(s.val >= 100000 ? 0 : 1).replace('.', ',') + 'k' + s.suffix : s.val + s.suffix }
          })
        })
      }
    })
  })
})

// ─── GSAP scroll animations ───
const featuresRef = ref(null)
const heroCopyRef = ref(null)
const heroVisualRef = ref(null)

onMounted(() => {
  nextTick(() => {
    // Hero entrance
    if (heroCopyRef.value) {
      gsap.from(heroCopyRef.value.children, {
        y: 30, opacity: 0, duration: 0.8, stagger: 0.12, ease: 'power3.out', delay: 0.2
      })
    }
    if (heroVisualRef.value) {
      gsap.from(heroVisualRef.value, {
        y: 50, opacity: 0, duration: 1, ease: 'power3.out', delay: 0.5
      })
    }

    // Scroll animations for sections
    document.querySelectorAll('.section-eyebrow, .section-title, .section-body, .feat-tabs, .sectors-grid .sector-card, .testi-card').forEach((el, i) => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 88%', once: true },
        y: 24, opacity: 0, duration: 0.7,
        ease: 'power3.out',
        delay: el.classList.contains('sector-card') || el.classList.contains('testi-card') ? (i % 4) * 0.1 : 0
      })
    })
  })
})

onUnmounted(() => ScrollTrigger.killAll())

// ─── Feature tabs ───
const activeTab = ref(0)
const featureTabs = [
  {
    icon: 'mdi-calendar-month-outline', label: 'Planification', color: '#4F46E5',
    title: 'Planifiez les bons employés au bon endroit',
    points: [
      'Générateur de planning intelligent en 1 clic',
      'Gestion des contraintes légales automatique',
      'Notifications en temps réel aux équipes',
      'Remplacement de dernière minute simplifié',
    ],
    metrics: [{ val: '80%', label: 'Moins de temps passé' }, { val: '0', label: 'Erreur légale' }],
    img: 'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=900&q=80',
  },
  {
    icon: 'mdi-clock-time-four-outline', label: 'Temps & Absences', color: '#10B981',
    title: 'Suivez chaque heure, chaque absence',
    points: [
      'Badgeuse mobile et tablette intégrée',
      'Compteurs CP, RTT et RCR en temps réel',
      'Signature électronique des feuilles d\'heures',
      'Alertes heures supplémentaires automatiques',
    ],
    metrics: [{ val: '-22%', label: 'Heures supp.' }, { val: '100%', label: 'Conformité' }],
    img: 'https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=900&q=80',
  },
  {
    icon: 'mdi-cash-multiple', label: 'Paie', color: '#F97316',
    title: 'Une paie préparée en quelques minutes',
    points: [
      'Calcul automatique des variables de paie',
      'Connexion avec les principaux logiciels de paie',
      'Distribution automatique des fiches de paie',
      'Export comptable en un clic',
    ],
    metrics: [{ val: '3h', label: 'Économisées/semaine' }, { val: '99%', label: 'Exactitude' }],
    img: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80',
  },
  {
    icon: 'mdi-account-cog-outline', label: 'Admin RH', color: '#A855F7',
    title: 'Centralisez toute la gestion RH',
    points: [
      'SIRH complet : contrats, documents, DPAEs',
      'Signature électronique des documents',
      'Registre du personnel conforme RGPD',
      'Gestion des onboarding et offboarding',
    ],
    metrics: [{ val: '-60%', label: 'Tâches manuelles' }, { val: 'RGPD', label: 'Certifié' }],
    img: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=900&q=80',
  },
]

// ─── Sectors ───
const hoveredSector = ref(null)
const sectors = [
  { name: 'Hôtellerie & Restauration', icon: 'mdi-silverware-fork-knife', color: '#F97316', bg: '#FFF7ED', desc: 'Horaires variables, gestion des extras et pics d\'activité.', tag: '🍽️ Restauration' },
  { name: 'Commerce & Distribution', icon: 'mdi-cart-outline', color: '#E11D48', bg: '#FFF1F2', desc: 'Temps partiels, ouvertures dominicales, rotation des équipes.', tag: '🛒 Retail' },
  { name: 'Pharmacie & Médical', icon: 'mdi-hospital-box', color: '#10B981', bg: '#ECFDF5', desc: 'Gardes, astreintes et qualification spécifique.', tag: '💊 Santé' },
  { name: 'Construction', icon: 'mdi-hard-hat', color: '#D97706', bg: '#FFFBEB', desc: 'Chantiers multiples et suivi des heures sur site.', tag: '🏗️ BTP' },
  { name: 'Industrie', icon: 'mdi-factory', color: '#3B82F6', bg: '#EFF6FF', desc: 'Cycles 2×8/3×8 et intégration des intérimaires.', tag: '⚙️ Industrie' },
  { name: 'Services', icon: 'mdi-briefcase-outline', color: '#8B5CF6', bg: '#F5F3FF', desc: 'Polyvalence des équipes et gestion des déplacements.', tag: '💼 Services' },
  { name: 'Loisirs & Bien-être', icon: 'mdi-dumbbell', color: '#EC4899', bg: '#FDF4FF', desc: 'Saisonnalité et horaires atypiques.', tag: '🏋️ Sport & Wellness' },
  { name: 'Grandes entreprises', icon: 'mdi-office-building', color: '#4F46E5', bg: '#EEF2FF', desc: 'Multi-sites, multi-conventions, tableaux de bord avancés.', tag: '🏢 Enterprise' },
]

// ─── AI section ───
const aiPoints = [
  'Planification automatique selon les contraintes et préférences',
  'Détection des conflits et suggestions de remplacement en temps réel',
  'Analyse prédictive des pics d\'activité',
  'Réponses RH instantanées 24h/24 via le chat',
]
const aiSuggestions = [
  { name: 'Marie Dubois', hours: 'Disponible 8h–16h · 38h/sem', color: '#4F46E5', init: 'MD' },
  { name: 'Paul Leroy', hours: 'Disponible 9h–17h · 35h/sem', color: '#10B981', init: 'PL' },
  { name: 'Camille V.', hours: 'Disponible toute la journée', color: '#A855F7', init: 'CV' },
]

// ─── Testimonials ───
const testiTrackRef = ref(null)
const testiScroll = (dir) => {
  if (testiTrackRef.value) {
    testiTrackRef.value.scrollBy({ left: dir * 380, behavior: 'smooth' })
  }
}
const testimonials = [
  { text: 'TimeApp a transformé notre façon de gérer les plannings. Ce qui prenait 3 heures nous prend maintenant 20 minutes. C\'est bluffant.', name: 'Sophie Marchand', role: 'Directrice RH · Groupe Brasserie', sector: '#Restauration', photo: 'https://i.pravatar.cc/56?img=47' },
  { text: 'La gestion des remplacements de dernière minute est devenue un jeu d\'enfant. L\'IA suggère les bons profils instantanément.', name: 'Nicolas Ferrand', role: 'Gérant · Intermarché Rebecq', sector: '#Commerce', photo: 'https://i.pravatar.cc/56?img=52' },
  { text: 'Nous gérons 45 collaborateurs sur 3 sites. TimeApp centralise tout. Je ne pourrais plus m\'en passer.', name: 'Anaïs Petit', role: 'Manager · Krys Group', sector: '#Optique', photo: 'https://i.pravatar.cc/56?img=48' },
  { text: 'Le suivi des heures sur chantier est enfin fiable. Finis les litiges avec les équipes en fin de mois.', name: 'Marc Dubois', role: 'Directeur · BTP Solutions', sector: '#Construction', photo: 'https://i.pravatar.cc/56?img=51' },
  { text: 'La conformité légale est gérée automatiquement. Je dors mieux la nuit, vraiment.', name: 'Charlène Jaffré', role: 'Directrice · Clinique Odento', sector: '#Médical', photo: 'https://i.pravatar.cc/56?img=44' },
  { text: 'L\'interface est tellement intuitive que même mes équipes qui ne sont pas à l\'aise avec la technologie l\'utilisent sans problème.', name: 'Thomas Garnier', role: 'Gérant · Starbucks Monaco', sector: '#Restauration', photo: 'https://i.pravatar.cc/56?img=53' },
]

// ─── CTA ───
const ctaLogos = ['Carrefour', 'Starbucks', 'Accor', 'Intermarché', '+21 000 autres']

// ─── FAQ ───
const openFaq = ref(0)
const faqItems = [
  { q: "Combien de temps pour démarrer avec TimeApp ?", a: "L'onboarding est rapide : importez vos données employés, configurez vos règles d'établissement et créez votre premier planning en moins d'une heure. Notre équipe vous accompagne tout au long de la prise en main." },
  { q: "TimeApp respecte-t-il la réglementation du travail ?", a: "Oui. TimeApp intègre les conventions collectives de votre secteur et les met à jour automatiquement. Des alertes vous préviennent en cas de dépassement légal avant la publication du planning." },
  { q: "Peut-on connecter TimeApp à notre logiciel de paie ?", a: "TimeApp s'intègre avec les principaux logiciels de paie (Silae, Sage, ADP, Cegid...). L'export des éléments variables de paie est automatisé et fiable." },
  { q: "Comment les salariés accèdent-ils à leur planning ?", a: "Via l'application mobile iOS/Android, l'espace web salarié, par email ou SMS. Chaque modification déclenche une notification automatique en temps réel." },
  { q: "Qu'est-ce qui se passe après les 14 jours d'essai ?", a: "Vous choisissez l'offre adaptée à votre équipe ou vous résiliez sans aucun frais. Aucune carte de crédit n'est requise pour l'essai." },
  { q: "Les données sont-elles sécurisées ?", a: "Vos données sont hébergées en Europe, chiffrées et certifiées ISO 27001. TimeApp est conforme au RGPD et effectue des audits de sécurité réguliers." },
]

// ─── Footer ───
const footerCols = [
  { title: 'Solutions', links: ['Planification', 'Temps & Absences', 'Paie', 'Admin RH', 'Assistant IA', 'App mobile', 'Badgeuse'] },
  { title: 'Secteurs', links: ['Restauration', 'Commerce', 'Pharma & Médical', 'Construction', 'Industrie', 'Services', 'Grandes entreprises'] },
  { title: 'Ressources', links: ['Centre d\'aide', 'Blog', 'Nouveautés', 'Témoignages', 'Partenaires', 'Carrières', 'À propos'] },
]
</script>

<style scoped>
/* ━━━ GLOBALS ━━━ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.land {
  font-family: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  color: #18181B;
  background: #FAFAFA;
  overflow-x: hidden;
}

.section-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #4F46E5;
  background: #EEF2FF;
  padding: 5px 14px;
  border-radius: 999px;
  margin-bottom: 20px;
}
.section-eyebrow--light {
  color: #A5B4FC;
  background: rgba(79, 70, 229, 0.25);
}

.section-title {
  font-size: clamp(1.8rem, 3.5vw, 2.75rem);
  font-weight: 800;
  line-height: 1.18;
  color: #09090B;
  margin-bottom: 18px;
}
.section-title em { color: #4F46E5; font-style: normal; }
.section-title--light { color: #FFFFFF; }

.section-body {
  font-size: 1.05rem;
  color: #71717A;
  line-height: 1.7;
  max-width: 540px;
  margin-bottom: 40px;
}
.section-body--light { color: #A1A1AA; }

/* ━━━ BUTTONS ━━━ */
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  background: #4F46E5; color: #fff !important; text-decoration: none;
  padding: 12px 24px; border-radius: 12px; font-size: 0.9rem; font-weight: 700;
  border: none; cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 14px rgba(79,70,229,0.35);
}
.btn-primary:hover { background: #4338CA; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(79,70,229,0.45); }
.btn-sm { padding: 9px 18px !important; font-size: 0.82rem !important; border-radius: 10px !important; }
.btn-hero { padding: 14px 28px; font-size: 0.97rem; border-radius: 14px; box-shadow: 0 6px 20px rgba(79,70,229,0.4); }
.btn-xl { padding: 16px 32px; font-size: 1rem; border-radius: 14px; }
.btn-inline { padding: 10px 20px; font-size: 0.875rem; }

.btn-video {
  display: inline-flex; align-items: center; gap: 10px;
  background: none; color: #3F3F46 !important; text-decoration: none;
  font-size: 0.9rem; font-weight: 600; cursor: pointer;
  transition: color 0.2s;
}
.btn-video:hover { color: #4F46E5 !important; }
.btn-video:hover .btn-video__play { background: #4F46E5; }
.btn-video__play {
  width: 40px; height: 40px; background: white;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  transition: background 0.2s; padding-left: 2px;
  color: #4F46E5;
}
.btn-video:hover .btn-video__play { color: white; }

.btn-ghost {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  background: none; color: #52525B !important; text-decoration: none;
  padding: 11px 20px; border-radius: 10px; font-size: 0.88rem; font-weight: 600;
  border: 1.5px solid #E4E4E7;
  transition: border-color 0.2s, color 0.2s;
}
.btn-ghost:hover { border-color: #4F46E5; color: #4F46E5 !important; }

.btn-full { width: 100%; }

.btn-outline-white {
  display: inline-flex; align-items: center; gap: 8px;
  background: none; color: white !important; text-decoration: none;
  padding: 16px 32px; border-radius: 14px; font-size: 1rem; font-weight: 700;
  border: 2px solid rgba(255,255,255,0.4);
  transition: background 0.2s, border-color 0.2s, transform 0.15s;
}
.btn-outline-white:hover { background: rgba(255,255,255,0.1); border-color: white; transform: translateY(-2px); }

.btn-white-outline {
  display: inline-flex; align-items: center; gap: 8px;
  background: none; color: white !important; text-decoration: none;
  padding: 10px 20px; border-radius: 12px; font-size: 0.875rem; font-weight: 600;
  border: 1.5px solid rgba(255,255,255,0.3);
  transition: background 0.2s, transform 0.15s;
}
.btn-white-outline:hover { background: rgba(255,255,255,0.1); transform: translateY(-2px); }

/* ━━━ NAVBAR ━━━ */
.nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  background: rgba(250, 250, 250, 0.8);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.nav--scrolled {
  border-color: rgba(0,0,0,0.08);
  box-shadow: 0 1px 20px rgba(0,0,0,0.06);
}
.nav__inner {
  max-width: 1200px; margin: 0 auto; padding: 0 24px;
  height: 68px; display: flex; align-items: center; gap: 32px;
}
.nav__logo {
  display: flex; align-items: center; gap: 9px;
  font-size: 1.18rem; font-weight: 800; color: #09090B !important; text-decoration: none;
  white-space: nowrap;
}
.nav__logo-icon {
  width: 32px; height: 32px; background: #4F46E5; border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 8px rgba(79,70,229,0.4);
}
.nav__links { display: flex; gap: 28px; flex: 1; }
.nav__links a {
  font-size: 0.875rem; font-weight: 500; color: #52525B;
  text-decoration: none; cursor: pointer; transition: color 0.2s;
}
.nav__links a:hover { color: #4F46E5; }
.nav__cta { display: flex; align-items: center; gap: 12px; white-space: nowrap; }
.nav__login {
  font-size: 0.875rem; font-weight: 600; color: #52525B !important; text-decoration: none;
  transition: color 0.2s;
}
.nav__login:hover { color: #4F46E5 !important; }
.nav__burger { display: none; background: none; border: none; cursor: pointer; padding: 4px; flex-direction: column; gap: 5px; margin-left: auto; }
.burger-line {
  display: block; width: 22px; height: 2px; background: #52525B;
  border-radius: 2px; transition: all 0.3s;
}
.nav__mobile {
  border-top: 1px solid #E4E4E7; padding: 20px 24px;
  background: white; display: flex; flex-direction: column; gap: 16px;
}
.nav__mobile a { font-size: 0.95rem; font-weight: 500; color: #3F3F46; text-decoration: none; }
.nav__mobile-cta { display: flex; flex-direction: column; gap: 8px; padding-top: 8px; }

/* ━━━ HERO ━━━ */
.hero {
  min-height: 100vh; padding-top: 68px;
  display: flex; flex-direction: column; align-items: stretch;
  position: relative; overflow: hidden; background: white;
}
.hero__blobs { position: absolute; inset: 0; pointer-events: none; z-index: 0; }
.blob {
  position: absolute; border-radius: 50%; filter: blur(80px);
  animation: blobFloat 8s ease-in-out infinite;
}
.blob--1 { width: 500px; height: 500px; background: rgba(79,70,229,0.08); top: -100px; right: -50px; animation-delay: 0s; }
.blob--2 { width: 400px; height: 400px; background: rgba(168,85,247,0.06); top: 200px; left: -100px; animation-delay: 2s; }
.blob--3 { width: 300px; height: 300px; background: rgba(16,185,129,0.05); bottom: 0; right: 200px; animation-delay: 4s; }
@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(20px, -20px) scale(1.05); }
  66% { transform: translate(-10px, 10px) scale(0.97); }
}
.hero__noise {
  position: absolute; inset: 0; z-index: 1; pointer-events: none; opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size: 200px;
}

.hero__container {
  max-width: 1200px; margin: 0 auto; padding: 80px 24px 60px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
  position: relative; z-index: 2; flex: 1;
}

.hero__badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: #EEF2FF; border: 1px solid #C7D2FE; color: #4F46E5;
  font-size: 0.78rem; font-weight: 700; padding: 7px 14px; border-radius: 999px;
  margin-bottom: 24px;
}
.badge__dot {
  width: 7px; height: 7px; background: #4F46E5; border-radius: 50%;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(79,70,229,0.4); }
  50% { box-shadow: 0 0 0 5px rgba(79,70,229,0); }
}

.hero__title {
  font-size: clamp(2.2rem, 4.5vw, 3.5rem); font-weight: 900; line-height: 1.12;
  color: #09090B; margin-bottom: 24px;
}
.hero__title-gradient {
  background: linear-gradient(135deg, #4F46E5 0%, #A855F7 60%, #EC4899 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.hero__features { height: 36px; margin-bottom: 20px; overflow: hidden; position: relative; }
.hero__features-inner { position: relative; height: 100%; }
.hero__feature-item {
  display: flex; align-items: center; gap: 10px;
  font-size: 0.95rem; font-weight: 600; color: #52525B;
  position: absolute; top: 0; left: 0; white-space: nowrap;
}
.hero__feature-icon {
  width: 28px; height: 28px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.hero__sub {
  font-size: 1rem; color: #71717A; line-height: 1.7; margin-bottom: 32px; max-width: 480px;
}
.hero__actions { display: flex; align-items: center; gap: 16px; margin-bottom: 36px; flex-wrap: wrap; }
.hero__trust { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.trust-avatars { display: flex; }
.trust-avatar {
  width: 30px; height: 30px; border-radius: 50%; border: 2px solid white;
  margin-left: -8px; object-fit: cover;
}
.trust-avatar:first-child { margin-left: 0; }
.trust-text { font-size: 0.82rem; color: #71717A; }
.trust-stars { display: flex; gap: 1px; margin-bottom: 2px; }
.trust-text strong { color: #09090B; }

/* Hero Visual */
.hero__visual {
  perspective: 1200px; position: relative; cursor: pointer;
  padding: 30px;
}
.hero__card {
  background: white; border-radius: 20px;
  box-shadow: 0 24px 80px rgba(0,0,0,0.12), 0 4px 20px rgba(79,70,229,0.1);
  border: 1px solid rgba(0,0,0,0.06); overflow: hidden;
  transform-style: preserve-3d; will-change: transform;
}
.app-bar {
  background: #F4F4F5; border-bottom: 1px solid #E4E4E7;
  padding: 12px 16px; display: flex; align-items: center; gap: 12px;
}
.app-bar__dots { display: flex; gap: 5px; }
.dot { width: 11px; height: 11px; border-radius: 50%; }
.dot--red { background: #FF5F57; }
.dot--yellow { background: #FEBC2E; }
.dot--green { background: #28C840; }
.app-bar__title { flex: 1; font-size: 0.8rem; font-weight: 600; color: #52525B; text-align: center; }
.app-bar__btn { font-size: 0.72rem; font-weight: 700; background: #4F46E5; color: white; padding: 4px 12px; border-radius: 6px; }

.schedule-header {
  display: grid; grid-template-columns: 140px repeat(7, 1fr);
  padding: 8px 14px; background: #FAFAFA; border-bottom: 1px solid #F0F0F0;
}
.day-col { text-align: center; font-size: 0.72rem; font-weight: 700; color: #A1A1AA; }

.schedule-body { padding: 8px 14px 0; display: flex; flex-direction: column; gap: 6px; }
.schedule-row { display: grid; grid-template-columns: 140px 1fr; align-items: center; gap: 10px; }
.emp-info { display: flex; align-items: center; gap: 9px; }
.emp-avatar {
  width: 28px; height: 28px; border-radius: 8px;
  font-size: 0.65rem; font-weight: 800; color: white;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.emp-name { font-size: 0.78rem; font-weight: 700; color: #18181B; white-space: nowrap; }
.emp-role { font-size: 0.65rem; color: #A1A1AA; }
.emp-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; }
.shift {
  border-radius: 5px; padding: 3px 2px; font-size: 0.6rem; font-weight: 700;
  text-align: center; transition: transform 0.1s;
}
.shift:hover { transform: scale(1.05); }
.shift--empty { background: #F4F4F5; }
.shift--morning { background: #EEF2FF; color: #4F46E5; }
.shift--day { background: #ECFDF5; color: #059669; }
.shift--evening { background: #FDF4FF; color: #9333EA; }

.card-footer {
  display: flex; border-top: 1px solid #F0F0F0; margin: 10px 0 0;
}
.card-stat {
  flex: 1; padding: 10px 12px; text-align: center;
  border-right: 1px solid #F0F0F0;
}
.card-stat:last-child { border-right: none; }
.card-stat__val { display: block; font-size: 0.9rem; font-weight: 800; color: #09090B; }
.card-stat__label { font-size: 0.6rem; color: #A1A1AA; }

/* Float chips */
.float-chip {
  position: absolute; background: white; border-radius: 14px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.12); padding: 10px 14px;
  display: flex; align-items: center; gap: 10px;
  border: 1px solid rgba(0,0,0,0.06);
}
.float-chip--tl { top: 0; right: -10px; }
.float-chip--br { bottom: 4px; left: 0; }
.float-chip--ml { left: -18px; top: 50%; transform: translateY(-50%); }
.chip-icon {
  width: 30px; height: 30px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
}
.chip-icon--green { background: #10B981; }
.chip-icon--blue { background: #3B82F6; }
.chip-icon--purple { background: #A855F7; }
.chip-val { font-size: 0.95rem; font-weight: 800; color: #09090B; }
.chip-label { font-size: 0.62rem; color: #A1A1AA; white-space: nowrap; }

/* Hero scroll */
.hero__scroll {
  position: relative; z-index: 2; display: flex; flex-direction: column;
  align-items: center; gap: 8px; padding-bottom: 32px;
  font-size: 0.75rem; color: #A1A1AA; font-weight: 500;
}
.scroll-pill {
  width: 22px; height: 36px; border: 2px solid #D4D4D8; border-radius: 12px;
  display: flex; justify-content: center; padding: 4px;
}
.scroll-ball {
  width: 6px; height: 6px; background: #4F46E5; border-radius: 50%;
  animation: scrollBall 1.8s ease-in-out infinite;
}
@keyframes scrollBall { 0% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(18px); opacity: 0; } }

/* ━━━ LOGOS ━━━ */
.logos-section {
  padding: 80px 0 64px;
  background: white;
  overflow: hidden;
  border-top: 1px solid #F0F0F0;
  border-bottom: 1px solid #F0F0F0;
}

/* Header */
.logos-header { text-align: center; margin-bottom: 48px; }

.logos-stat-pill {
  display: inline-flex; align-items: center; gap: 10px;
  background: #F4F4F5; border: 1px solid #E4E4E7;
  border-radius: 999px; padding: 7px 18px;
  font-size: 0.82rem; color: #52525B;
  margin-bottom: 20px;
}
.logos-stat-pill strong { color: #09090B; }
.logos-stat-pill__dot {
  width: 7px; height: 7px; background: #10B981; border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.2);
  animation: pulse 2s infinite;
}

.logos-headline {
  font-size: clamp(1.3rem, 2.5vw, 1.9rem); font-weight: 800;
  color: #09090B; margin-bottom: 10px; line-height: 1.25;
}
.logos-sub { font-size: 0.9rem; color: #71717A; }

/* Rail */
.logos-rail { overflow: hidden; position: relative; padding: 8px 0; }
.logos-fade {
  position: absolute; top: 0; bottom: 0; width: 120px; z-index: 2; pointer-events: none;
}
.logos-fade--l { left: 0; background: linear-gradient(to right, white 0%, transparent 100%); }
.logos-fade--r { right: 0; background: linear-gradient(to left, white 0%, transparent 100%); }

.logos-track {
  display: flex; gap: 20px; width: max-content; padding: 4px 0;
}
.logos-track--fwd { animation: logoFwd 50s linear infinite; }
@keyframes logoFwd { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@keyframes logoRev { from { transform: translateX(-50%); } to { transform: translateX(0); } }

/* Logo cards */
.logo-card {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 12px; min-width: 160px;
  border: 1.5px solid rgba(0,0,0,0.06); border-radius: 20px;
  padding: 24px 28px; flex-shrink: 0;
  transition: box-shadow 0.25s, transform 0.25s, border-color 0.25s;
  cursor: default;
}
.logo-card:hover {
  box-shadow: 0 12px 32px rgba(0,0,0,0.1);
  transform: translateY(-4px);
  border-color: rgba(0,0,0,0.1);
}
.logo-si-img {
  width: 64px; height: 64px;
  object-fit: contain;
  display: block;
  transition: transform 0.25s;
}
.logo-card:hover .logo-si-img {
  transform: scale(1.1);
}
.logo-brand-name {
  font-size: 0.8rem; font-weight: 800;
  text-align: center; white-space: nowrap;
  line-height: 1; letter-spacing: 0.01em;
}

/* Footer trust notes */
.logos-footer-note { margin-top: 48px; }
.logos-footer-note__inner {
  display: flex; align-items: center; justify-content: center;
  gap: 32px; flex-wrap: wrap;
  padding: 20px 28px;
  background: #FAFAFA; border: 1px solid #F0F0F0; border-radius: 16px;
}
.trust-note {
  display: flex; align-items: center; gap: 7px;
  font-size: 0.8rem; font-weight: 600; color: #52525B;
  white-space: nowrap;
}

/* ━━━ STATS ━━━ */
.stats-section { padding: 96px 0; background: white; }
.stats-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;
}
.stat-card {
  background: #FAFAFA; border-radius: 20px; padding: 28px 24px;
  border: 1px solid #E4E4E7; text-align: center;
  transition: box-shadow 0.2s, transform 0.2s;
}
.stat-card:hover { box-shadow: 0 8px 32px rgba(0,0,0,0.08); transform: translateY(-3px); }
.stat-card__icon {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.stat-card__val {
  display: block; font-size: 2.2rem; font-weight: 900; color: #09090B;
  margin-bottom: 6px; font-variant-numeric: tabular-nums;
}
.stat-card__label { font-size: 0.82rem; color: #71717A; font-weight: 500; }

/* ━━━ FEATURES ━━━ */
.features-section { padding: 96px 0; background: #FAFAFA; }
.feat-tabs {
  display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 48px;
  background: white; border-radius: 16px; padding: 6px;
  border: 1px solid #E4E4E7; display: inline-flex;
}
.feat-tab {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 18px; font-size: 0.875rem; font-weight: 600; color: #71717A;
  background: none; border: none; border-radius: 11px; cursor: pointer;
  transition: all 0.2s;
}
.feat-tab:hover { color: #18181B; background: #F4F4F5; }
.feat-tab.active { color: #18181B; background: #F4F4F5; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.feat-tab__icon {
  width: 26px; height: 26px; border-radius: 8px; background: #F4F4F5;
  display: flex; align-items: center; justify-content: center; transition: background 0.2s;
}

.feat-content {
  display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
}
.feat-text h3 { font-size: 1.7rem; font-weight: 800; color: #09090B; margin-bottom: 24px; line-height: 1.3; }
.feat-list { list-style: none; display: flex; flex-direction: column; gap: 13px; margin-bottom: 28px; }
.feat-list li { display: flex; align-items: flex-start; gap: 11px; font-size: 0.95rem; color: #52525B; line-height: 1.5; }
.feat-list--light li { color: #A1A1AA; }
.feat-check {
  width: 20px; height: 20px; background: #4F46E5; border-radius: 6px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px;
}
.feat-check--light { background: rgba(255,255,255,0.15); }
.feat-metrics {
  display: flex; gap: 24px; margin-bottom: 28px; padding: 20px;
  background: #F4F4F5; border-radius: 14px; border: 1px solid #E4E4E7;
}
.feat-metric__val { display: block; font-size: 1.6rem; font-weight: 900; color: #4F46E5; }
.feat-metric__label { font-size: 0.75rem; color: #71717A; font-weight: 500; }

.feat-visual { position: relative; border-radius: 20px; overflow: hidden; }
.feat-photo {
  width: 100%; height: 380px; object-fit: cover; display: block;
  transition: transform 0.5s; border-radius: 20px;
}
.feat-visual:hover .feat-photo { transform: scale(1.03); }
.feat-visual__overlay {
  position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.4) 0%, transparent 50%);
  border-radius: 20px; display: flex; align-items: flex-end; padding: 20px;
}
.feat-badge {
  display: flex; align-items: center; gap: 7px;
  background: rgba(79,70,229,0.9); backdrop-filter: blur(8px);
  color: white; font-size: 0.8rem; font-weight: 700;
  padding: 7px 14px; border-radius: 999px;
}

/* ━━━ SECTORS ━━━ */
.sectors-section { padding: 96px 0; background: white; }
.sectors-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 48px;
}
.sector-card {
  background: #FAFAFA; border-radius: 18px; padding: 24px;
  border: 1px solid #E4E4E7; cursor: pointer;
  transition: box-shadow 0.25s, transform 0.25s, border-color 0.25s;
}
.sector-card:hover {
  box-shadow: 0 12px 36px rgba(79,70,229,0.12); transform: translateY(-4px); border-color: #C7D2FE;
}
.sector-card__top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
.sector-icon {
  width: 46px; height: 46px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
}
.sector-arrow { opacity: 0; transition: opacity 0.2s; }
.sector-arrow.visible { opacity: 1; }
.sector-card__title { font-size: 0.92rem; font-weight: 800; color: #18181B; margin-bottom: 8px; }
.sector-card__desc { font-size: 0.8rem; color: #71717A; line-height: 1.55; margin-bottom: 12px; }
.sector-card__tag {
  font-size: 0.72rem; font-weight: 700; color: #71717A;
  background: #F4F4F5; padding: 3px 10px; border-radius: 999px; display: inline-block;
}

/* ━━━ AI ━━━ */
.ai-section {
  padding: 0;
  background: linear-gradient(135deg, #09090B 0%, #1E1B4B 60%, #0C0A1E 100%);
  position: relative; overflow: hidden;
}
.ai-section__inner { padding: 96px 0; }
.ai-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 72px; align-items: center; }

.ai-chat {
  background: #131316; border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.08); overflow: hidden;
  box-shadow: 0 24px 80px rgba(0,0,0,0.5);
}
.ai-chat__header {
  display: flex; align-items: center; gap: 12px; padding: 16px 20px;
  background: #1C1C1F; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.ai-avatar {
  width: 38px; height: 38px; background: #4F46E5; border-radius: 11px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.ai-chat__name { font-size: 0.9rem; font-weight: 700; color: white; }
.ai-chat__status { font-size: 0.72rem; color: #71717A; display: flex; align-items: center; gap: 5px; }
.status-dot { width: 6px; height: 6px; background: #10B981; border-radius: 50%; animation: pulse 2s infinite; }
.ai-chat__badge {
  margin-left: auto; font-size: 0.7rem; font-weight: 800; color: #A5B4FC;
  background: rgba(79,70,229,0.25); padding: 3px 9px; border-radius: 6px; letter-spacing: 0.05em;
}

.ai-chat__body { padding: 20px; display: flex; flex-direction: column; gap: 12px; }
.chat-msg { display: flex; flex-direction: column; gap: 3px; }
.chat-msg--bot { align-items: flex-start; }
.chat-msg--user { align-items: flex-end; }
.chat-msg__bubble {
  padding: 10px 14px; border-radius: 14px; font-size: 0.83rem; line-height: 1.55;
  max-width: 88%;
}
.chat-msg--bot .chat-msg__bubble { background: #1C1C1F; color: #D4D4D8; border-bottom-left-radius: 4px; }
.chat-msg--user .chat-msg__bubble { background: #4F46E5; color: white; border-bottom-right-radius: 4px; }
.chat-msg__time { font-size: 0.65rem; color: #52525B; }

.chat-suggestions { display: flex; flex-direction: column; gap: 8px; }
.chat-suggestion {
  display: flex; align-items: center; gap: 10px;
  background: #1C1C1F; border-radius: 12px; padding: 10px 12px;
  border: 1px solid rgba(255,255,255,0.06);
}
.chat-sugg__avatar {
  width: 30px; height: 30px; border-radius: 8px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.65rem; font-weight: 800; color: white;
}
.chat-sugg__name { font-size: 0.8rem; font-weight: 700; color: #E4E4E7; }
.chat-sugg__hours { font-size: 0.68rem; color: #71717A; }
.chat-sugg__btn {
  margin-left: auto; font-size: 0.72rem; font-weight: 700; color: #818CF8;
  background: rgba(79,70,229,0.15); border: none; border-radius: 7px;
  padding: 5px 12px; cursor: pointer; transition: background 0.2s;
  white-space: nowrap;
}
.chat-sugg__btn:hover { background: rgba(79,70,229,0.3); }
.chat-typing { display: flex; gap: 4px; padding: 10px 14px; background: #1C1C1F; border-radius: 14px; border-bottom-left-radius: 4px; width: fit-content; }
.chat-typing span { width: 6px; height: 6px; background: #52525B; border-radius: 50%; animation: typing 1.2s infinite; }
.chat-typing span:nth-child(2) { animation-delay: 0.2s; }
.chat-typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing { 0%, 60%, 100% { transform: translateY(0); opacity: 0.4; } 30% { transform: translateY(-5px); opacity: 1; } }

.ai-stat {
  position: absolute; background: rgba(255,255,255,0.05); backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;
  display: flex; align-items: center; gap: 8px;
  padding: 10px 16px; font-size: 0.8rem; color: #D4D4D8; font-weight: 600;
  white-space: nowrap;
}
.ai-stat--1 { top: 32px; right: 24px; }
.ai-stat--2 { bottom: 32px; left: 24px; }

/* ━━━ TESTIMONIALS ━━━ */
.testi-section { padding: 96px 0; background: #FAFAFA; }
.testi-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; flex-wrap: wrap; gap: 16px; }
.testi-header .section-title { margin-bottom: 0; }
.testi-nav { display: flex; gap: 8px; }
.testi-nav__btn {
  width: 40px; height: 40px; border-radius: 12px; background: white;
  border: 1px solid #E4E4E7; display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #52525B; transition: all 0.2s;
}
.testi-nav__btn:hover { border-color: #4F46E5; color: #4F46E5; background: #EEF2FF; }

.testi-track {
  display: flex; gap: 20px; overflow-x: auto; padding-bottom: 16px;
  scroll-snap-type: x mandatory; scrollbar-width: none;
}
.testi-track::-webkit-scrollbar { display: none; }
.testi-card {
  min-width: 340px; max-width: 340px; background: white;
  border-radius: 20px; padding: 28px; border: 1px solid #E4E4E7;
  scroll-snap-align: start; display: flex; flex-direction: column; gap: 16px;
  transition: box-shadow 0.2s, transform 0.2s;
}
.testi-card:hover { box-shadow: 0 12px 36px rgba(0,0,0,0.08); transform: translateY(-3px); }
.testi-card__top { display: flex; justify-content: space-between; align-items: flex-start; }
.testi-card__stars { display: flex; gap: 2px; }
.testi-card__text { font-size: 0.9rem; color: #3F3F46; line-height: 1.65; flex: 1; }
.testi-card__author { display: flex; align-items: center; gap: 12px; margin-top: auto; }
.testi-avatar { width: 44px; height: 44px; border-radius: 12px; object-fit: cover; flex-shrink: 0; }
.testi-name { font-size: 0.875rem; font-weight: 700; color: #09090B; }
.testi-role { font-size: 0.75rem; color: #A1A1AA; }
.testi-tag {
  margin-left: auto; font-size: 0.7rem; font-weight: 700; color: #4F46E5;
  background: #EEF2FF; padding: 3px 10px; border-radius: 999px; white-space: nowrap;
}

/* ━━━ CTA ━━━ */
.cta-section {
  background: linear-gradient(135deg, #1E1B4B 0%, #4F46E5 50%, #7C3AED 100%);
  position: relative; overflow: hidden;
}
.cta-section__inner { padding: 96px 0; position: relative; }
.cta-glow {
  position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none;
}
.cta-glow--1 { width: 400px; height: 400px; background: rgba(168,85,247,0.25); top: -100px; right: -100px; }
.cta-glow--2 { width: 300px; height: 300px; background: rgba(79,70,229,0.2); bottom: -50px; left: 50px; }
.cta-content { text-align: center; position: relative; z-index: 1; }
.cta-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.15); backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.2); color: white;
  font-size: 0.82rem; font-weight: 700; padding: 7px 18px; border-radius: 999px;
  margin-bottom: 28px;
}
.cta-title {
  font-size: clamp(1.8rem, 3.5vw, 2.75rem); font-weight: 900; color: white;
  line-height: 1.2; margin-bottom: 16px;
}
.cta-sub { font-size: 1rem; color: rgba(255,255,255,0.7); margin-bottom: 36px; }
.cta-actions { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 40px; }
.cta-section .btn-primary { background: white; color: #4F46E5 !important; box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
.cta-section .btn-primary:hover { background: #F5F3FF; }

.cta-logos { display: flex; justify-content: center; align-items: center; gap: 12px; flex-wrap: wrap; }
.cta-logo-item {
  font-size: 0.8rem; font-weight: 700; color: rgba(255,255,255,0.6);
  background: rgba(255,255,255,0.08); padding: 6px 14px; border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.12);
}

/* ━━━ FAQ ━━━ */
.faq-section { padding: 96px 0; background: white; }
.faq-inner { display: grid; grid-template-columns: 1fr 1.6fr; gap: 64px; align-items: start; }
.faq-contact { color: #4F46E5; font-weight: 600; text-decoration: none; }
.faq-contact:hover { text-decoration: underline; }
.faq-list { display: flex; flex-direction: column; }
.faq-item {
  border-bottom: 1px solid #E4E4E7; cursor: pointer;
  transition: background 0.15s;
}
.faq-item:first-child { border-top: 1px solid #E4E4E7; }
.faq-item__q {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 4px; font-size: 0.95rem; font-weight: 600; color: #18181B;
  gap: 16px; user-select: none;
}
.faq-item--open .faq-item__q { color: #4F46E5; }
.faq-item__icon { transition: transform 0.3s; flex-shrink: 0; }
.faq-item__icon.rotated { transform: rotate(180deg); }
.faq-item__a { padding: 0 4px 20px; font-size: 0.88rem; color: #71717A; line-height: 1.75; }

/* Transitions */
.faq-expand-enter-active, .faq-expand-leave-active { transition: all 0.3s ease; overflow: hidden; }
.faq-expand-enter-from, .faq-expand-leave-to { opacity: 0; max-height: 0; padding-bottom: 0 !important; }
.faq-expand-enter-to, .faq-expand-leave-from { opacity: 1; max-height: 200px; }

.feature-slide-enter-active, .feature-slide-leave-active { transition: all 0.4s ease; position: absolute; }
.feature-slide-enter-from { opacity: 0; transform: translateY(10px); }
.feature-slide-leave-to { opacity: 0; transform: translateY(-10px); }

.mobile-enter-active, .mobile-leave-active { transition: all 0.25s ease; overflow: hidden; }
.mobile-enter-from, .mobile-leave-to { opacity: 0; max-height: 0; }
.mobile-enter-to, .mobile-leave-from { opacity: 1; max-height: 400px; }

/* ━━━ FOOTER ━━━ */
.site-footer { background: #09090B; padding: 64px 0 32px; }
.footer-top {
  display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; margin-bottom: 48px;
}
.footer-logo { color: white !important; }
.footer-brand p { font-size: 0.875rem; color: #71717A; line-height: 1.6; margin: 12px 0 20px; }
.footer-social { display: flex; gap: 10px; }
.footer-social a {
  width: 36px; height: 36px; background: rgba(255,255,255,0.05); border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  color: #71717A; text-decoration: none; border: 1px solid rgba(255,255,255,0.08);
  transition: all 0.2s;
}
.footer-social a:hover { background: #4F46E5; color: white; border-color: #4F46E5; }
.footer-col h5 { font-size: 0.82rem; font-weight: 700; color: #E4E4E7; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.06em; }
.footer-col ul { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.footer-col a { font-size: 0.82rem; color: #71717A; text-decoration: none; transition: color 0.2s; }
.footer-col a:hover { color: #E4E4E7; }
.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.06); padding-top: 24px;
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;
  gap: 12px; font-size: 0.78rem; color: #52525B;
}
.footer-legal { display: flex; gap: 20px; }
.footer-legal a { color: #52525B; text-decoration: none; transition: color 0.2s; }
.footer-legal a:hover { color: #71717A; }

/* ━━━ RESPONSIVE ━━━ */
@media (max-width: 1024px) {
  .sectors-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-top { grid-template-columns: 1fr 1fr; }
  .ai-grid { grid-template-columns: 1fr; }
  .ai-stat--1, .ai-stat--2 { display: none; }
}

@media (max-width: 768px) {
  .hero__container { grid-template-columns: 1fr; gap: 40px; padding: 60px 24px 40px; }
  .hero__visual { display: none; }
  .feat-content { grid-template-columns: 1fr; }
  .feat-photo { height: 240px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .sectors-grid { grid-template-columns: repeat(2, 1fr); }
  .faq-inner { grid-template-columns: 1fr; gap: 32px; }
  .nav__links, .nav__cta { display: none; }
  .nav__burger { display: flex; }
  .footer-top { grid-template-columns: 1fr; gap: 32px; }
  .testi-card { min-width: 280px; }
  .feat-tabs { flex-direction: column; width: 100%; }
  .feat-tab { justify-content: center; }
}

@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr 1fr; }
  .sectors-grid { grid-template-columns: 1fr; }
  .hero__actions { flex-direction: column; align-items: flex-start; }
  .cta-actions { flex-direction: column; align-items: center; }
}
</style>
