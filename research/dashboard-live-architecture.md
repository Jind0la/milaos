# MilaOS Live-Dashboard Architektur

## Zusammenfassung der Recherche

### Verfügbare OpenClaw Datenquellen

| Datenquelle | Quelle | Update-Frequenz |
|-------------|--------|------------------|
| Agent Status | `memory/heartbeat-state.json` | Alle 30 Min (Cron) |
| Token Usage | WebSocket API `usage.status` | Echtzeit |
| Sessions | WebSocket API `sessions.list` | Echtzeit |
| Chat History | WebSocket API `chat.history` | Echtzeit |
| Nodes | WebSocket API `node.list` | Echtzeit |
| System Events | WebSocket API `system-event` | Echtzeit |
| Dokumente | `research/*.md` Ordner | Bei Änderung |
| Cron Runs | `cron/runs/*.jsonl` | Nach Ausführung |

### OpenClaw Gateway

- **Port:** 18789
- **Protokoll:** WebSocket (primär), HTTP (Control UI)
- **Verfügbare API-Endpunkte** (aus gateway.log):
  - `sessions.list` - Listet alle Sessions
  - `sessions.preview` - Session Vorschau
  - `usage.status` - Token Usage / Kosten
  - `chat.history` - Chat Verlauf
  - `node.list` - Verbundene Nodes
  - `system-event` - System Events
  - `health` - Health Check

---

## Empfohlene Lösung: JavaScript Polling mit WebSocket

### Warum diese Lösung?

| Kriterium | Bewertung |
|-----------|-----------|
| **Einfachheit** | ⭐⭐⭐⭐⭐ - Direkt im Browser, keine Server-Side |
| **Zuverlässigkeit** | ⭐⭐⭐⭐⭐ - WebSocket ist stabil, Automatic Reconnect |
| **Live-Faktor** | ⭐⭐⭐⭐⭐ - Echtzeit Updates via WebSocket |
| **OpenClaw Integration** | ⭐⭐⭐⭐⭐ - Direkte Nutzung der API |

### Alternative: JavaScript Polling (Fallback)

Falls WebSocket Probleme macht:
- Alle 30-60 Sekunden `fetch()` auf eine JSON-Datei
- Die JSON-Datei wird von einem separaten Script aktualisiert

---

## Implementierung

### 1. Neue Dateien erstellen

```
workspace/
├── dashboard-api.js        # WebSocket Client für OpenClaw API
├── dashboard-data.json     # Gecachte Daten (für Polling Fallback)
└── index.html             # (existiert already - anpassen)
```

### 2. dashboard-api.js (WebSocket Client)

```javascript
// WebSocket Verbindung zum OpenClaw Gateway
class OpenClawAPI {
  constructor() {
    this.ws = null;
    this.reconnectDelay = 5000;
    this.listeners = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket('ws://localhost:18789');
      
      this.ws.onopen = () => {
        console.log('Connected to OpenClaw Gateway');
        resolve();
      };
      
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      };
      
      this.ws.onclose = () => {
        console.log('Disconnected, reconnecting...');
        setTimeout(() => this.connect(), this.reconnectDelay);
      };
    });
  }

  async call(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = crypto.randomUUID();
      const listener = (data) => {
        if (data.id === id) {
          resolve(data.result || data);
          this.listeners.delete(id);
        }
      };
      this.listeners.set(id, listener);
      
      this.ws.send(JSON.stringify({
        method,
        params,
        id
      }));
    });
  }

  // Verfügbare Methoden
  async getSessions() {
    return this.call('sessions.list');
  }

  async getUsage() {
    return this.call('usage.status');
  }

  async getNodes() {
    return this.call('node.list');
  }

  async getChatHistory(limit = 50) {
    return this.call('chat.history', { limit });
  }
}
```

### 3. Dashboard Integration (in index.html)

```javascript
// Nach dem bestehenden Script-Bereich hinzufügen

// 1. Heartbeat-State laden (existierende Datei)
async function loadHeartbeatState() {
  try {
    const response = await fetch('memory/heartbeat-state.json');
    return await response.json();
  } catch (e) {
    console.warn('Heartbeat state not available:', e);
    return null;
  }
}

// 2. Dokumente scannen
async function loadDocuments() {
  // Die existierenden Dokumente aus dem JavaScript Array
  // Werden bereits im Dashboard geladen
  return documents; // Aus dem existierenden Script
}

// 3. WebSocket API (für Echtzeit)
async function loadLiveData() {
  try {
    const api = new OpenClawAPI();
    await api.connect();
    
    const [sessions, usage, nodes] = await Promise.all([
      api.getSessions(),
      api.getUsage(),
      api.getNodes()
    ]);
    
    return { sessions, usage, nodes };
  } catch (e) {
    console.warn('Live API not available:', e);
    return null;
  }
}

// Update-Funktion für das Dashboard
async function updateDashboard() {
  const [heartbeat, live, docs] = await Promise.all([
    loadHeartbeatState(),
    loadLiveData(),
    loadDocuments()
  ]);
  
  // Agent Status updaten
  if (heartbeat?.agents) {
    updateAgentStatus(heartbeat.agents);
  }
  
  // Usage Metriken updaten
  if (live?.usage) {
    updateUsageMetrics(live.usage);
  }
  
  // Sessions updaten
  if (live?.sessions) {
    updateSessions(live.sessions);
  }
  
  // Dokumente updaten
  if (docs) {
    updateDocumentsCount(docs.length);
  }
}

// Alle 30 Sekunden updaten
setInterval(updateDashboard, 30000);
// Initiales Laden
updateDashboard();
```

---

## Dashboard Anzeige-Elemente

### Was das Dashboard zeigen soll:

| Element | Datenquelle | Update |
|---------|-------------|--------|
| **Agent Status** | `heartbeat-state.json` + WebSocket | 30s |
| **Agent Activities** | WebSocket `sessions.list` | 30s |
| **Dokumente** | `research/*.md` Ordner | 60s |
| **Token Usage** | WebSocket `usage.status` | 30s |
| **Kosten** | WebSocket `usage.status` | 30s |
| **Kalender/Erinnerungen** | Zukünftig (CalDAV/API) | - |

---

## Setup Anleitung

### Schritt 1: WebSocket Client erstellen

```bash
# Datei erstellen
touch workspace/dashboard-api.js
```

### Schritt 2: index.html anpassen

Das existierende Dashboard hat bereits:
- KPI Cards (Agenten, Tasks, Success Rate, Kosten)
- Charts (Performance, Token Usage)
- Memory Section
- Documents Grid
- Activity Table

**Anpassungen nötig:**
1. Statische Werte durch dynamische ersetzen
2. WebSocket/Poll-Loop hinzufügen
3. Aktualisierungs-Interval setzen

### Schritt 3: Testen

```bash
# Gateway läuft?
curl http://localhost:18789/health

# WebSocket Test
wscat -c ws://localhost:18789
```

---

## Geschätzter Aufwand

| Task | Aufwand | Komplexität |
|------|---------|-------------|
| WebSocket Client erstellen | 1 Stunde | Niedrig |
| Dashboard anpassen | 2-3 Stunden | Mittel |
| Agent Status Integration | 1 Stunde | Niedrig |
| Usage/Metrics Integration | 1 Stunde | Niedrig |
| Dokumente automatisch scannen | 1 Stunde | Mittel |
| **Gesamt** | **6-8 Stunden** | - |

---

## Fallback: Polling Lösung

Falls WebSocket nicht funktioniert (z.B. Cross-Origin):

### Server-seitiges Script (Python/Node)

```python
# dashboard-data-collector.py
import websocket
import json
import time

def collect_dashboard_data():
    ws = websocket.create_connection("ws://localhost:18789")
    
    # Sessions abrufen
    ws.send(json.dumps({"method": "sessions.list", "id": "1"}))
    sessions = json.loads(ws.recv())
    
    # Usage abrufen
    ws.send(json.dumps({"method": "usage.status", "id": "2"}))
    usage = json.loads(ws.recv())
    
    ws.close()
    
    # Als JSON speichern
    with open('dashboard-data.json', 'w') as f:
        json.dump({
            "timestamp": time.time(),
            "sessions": sessions,
            "usage": usage
        }, f)

# Alle 30 Sekunden
while True:
    collect_dashboard_data()
    time.sleep(30)
```

---

## Zusammenfassung

**Empfohlene Architektur:**

1. **Primär:** WebSocket-Verbindung direkt im Browser
2. **Sekundär:** Heartbeat-State JSON (alle 30 Min aktualisiert)
3. **Fallback:** Polling alle 60s gegen dashboard-data.json

**Vorteile:**
- ✅ Echtzeit-Updates via WebSocket
- ✅ Keine zusätzliche Server-Infrastruktur
- ✅ Direkte OpenClaw-Integration
- ✅ Einfach zu implementieren
- ✅ Funktioniert im lokalen Netzwerk

**Nächste Schritte:**
1. `dashboard-api.js` erstellen
2. `index.html` anpassen (dynamische Daten)
3. Testen mit lokaler WebSocket-Verbindung

---

*Erstellt am: 2026-02-16*
*Research Agent: MilaOS*
