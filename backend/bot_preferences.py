"""
Bot Preferences and Simulation Modes.
Defines how different bots prioritize content and how simulation modes affect scoring.
"""
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field

class SimulationMode(str, Enum):
    """
    Comparison modes for the simulator.
    """
    WAIO_THEORY = "WAIO Theory"
    INDUSTRY_STANDARD = "Industry Consensus"

class BotType(str, Enum):
    """
    Supported bot types (must match bot_factory.py).
    """
    GPTBOT = "GPTBot"
    CLAUDEBOT = "ClaudeBot"
    CHATGPT_USER = "ChatGPT-User"
    GOOGLEBOT = "Googlebot"
    GOOGLE_EXTENDED = "Google-Extended"
    BINGBOT = "Bingbot"
    PERPLEXITY = "PerplexityBot"
    YOUBOT = "YouBot"
    META = "MetaBot"

@dataclass
class BotPreferenceProfile:
    """
    Defines which Schema.org types a specific bot prioritizes.
    Based on WAIO Microdata Priority Matrix.
    """
    file_types: List[str] = field(default_factory=list) # e.g. ["FAQPage", "Article"]
    attributes: List[str] = field(default_factory=list) # e.g. ["datePublished"]
    
    # Modifier for standard (non-WAIO) heuristic matches
    heuristic_penalty: float = 1.0 

# Profile Definitions from Priority Matrix
BOT_PROFILES: Dict[BotType, BotPreferenceProfile] = {
    BotType.GPTBOT: BotPreferenceProfile(
        file_types=["FAQPage", "Article", "Product"],
        attributes=["mainEntity", "acceptedAnswer"]
    ),
    BotType.CLAUDEBOT: BotPreferenceProfile(
        file_types=["Article", "FAQPage", "Review"],
        attributes=["author", "datePublished"]
    ),
    BotType.PERPLEXITY: BotPreferenceProfile(
        file_types=["Article", "FAQPage", "Review"],
        attributes=["citation", "breadcrumb"]
    ),
    BotType.GOOGLE_EXTENDED: BotPreferenceProfile(
        file_types=["FAQPage", "Article", "Review", "Product"],
        attributes=[]
    ),
    BotType.BINGBOT: BotPreferenceProfile(
        file_types=["Product", "LocalBusiness", "Review"],
        attributes=["offers", "price"]
    ),
    # Default fallback for others
    BotType.GOOGLEBOT: BotPreferenceProfile(),
    BotType.CHATGPT_USER: BotPreferenceProfile(),
    BotType.YOUBOT: BotPreferenceProfile(),
    BotType.META: BotPreferenceProfile(),
}

def get_scoring_modifier(
    bot_type: BotType, 
    simulation_mode: SimulationMode,
    found_attributes: Dict[str, str] = None
) -> float:
    """
    Calculates the 'Cognitive Speedup Multiplier' based on the simulation mode.
    
    Args:
        bot_type: The bot being simulated.
        simulation_mode: WAIO_THEORY vs INDUSTRY_STANDARD.
        found_attributes: Dictionary of attributes/schemas found in the HTML.
    
    Returns:
        float: A multiplier for the WAIO speedup score (e.g. 1.0 = normal, 1.5 = 50% faster).
    """
    base_modifier = 1.0
    
    if found_attributes is None:
        return base_modifier

    # Convert found keys to lower for fuzzy matching
    found_keys = " ".join(found_attributes.keys()).lower()
    found_values = " ".join(found_attributes.values()).lower()
    
    profile = BOT_PROFILES.get(bot_type, BOT_PROFILES[BotType.GPTBOT])
    
    # Check if the page contains content the bot loves
    has_preferred_content = False
    for schema in profile.file_types:
        if schema.lower() in found_keys or schema.lower() in found_values:
            has_preferred_content = True
            break
            
    # --- Mode A: WAIO Theory ---
    # Premise: Microdata is parsed significantly faster because it's in the DOM tree.
    # Premise: Bots have STRONG preferences and will "skip" non-preferred content faster if structured data exists.
    if simulation_mode == SimulationMode.WAIO_THEORY:
        # Bonus 1: Microdata Existence (The "Fast Parse" bonus)
        # Any WAIO/Microdata usage gets a small boost just for being explicit
        base_modifier *= 1.2
        
        # Bonus 2: Bot Preference Match (The "Priority Matrix" bonus)
        if has_preferred_content:
            base_modifier *= 1.4 # Stacks with base, total ~1.68x
            
    # --- Mode B: Industry Consensus ---
    # Premise: JSON-LD is preferred or equal. Microdata has no speed advantage.
    # Premise: Bots are general purpose; preferences exist but aren't dramatic filters.
    elif simulation_mode == SimulationMode.INDUSTRY_STANDARD:
        # No "Fast Parse" bonus for Microdata alone (assumes JSON-LD is just as fast)
        base_modifier = 1.0
        
        # Small preference bonus (bots still like structured data, just less dramatic extraction difference)
        if has_preferred_content:
            base_modifier *= 1.1

    return base_modifier
