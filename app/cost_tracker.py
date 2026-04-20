"""
Activity 7 - Neighborhood Knowledge Base: Token Usage & Cost Tracker
Track token usage across both search and chat API calls.
"""
import json
import os


def load_pricing(path: str | None = None) -> dict:
    """Load Azure OpenAI token pricing data.

    Args:
        path: Path to pricing.json. Defaults to data/pricing.json
              relative to the project root.

    Returns:
        Dict keyed by model name with input/output pricing per 1k tokens.
    """
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "pricing.json")
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# TODO: Step 6 - Implement cost calculation
# ---------------------------------------------------------------------------
def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    model: str = "gpt-4o",
    pricing: dict | None = None,
) -> float:
    """Calculate the dollar cost for a given number of tokens.

    Cost formula:
        cost = (prompt_tokens / 1000 * input_price_per_1k)
             + (completion_tokens / 1000 * output_price_per_1k)

    Args:
        prompt_tokens: Number of input/prompt tokens.
        completion_tokens: Number of output/completion tokens.
        model: Model name to look up in pricing data (default "gpt-4o").
        pricing: Optional pricing dict. If None, loads from data/pricing.json.

    Returns:
        Float representing the cost in US dollars.

    Raises:
        KeyError: If the model name is not found in pricing data.
    """
    # TODO: Step 6 - Implement cost calculation
    #   1. Load pricing data if not provided (use load_pricing())
    #   2. Look up the model's input and output prices
    #   3. Apply the cost formula
    #   4. Return the dollar amount as a float
    raise NotImplementedError("Implement calculate_cost in Step 6")


class CostTracker:
    """Tracks cumulative token usage and cost across multiple API calls.

    Usage:
        tracker = CostTracker(model="gpt-4o")
        tracker.record(prompt_tokens=500, completion_tokens=200)
        tracker.record(prompt_tokens=480, completion_tokens=180)
        print(tracker.summary())
    """

    def __init__(self, model: str = "gpt-4o"):
        """Initialize the cost tracker.

        Args:
            model: The model name for pricing lookups.
        """
        self.model = model
        # TODO: Step 6 - Initialize tracking variables:
        #   self.total_prompt_tokens = 0
        #   self.total_completion_tokens = 0
        #   self.total_cost = 0.0
        #   self.call_count = 0
        #   self._pricing = load_pricing()
        raise NotImplementedError("Implement CostTracker.__init__ in Step 6")

    def record(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Record token usage from one API call and return its cost.

        Args:
            prompt_tokens: Number of input tokens for this call.
            completion_tokens: Number of output tokens for this call.

        Returns:
            Float cost in dollars for this single call.
        """
        # TODO: Step 6 - Implement recording
        #   1. Calculate cost for this call using calculate_cost()
        #   2. Add tokens to running totals
        #   3. Add cost to running total
        #   4. Increment call_count
        #   5. Return the cost of this single call
        raise NotImplementedError("Implement CostTracker.record in Step 6")

    def summary(self) -> dict:
        """Return a summary of all tracked costs.

        Returns:
            Dict with keys: model, call_count, total_prompt_tokens,
            total_completion_tokens, total_tokens, total_cost,
            avg_cost_per_call.
        """
        # TODO: Step 6 - Implement summary
        #   1. Calculate averages (handle zero call_count)
        #   2. Return the summary dict
        raise NotImplementedError("Implement CostTracker.summary in Step 6")
