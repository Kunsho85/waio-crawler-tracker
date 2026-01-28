"""
Extraction algorithms for the WAIO Crawler Tracker.
Implements both heuristic (trafilatura) and WAIO (data-ai-*) extraction methods.
"""
import time
from typing import Tuple, Optional
from bs4 import BeautifulSoup
import trafilatura
from lxml import html as lxml_html

from metrics import ExtractionResult, MetricTimer


class HeuristicExtractor:
    """
    Algorithm A: Simulates current bot behavior.
    Uses trafilatura and readability-like heuristics to guess content.
    This represents the HIGH CPU COST of understanding unstructured HTML.
    """
    
    def extract(self, html_content: str) -> Tuple[ExtractionResult, float]:
        """
        Extract content using heuristic methods.
        Returns extraction result and cognitive_time in seconds.
        """
        timer = MetricTimer()
        result = ExtractionResult()
        
        with timer:
            # Use trafilatura for main content extraction
            # This library performs extensive heuristic analysis:
            # - Text density calculation
            # - Tag scoring
            # - Boilerplate detection
            # - Language detection
            extracted = trafilatura.extract(
                html_content,
                include_comments=False,
                include_tables=True,
                no_fallback=False,
                favor_precision=True
            )
            
            if extracted:
                result.main_content = extracted
            
            # Parse with BeautifulSoup for additional extraction
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Title extraction (multiple fallback strategies)
            title = None
            
            # Try og:title first
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title['content']
            
            # Try twitter:title
            if not title:
                tw_title = soup.find('meta', attrs={'name': 'twitter:title'})
                if tw_title and tw_title.get('content'):
                    title = tw_title['content']
            
            # Fall back to <title> tag
            if not title:
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
            
            # Try h1 as last resort
            if not title:
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
            
            result.title = title
            
            # Summary extraction (description meta tags)
            summary = None
            
            # Try og:description
            og_desc = soup.find('meta', property='og:description')
            if og_desc and og_desc.get('content'):
                summary = og_desc['content']
            
            # Try meta description
            if not summary:
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    summary = meta_desc['content']
            
            # Try to extract from first paragraph if no summary found
            if not summary and result.main_content:
                # Take first 200 chars as summary
                summary = result.main_content[:200].strip()
                if len(result.main_content) > 200:
                    summary += "..."
            
            result.summary = summary
            
            # OPTIMIZED: Use a faster way to detect WAIO instead of slow soup.find_all with lambda
            # This ensures we don't penalize the Standard extractor's time measurement
            try:
                tree = lxml_html.fromstring(html_content)
                waio_nodes = tree.xpath('//*[@*[starts-with(name(), "data-ai-")]]')
                result.waio_detected = len(waio_nodes) > 0
            except:
                result.waio_detected = False

            # Set sources
            for field in ['title', 'summary', 'main_content']:
                if getattr(result, field):
                    result.sources[field] = 'heuristic'
        
        return result, timer.elapsed


class WAIOExtractor:
    """
    Algorithm B: Simulates optimized WAIO-aware bot behavior.
    Uses refined Weighted Semantic Scoping for deterministic content lookup.
    This represents the LOW CPU COST of deterministic extraction.
    """
    
    # Scoring Weights (Version 2.0)
    SCORE_CRITICAL = 100
    SCORE_MATCH_DIRECT = 100
    SCORE_MATCH_ENTITY = 50
    SCORE_SCOPE_MAIN = 50
    
    def __init__(self, heuristic_fallback: HeuristicExtractor):
        self.fallback = heuristic_fallback
    
    def extract(self, html_content: str, baseline_time: Optional[float] = None, 
                bot_type: str = "GPTBot", simulation_mode: str = "WAIO Theory") -> Tuple[ExtractionResult, float]:
        """
        Extract content using WAIO Weighted Scoping.
        Simulates proportional cost savings: Each field found via WAIO
        saves ~33% of the heuristic cognitive effort.
        
        Now includes Bot Preference Modifiers based on Simulation Mode.
        """
        from bot_preferences import BotType, SimulationMode, get_scoring_modifier
        
        timer = MetricTimer()
        result = ExtractionResult()
        result.waio_detected = False
        
        pool = {'title': [], 'summary': [], 'main_content': []}
        reasoning = {}

        # STEP 1: Cognitive Scan (Timed)
        with timer:
            try:
                tree = lxml_html.fromstring(html_content)
                all_ai_elements = tree.xpath('//*[@*[starts-with(name(), "data-ai-") or name()="data-importance"]]')
                
                if all_ai_elements:
                    result.waio_detected = True
                    
                    # O(N) Indexing
                    main_containers = tree.xpath('//main | //article | //*[@data-ai-entity-type="Main"] | //*[@data-ai-intent="article"]')
                    critical_containers = tree.xpath('//*[@data-importance="critical"]')
                    
                    main_elements_set = set()
                    for c in main_containers: main_elements_set.update(c.iter())
                    critical_elements_set = set()
                    for c in critical_containers: critical_elements_set.update(c.iter())

                    for element in all_ai_elements:
                        attrs = element.attrib
                        is_in_main = element in main_elements_set
                        base_score = self.SCORE_SCOPE_MAIN if is_in_main else 0
                        is_critical = attrs.get('data-importance') == 'critical' or element in critical_elements_set
                        if is_critical: base_score += self.SCORE_CRITICAL
                        
                        def get_val(attr_name):
                            v = attrs.get(attr_name)
                            return v.strip() if v and v.strip() else element.text_content().strip()

                        # Logic and Scoring
                        if 'data-ai-title' in attrs:
                            pool['title'].append((get_val('data-ai-title'), base_score + self.SCORE_MATCH_DIRECT, "Direct data-ai-title"))
                        elif 'data-ai-entity-type' in attrs and 'Title' in attrs['data-ai-entity-type']:
                            pool['title'].append((get_val('data-ai-entity-type'), base_score + self.SCORE_MATCH_ENTITY, "Entity Type match (Title)"))
                            
                        if any(k in attrs for k in ['data-ai-summary', 'data-ai-description']):
                            attr = 'data-ai-summary' if 'data-ai-summary' in attrs else 'data-ai-description'
                            pool['summary'].append((get_val(attr), base_score + self.SCORE_MATCH_DIRECT, f"Direct {attr}"))
                        elif 'data-ai-entity-type' in attrs and ('Summary' in attrs['data-ai-entity-type'] or 'Description' in attrs['data-ai-entity-type']):
                            pool['summary'].append((get_val('data-ai-entity-type'), base_score + self.SCORE_MATCH_ENTITY, "Entity Type match (Summary/Desc)"))

                        if any(k in attrs for k in ['data-ai-content', 'data-ai-main', 'data-ai-article']):
                            attr = next(k for k in ['data-ai-content', 'data-ai-main', 'data-ai-article'] if k in attrs)
                            pool['main_content'].append((get_val(attr), base_score + self.SCORE_MATCH_DIRECT, f"Direct {attr}"))
                        elif 'data-ai-entity-type' in attrs and ('Article' in attrs['data-ai-entity-type'] or 'Main' in attrs['data-ai-entity-type'] or 'Content' in attrs['data-ai-entity-type']):
                            pool['main_content'].append((get_val('data-ai-entity-type'), base_score + self.SCORE_MATCH_ENTITY, "Entity Type match (Article/Main)"))

                    # Selection
                    for f in pool:
                        if pool[f]:
                            pool[f].sort(key=lambda x: x[1], reverse=True)
                            best_val, best_score, best_reason = pool[f][0]
                            setattr(result, f, best_val)
                            result.sources[f] = 'waio'
                            reasoning[f] = f"{best_reason} (Score: {best_score})"
            except: pass

        # STEP 2: Cost Simulation (The Benchmark Logic)
        cognitive_overhead = timer.elapsed
        
        # Collect detected attributes for scoring modifier
        # We need to map Found Attributes -> Schema Types (simple heuristic map)
        found_attrs_map = {}
        if result.waio_detected:
            # Re-parse to get all data-ai attributes for preference matching
            try:
                tree = lxml_html.fromstring(html_content)
                all_ai = tree.xpath('//*[@*[starts-with(name(), "data-ai-")]]')
                for elem in all_ai:
                    for k, v in elem.attrib.items():
                        if k.startswith('data-ai-'): found_attrs_map[v] = k
            except: pass
            
        found_via_waio = sum(1 for s in result.sources.values() if s == 'waio')
        
        if baseline_time is not None:
            if found_via_waio == 0:
                # OPTION A: No WAIO benefit. Match baseline exactly.
                simulated_time = baseline_time
            else:
                # OPTION B: Proportional benefit + Bot Preference Modifier.
                
                # 1. Base Multiplier (Quantity of fields found)
                # Even if we find everything, there's a small cognitive floor (5%)
                # that represents the work of "confirming" the data.
                thinking_skipped_ratio = found_via_waio / 3.0
                remaining_effort_ratio = max(0.05, 1.0 - (thinking_skipped_ratio * 0.95))
                
                # 2. Score Modifier (Quality/Preference of fields found)
                # Does this bot LIKE what we found? 
                # A modifier > 1.0 means "Speedup". 
                try:
                    modifier = get_scoring_modifier(
                        BotType(bot_type), 
                        SimulationMode(simulation_mode), 
                        found_attributes=found_attrs_map
                    )
                    # Speedup reduces the TIME.
                    remaining_effort_ratio = remaining_effort_ratio / modifier
                except: 
                    pass 

                simulated_time = (baseline_time * remaining_effort_ratio) + cognitive_overhead
            
            # Ensure we don't return unrealistic zero (min 1ms floor)
            simulated_time = max(0.001, simulated_time)
            
            # Always get fallback data for missing fields
            if found_via_waio < 3:
                h_result, _ = self.fallback.extract(html_content)
                for f in ['title', 'summary', 'main_content']:
                    if not getattr(result, f):
                        val = getattr(h_result, f)
                        if val:
                            setattr(result, f, val)
                            result.sources[f] = 'heuristic'
        else:
            # No baseline provided, just use the raw measurement + heuristic fallback
            h_result, h_time = self.fallback.extract(html_content)
            simulated_time = cognitive_overhead + h_time
            for f in ['title', 'summary', 'main_content']:
                if not getattr(result, f):
                    setattr(result, f, getattr(h_result, f))
                    result.sources[f] = 'heuristic'

        # STEP 3: Report Generation (Metadata only)
        try:
            for f, reason in reasoning.items():
                result.attributes_found[f"Selected {f.replace('_', ' ').title()} via"] = reason
            tree = lxml_html.fromstring(html_content)
            all_ai = tree.xpath('//*[@*[starts-with(name(), "data-ai-") or name()="data-importance"]]')
            for elem in all_ai:
                for attr_name, attr_value in elem.attrib.items():
                    if attr_name.startswith('data-ai-') or attr_name == 'data-importance':
                        ui_key = f"<{elem.tag}> {attr_name}"
                        if ui_key not in result.attributes_found:
                            result.attributes_found[ui_key] = attr_value[:100]
        except: pass

        return result, simulated_time

# Singleton instances
heuristic_extractor = HeuristicExtractor()
waio_extractor = WAIOExtractor(heuristic_fallback=heuristic_extractor)

