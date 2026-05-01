import React from 'react';
import FormPanel from './FormPanel';
import ChatPanel from './ChatPanel';

const LogInteractionScreen = () => {
  return (
    <div className="flex flex-col lg:flex-row gap-6 items-start">
      <div className="w-full lg:w-2/3 bg-white rounded-xl shadow-sm border border-amber-100 overflow-hidden">
        <FormPanel />
      </div>
      <div className="w-full lg:w-1/3 bg-white rounded-xl shadow-sm border border-amber-100 overflow-hidden lg:sticky lg:top-24 h-[calc(100vh-8rem)]">
        <ChatPanel />
      </div>
    </div>
  );
};

export default LogInteractionScreen;
