"""
Metrics collection for benchmark engine.
Captures network_time, dom_load_time, and cognitive_time.
"""
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from contextlib import contextmanager


@dataclass
class ExtractionResult:
    """Results from content extraction."""
    title: Optional[str] = None
    summary: Optional[str] = None
    main_content: Optional[str] = None
    waio_detected: bool = False
    attributes_found: Dict[str, str] = field(default_factory=dict)
    # Track which fields came from where: 'waio' or 'heuristic'
    sources: Dict[str, str] = field(default_factory=dict)
    
    @property
    def integrity_score(self) -> float:
        """Percentage of core fields found via WAIO."""
        core_fields = ['title', 'summary', 'main_content']
        waio_fields = sum(1 for f in core_fields if self.sources.get(f) == 'waio')
        return (waio_fields / len(core_fields)) * 100


@dataclass
class BenchmarkMetrics:
    """Container for all benchmark timing metrics."""
    network_time: float = 0.0  # Time to download raw bytes
    dom_load_time: float = 0.0  # Time to parse into DOM tree
    cognitive_time: float = 0.0  # Time to extract meaning
    
    # Additional metadata
    response_size: int = 0
    status_code: int = 0
    headers_sent: Dict[str, str] = field(default_factory=dict)
    
    @property
    def total_time(self) -> float:
        """Total time for the complete operation."""
        return self.network_time + self.dom_load_time + self.cognitive_time
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "network_time_ms": round(self.network_time * 1000, 2),
            "dom_load_time_ms": round(self.dom_load_time * 1000, 2),
            "cognitive_time_ms": round(self.cognitive_time * 1000, 2),
            "total_time_ms": round(self.total_time * 1000, 2),
            "response_size_bytes": self.response_size,
            "status_code": self.status_code,
            "headers_sent": self.headers_sent
        }


@dataclass 
class ComparisonResult:
    """Complete comparison between heuristic and WAIO extraction."""
    url: str
    bot_type: str
    
    # Heuristic (Standard) results
    heuristic_metrics: BenchmarkMetrics = field(default_factory=BenchmarkMetrics)
    heuristic_extraction: ExtractionResult = field(default_factory=ExtractionResult)
    
    # WAIO results  
    waio_metrics: BenchmarkMetrics = field(default_factory=BenchmarkMetrics)
    waio_extraction: ExtractionResult = field(default_factory=ExtractionResult)
    
    @property
    def cognitive_speedup(self) -> float:
        """Calculate how much faster WAIO is for cognitive extraction."""
        if self.waio_metrics.cognitive_time == 0:
            return 0.0
        return self.heuristic_metrics.cognitive_time / self.waio_metrics.cognitive_time
    
    @property
    def performance_gain_percent(self) -> float:
        """Percentage improvement in cognitive time."""
        if self.heuristic_metrics.cognitive_time == 0:
            return 0.0
        reduction = self.heuristic_metrics.cognitive_time - self.waio_metrics.cognitive_time
        return (reduction / self.heuristic_metrics.cognitive_time) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "bot_type": self.bot_type,
            "heuristic": {
                "metrics": self.heuristic_metrics.to_dict(),
                "extraction": {
                    "title": self.heuristic_extraction.title,
                    "summary": self.heuristic_extraction.summary,
                    "main_content": self.heuristic_extraction.main_content[:500] if self.heuristic_extraction.main_content else None,
                    "waio_detected": self.heuristic_extraction.waio_detected,
                    "sources": self.heuristic_extraction.sources
                }
            },
            "waio": {
                "metrics": self.waio_metrics.to_dict(),
                "extraction": {
                    "title": self.waio_extraction.title,
                    "summary": self.waio_extraction.summary,
                    "main_content": self.waio_extraction.main_content[:500] if self.waio_extraction.main_content else None,
                    "waio_detected": self.waio_extraction.waio_detected,
                    "attributes_found": self.waio_extraction.attributes_found,
                    "sources": self.waio_extraction.sources,
                    "integrity_score": round(self.waio_extraction.integrity_score, 1)
                }
            },
            "comparison": {
                "cognitive_speedup": round(self.cognitive_speedup, 2),
                "performance_gain_percent": round(self.performance_gain_percent, 2),
                "waio_framework_detected": self.waio_extraction.waio_detected,
                "bot_intent": "AI Search / Extraction" # Default, can be overridden in main.py if needed
            }
        }


class MetricTimer:
    """Context manager for precise timing measurements."""
    
    def __init__(self):
        self.start_time: float = 0
        self.end_time: float = 0
        self.elapsed: float = 0
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time


@contextmanager
def measure_time():
    """Simple context manager that yields elapsed time."""
    timer = MetricTimer()
    with timer:
        yield timer
