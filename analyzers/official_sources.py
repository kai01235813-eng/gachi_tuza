from pydantic import BaseModel

class OfficialProjectLinks(BaseModel):
    symbol: str
    official_website: str
    x_twitter_url: str
    github_url: str

class OfficialSourceResolver:
    @staticmethod
    def get_links(symbol: str) -> OfficialProjectLinks:
        sym = symbol.upper().replace("KRW-", "").strip()

        links = {
            "BTC": ("https://bitcoin.org", "https://x.com/bitcoin", "https://github.com/bitcoin/bitcoin"),
            "ETH": ("https://ethereum.org", "https://x.com/ethereum", "https://github.com/ethereum/go-ethereum"),
            "SOL": ("https://solana.com", "https://x.com/solana", "https://github.com/solana-labs/solana"),
            "SAND": ("https://sandbox.game", "https://x.com/TheSandboxGame", "https://github.com/thesandboxgame"),
            "LINK": ("https://chain.link", "https://x.com/chainlink", "https://github.com/smartcontractkit/chainlink")
        }

        web, x_url, gh_url = links.get(sym, (f"https://{sym.lower()}.io", f"https://x.com/{sym.lower()}", f"https://github.com/crypto-{sym.lower()}"))

        return OfficialProjectLinks(
            symbol=sym,
            official_website=web,
            x_twitter_url=x_url,
            github_url=gh_url
        )
