# import pytest (removed for standalone execution)
from bot_preferences import BotType, SimulationMode, get_scoring_modifier

def test_waio_theory_scoring():
    """Test that WAIO Theory applies the correct bonus for preferred content."""
    # GPTBot loves FAQPage
    found = {"data-ai-entity-type": "FAQPage"}
    
    modifier = get_scoring_modifier(
        BotType.GPTBOT, 
        SimulationMode.WAIO_THEORY, 
        found_attributes=found
    )
    
    # 1.2 (Base) * 1.4 (Preference) = 1.68
    assert modifier > 1.6
    assert modifier < 1.7

def test_industry_standard_scoring():
    """Test that Industry Standard applies minimal/no bonus."""
    found = {"data-ai-entity-type": "FAQPage"}
    
    modifier = get_scoring_modifier(
        BotType.GPTBOT, 
        SimulationMode.INDUSTRY_STANDARD, 
        found_attributes=found
    )
    
    # 1.0 (Base) * 1.1 (Preference) = 1.1
    assert modifier == 1.1

def test_unpreferred_content():
    """Test scoring for content the bot does not prioritize."""
    # GPTBot doesn't care about 'LocalBusiness' in our profile
    found = {"data-ai-entity-type": "LocalBusiness"}
    
    modifier_waio = get_scoring_modifier(
        BotType.GPTBOT, 
        SimulationMode.WAIO_THEORY, 
        found_attributes=found
    )
    
    # 1.2 (Base) * 1.0 (No pref) = 1.2
    assert modifier_waio == 1.2

if __name__ == "__main__":
    # Simple manual run if pytest isn't available in env
    test_waio_theory_scoring()
    test_industry_standard_scoring()
    test_unpreferred_content()
    print("All tests passed!")
