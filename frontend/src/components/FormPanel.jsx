import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Search, Calendar, Clock, Mic, Plus, Check } from 'lucide-react';
import { updateFormField } from '../store';
import { useLogInteractionMutation, useSuggestFollowupMutation } from '../apiSlice';

const FormPanel = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.interaction.currentInteraction);
  const [logInteraction, { isLoading, isSuccess, isError }] = useLogInteractionMutation();
  const [dynamicSuggestion, setDynamicSuggestion] = useState(null);
  const [getSuggestion, { isLoading: isSuggesting }] = useSuggestFollowupMutation();

  const handleGetSuggestion = async () => {
    const context = `Doctor: ${formData.doctor_name}, Notes: ${formData.notes}, Outcome: ${formData.outcome}`;
    try {
      const res = await getSuggestion(context).unwrap();
      setDynamicSuggestion(res.suggestion);
    } catch (e) {
      console.error("Failed to get suggestion", e);
    }
  };

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    if (type === 'radio') {
      dispatch(updateFormField({ field: name, value: e.target.value }));
    } else {
      dispatch(updateFormField({ field: name, value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // In a real app, this would be mapped to the expected backend payload
    const payload = {
      doctor_name: formData.doctor_name,
      interaction_type: formData.interaction_type,
      notes: formData.notes,
      outcome: formData.outcome,
      follow_up: formData.follow_up
    };
    
    // For logging interaction via tool (it accepts a single string usually in tool 1, but let's assume we map it)
    // Here we'll pass the whole object or a constructed string
    const stringified = `Doctor: ${formData.doctor_name}, Type: ${formData.interaction_type}, Notes: ${formData.notes}, Outcome: ${formData.outcome}, Follow-up: ${formData.follow_up}`;
    
    // Call the backend API (adjust endpoint based on actual backend route)
    // Assuming a generic /interactions endpoint or specific agent log tool route
    // This is just a placeholder to show integration
    console.log("Submitting:", stringified);
    alert("Interaction logged!");
  };

  return (
    <form onSubmit={handleSubmit} className="p-6">
      <div className="border-b border-amber-100 pb-4 mb-6">
        <h2 className="text-lg font-semibold text-slate-800">Interaction Details</h2>
      </div>

      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-700">HCP Name</label>
            <div className="relative">
              <input
                type="text"
                name="doctor_name"
                value={formData.doctor_name}
                onChange={handleChange}
                placeholder="Search or select HCP..."
                className="w-full pl-3 pr-10 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none transition-shadow"
              />
              <Search className="absolute right-3 top-2.5 h-5 w-5 text-slate-400" />
            </div>
          </div>
          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-700">Interaction Type</label>
            <select
              name="interaction_type"
              value={formData.interaction_type}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none bg-white"
            >
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Email">Email</option>
              <option value="Conference">Conference</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-700">Date</label>
            <div className="relative">
              <input
                type="date"
                name="date"
                value={formData.date}
                onChange={handleChange}
                className="w-full pl-3 pr-10 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-slate-700"
              />
              <Calendar className="absolute right-3 top-2.5 h-5 w-5 text-slate-400 pointer-events-none" />
            </div>
          </div>
          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-700">Time</label>
            <div className="relative">
              <input
                type="time"
                name="time"
                value={formData.time}
                onChange={handleChange}
                className="w-full pl-3 pr-10 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-slate-700"
              />
              <Clock className="absolute right-3 top-2.5 h-5 w-5 text-slate-400 pointer-events-none" />
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-slate-700">Attendees</label>
          <input
            type="text"
            name="attendees"
            value={formData.attendees}
            onChange={handleChange}
            placeholder="Enter names or search..."
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none"
          />
        </div>

        <div className="space-y-2 relative">
          <label className="block text-sm font-medium text-slate-700">Topics Discussed</label>
          <div className="relative">
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows={4}
              placeholder="Enter key discussion points..."
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none resize-none"
            />
            <button type="button" className="absolute bottom-3 right-3 p-1.5 bg-amber-50 text-amber-600 hover:bg-amber-100 rounded-md transition-colors">
              <Mic className="h-4 w-4" />
            </button>
          </div>
          <button type="button" className="mt-2 text-sm text-amber-600 bg-amber-50 hover:bg-amber-100 px-3 py-1.5 rounded-md transition-colors font-medium flex items-center gap-2 border border-amber-200">
            <Mic className="h-4 w-4" /> Summarize from Voice Note (Requires Consent)
          </button>
        </div>

        <div className="border-t border-amber-100 pt-6">
          <h3 className="text-sm font-semibold text-slate-800 mb-4">Materials Shared / Samples Distributed</h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between border border-slate-200 p-3 rounded-lg bg-slate-50">
              <span className="text-sm text-slate-600">Materials Shared</span>
              <button type="button" className="text-sm font-medium text-slate-700 bg-white border border-slate-300 px-3 py-1.5 rounded-md hover:bg-slate-50 flex items-center gap-1">
                <Search className="h-3 w-3" /> Search/Add
              </button>
            </div>
            
            <div className="flex items-center justify-between border border-slate-200 p-3 rounded-lg bg-slate-50">
              <span className="text-sm text-slate-600">Samples Distributed</span>
              <button type="button" className="text-sm font-medium text-slate-700 bg-white border border-slate-300 px-3 py-1.5 rounded-md hover:bg-slate-50 flex items-center gap-1">
                <Plus className="h-3 w-3" /> Add Sample
              </button>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <label className="block text-sm font-medium text-slate-700">Observed/Inferred HCP Sentiment</label>
          <div className="flex gap-6">
            <label className="flex items-center gap-2 cursor-pointer group">
              <input type="radio" name="sentiment" value="Positive" checked={formData.sentiment === 'Positive'} onChange={handleChange} className="w-4 h-4 text-amber-600 focus:ring-amber-500 border-slate-300" />
              <span className="text-slate-700 flex items-center gap-1 group-hover:text-amber-600 transition-colors">😄 Positive</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer group">
              <input type="radio" name="sentiment" value="Neutral" checked={formData.sentiment === 'Neutral'} onChange={handleChange} className="w-4 h-4 text-amber-600 focus:ring-amber-500 border-slate-300" />
              <span className="text-slate-700 flex items-center gap-1 group-hover:text-amber-600 transition-colors">😐 Neutral</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer group">
              <input type="radio" name="sentiment" value="Negative" checked={formData.sentiment === 'Negative'} onChange={handleChange} className="w-4 h-4 text-amber-600 focus:ring-amber-500 border-slate-300" />
              <span className="text-slate-700 flex items-center gap-1 group-hover:text-amber-600 transition-colors">🙁 Negative</span>
            </label>
          </div>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-slate-700">Outcomes</label>
          <textarea
            name="outcome"
            value={formData.outcome}
            onChange={handleChange}
            rows={2}
            placeholder="Key outcomes or agreements..."
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none resize-none"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-slate-700">Follow-up Actions</label>
          <textarea
            name="follow_up"
            value={formData.follow_up}
            onChange={handleChange}
            rows={2}
            placeholder="Enter next steps or tasks..."
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none resize-none"
          />
          <div className="mt-2 p-3 bg-amber-50 border border-amber-200 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-amber-800 uppercase tracking-wider">AI Suggested Follow-ups:</span>
              <button
                type="button"
                onClick={handleGetSuggestion}
                disabled={isSuggesting}
                className="text-xs font-medium bg-amber-100 hover:bg-amber-200 text-amber-800 px-2 py-1 rounded transition-colors disabled:opacity-50"
              >
                {isSuggesting ? "Generating..." : "Generate Suggestion"}
              </button>
            </div>
            {dynamicSuggestion ? (
              <ul className="mt-2 text-sm text-amber-700 space-y-1">
                <li className="flex items-center gap-2 hover:text-amber-900 cursor-pointer" onClick={() => dispatch(updateFormField({ field: 'follow_up', value: dynamicSuggestion }))}>
                  <Plus className="h-3 w-3 flex-shrink-0" />
                  <span>{dynamicSuggestion}</span>
                </li>
              </ul>
            ) : (
              <p className="mt-2 text-sm text-amber-700/70 italic">Click generate to get an AI recommendation based on your notes.</p>
            )}
          </div>
        </div>
      </div>
      
      <div className="mt-8 flex justify-end">
        <button
          type="submit"
          className="bg-amber-600 hover:bg-amber-700 text-white px-6 py-2 rounded-lg font-medium shadow-sm transition-colors flex items-center gap-2"
        >
          <Check className="h-4 w-4" /> Save Interaction
        </button>
      </div>
    </form>
  );
};

export default FormPanel;
