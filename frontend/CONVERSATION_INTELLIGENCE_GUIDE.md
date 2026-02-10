# 🎨 Conversation Intelligence Visualization Guide

## 🚀 What's New?

You now have **3 beautiful new visualization components** that display AI-powered conversation analysis:

### 1️⃣ **Decisions Timeline Card** ✅
Shows all decisions extracted from team conversations with:
- Decision type categorization (technical, process, resource, timeline, scope)
- Confidence scores
- Who made the decision
- Rationale/reasoning (when available)
- Color-coded by type

### 2️⃣ **Unanswered Questions Card** ❓
Tracks questions that need attention with:
- Urgency levels (high, medium, low)
- Question types (technical, clarification, status, permission, information)
- Alerts for critical unanswered questions
- Who asked the question
- Answer status tracking

### 3️⃣ **Entity Network Card** 🔗
Visualizes entities and relationships:
- People mentioned (@mentions)
- Tasks/Issues (Jira tickets, GitHub PRs/issues)
- Technologies (languages, frameworks, databases, tools)
- Relationship counts (person→task, person→tech, etc.)
- Most mentioned entities

---

## 📍 How to Access

### Option 1: Direct URL
Navigate to: **`http://localhost:5173/conversation`**

### Option 2: From Intelligence Dashboard
Add a navigation link to your existing dashboard

---

## 🎯 What You'll See

### **Page Layout:**

```
┌─────────────────────────────────────────────────────────┐
│  💬 Conversation Intelligence                           │
│  AI-powered analysis of team conversations              │
├─────────────────────────────────────────────────────────┤
│  [🔍 Analyze Conversation]  Analyzing 8 messages        │
├─────────────────────────────────────────────────────────┤
│  Messages: 8  │  Decisions: 3  │  Questions: 2  │ ...  │
├──────────────────────────┬──────────────────────────────┤
│  ✅ Decisions Made       │  ❓ Unanswered Questions     │
│  ┌──────────────────┐   │  ┌──────────────────┐       │
│  │ Technical: 3     │   │  │ Total: 2         │       │
│  │ Process: 0       │   │  │ Answered: 0      │       │
│  ├──────────────────┤   │  │ Unanswered: 2    │       │
│  │ Decision 1       │   │  ├──────────────────┤       │
│  │ Decision 2       │   │  │ Question 1       │       │
│  │ Decision 3       │   │  │ Question 2       │       │
│  └──────────────────┘   │  └──────────────────┘       │
├──────────────────────────┴──────────────────────────────┤
│  🔗 Entity Network                                      │
│  ┌────────────────────────────────────────────────────┐│
│  │ 👥 People: 4  │  📋 Tasks: 2  │  ⚙️ Tech: 6       ││
│  ├────────────────────────────────────────────────────┤│
│  │ Most Mentioned Tasks:                              ││
│  │ • PR-123 (2x)                                      ││
│  │ • PROJ-456 (1x)                                    ││
│  ├────────────────────────────────────────────────────┤│
│  │ Most Discussed Tech:                               ││
│  │ PostgreSQL (2x) │ React (1x) │ Django (1x) ...    ││
│  └────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

---

## 🔌 API Endpoints

The visualization uses these new backend endpoints:

### 1. Analyze Decisions
```http
POST /api/v1/conversation/analyze-decisions
Content-Type: application/json

{
  "messages": [
    {
      "user": "alice@example.com",
      "text": "We decided to use PostgreSQL",
      "timestamp": "2024-01-15T10:00:00"
    }
  ],
  "min_confidence": 0.6
}
```

**Response:**
```json
{
  "decisions": [...],
  "total_count": 3,
  "by_type": {
    "technical": 3,
    "process": 0
  },
  "summary": "## Decisions Summary..."
}
```

### 2. Analyze Questions
```http
POST /api/v1/conversation/analyze-questions
```

**Response:**
```json
{
  "questions": [...],
  "total_count": 2,
  "unanswered_count": 2,
  "alerts": [...],
  "summary": "## Questions Summary..."
}
```

### 3. Extract Entities
```http
POST /api/v1/conversation/extract-entities
```

**Response:**
```json
{
  "entities": {
    "people": [...],
    "tasks": [...],
    "technologies": [...]
  },
  "relationships": {...},
  "most_mentioned": {...},
  "summary": "## Entity Summary..."
}
```

### 4. Full Analysis
```http
POST /api/v1/conversation/analyze-full
```

Returns all three analyses combined with insights.

---

## 🎨 Component Features

### **DecisionsTimelineCard**

**Visual Elements:**
- 🎨 Purple/Pink gradient background
- 📊 Stats grid showing total and by-type counts
- 📜 Scrollable timeline of decisions
- 🏷️ Type badges (technical, process, etc.)
- 💡 Rationale display when available
- 📈 Confidence percentage

**Interactions:**
- Hover effects on decision cards
- Smooth animations on load
- "View all" link when >10 decisions

### **UnansweredQuestionsCard**

**Visual Elements:**
- 🎨 Orange/Red gradient background
- 🚨 Alert banner for critical questions
- 🎯 Urgency badges (high, medium, low)
- 📊 Stats: Total, Answered, Unanswered
- 🏷️ Question type indicators

**Interactions:**
- Color-coded by urgency
- Animated question cards
- Empty state celebration when all answered

### **EntityNetworkCard**

**Visual Elements:**
- 🎨 Cyan/Blue gradient background
- 📊 Entity count stats
- 🔗 Relationship summary
- 📋 Most mentioned lists
- 🏷️ Technology tags with counts

**Interactions:**
- Tag cloud for technologies
- Scrollable entity lists
- Animated entity cards

---

## 🧪 Testing the Visualization

### Step 1: Start Services
```bash
# Backend (if not running)
cd services/intelligence-service
python -m uvicorn src.main:app --reload --port 8002

# Frontend (if not running)
cd frontend
npm run dev
```

### Step 2: Open Browser
Navigate to: `http://localhost:5173/conversation`

### Step 3: Click "Analyze Conversation"
The page will:
1. Send sample conversation to backend
2. Extract decisions, questions, and entities
3. Display results in beautiful cards

### Step 4: Explore the Data
- Scroll through decisions
- Check unanswered questions
- View entity relationships

---

## 🎯 Sample Data

The page includes 8 sample messages demonstrating:

**Decisions:**
- "We decided to go with PostgreSQL..."
- "Let's also use React for the frontend..."
- "We will implement the new feature using TypeScript..."

**Questions:**
- "Should we use PostgreSQL or MongoDB?"
- "How urgent is this?"
- "What about the deployment strategy?"

**Entities:**
- **People:** alice, bob, charlie, david
- **Tasks:** PR-123, PROJ-456
- **Technologies:** PostgreSQL, MongoDB, React, Django, FastAPI, TypeScript, Next.js, Docker, Kubernetes

---

## 🔧 Customization

### Change Sample Data
Edit `ConversationIntelligence.jsx`:
```javascript
const sampleMessages = [
    {
        user: 'your@email.com',
        text: 'Your message here',
        timestamp: new Date().toISOString()
    },
    // Add more messages...
];
```

### Adjust Confidence Threshold
```javascript
min_confidence: 0.5  // Lower = more results, Higher = more accurate
```

### Modify Colors
Each card has gradient classes you can customize:
```javascript
// DecisionsTimelineCard
className="bg-gradient-to-br from-purple-900/40 to-pink-900/40"

// UnansweredQuestionsCard
className="bg-gradient-to-br from-orange-900/40 to-red-900/40"

// EntityNetworkCard
className="bg-gradient-to-br from-cyan-900/40 to-blue-900/40"
```

---

## 📊 Real-World Usage

### Integrate with Slack/Teams
```javascript
// Fetch messages from Slack API
const slackMessages = await fetchSlackMessages(channelId);

// Convert to format
const formattedMessages = slackMessages.map(msg => ({
    user: msg.user_email,
    text: msg.text,
    timestamp: msg.ts
}));

// Analyze
const analysis = await analyzeConversation(formattedMessages);
```

### Integrate with Jira Comments
```javascript
// Fetch Jira issue comments
const jiraComments = await fetchJiraComments(issueKey);

// Analyze for decisions and questions
const decisions = await analyzeDecisions(jiraComments);
```

### Integrate with GitHub Discussions
```javascript
// Fetch GitHub discussion
const discussion = await fetchGitHubDiscussion(discussionId);

// Extract entities
const entities = await extractEntities(discussion.comments);
```

---

## 🚀 Next Steps

### 1. Add to Main Dashboard
Create a navigation link:
```jsx
<Link to="/conversation">
    💬 Conversation Intelligence
</Link>
```

### 2. Connect Real Data
Replace sample messages with:
- Slack integration
- Teams integration
- Jira comments
- GitHub discussions
- Email threads

### 3. Add Filters
```jsx
// Filter by date range
<DateRangePicker onChange={setDateRange} />

// Filter by person
<PersonFilter onChange={setSelectedPerson} />

// Filter by urgency
<UrgencyFilter onChange={setUrgencyLevel} />
```

### 4. Export Reports
```jsx
<button onClick={exportToPDF}>
    📄 Export Report
</button>
```

---

## 🎉 Summary

**You now have:**
- ✅ 3 beautiful visualization components
- ✅ 4 new API endpoints
- ✅ Full conversation intelligence page
- ✅ Sample data for testing
- ✅ Real-time analysis

**Access it at:** `http://localhost:5173/conversation`

**Enjoy your new AI-powered conversation insights!** 🚀
