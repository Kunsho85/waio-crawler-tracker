import pytest
from extractors import waio_extractor, heuristic_extractor

def test_weighted_scoping_title():
    html = """
    <html>
        <body>
            <nav>
                <span data-ai-title="Wrong Title">Sidebar Title</span>
            </nav>
            <main>
                <h1 data-ai-title="Correct Title">Main Title</h1>
            </main>
        </body>
    </html>
    """
    result, _ = waio_extractor.extract(html)
    assert result.title == "Correct Title"
    assert "Selected Title via" in result.attributes_found
    assert "Score: 150" in result.attributes_found["Selected Title via"]

def test_importance_boost():
    html = """
    <html>
        <body>
            <div data-ai-title="Standard">Title 1</div>
            <div data-ai-title="Critical" data-importance="critical">Title 2</div>
        </body>
    </html>
    """
    result, _ = waio_extractor.extract(html)
    assert result.title == "Critical"
    assert "Score: 200" in result.attributes_found["Selected Title via"]

def test_entity_type_fallback():
    html = """
    <html>
        <body>
            <div data-ai-entity-type="Title">Entity Title</div>
            <div data-ai-title="Direct Title">Direct Title</div>
        </body>
    </html>
    """
    result, _ = waio_extractor.extract(html)
    assert result.title == "Direct Title"
    assert "Direct data-ai-title" in result.attributes_found["Selected Title via"]

def test_scoping_containers():
    for tag in ["main", "article"]:
        html = f"""
        <html>
            <{tag}>
                <h1 data-ai-title="In Scope">Title</h1>
            </{tag}>
            <div data-ai-title="Out of Scope">Outside</div>
        </html>
        """
        result, _ = waio_extractor.extract(html)
        assert result.title == "In Scope", f"Failed for tag {tag}"

def test_data_ai_intent_scoping():
    html = """
    <div data-ai-intent="article">
        <h1 data-ai-title="Scoped Title">Title</h1>
    </div>
    <div data-ai-title="Unscoped Title">Other</div>
    """
    result, _ = waio_extractor.extract(html)
    assert result.title == "Scoped Title"

def test_deterministic_reasoning_in_report():
    html = """
    <main data-importance="critical">
        <h1 data-ai-title="Main Title">Target</h1>
    </main>
    """
    result, _ = waio_extractor.extract(html)
    # 50 (main) + 100 (critical) + 100 (direct) = 250
    assert "Score: 250" in result.attributes_found["Selected Title via"]
