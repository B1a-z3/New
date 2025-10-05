from typing import List, Dict
from ..graph import Message

_DATA: Dict[str, Dict[str, str]] = {
    "math": {
        "Central Limit Theorem": "Sample means approach normality as n grows.",
        "Law of Large Numbers": "Sample average converges to expected value.",
    },
    "stats": {
        "p-value": "Probability of data as extreme under null hypothesis.",
        "Confidence Interval": "Range likely containing true parameter.",
    },
    "ml": {
        "Bias-Variance Tradeoff": "Balance under/overfitting by model complexity.",
        "Cross-Validation": "Estimate generalization via data resampling.",
        "Gradient Descent": "Iteratively minimize loss via gradients.",
    },
}


def search_snippets(query: str, domains: List[str]) -> List[Dict[str, str]]:
    query_lower = query.lower()
    results: List[Dict[str, str]] = []
    for domain in domains:
        for title, summary in _DATA.get(domain, {}).items():
            if query_lower in title.lower() or query_lower in summary.lower():
                results.append({
                    "domain": domain,
                    "title": title,
                    "summary": summary,
                })
    if not results:
        # return top items if nothing matched
        for domain in domains:
            for title, summary in list(_DATA.get(domain, {}).items())[:3]:
                results.append({
                    "domain": domain,
                    "title": title,
                    "summary": summary,
                })
    return results
