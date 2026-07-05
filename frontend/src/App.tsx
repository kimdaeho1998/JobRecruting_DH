const App = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <main className="mx-auto flex max-w-5xl flex-col gap-6 px-6 py-16">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">
            JobInsight AI
          </p>
          <h1 className="mt-4 text-4xl font-bold">AI 기반 채용공고 분석 플랫폼</h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-300">
            Mock Data 기반 MVP 구조로 시작하는 기본 프론트엔드 화면입니다.
          </p>
        </div>
      </main>
    </div>
  );
};

export default App;
