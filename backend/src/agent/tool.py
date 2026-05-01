"""
LangGraph Tools — 5 sales-focused tools for the HCP CRM Agent.

Tools:
  1. log_interaction   — Extract entities via LLM + persist to DB
  2. edit_interaction  — Update an existing interaction by ID
  3. get_hcp_insights  — Retrieve history + stats for a named doctor
  4. suggest_followup  — LLM-generated next-best-action recommendation
  5. summary           — Summarize all interactions via LLM
"""
import json
import re
from src.utils.database import SessionLocal
from src.models.models import Interaction
from src.agent.llm import call_llm


# ---------------------------------------------------------------------------
# Helper: get a fresh session per tool call (avoids stale connection issues)
# ---------------------------------------------------------------------------
def _db():
    return SessionLocal()


# ---------------------------------------------------------------------------
# Tool 1 — Log Interaction
# Uses the LLM to extract structured entities from a natural-language input,
# then persists the interaction to the database.
# ---------------------------------------------------------------------------
def log_interaction_tool(user_input: str) -> dict:
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")

    extraction_prompt = f"""
You are a medical CRM data extractor for a pharmaceutical field representative.
Current Date: {current_date}

Extract structured data from the following free-text note and return ONLY valid JSON
with these exact keys (use null if a field is not mentioned):
{{
  "doctor_name": string or null,
  "hospital": string or null,
  "specialty": string or null,
  "interaction_type": string or null,  // e.g. "Visit", "Call", "Email", "Conference"
  "product_discussed": string or null,
  "date": string or null,              // e.g. "2024-05-01" (resolve relative dates like "yesterday" using Current Date)
  "time": string or null,              // e.g. "14:30"
  "notes": string,                     // cleaned summary of the interaction
  "follow_up": string or null,         // e.g. "Call next Monday", "Send samples"
  "outcome": string or null            // e.g. "Interested", "Needs more info", "Declined"
}}

Field rep's note:
\"\"\"{user_input}\"\"\"

Return ONLY the JSON object. No explanation, no markdown.
"""

    raw = call_llm(extraction_prompt, model="llama-3.1-8b-instant")

    # Strip markdown code fences if model wraps output
    cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: store the raw note with minimal metadata
        data = {
            "doctor_name": "Unknown",
            "hospital": None,
            "specialty": None,
            "interaction_type": None,
            "product_discussed": None,
            "date": None,
            "time": None,
            "notes": user_input,
            "follow_up": None,
            "outcome": None,
        }

    # Replace None-valued keys that are missing from LLM output
    defaults = {
        "doctor_name": "Unknown",
        "hospital": None,
        "specialty": None,
        "interaction_type": None,
        "product_discussed": None,
        "date": None,
        "time": None,
        "notes": user_input,
        "follow_up": None,
        "outcome": None,
    }
    for k, v in defaults.items():
        data.setdefault(k, v)

    db = _db()
    try:
        interaction = Interaction(**{k: data[k] for k in defaults})
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return {"message": "Interaction logged successfully", "id": interaction.id, "data": data}
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Tool 2 — Edit Interaction
# Looks up the most recent interaction for a doctor and updates the specified fields.
# ---------------------------------------------------------------------------
def edit_interaction_tool(doctor_name: str, updates: dict) -> dict:
    db = _db()
    try:
        # Improve fuzzy matching by using the last word of the name (e.g. "Jenkins" from "Dr. Jenkins")
        search_term = doctor_name.replace("Dr.", "").replace("Dr ", "").strip()
        last_name = search_term.split()[-1] if search_term.split() else doctor_name

        matching_interactions = (
            db.query(Interaction)
            .filter(Interaction.doctor_name.ilike(f"%{last_name}%"))
            .order_by(Interaction.created_at.desc())
            .all()
        )
        
        if not matching_interactions:
            return {"error": f"No recent interaction found for doctor: {doctor_name}"}

        # Check for ambiguity
        distinct_doctors = list(set(i.doctor_name for i in matching_interactions))
        if len(distinct_doctors) > 1:
            return {
                "needs_disambiguation": True,
                "options": distinct_doctors,
                "message": f"I found multiple doctors matching '{doctor_name}'. Which one did you mean?",
                "context": {"tool": "edit_interaction", "updates": updates}
            }

        interaction = matching_interactions[0]

        allowed = {
            "doctor_name", "hospital", "specialty", "interaction_type",
            "product_discussed", "date", "time", "notes", "follow_up", "outcome"
        }
        for field, value in updates.items():
            if field in allowed:
                setattr(interaction, field, value)

        db.commit()
        db.refresh(interaction)
        return {"message": f"Interaction for Dr. {doctor_name} updated", "updated_fields": list(updates.keys()), "data": {k: getattr(interaction, k) for k in allowed}}
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Tool 3 — Get HCP Insights
# Retrieves all interactions for a given doctor name and returns stats + notes.
# ---------------------------------------------------------------------------
def get_hcp_insights_tool(doctor_name: str) -> dict:
    db = _db()
    try:
        search_term = doctor_name.replace("Dr.", "").replace("Dr ", "").strip()
        last_name = search_term.split()[-1] if search_term.split() else doctor_name

        matching_interactions = (
            db.query(Interaction)
            .filter(Interaction.doctor_name.ilike(f"%{last_name}%"))
            .order_by(Interaction.created_at.desc())
            .all()
        )

        if not matching_interactions:
            return {"doctor": doctor_name, "total_interactions": 0, "history": []}

        distinct_doctors = list(set(i.doctor_name for i in matching_interactions))
        if len(distinct_doctors) > 1:
            return {
                "needs_disambiguation": True,
                "options": distinct_doctors,
                "message": f"I found multiple doctors matching '{doctor_name}'. Which one did you mean?",
                "context": {"tool": "get_hcp_insights"}
            }

        # Filter interactions to only those matching the 1 distinct doctor
        exact_doctor = distinct_doctors[0]
        interactions = [i for i in matching_interactions if i.doctor_name == exact_doctor]

        history = [
            {
                "id": i.id,
                "type": i.interaction_type,
                "product": i.product_discussed,
                "date": i.date or str(i.created_at.date()),
                "time": i.time or str(i.created_at.time()),
                "outcome": i.outcome,
                "notes": i.notes,
                "follow_up": i.follow_up,
            }
            for i in interactions
        ]
        return {
            "doctor": doctor_name,
            "hospital": interactions[0].hospital,
            "specialty": interactions[0].specialty,
            "total_interactions": len(interactions),
            "history": history,
        }
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Tool 4 — Suggest Follow-up
# Uses the LLM to recommend the next best sales action based on past context.
# ---------------------------------------------------------------------------
def suggest_followup_tool(context: str) -> dict:
    prompt = f"""
You are an AI sales coach for a pharmaceutical field representative.

Based on the following context about a recent HCP interaction, suggest the single best
follow-up action the rep should take. Be specific, concise, and actionable.

Context:
\"\"\"{context}\"\"\"

Return ONLY the follow-up suggestion (1-2 sentences).
"""
    suggestion = call_llm(prompt, model="llama-3.3-70b-versatile")
    return {"suggestion": suggestion.strip()}


# ---------------------------------------------------------------------------
# Tool 5 — Interaction Summary
# Fetches all interaction notes and asks the LLM to produce a high-level summary.
# ---------------------------------------------------------------------------
def summary_tool() -> dict:
    db = _db()
    try:
        interactions = db.query(Interaction).order_by(Interaction.created_at.desc()).limit(50).all()
        if not interactions:
            return {"summary": "No interactions found in the database."}

        notes_text = "\n".join(
            f"- [{i.doctor_name} @ {i.hospital}] {i.notes} (Outcome: {i.outcome})"
            for i in interactions
        )

        prompt = f"""
You are a CRM analytics assistant.

Summarize the following HCP interaction records for a pharmaceutical field manager.
Highlight: key doctors engaged, top products discussed, common outcomes, and any
critical follow-up actions pending.

Records:
{notes_text}

Provide a structured summary (3-5 bullet points).
CRITICAL: Use ONLY plain text. Do NOT use markdown like asterisks (**) or hashes (#).
Separate bullet points with a standard dash (-) and a new line.
"""
        result = call_llm(prompt, model="llama-3.3-70b-versatile")
        return {"summary": result.strip(), "total_records_analyzed": len(interactions)}
    finally:
        db.close()