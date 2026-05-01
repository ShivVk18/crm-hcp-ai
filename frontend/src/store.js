import { configureStore, createSlice } from '@reduxjs/toolkit';
import { apiSlice } from './apiSlice';

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: {
    currentInteraction: {
      doctor_name: '',
      interaction_type: 'Meeting',
      date: '',
      time: '',
      attendees: '',
      notes: '',
      materials: [],
      samples: [],
      sentiment: 'Neutral',
      outcome: '',
      follow_up: ''
    },
    chatMessages: [
      { id: 1, type: 'bot', text: 'Hello! I am your AI Assistant. You can log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment") or ask for help.' }
    ]
  },
  reducers: {
    updateFormField: (state, action) => {
      const { field, value } = action.payload;
      state.currentInteraction[field] = value;
    },
    setInteraction: (state, action) => {
      state.currentInteraction = { ...state.currentInteraction, ...action.payload };
    },
    addChatMessage: (state, action) => {
      state.chatMessages.push(action.payload);
    },
    resetForm: (state) => {
      state.currentInteraction = {
        doctor_name: '',
        interaction_type: 'Meeting',
        date: '',
        time: '',
        attendees: '',
        notes: '',
        materials: [],
        samples: [],
        sentiment: 'Neutral',
        outcome: '',
        follow_up: ''
      };
    }
  }
});

export const { updateFormField, setInteraction, addChatMessage, resetForm } = interactionSlice.actions;

export const store = configureStore({
  reducer: {
    interaction: interactionSlice.reducer,
    [apiSlice.reducerPath]: apiSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware),
});
