import React from 'react';
import LogInteractionScreen from './components/LogInteractionScreen';

function App() {
  return (
    <div className="min-h-screen bg-amber-50">
      <header className="bg-white border-b border-amber-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              
              <span className="font-semibold text-xl text-slate-800">AI CRM</span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-amber-600 font-medium border-b-2 border-amber-600 px-1 py-5">Log Interaction</a>

            </nav>
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center text-amber-700 font-medium">
                SS
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-slate-800">Log HCP Interaction</h1>
          <p className="text-slate-500 mt-1">Record your recent meeting or call with a Healthcare Professional.</p>
        </div>
        <LogInteractionScreen />
      </main>
    </div>
  );
}

export default App;
