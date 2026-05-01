import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://localhost:8000/api' }),
  endpoints: (builder) => ({
    chat: builder.mutation({
      query: (message) => ({
        url: '/chat',
        method: 'POST',
        body: { message },
      }),
    }),
    logInteraction: builder.mutation({
      query: (interaction) => ({
        url: '/interaction/log',
        method: 'POST',
        body: interaction,
      }),
    }),
    suggestFollowup: builder.mutation({
      query: (context) => ({
        url: '/interaction/suggest_followup',
        method: 'POST',
        body: { context },
      }),
    }),
  }),
});

export const { useChatMutation, useLogInteractionMutation, useSuggestFollowupMutation } = apiSlice;
