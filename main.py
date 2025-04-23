import feedparser
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport

mcp = FastMCP(
    name="bbc_news_mcp_server_demo",
    description="An example MCP Server utilising FastMCP and feedparser to inject BBC articles into Claude Desktop"
)

RSS_URL = "https://feeds.bbci.co.uk/news/rss.xml"

@mcp.tool()
async def get_n_article_titles_and_links_from_bbc_news(limit: int = 5) -> str:
    feed = feedparser.parse(RSS_URL)
    entries = feed.entries[:limit]
    return "\n".join(f"{e.title} — {e.link}" for e in entries)

transport = SseServerTransport("/sse/")

async def app(scope, receive, send):
    async with transport.connect_sse(scope, receive, send):
        await mcp._mcp_server.run(
            send,
            receive,
            mcp._mcp_server.create_initialization_options()
        )
    return