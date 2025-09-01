<template>
  <div id="app">
    <!-- Header Section -->
    <header class="header">
      <div class="header-content">
        <div class="logo-section">
          <div class="brain-icon">🧠</div>
          <h1 class="app-title">Agent IA BCT</h1>
          <span class="subtitle">Assistant Intelligent de la Banque Centrale de Tunisie</span>
        </div>
        
        <div class="auth-section">
          <div v-if="!user" class="login-container">
            <button @click="loginWithGoogle" class="login-btn">
              <svg class="google-icon" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Se connecter avec Google
            </button>
          </div>
          
          <div v-else class="user-menu">
            <div class="user-info">
              <div class="user-avatar">{{ user.name.charAt(0) }}</div>
              <span class="user-name">{{ user.name }}</span>
            </div>
            <button @click="logout" class="logout-btn">
              <svg class="logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="container">
        <!-- Question Input Section -->
        <div class="input-section">
          <div class="input-container">
            <div class="input-header">
              <h2>Posez votre question</h2>
              <p>Explorez les documents de la BCT avec l'aide de l'intelligence artificielle</p>
            </div>
            
            <div class="input-wrapper">
              <textarea
                v-model="question"
                placeholder="Décrivez votre question en détail..."
                rows="4"
                class="question-input"
                @keydown.enter.ctrl.prevent="askQuestion"
                :disabled="loading"
              ></textarea>
              
              <div class="input-actions">
                <div class="input-hint">
                  <svg class="hint-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                  <span>Ctrl + Entrée pour envoyer</span>
                </div>
                
                <button 
                  @click="askQuestion" 
                  :disabled="loading || !question.trim()"
                  class="send-btn"
                >
                  <svg v-if="loading" class="loading-icon" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <svg v-else class="send-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                  </svg>
                  {{ loading ? 'Analyse...' : 'Envoyer' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="error-container">
          <div class="error-content">
            <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div>
              <h3>Une erreur s'est produite</h3>
              <p>{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- History Section -->
        <div v-if="history.length" class="history-section">
          <div class="history-header">
            <h2>
              <svg class="history-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Historique des conversations
            </h2>
            <span class="history-count">{{ history.length }} question{{ history.length > 1 ? 's' : '' }}</span>
          </div>

          <div class="conversation-list">
            <div
              v-for="(item, index) in history"
              :key="index"
              class="conversation-item"
            >
              <div class="conversation-content">
                <div class="question-block">
                  <div class="question-icon">❓</div>
                  <div class="question-text">{{ item.question }}</div>
                </div>

                <div class="answer-block">
                  <div class="answer-icon">🤖</div>
                  <div class="answer-content">
                    <div v-if="item.answer.text" class="answer-text">
                      {{ item.answer.text }}
                    </div>

                    <ul v-if="item.answer.bullets.length" class="answer-bullets">
                      <li v-for="(bullet, i) in item.answer.bullets" :key="i">
                        {{ bullet }}
                      </li>
                    </ul>

                    <div v-if="item.answer.sources.length" class="sources-section">
                      <h4 class="sources-title">
                        <svg class="sources-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                        </svg>
                        Sources référencées
                      </h4>
                      <div class="sources-list">
                        <a
                          v-for="(source, i) in item.answer.sources"
                          :key="i"
                          :href="getDocLink(source.doc, source.page)"
                          target="_blank"
                          rel="noopener noreferrer"
                          class="source-link"
                        >
                          <div class="source-info">
                            <strong class="source-doc">{{ source.doc }}</strong>
                            <span class="source-page">Page {{ source.page }}</span>
                          </div>
                          <svg class="external-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                          </svg>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <button class="delete-btn" @click="deleteHistory(index)" title="Supprimer cette conversation">
                <svg class="delete-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!history.length && !loading" class="empty-state">
          <div class="empty-icon">💡</div>
          <h3>Commencez votre recherche</h3>
          <p>Posez une question sur les documents de la Banque Centrale de Tunisie pour obtenir des réponses précises et documentées.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      question: "",
      loading: false,
      error: "",
      history: [],
    };
  },

  mounted() {
    this.getAuthenticatedUser();
  },

  methods: {
    async getAuthenticatedUser() {
      try {
        const res = await fetch("http://localhost:8000/api/user", {
          credentials: "include",
        });
        if (res.ok) {
          const data = await res.json();
          this.user = data;
        }
      } catch (err) {
        console.error("Error fetching user:", err);
      }
    },

    async loginWithGoogle() {
      window.location.href = "http://localhost:8000/login";
    },

    async logout() {
      try {
        const res = await fetch("http://localhost:8000/logout", {
          method: "GET",
          credentials: "include"
        });
        const data = await res.json();
        window.location.href = data.redirect_url;
      } catch (err) {
        console.error("Logout failed:", err);
      }
    },

    async askQuestion() {
      if (!this.question.trim()) return;

      const asked = this.question.trim();
      this.loading = true;
      this.error = "";

      try {
        const res = await fetch("/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: asked }),
        });

        if (!res.ok) {
          const text = await res.text().catch(() => "");
          throw new Error(`Erreur requête (${res.status}) ${text}`);
        }

        const data = await res.json();
        const cleaned = (data.answer || "")
          .replace(/\*\*(.*?)\*\*/g, "$1")
          .replace(/\b(Réponse\s*:?|Conclusion\s*:?)\b/gi, "")
          .replace(/\r/g, "")
          .replace(/[ \t]+/g, " ")
          .replace(/\n{2,}/g, "\n")
          .trim();

        const formatted = this.formatForDisplay(cleaned);
        if (Array.isArray(data.sources) && data.sources.length) {
          formatted.sources = data.sources;
        }

        this.history.unshift({ question: asked, answer: formatted });
        this.question = "";

      } catch (err) {
        this.error = err?.message || "Erreur inconnue";
      } finally {
        this.loading = false;
      }
    },

    deleteHistory(index) {
      this.history.splice(index, 1);
    },

    formatForDisplay(str) {
      const sourceRegex = /\[Document\s*:\s*([^|\]]+)\|\s*Page\s*:\s*([^\]]+)\]/g;
      const sourcesMap = new Map();
      let m;
      while ((m = sourceRegex.exec(str)) !== null) {
        const doc = m[1].trim();
        const page = m[2].trim();
        const key = `${doc}__${page}`;
        if (!sourcesMap.has(key)) sourcesMap.set(key, { doc, page });
      }
      const extractedSources = Array.from(sourcesMap.values());

      let body = str.replace(sourceRegex, "").replace(/\s{2,}/g, " ").trim();

      const lines = body.split(/\n/);
      const bullets = [];
      const kept = [];
      for (const line of lines) {
        const hit = line.match(/^\s*\*\s+(.*)$/);
        if (hit) bullets.push(hit[1].trim());
        else kept.push(line.trim());
      }

      const text = kept.filter(Boolean).join(" ").replace(/\s{2,}/g, " ").trim();

      return { text, bullets, sources: extractedSources };
    },

    getDocLink(doc, page) {
      return `https://www.bct.gov.tn/bct/siteprod/documents/${encodeURIComponent(doc)}#page=${encodeURIComponent(page)}`;
    }
  },
};
</script>

<style>
* {
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  color: #1a1a1a;
}

/* Header */
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brain-icon {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.app-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.subtitle {
  font-size: 0.85rem;
  color: #6b7280;
  margin-left: 0.5rem;
  font-weight: 400;
}

/* Authentication */
.login-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: white;
  color: #374151;
  border: 2px solid #e5e7eb;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.login-btn:hover {
  border-color: #667eea;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
  transform: translateY(-1px);
}

.google-icon {
  width: 20px;
  height: 20px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
}

.user-name {
  font-weight: 600;
  color: #374151;
}

.logout-btn {
  padding: 0.5rem;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #fecaca;
  transform: scale(1.05);
}

.logout-icon {
  width: 20px;
  height: 20px;
}

/* Main Content */
.main-content {
  min-height: calc(100vh - 120px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* Input Section */
.input-section {
  margin-bottom: 3rem;
}

.input-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.input-header {
  text-align: center;
  margin-bottom: 2rem;
}

.input-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.input-header p {
  color: #6b7280;
  font-size: 1rem;
  margin: 0;
}

.input-wrapper {
  position: relative;
}

.question-input {
  width: 100%;
  min-height: 120px;
  padding: 1.5rem;
  font-size: 1rem;
  line-height: 1.6;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  resize: vertical;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  background: #fafafa;
}

.question-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  background: white;
}

.question-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.hint-icon {
  width: 16px;
  height: 16px;
}

.send-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.send-icon, .loading-icon {
  width: 20px;
  height: 20px;
}

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Error */
.error-container {
  margin: 2rem 0;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 16px;
  color: #dc2626;
}

.error-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.error-content h3 {
  margin: 0 0 0.25rem;
  font-weight: 600;
}

.error-content p {
  margin: 0;
  font-size: 0.95rem;
}

/* History Section */
.history-section {
  margin-top: 3rem;
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.history-header h2 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

.history-icon {
  width: 24px;
  height: 24px;
}

.history-count {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 500;
}

.conversation-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.conversation-item {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.conversation-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.question-block, .answer-block {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.question-block:last-child, .answer-block:last-child {
  margin-bottom: 0;
}

.question-icon, .answer-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.question-text {
  font-weight: 600;
  font-size: 1.1rem;
  color: white;
  line-height: 1.5;
}

.answer-content {
  flex: 1;
}

.answer-text {
  color: white;
  line-height: 1.7;
  margin-bottom: 1rem;
  font-size: 1rem;
}

.answer-bullets {
  margin: 1rem 0;
  padding-left: 1rem;
}

.answer-bullets li {
  margin: 0.5rem 0;
  color: white;
  line-height: 1.6;
}

.sources-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.sources-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #a6b0c1;
  margin: 0 0 1rem;
}

.sources-icon {
  width: 18px;
  height: 18px;
}

.sources-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.source-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  color: #475569;
  transition: all 0.2s ease;
}

.source-link:hover {
  background: #e2e8f0;
  border-color: #667eea;
  transform: translateX(4px);
}

.source-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.source-doc {
  color: #a6b0c1;
  font-weight: 600;
}

.source-page {
  font-size: 0.875rem;
  color: #64748b;
}

.external-icon {
  width: 16px;
  height: 16px;
  opacity: 0.6;
}

.delete-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0.7;
}

.delete-btn:hover {
  background: #fecaca;
  opacity: 1;
  transform: scale(1.1);
}

.delete-icon {
  width: 18px;
  height: 18px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: white;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1rem;
  opacity: 0.9;
}

.empty-state p {
  font-size: 1rem;
  opacity: 0.7;
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }

  .header-content {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
  }

  .logo-section {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .subtitle {
    margin-left: 0;
    font-size: 0.8rem;
  }

  .input-container {
    padding: 1.5rem;
    border-radius: 16px;
  }

  .input-header h2 {
    font-size: 1.5rem;
  }

  .input-actions {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .send-btn {
    width: 100%;
    justify-content: center;
  }

  .conversation-item {
    padding: 1.5rem;
    border-radius: 16px;
  }

  .question-block, .answer-block {
    flex-direction: column;
    gap: 0.75rem;
  }

  .question-icon, .answer-icon {
    align-self: flex-start;
  }

  .sources-list {
    gap: 0.5rem;
  }

  .source-link {
    padding: 0.75rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .delete-btn {
    position: static;
    align-self: flex-end;
    margin-top: 1rem;
  }

  .history-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .history-header h2 {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .brain-icon {
    font-size: 2rem;
  }

  .app-title {
    font-size: 1.25rem;
  }

  .subtitle {
    font-size: 0.75rem;
  }

  .input-container {
    padding: 1rem;
  }

  .input-header h2 {
    font-size: 1.25rem;
  }

  .question-input {
    min-height: 100px;
    padding: 1rem;
  }

  .conversation-item {
    padding: 1rem;
  }

  .empty-state {
    padding: 3rem 1rem;
  }

  .empty-icon {
    font-size: 3rem;
  }
}

/* Animation Improvements */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.conversation-item {
  animation: fadeIn 0.5s ease-out;
}

.question-block {
  animation: slideIn 0.3s ease-out;
}

.answer-block {
  animation: slideIn 0.3s ease-out 0.1s both;
}

/* Focus States for Accessibility */
.send-btn:focus,
.login-btn:focus,
.logout-btn:focus,
.delete-btn:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

.question-input:focus {
  outline: none;
}

/* Loading States */
.send-btn:disabled .loading-icon {
  animation: spin 1s linear infinite;
}

/* Smooth Scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Print Styles */
@media print {
  .header,
  .input-section,
  .delete-btn {
    display: none;
  }

  .conversation-item {
    background: white;
    box-shadow: none;
    border: 1px solid #e5e7eb;
    margin-bottom: 2rem;
    page-break-inside: avoid;
  }

  .source-link {
    color: #1e293b;
    text-decoration: underline;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .input-container,
  .conversation-item {
    background: white;
    border: 2px solid #000;
  }

  .question-input {
    border: 2px solid #000;
  }

  .send-btn {
    background: #000;
    color: white;
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .input-container,
  .conversation-item {
    background: rgba(31, 41, 55, 0.95);
    color: #f9fafb;
  }

  .question-input {
    background: #374151;
    color: #f9fafb;
    border-color: #4b5563;
  }

  .question-input:focus {
    background: #4b5563;
  }

  .source-link {
    background: #374151;
    border-color: #4b5563;
    color: #d1d5db;
  }

  .source-link:hover {
    background: #4b5563;
  }

  .error-content {
    background: rgba(220, 38, 38, 0.1);
    border-color: rgba(220, 38, 38, 0.3);
    color: #fca5a5;
  }
}
</style>