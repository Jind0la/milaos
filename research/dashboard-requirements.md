# Unternehmensdashboard – Anforderungen & Best Practices

**Research Report für MilaOS**  
*Erstellt: Februar 2026*

---

## Inhaltsverzeichnis

1. [Was gehört in ein Unternehmens-Dashboard?](#1-was-gehört-in-ein-unternehmens-dashboard)
2. [Zielgruppen & ihre Anforderungen](#2-zielgruppen--ihre-anforderungen)
3. [Dashboard-Tools & Plattformen](#3-dashboard-tools--plattformen)
4. [UX/UI Best Practices](#4-uxui-best-practices)
5. [MilaOS spezifische Anforderungen](#5-milaos-spezifische-anforderungen)
6. [Zusammenfassung & Empfehlungen](#6-zusammenfassung--empfehlungen)

---

## 1. Was gehört in ein Unternehmens-Dashboard?

### 1.1 Wichtige Metriken (KPIs)

Ein effektives Unternehmensdashboard sollte **5–15 Kern-KPIs** enthalten, um den Fokus zu wahren und Informationsüberflutung zu vermeiden.

| **Kategorie** | **Kern-Metriken** |
|---------------|-------------------|
| **Finanzen** | Umsatz, EBITDA, Cashflow, Budgetabweichung, Gewinnmarge, Kosten pro Einheit |
| **Vertrieb** | Umsatz nach Region/Produkt, Conversion-Rate, Pipeline-Wert, durchschnittlicher Deal-Wert, Verkaufszyklus-Dauer |
| **Marketing** | Lead-Generierung, CAC (Customer Acquisition Cost), ROI, Website-Traffic, Conversion-Rate, NPS |
| **Operations** | Produktionsauslastung, Lieferketten-Performance, Qualitätsmetriken (Fehlerquote), Durchlaufzeiten |
| **Personal** | Headcount, Fluktuationsrate, Produktivität, Krankenstand, Employee NPS |
| **Kunden** | Churn Rate, Customer Lifetime Value, NPS, Zufriedenheitsscore, Support-Tickets |

### 1.2 Abgedeckte Bereiche

Ein vollständiges Unternehmensdashboard sollte mehrere Dimensionen abdecken:

- **Übersicht (Executive Summary)**: Die wichtigsten 5–7 KPIs auf einen Blick
- **Trend-Analyse**: Zeitliche Entwicklung über Tage, Wochen, Monate
- **Vergleiche**: Ist-Zustand vs. Ziel, aktuell vs. Vorperiode, Benchmarking
- **Operative Details**: Drill-Down-Möglichkeiten für tiefergehende Analysen
- **Alarme/Warnungen**: Automatische Benachrichtigungen bei Schwellwertüberschreitungen

### 1.3 Essentielle Funktionen

| **Funktion** | **Beschreibung** |
|--------------|-------------------|
| **Echtzeit-Daten** | Automatische Aktualisierung ohne manuellen Refresh |
| **Drill-Down** | Von aggregierten Daten zu Details navigieren |
| **Filterung** | Nach Zeitraum, Region, Produkt, Team filtern |
| **Export** | PDF, Excel, CSV Export für Berichte |
| **Benachrichtigungen** | Automatische Alerts bei Threshold-Überschreitungen |
| **Rollenbasiert** | Verschiedene Ansichten für verschiedene Nutzer |
| **Mobile Optimierung** | Responsive Design für Smartphones/Tablets |

---

## 2. Zielgruppen & ihre Anforderungen

### 2.1 Executive Dashboard (CEO/CFO/CSO)

**Zielgruppe**: C-Suite, Vorstand, Geschäftsführung

| **Aspekt** | **Anforderung** |
|------------|-----------------|
| **Umfang** | 5–10 kritische KPIs |
| **Detailtiefe** | Hoch aggregiert, mit Drill-Down-Möglichkeit |
| **Fokus** | Strategische Ziele, finanzielle Gesundheit, Marktposition |
| **Aktualisierung** | Täglich oder in Echtzeit |
| **Vergleiche** | vs. Budget, vs. Vorjahr, vs. Wettbewerb |

**Empfohlene Metriken für CEOs:**

- Umsatzentwicklung & Wachstumsrate
- EBITDA & Profitabilität
- Customer Acquisition Cost (CAC) vs. Lifetime Value (LTV)
- Mitarbeiterengagement & Produktivität
- Marktaussichten & Wettbewerbsposition

**Empfohlene Metriken für CFOs:**

- Cashflow & Liquidität
- Budget vs. Ist-Vergleich
- EBITDA & Nettogewinn
- Forderungen & Verbindlichkeiten
- Kostenstruktur & Kosteneffizienz

### 2.2 Team Dashboard

**Zielgruppe**: Abteilungsleiter, Team-Lead, Projektmanager

| **Aspekt** | **Anforderung** |
|------------|-----------------|
| **Umfang** | 10–20 KPIs |
| **Detailtiefe** | Operativ, aufgabenbezogen |
| **Fokus** | Team-Ziele, Projekfortschritt, Ressourcen |
| **Aktualisierung** | Täglich oder stündlich |
| **Vergleiche** | vs. Team-Ziel, Trend über Zeit |

**Empfohlene Metriken für Teams:**

| **Team** | **Kern-KPIs** |
|----------|---------------|
| **Vertrieb** | Pipeline-Wert, abgeschlossene Deals, Conversion-Rate, durchschnittlicher Deal-Wert |
| **Marketing** | Leads generiert, CAC, ROI, Website-Traffic, Engagement-Rate |
| **Entwicklung** | Story Points delivered, Bug-Rate, Deployments, Build-Success-Rate |
| **Support** | Ticket-Volumen, durchschnittliche Lösungszeit, First-Contact-Resolution, CSAT |
| **HR** | Bewerbungen, Einstellungsrate, Fluktuationsrate, Zufriedenheit |

### 2.3 Externe Stakeholder

**Zielgruppe**: Investoren, Partner, Aufsichtsrat, Kunden (Self-Service)

| **Aspekt** | **Anforderung** |
|------------|-----------------|
| **Umfang** | 5–10 öffentlichkeitsrelevante KPIs |
| **Detailtiefe** | Stark aggregiert, vordefinierte Sichten |
| **Fokus** | Transparenz, Vertrauensbildung, Compliance |
| **Aktualisierung** | Wöchentlich/Monatlich |
| **Sicherheit** | Rollenbasiert, strikte Zugriffskontrolle |

**Hinweis**: Externe Dashboards erfordern besondere Datenschutzmaßnahmen und oft separate Plattformen mit eingeschränktem Datenzugriff.

---

## 3. Dashboard-Tools & Plattformen

### 3.1 Vergleich der führenden BI-Plattformen (2025/2026)

| **Tool** | **Stärken** | **Ideal für** | **Preismodell** |
|----------|-------------|---------------|-----------------|
| **Microsoft Power BI** | Microsoft-Integration, Preis-Leistung, KI-Features | Mid-Market, Microsoft-Umgebungen | ~€10–€20/User/Monat |
| **Tableau** | Herausragende Visualisierung, Flexibilität | Data-Driven Enterprises, Analysten | ~€35–€75/User/Monat |
| **Google Looker Studio** | Kostenlos, Google-Ökosystem-Integration | Marketing, Start-ups | Kostenlos |
| **Qlik Sense** | Assoziative Datenmodellierung, Self-Service | Komplexe Datenanalysen | ~€30/User/Monat |
| **Metabase** | Open-Source, einfach zu bedienen | Start-ups, Tech-Teams | Kostenlos / Enterprise |
| **Apache Superset** | Open-Source, skalierbar | Enterprise, Tech-Unternehmen | Kostenlos |

### 3.2 AI/Agent Observability Tools

Für das Monitoring von AI-Agenten und LLM-Applikationen:

| **Tool** | **Fokus** | **Besonderheit** |
|----------|-----------|------------------|
| **LangSmith (LangChain)** | LLM Observability | Traces, Debugging, Cost-Tracking |
| **Langfuse** | AI Agent Tracing | Open-Source, Alternative zu LangSmith |
| **Datadog LLM Observability** | Enterprise Monitoring | Integriert in bestehende Monitoring-Stacks |
| **Arize AI** | ML Model Monitoring | Production ML/AI Monitoring |
| **AgentOps** | AI Agent Operations | Speziell für Agentic Workflows |

---

## 4. UX/UI Best Practices

### 4.1 Design-Prinzipien

| **Prinzip** | **Beschreibung** |
|-------------|------------------|
| **Hierarchisches Design** | Wichtigste KPIs oben links (F-Pattern Leserichtung) |
| **5-10 Regel** | Maximal 5–10 Metriken pro View, um Überforderung zu vermeiden |
| **Konsistenz** | Einheitliches Farbschema, Layout, Typografie |
| **Weißraum** | Genügend Abstand zwischen Elementen für bessere Lesbarkeit |
| **Progressive Offenlegung** | Details nur bei Bedarf einblenden |
| **Farbcodierung** | Farben für Status (Grün/Gelb/Rot) konsistent verwenden |

### 4.2 Visuelle Empfehlungen

**Diagramm-Typ nach Datentyp:**

| **Datentyp** | **Empfohlene Visualisierung** |
|--------------|------------------------------|
| Trends über Zeit | Liniendiagramm, Flächendiagramm |
| Vergleiche zwischen Kategorien | Balkendiagramm, Säulendiagramm |
| Anteile/Ganzes | Torten-/Donut-Diagramm |
| Einzelne Kennzahlen | KPI-Karte (Big Number) |
| Status/Status quo | Gauge, Traffic Lights |
| Geografische Daten | Heatmap, Choroplethenkarte |

### 4.3 Farbschema & Accessibility

- **Primärfarben**: Maximal 3–5 Farben für das gesamte Dashboard
- **Statusfarben**: 
  - ✅ Grün: Zielerreichung (>90%)
  - 🟡 Gelb: Warnung (70–90%)
  - 🔴 Rot: Kritisch (<70%)
- **Kontrast**: WCAG AA Kontrastverhältnisse einhalten
- **Farbenblindheit**: Nicht ausschließlich auf Farben verlassen (Muster, Labels)

### 4.4 Layout-Struktur

```
┌─────────────────────────────────────────────────────────┐
│  HEADER: Dashboard Title | Filter | Zeitraum | Export│
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐│
│ │   KPI 1     │ │   KPI 2     │ │      KPI 3          ││
│ │  (Big #)    │ │  (Big #)    │ │     (Big #)         ││
│ └─────────────┘ └─────────────┘ └─────────────────────┘│
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │   Trend Chart 1      │  │    Trend Chart 2         │ │
│  │   (Liniendiagramm)   │  │    (Balkendiagramm)     │ │
│  └──────────────────────┘  └──────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐ │
│  │              Detail-Tabelle / Grid                │ │
│  │              (Sortierbar, mit Filter              │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 5. MilaOS spezifische Anforderungen

### 5.1 Fractal Memory System – Dashboard-Anforderungen

Das **Fractal Memory System** von MilaOS erfordert spezifische Metriken zur Überwachung des Gedächtnissystems und der Wissensrepräsentation.

| **Komponente** | **Metriken** | **Beschreibung** |
|----------------|--------------|------------------|
| **Memory Nodes** | Anzahl aktive/passive Nodes, Speicherauslastung, Verknüpfungsdichte | Übersicht über Wissensbasis |
| **Context Loading** | Kontext-Hits, Context-Misses, Ladezeiten | Effektivität des Kontext-Managements |
| **Memory Consolidation** | Neue Erinnerungen/Tag, Konsolidierungsrate | Wissensaufbau über Zeit |
| **Retrieval Performance** | Recall-Accuracy, Suchlatenz, Relevanz-Score | Qualität des Abrufsystems |
| **Fractal Depth** | Aktuelle Tiefe, Verzweigungstiefe | Komplexität des Wissensgraphen |

### 5.2 AI-Agent Metriken (für MilaOS Agenten)

| **Kategorie** | **Metrik** | **Beschreibung** |
|---------------|------------|------------------|
| **Performance** | Task-Success-Rate, durchschnittliche Task-Dauer, Retry-Rate | Wie gut erfüllt der Agent seine Aufgaben? |
| **Latenz** | First-Response-Time, Total-Processing-Time, Token-generation-Speed | Reaktionsfähigkeit |
| **Kosten** | Token-Verbrauch/Request, Kosten/Task, Kosten/Tag | Ressourceneffizienz |
| **Qualität** | User-Satisfaction-Score, Error-Rate, Hallucination-Rate | Ausgabequalität |
| **Nutzung** | Requests/Tag, aktive Benutzer, Peak-Zeiten | Nutzungsverhalten |
| **Reliabilität** | Uptime, Error-Rate, Recovery-Time | Verfügbarkeit & Stabilität |

### 5.3 Empfohlene Dashboard-Architektur für MilaOS

```
┌──────────────────────────────────────────────────────────────────┐
│                    MILAOS DASHBOARD SUITE                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │   AGENT OVERVIEW     │  │      FRACTAL MEMORY STATUS       │ │
│  │  ┌────────────────┐  │  │  ┌────────────────────────────┐  │ │
│  │  │ Aktive Agents  │  │  │  │ Memory Nodes: 127          │  │ │
│  │  │ Tasks Today: X │  │  │  │ Context Depth: 5           │  │ │
│  │  │ Success Rate:% │  │  │  │ Links: 1,247               │  │ │
│  │  └────────────────┘  │  │  │ Memory Usage: 2.3GB        │  │ │
│  └──────────────────────┘  │  └────────────────────────────┘  │ │
│                             └──────────────────────────────────┘ │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │   PERFORMANCE        │  │      COST TRACKING              │ │
│  │  ┌────────────────┐  │  │  ┌────────────────────────────┐  │ │
│  │  │ Latency Chart │  │  │  │ Tokens Today: XX,XXX       │  │ │
│  │  │ Error Graph   │  │  │  │ Est. Cost Today: $X.XX     │  │ │
│  │  └────────────────┘  │  │  │ Cost Trend (7d)             │  │ │
│  └──────────────────────┘  │  └────────────────────────────┘  │ │
│                             └──────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │                     RECENT ACTIVITY LOG                      ││
│  │  Timestamp | Agent | Task | Status | Duration | Cost        ││
│  └──────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

### 5.4 Monitoring-Stack Empfehlung für MilaOS

| **Schicht** | **Tool/Technologie** | **Zweck** |
|-------------|---------------------|-----------|
| **Metrics** | Prometheus + Grafana | Metriken-Sammlung & Visualisierung |
| **Tracing** | Langfuse / LangSmith | Request-Tracing für Agenten |
| **Logging** | ELK Stack / Loki | Log-Aggregation |
| **Alerting** | Alertmanager / PagerDuty | Incident-Management |
| **BI/Reporting** | Metabase (Self-hosted) | Executive Dashboards |

---

## 6. Zusammenfassung & Empfehlungen

### 6.1 Key Takeaways

1. **Weniger ist mehr**: 5–15 KPIs pro Dashboard; Überladung reduziert die Nutzbarkeit
2. **Zielgruppe definieren**: Executive-, Team- und externe Stakeholder brauchen unterschiedliche Views
3. **Hierarchie beachten**: Wichtigste Metriken oben links, Details per Drill-Down
4. **Echtzeit vs. Batch**: Executive-Dashboards täglich, Team-Dashboards stündlich, AI-Monitoring in Echtzeit
5. **Tool-Wahl**: Power BI für Microsoft-Umgebungen, Tableau für Visualisierungsexzellenz, Metabase für Open-Source

### 6.2 Prioritäten für MilaOS

| **Priorität** | **Bereich** | **Empfehlung** |
|---------------|-------------|-----------------|
| 🔴 **Hohe** | AI-Agent Monitoring | Langfuse oder Prometheus/Grafana für Echtzeit-Metriken |
| 🔴 **Hohe** | Fractal Memory Dashboard | Eigenentwicklung mit Memory-Node-Visualisierung |
| 🟡 **Mittlere** | Executive Dashboard | Metabase oder Grafana (kostengünstig, flexibel) |
| 🟢 **Niedrige** | Team-Dashboards | Jira/Linear-Integration, spätere Phase |

### 6.3 Nächste Schritte

1. **Kurzfristig**: Implementierung eines Basis-Monitorings mit Prometheus + Grafana
2. **Mittelfristig**: Integration von Langfuse für Agent-Observability
3. **Langfristig**: Entwicklung eines dedizierten Fractal Memory Dashboards mit Netzwerkvisualisierung

---

*Dieser Report wurde als Research-Grundlage für die MilaOS Dashboard-Entwicklung erstellt.*
