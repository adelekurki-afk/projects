"""Wrap Hex APP CODE cells so a missing SQL dataframe cannot red-error the App."""

PREFIX = '''import plotly.graph_objects as go
try:
    from IPython.display import display
except ImportError:
    def display(obj):
        return obj

def _itl_empty(msg="Run all, then refresh the App."):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(size=14, color="#6B7280"))
    fig.update_layout(
        height=220,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(t=20, b=20, l=20, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
    )
    return fig

def _itl_ready(*names):
    return all(name in globals() for name in names)

'''


def _indent(source: str, n: int) -> str:
    pad = " " * n
    lines = []
    for line in source.splitlines():
        lines.append(pad + line if line.strip() else "")
    return "\n".join(lines)


def wrap_last_fig(source: str, names: list[str]) -> str:
    names_lit = ", ".join(repr(n) for n in names)
    return (
        PREFIX
        + f"if not _itl_ready({names_lit}):\n"
        + "    fig = _itl_empty()\n"
        + "else:\n"
        + "    try:\n"
        + _indent(source, 8)
        + "\n"
        + "    except Exception as e:\n"
        + '        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")\n'
        + "fig\n"
    )


def wrap_display(source: str, names: list[str]) -> str:
    names_lit = ", ".join(repr(n) for n in names)
    return (
        PREFIX
        + f"if not _itl_ready({names_lit}):\n"
        + "    display(_itl_empty())\n"
        + "else:\n"
        + "    try:\n"
        + _indent(source, 8)
        + "\n"
        + "    except Exception as e:\n"
        + '        display(_itl_empty("Run all first (" + type(e).__name__ + ")"))\n'
    )
