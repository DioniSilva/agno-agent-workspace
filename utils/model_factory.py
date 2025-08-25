from typing import Any, Dict, Optional, Tuple, Callable



def _parse_model_string(model_str: Optional[str], default: str) -> Tuple[str, str]:
    """Parse model string allowing optional provider prefix.

    Examples:
        'gemini:gemini-2.5-pro' -> ('gemini', 'gemini-2.5-pro')
        'gemini-2.5-pro' -> ('gemini', 'gemini-2.5-pro')  # default provider
    """
    if not model_str:
        provider = default.split(":")[0] if ":" in default else "gemini"
        return provider, default
    if ":" in model_str:
        provider, mid = model_str.split(":", 1)
        return provider.lower(), mid
    # no provider prefix: assume gemini
    return "gemini", model_str


# Provider registry pattern
_PROVIDERS: Dict[str, Callable[[str, Dict[str, Any]], Any]] = {}


def register_provider(name: str):
    def _decorator(fn: Callable[[str, Dict[str, Any]], Any]):
        _PROVIDERS[name.lower()] = fn
        return fn

    return _decorator


def create_model(model_str: Optional[str], **kwargs) -> Any:
    """Create a provider-specific model object using the provider registry.

    To add support for a new provider, register a factory function with
    `register_provider("myprovider")` that accepts (model_id, kwargs) and
    returns a provider-specific model object.
    """
    default_model = "gemini:gemini-2.5-flash"
    provider, mid = _parse_model_string(model_str, default_model)
    factory = _PROVIDERS.get(provider)
    if not factory:
        raise NotImplementedError(f"Model provider not supported: {provider}")
    return factory(mid, kwargs)


# Built-in providers
@register_provider("gemini")
def _gemini_factory(mid: str, opts: Dict[str, Any]):
    try:
        from agno.models.google import Gemini

        allowed = {k: v for k, v in opts.items() if k in ("max_output_tokens", "temperature")}
        return Gemini(id=mid, **allowed)
    except Exception as exc:
        raise RuntimeError("Gemini model builder error: " + str(exc))


@register_provider("openai")
def _openai_factory(mid: str, opts: Dict[str, Any]):
    """Adapter that uses agno's OpenAI model wrapper when available.

    Tries a few likely import paths and raises a clear error if none are
    present so the user knows to install the appropriate `agno` extras or
    add an adapter.
    """
    tried = []
    candidates = [
        "agno.models.openai.OpenAI",
        "agno.models.openai.OpenAIModel",
        "agno.models.openai_api.OpenAI",
        "agno.models.openai_api.OpenAIModel",
    ]
    for path in candidates:
        modname, clsname = path.rsplit(".", 1)
        try:
            mod = __import__(modname, fromlist=[clsname])
            cls = getattr(mod, clsname)
            # pass only known kwargs; let the wrapper handle extras
            return cls(id=mid, **opts)
        except Exception as exc:
            tried.append(f"{path}: {type(exc).__name__}")

    raise NotImplementedError(
        "OpenAI provider via agno not available. Tried: " + ", ".join(tried)
        + ".\nIf you want OpenAI support, install the agno OpenAI adapter or provide a custom provider using register_provider('openai')."
    )

