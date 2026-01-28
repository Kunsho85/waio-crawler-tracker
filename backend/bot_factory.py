"""
Bot Factory for simulating different AI crawler behaviors.
Implements static bots (curl_cffi) and dynamic bots (Playwright).
"""
import asyncio
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from curl_cffi import requests as curl_requests
from bs4 import BeautifulSoup

from metrics import BenchmarkMetrics, MetricTimer


class BotType(str, Enum):
    """Supported bot types for simulation."""
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
class BotConfig:
    """Configuration for a specific bot."""
    name: str
    user_agent: str
    is_dynamic: bool = False  # True = uses Playwright
    extra_headers: Dict[str, str] = None
    tls_fingerprint: str = "chrome"  # curl_cffi fingerprint
    
    def __post_init__(self):
        if self.extra_headers is None:
            self.extra_headers = {}


# Bot configurations based on real-world user agents
BOT_CONFIGS: Dict[BotType, BotConfig] = {
    BotType.GPTBOT: BotConfig(
        name="GPTBot",
        user_agent="Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)",
        is_dynamic=False,
        extra_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        },
        tls_fingerprint="chrome120"
    ),
    BotType.CLAUDEBOT: BotConfig(
        name="ClaudeBot",
        user_agent="Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +https://www.anthropic.com/claude-bot)",
        is_dynamic=False,
        extra_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
        },
        tls_fingerprint="chrome120"
    ),
    BotType.CHATGPT_USER: BotConfig(
        name="ChatGPT-User",
        user_agent="Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ChatGPT-User/1.0; +https://openai.com/bot)",
        is_dynamic=True,  # Uses Playwright for JS execution
        extra_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    ),
    BotType.GOOGLEBOT: BotConfig(
        name="Googlebot",
        user_agent="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        is_dynamic=False,
        extra_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
        },
        tls_fingerprint="chrome"
    ),
    BotType.GOOGLE_EXTENDED: BotConfig(
        name="Google-Extended",
        user_agent="Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Google-Extended)",
        is_dynamic=False,
        extra_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
        },
        tls_fingerprint="chrome"
    ),
    BotType.BINGBOT: BotConfig(
        name="Bingbot",
        user_agent="Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        is_dynamic=False,
        extra_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        tls_fingerprint="edge"
    ),
    BotType.PERPLEXITY: BotConfig(
        name="PerplexityBot",
        user_agent="Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://www.perplexity.ai/proximity)",
        is_dynamic=False,
        extra_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        tls_fingerprint="chrome110"
    ),
    BotType.YOUBOT: BotConfig(
        name="YouBot",
        user_agent="Mozilla/5.0 (compatible; YouBot/1.0; +https://you.com/static/gethelp/developers/bot)",
        is_dynamic=False,
        tls_fingerprint="chrome"
    ),
    BotType.META: BotConfig(
        name="MetaBot",
        user_agent="facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
        is_dynamic=False,
        tls_fingerprint="chrome"
    ),
}


class BotFactory:
    """
    Factory for creating and running bot simulations.
    Handles both static (curl_cffi) and dynamic (Playwright) bots.
    """
    
    def __init__(self):
        self._playwright = None
        self._browser = None
    
    async def _ensure_playwright(self):
        """Lazy initialization of Playwright browser."""
        if self._playwright is None:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
    
    async def close(self):
        """Clean up Playwright resources."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
    
    def get_bot_config(self, bot_type: BotType) -> BotConfig:
        """Get configuration for a specific bot type."""
        return BOT_CONFIGS.get(bot_type, BOT_CONFIGS[BotType.GPTBOT])
    
    async def fetch_page(self, url: str, bot_type: BotType) -> Tuple[str, BenchmarkMetrics]:
        """
        Fetch a page using the specified bot simulation.
        Returns HTML content and metrics.
        """
        config = self.get_bot_config(bot_type)
        metrics = BenchmarkMetrics()
        
        # Store headers that will be sent
        headers = {
            "User-Agent": config.user_agent,
            **config.extra_headers
        }
        metrics.headers_sent = headers
        
        if config.is_dynamic:
            html, metrics = await self._fetch_dynamic(url, config, metrics)
        else:
            html, metrics = await self._fetch_static(url, config, metrics)
        
        return html, metrics
    
    async def _fetch_static(self, url: str, config: BotConfig, metrics: BenchmarkMetrics) -> Tuple[str, BenchmarkMetrics]:
        """
        Fetch page using curl_cffi for static bot simulation.
        Mimics TLS fingerprints of real browsers/bots.
        """
        headers = {
            "User-Agent": config.user_agent,
            **config.extra_headers
        }
        
        # Network time measurement
        network_timer = MetricTimer()
        with network_timer:
            try:
                response = curl_requests.get(
                    url,
                    headers=headers,
                    impersonate=config.tls_fingerprint,
                    timeout=30,
                    allow_redirects=True
                )
                html = response.text
                metrics.status_code = response.status_code
                metrics.response_size = len(response.content)
            except Exception as e:
                raise Exception(f"Failed to fetch {url}: {str(e)}")
        
        metrics.network_time = network_timer.elapsed
        
        # DOM parsing time measurement
        dom_timer = MetricTimer()
        with dom_timer:
            # Parse to verify valid HTML (this is the DOM load cost)
            soup = BeautifulSoup(html, 'lxml')
            _ = soup.find('body')  # Force parse
        
        metrics.dom_load_time = dom_timer.elapsed
        
        return html, metrics
    
    async def _fetch_dynamic(self, url: str, config: BotConfig, metrics: BenchmarkMetrics) -> Tuple[str, BenchmarkMetrics]:
        """
        Fetch page using Playwright for dynamic bot simulation.
        Includes JavaScript hydration time in dom_load_time.
        """
        await self._ensure_playwright()
        
        context = await self._browser.new_context(
            user_agent=config.user_agent,
            extra_http_headers=config.extra_headers
        )
        page = await context.new_page()
        
        try:
            # Combined network + DOM loading with JS execution
            network_timer = MetricTimer()
            with network_timer:
                response = await page.goto(url, wait_until='domcontentloaded')
                metrics.status_code = response.status if response else 0
            
            metrics.network_time = network_timer.elapsed
            
            # Wait for JS hydration (this is unique to dynamic bots)
            dom_timer = MetricTimer()
            with dom_timer:
                await page.wait_for_load_state('networkidle')
                html = await page.content()
                metrics.response_size = len(html.encode('utf-8'))
            
            metrics.dom_load_time = dom_timer.elapsed
            
        finally:
            await context.close()
        
        return html, metrics


# Global factory instance
bot_factory = BotFactory()
