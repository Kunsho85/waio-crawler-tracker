import { useState, useEffect } from 'react';
import './App.css';

// Types
interface BotInfo {
  id: string;
  name: string;
  user_agent: string;
  is_dynamic: boolean;
  description: string;
}

interface ExtractionData {
  title: string | null;
  summary: string | null;
  main_content: string | null;
  waio_detected: boolean;
  attributes_found?: Record<string, string>;
  sources?: Record<string, string>;
}

interface MetricsData {
  network_time_ms: number;
  dom_load_time_ms: number;
  cognitive_time_ms: number;
  total_time_ms: number;
  response_size_bytes: number;
  status_code: number;
  headers_sent: Record<string, string>;
}

interface ComparisonData {
  cognitive_speedup: number;
  performance_gain_percent: number;
  waio_framework_detected: boolean;
}

interface BenchmarkResult {
  url: string;
  bot_type: string;
  heuristic: {
    metrics: MetricsData;
    extraction: ExtractionData;
  };
  waio: {
    metrics: MetricsData;
    extraction: ExtractionData;
  };
  comparison: ComparisonData;
}

const API_BASE = import.meta.env.MODE === 'development' ? 'http://localhost:8000' : '';

function App() {
  const [url, setUrl] = useState('');
  const [botType, setBotType] = useState('GPTBot');
  const [simulationMode, setSimulationMode] = useState('WAIO Theory'); // New state
  const [bots, setBots] = useState<BotInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<BenchmarkResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showHeaders, setShowHeaders] = useState(false);

  // Fetch available bots on mount
  useEffect(() => {
    fetch(`${API_BASE}/api/bots`)
      .then(res => res.json())
      .then(data => setBots(data.bots))
      .catch(() => {
        // Fallback bots if API not available
        setBots([
            { id: 'GPTBot', name: 'GPTBot', user_agent: 'GPTBot/1.2', is_dynamic: false, description: 'OpenAI crawler' },
            { id: 'ClaudeBot', name: 'ClaudeBot', user_agent: 'ClaudeBot/1.0', is_dynamic: false, description: 'Anthropic crawler' },
            { id: 'ChatGPT-User', name: 'ChatGPT-User', user_agent: 'ChatGPT-User/1.0', is_dynamic: true, description: 'JS-enabled crawler' },
            { id: 'Googlebot', name: 'Googlebot', user_agent: 'Googlebot/2.1', is_dynamic: false, description: 'Google Search' },
            { id: 'Google-Extended', name: 'Google-Extended', user_agent: 'Google-Extended', is_dynamic: false, description: 'Google AI' },
            { id: 'PerplexityBot', name: 'PerplexityBot', user_agent: 'PerplexityBot/1.0', is_dynamic: false, description: 'Perplexity AI' },
            { id: 'YouBot', name: 'YouBot', user_agent: 'YouBot/1.0', is_dynamic: false, description: 'You.com search' },
            { id: 'MetaBot', name: 'MetaBot', user_agent: 'facebookexternalhit/1.1', is_dynamic: false, description: 'Meta crawler' },
          ]);
      });
  }, []);

  const reset = () => {
    setUrl('');
    setResult(null);
    setError(null);
    setBotType('GPTBot');
    // Keep simulation mode as preference
  };

  const runBenchmark = async () => {
    if (!url) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/benchmark`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            url, 
            bot_type: botType,
            simulation_mode: simulationMode // Pass selected mode
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Benchmark failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 lg:p-10">
      {/* Header */}
      <header className="text-center mb-10 animate-fade-in">
        <h1 className="text-4xl lg:text-5xl font-bold gradient-text mb-3">
          AI Crawler Tracker
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
          Predictive Extraction Engine — Visualizing how Semantic HTML (WAIO) 
          eliminates bot ambiguity and slashes processing latency.
        </p>
      </header>

      {/* Input Section */}
      <div className="glass-card max-w-4xl mx-auto p-6 mb-8 animate-slide-up">
        {/* Simulation Mode Toggle */}
        <div className="flex justify-center mb-6">
            <div className="bg-black/40 p-1 rounded-lg border border-gray-700 inline-flex">
                <button
                    onClick={() => setSimulationMode('WAIO Theory')}
                    className={`px-4 py-2 rounded-md text-sm font-semibold transition-all ${
                        simulationMode === 'WAIO Theory' 
                        ? 'bg-indigo-600 text-white shadow-lg' 
                        : 'text-gray-400 hover:text-white'
                    }`}
                >
                    WAIO Theory (Doc V2.1)
                </button>
                <button
                    onClick={() => setSimulationMode('Industry Consensus')}
                    className={`px-4 py-2 rounded-md text-sm font-semibold transition-all ${
                        simulationMode === 'Industry Consensus' 
                        ? 'bg-indigo-600 text-white shadow-lg' 
                        : 'text-gray-400 hover:text-white'
                    }`}
                >
                    Industry Consensus
                </button>
            </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-4">
          {/* URL Input */}
          <div className="flex-1">
            <label className="block text-sm text-gray-400 mb-2">Target URL</label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              className="w-full px-4 py-3 bg-black/40 border border-gray-700 rounded-lg 
                         text-white placeholder-gray-500 focus:border-indigo-500 
                         focus:ring-2 focus:ring-indigo-500/20 transition-all outline-none"
            />
          </div>

          {/* Bot Type Dropdown */}
          <div className="w-full lg:w-64">
            <label className="block text-sm text-gray-400 mb-2">Bot Simulation</label>
            <select
              value={botType}
              onChange={(e) => setBotType(e.target.value)}
              className="w-full px-4 py-3 bg-black/40 border border-gray-700 rounded-lg 
                         text-white focus:border-indigo-500 focus:ring-2 
                         focus:ring-indigo-500/20 transition-all outline-none cursor-pointer"
            >
              {bots.map((bot) => (
                <option key={bot.id} value={bot.id}>
                  {bot.name} {bot.is_dynamic ? '(JS)' : '(Static)'}
                </option>
              ))}
            </select>
          </div>

          {/* Buttons */}
          <div className="flex items-end gap-2">
            <button
              onClick={reset}
              className="px-6 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg text-gray-300 
                         font-semibold transition-all flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Reset
            </button>
            <button
              onClick={runBenchmark}
              disabled={loading}
              className="btn-primary w-full lg:w-auto px-8 py-3 rounded-lg text-white 
                         font-semibold disabled:opacity-50 disabled:cursor-not-allowed
                         flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="spinner w-5 h-5" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Run Benchmark
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400">
            {error}
          </div>
        )}
      </div>

      {/* Results Section */}
      {result && (
        <div className="animate-fade-in">
          {/* WAIO Detection Alert */}
          {!result.comparison.waio_framework_detected && (
            <div className="max-w-4xl mx-auto mb-6 p-4 bg-amber-500/20 border border-amber-500/50 
                           rounded-lg text-amber-400 flex items-center gap-3">
              <svg className="w-6 h-6 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>
                <strong>WAIO Framework not detected.</strong> Install it to see performance gains.
                The page doesn't contain <code className="bg-black/30 px-2 py-0.5 rounded">data-ai-*</code> attributes.
              </span>
            </div>
          )}

          {/* Performance Gain Banner */}
          {result.comparison.waio_framework_detected && (
            <div className="max-w-4xl mx-auto mb-8 text-center">
              {result.comparison.performance_gain_percent > 0 ? (
                <div className="inline-block performance-badge px-8 py-4 rounded-2xl">
                  <span className="text-3xl lg:text-5xl font-bold text-white leading-tight">
                    WAIO is {result.comparison.cognitive_speedup.toFixed(1)}x faster
                  </span>
                  <p className="text-emerald-100 mt-1">
                    {result.comparison.performance_gain_percent.toFixed(1)}% reduction in cognitive processing time
                  </p>
                </div>
              ) : result.comparison.performance_gain_percent === 0 ? (
                <div className="inline-block performance-badge-neutral px-8 py-4 rounded-2xl">
                  <span className="text-3xl lg:text-5xl font-bold text-white leading-tight">
                    WAIO-Ready: Direct Mapping
                  </span>
                  <p className="text-indigo-100 mt-1">
                    Semantic structure detected. Optimal clarity for bot extraction.
                  </p>
                </div>
              ) : (
                <div className="inline-block performance-badge-red px-8 py-4 rounded-2xl">
                  <span className="text-3xl lg:text-5xl font-bold text-white leading-tight">
                    WAIO is {(1 / result.comparison.cognitive_speedup).toFixed(1)}x slower
                  </span>
                  <p className="text-red-100 mt-1">
                    {Math.abs(result.comparison.performance_gain_percent).toFixed(1)}% increase in cognitive processing time
                  </p>
                </div>
              )}
            </div>
          )}

          {/* VS Split Screen */}
          <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-6 relative">
            {/* VS Divider (visible on large screens) */}
            <div className="hidden lg:block absolute left-1/2 top-0 bottom-0 w-8 -ml-4 flex items-center justify-center z-10">
              <div className="vs-divider h-full"></div>
              <div className="absolute bg-indigo-600 text-white font-bold px-3 py-2 rounded-full 
                              shadow-lg shadow-indigo-500/50">
                VS
              </div>
            </div>

            {/* Standard Extraction (Left) */}
            <div className="glass-card p-6 border-2 border-amber-500/30">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-3 h-3 rounded-full bg-amber-500 animate-pulse"></div>
                <h2 className="text-xl font-bold text-amber-400">Standard Extraction</h2>
                <span className="text-xs text-gray-500 ml-auto">Heuristic Algorithm</span>
              </div>

              <MetricsPanel 
                metrics={result.heuristic.metrics} 
                label="heuristic"
                highlightCognitive={true}
              />

              <div className="mt-6">
                <h3 className="text-sm font-semibold text-gray-400 mb-3">Extracted Content</h3>
                <ExtractionPanel extraction={result.heuristic.extraction} />
              </div>
            </div>

            {/* WAIO Extraction (Right) */}
            <div className="glass-card p-6 border-2 border-emerald-500/30">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></div>
                <h2 className="text-xl font-bold text-emerald-400">WAIO Extraction</h2>
                {!result.waio.extraction.waio_detected && (
                  <span className="text-[10px] bg-amber-500/10 text-amber-500 border border-amber-500/20 
                                 px-2 py-0.5 rounded uppercase font-bold tracking-tighter animate-pulse">
                    Standard Fallback
                  </span>
                )}
                <span className="text-xs text-gray-500 ml-auto">Semantic Lookup</span>
              </div>

              <div className={`transition-all duration-500 ${!result.waio.extraction.waio_detected ? 'opacity-40 grayscale pointer-events-none' : 'opacity-100'}`}>
                <MetricsPanel 
                  metrics={result.waio.metrics} 
                  label="waio"
                  highlightCognitive={true}
                  isWaio={true}
                />

                <div className="mt-6">
                  <h3 className="text-sm font-semibold text-gray-400 mb-3">Extracted Content</h3>
                  <ExtractionPanel 
                    extraction={result.waio.extraction} 
                    showAttributes={true}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Header Inspector Toggle */}
          <div className="max-w-4xl mx-auto mt-8">
            <button
              onClick={() => setShowHeaders(!showHeaders)}
              className="w-full glass-card p-4 flex items-center justify-between 
                         hover:border-indigo-500/50 transition-colors"
            >
              <span className="flex items-center gap-2 text-gray-300">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Request Headers Inspector
              </span>
              <svg 
                className={`w-5 h-5 text-gray-400 transition-transform ${showHeaders ? 'rotate-180' : ''}`} 
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {showHeaders && (
              <div className="headers-panel mt-2 p-4 rounded-lg overflow-x-auto">
                <p className="text-gray-400 mb-3">Headers sent by <span className="text-indigo-400">{result.bot_type}</span> simulation:</p>
                <table className="w-full">
                  <tbody>
                    {Object.entries(result.heuristic.metrics.headers_sent).map(([key, value]) => (
                      <tr key={key} className="border-b border-gray-800 last:border-0">
                        <td className="py-2 pr-4 text-indigo-400 whitespace-nowrap">{key}:</td>
                        <td className="py-2 text-gray-300 break-all">{value}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="text-center mt-16 text-gray-500 text-sm">
        <p>WAIO Crawler Tracker v1.0.0 — Proving the value of semantic HTML for AI</p>
      </footer>
    </div>
  );
}

// Metrics Panel Component
function MetricsPanel({ 
  metrics, 
  highlightCognitive = false,
  isWaio = false 
}: { 
  metrics: MetricsData; 
  label: string;
  highlightCognitive?: boolean;
  isWaio?: boolean;
}) {
  const formatTime = (ms: number) => {
    if (ms < 1) return `${(ms * 1000).toFixed(2)} μs`;
    if (ms < 1000) return `${ms.toFixed(2)} ms`;
    return `${(ms / 1000).toFixed(2)} s`;
  };

  const formatBytes = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="grid grid-cols-2 gap-4">
      <MetricCard 
        label="Network Time" 
        value={formatTime(metrics.network_time_ms)}
        icon="🌐"
      />
      <MetricCard 
        label="DOM Load Time" 
        value={formatTime(metrics.dom_load_time_ms)}
        icon="🏗️"
      />
      <MetricCard 
        label="Cognitive Time" 
        value={formatTime(metrics.cognitive_time_ms)}
        icon="🧠"
        highlight={highlightCognitive}
        isWaio={isWaio}
      />
      <MetricCard 
        label="Total Time" 
        value={formatTime(metrics.total_time_ms)}
        icon="⏱️"
      />
      <MetricCard 
        label="Response Size" 
        value={formatBytes(metrics.response_size_bytes)}
        icon="📦"
      />
      <MetricCard 
        label="Status Code" 
        value={metrics.status_code.toString()}
        icon="📡"
        status={metrics.status_code === 200}
      />
    </div>
  );
}

// Single Metric Card
function MetricCard({ 
  label, 
  value, 
  icon, 
  highlight = false,
  isWaio = false,
  status 
}: { 
  label: string; 
  value: string; 
  icon: string;
  highlight?: boolean;
  isWaio?: boolean;
  status?: boolean;
}) {
  return (
    <div className={`
      p-4 rounded-lg bg-black/30 border border-gray-800
      ${highlight && isWaio ? 'metric-glow border-emerald-500/50' : ''}
      ${highlight && !isWaio ? 'border-amber-500/30' : ''}
    `}>
      <div className="flex items-center gap-2 mb-1">
        <span className="text-lg">{icon}</span>
        <span className="text-xs text-gray-500 uppercase tracking-wide">{label}</span>
      </div>
      <div className={`text-xl font-bold ${
        highlight && isWaio ? 'text-emerald-400' : 
        highlight ? 'text-amber-400' : 
        status !== undefined ? (status ? 'text-emerald-400' : 'text-red-400') :
        'text-white'
      }`}>
        {value}
      </div>
    </div>
  );
}

// Extraction Panel Component
function ExtractionPanel({ 
  extraction, 
  showAttributes = false 
}: { 
  extraction: ExtractionData;
  showAttributes?: boolean;
}) {
  const getSourceBadge = (field: string) => {
    const source = extraction.sources?.[field];
    if (!source) return null;
    return (
      <span className={`text-[10px] px-1.5 py-0.5 rounded-full uppercase font-bold ml-2 ${
        source === 'waio' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 
        'bg-amber-500/20 text-amber-400 border border-amber-500/30'
      }`}>
        {source}
      </span>
    );
  };

  return (
    <div className="space-y-4">
      <div className="p-3 bg-black/30 rounded-lg group">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500 uppercase tracking-wide">Title</span>
          {getSourceBadge('title')}
        </div>
        <p className="text-white mt-1">{extraction.title || <span className="text-gray-600">Not found</span>}</p>
      </div>
      
      <div className="p-3 bg-black/30 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500 uppercase tracking-wide">Summary</span>
          {getSourceBadge('summary')}
        </div>
        <p className="text-white mt-1 text-sm">{extraction.summary || <span className="text-gray-600">Not found</span>}</p>
      </div>
      
      <div className="p-3 bg-black/30 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500 uppercase tracking-wide">Main Content Preview</span>
          {getSourceBadge('main_content')}
        </div>
        <p className="text-white mt-1 text-sm line-clamp-3">
          {extraction.main_content || <span className="text-gray-600">Not found</span>}
        </p>
      </div>

      {showAttributes && extraction.attributes_found && Object.keys(extraction.attributes_found).length > 0 && (
        <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
          <span className="text-xs text-emerald-400 uppercase tracking-wide font-bold">Semantic Mapping Report</span>
          <div className="mt-3 space-y-2 max-h-[250px] overflow-y-auto pr-2 custom-scrollbar">
            {Object.entries(extraction.attributes_found).map(([key, value]) => {
              const [tag, attr] = key.split(' ');
              return (
                <div key={key} className="flex flex-col border-b border-emerald-500/10 last:border-0 pb-2">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] text-emerald-500 font-mono bg-emerald-500/10 px-1 rounded">{tag}</span>
                    <code className="text-indigo-400 text-xs font-bold">{attr}</code>
                  </div>
                  <span className="text-gray-300 text-sm truncate pl-1" title={value}>{value}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
