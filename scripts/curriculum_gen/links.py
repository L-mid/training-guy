def links_for_tier(tier_n: int) -> list[dict[str, str]]:
    """
    Fallback docs links if config does not specify docs_links.

    Returned format:
      [{"label": "...", "url": "..."}, ...]
    """
    if tier_n <= 4:
        return [
            {"label": "Python Tutorial", "url": "https://docs.python.org/3/tutorial/"},
            {"label": "Built-in Functions", "url": "https://docs.python.org/3/library/functions.html"},
        ]
    if tier_n == 5:
        return [
            {"label": "Git Reference", "url": "https://git-scm.com/docs"},
            {"label": "Pro Git (free book)", "url": "https://git-scm.com/book/en/v2"},
        ]
    if tier_n == 6:
        return [
            {"label": "pathlib", "url": "https://docs.python.org/3/library/pathlib.html"},
            {"label": "csv", "url": "https://docs.python.org/3/library/csv.html"},
            {"label": "json", "url": "https://docs.python.org/3/library/json.html"},
        ]
    if tier_n == 7:
        return [{"label": "pytest docs", "url": "https://docs.pytest.org/en/stable/"}]
    if tier_n == 8:
        return [{"label": "Python turtle", "url": "https://docs.python.org/3/library/turtle.html"}]
    if tier_n == 9:
        return [
            {"label": "Luau docs", "url": "https://create.roblox.com/docs/luau"},
            {"label": "Luau control structures", "url": "https://create.roblox.com/docs/luau/control-structures"},
            {"label": "Luau functions", "url": "https://create.roblox.com/docs/luau/functions"},
        ]
    if tier_n == 10:
        return [
            {"label": "Roblox scripting docs", "url": "https://create.roblox.com/docs/scripting"},
            {
                "label": "Intro to scripting (tutorial)",
                "url": "https://create.roblox.com/docs/tutorials/use-case-tutorials/scripting/basic-scripting/intro-to-scripting",
            },
            {"label": "Luau docs", "url": "https://create.roblox.com/docs/luau"},
        ]
    return []
