# Supabase Setup Guide – Fractal Memory MVP

> ⏱️ **Dauer:** ~15 Minuten  
> 🧰 **Voraussetzung:** Supabase Account (kostenlos reicht)

---

## 1. Supabase Projekt erstellen

1. Öffne **[supabase.com](https://supabase.com)** und logge dich ein
2. Klick auf **"New Project"**
3. Fülle die Felder:
   - **Organization:** Wähle deine Organization (oder erstelle eine neue)
   - **Name:** `fractal-memory-mvp`
   - **Database Password:** Sicheres Passwort festlegen
   - **Region:** `Frankfurt (eu-central-1)` (EU = Datenschutz)
4. Klick auf **"Create new project"**
5. Warte ~2 Minuten bis das Projekt bereit ist

---

## 2. pgvector Extension aktivieren

1. Im Supabase Dashboard: **SQL Editor** (links im Menü)
2. Führe diesen SQL-Befehl aus:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

3. Klick auf **"Run"** → sollte `Success` zeigen

---

## 3. Tabellen erstellen

Kopiere und fühme im SQL Editor aus:

### 3.1 Memories Tabelle

```sql
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(1536),  -- OpenAI ada-002 Dimension
    cluster_id UUID REFERENCES clusters(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Index für Vector-Suche erstellen (nach dem Einrichten)
-- CREATE INDEX ON memories USING ivfflat (embedding vector_cosine_ops);
```

### 3.2 Clusters Tabelle

```sql
CREATE TABLE clusters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    centroid VECTOR(1536),
    label TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.3 Sessions Tabelle

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT NOT NULL,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ
);
```

### 3.4 RLS Policies (Sicherheit)

```sql
-- Row Level Security aktivieren
ALTER TABLE memories ENABLE ROW LEVEL SECURITY;
ALTER TABLE clusters ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

-- Öffentlicher Lesezugriff (für MVP – später einschränken!)
CREATE POLICY "Public read memories" ON memories FOR SELECT USING (true);
CREATE POLICY "Public read clusters" ON clusters FOR SELECT USING (true);
CREATE POLICY "Public read sessions" ON sessions FOR SELECT USING (true);

-- Insert/Update nur für authentifizierte User (Supabase Auth)
CREATE POLICY "Auth insert memories" ON memories FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Auth update memories" ON memories FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Auth insert clusters" ON clusters FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Auth insert sessions" ON sessions FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

---

## 4. API Credentials finden

1. Im Dashboard: **Project Settings** (Zahnrad-Icon unten links)
2. Klick auf **API**
3. Du siehst:
   - **Project URL:** `https://[deine-projekt-id].supabase.co`
   - **anon public (anon key):** `eyJ...` (langer String)

→ Notiere dir beide Werte!

---

## 5. Environment Variables

Erstelle eine Datei `.env.example` im Projekt-Root:

```bash
# Supabase Config
SUPABASE_URL=https://deine-projekt-id.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> ⚠️ **Wichtig:** Die echte `.env` (ohne `.example`) NIEMALS committen!

---

## ✅ Checkliste

- [ ] Supabase Projekt erstellt
- [ ] pgvector Extension aktiviert
- [ ] 3 Tabellen erstellt (memories, clusters, sessions)
- [ ] RLS Policies gesetzt
- [ ] URL + anon key notiert
- [ ] `.env.example` erstellt

---

## Nächste Schritte

Sobald Supabase läuft, kann der Dev Agent:
1. Supabase Client in Python installieren (`pip install supabase`)
2. Embedding-Generierung integrieren
3. Vector-Suche für Memory-Retrieval implementieren

---

*Fractal Memory MVP – Supabase Setup*
