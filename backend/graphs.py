import io, base64, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def generate_graph(expression: str) -> str | None:
    if not expression:
        return None
    # ponytail: only handles basic y=... plots; no eval, uses simple parser
    expr = expression.strip()
    if not expr.startswith("y="):
        return None
    try:
        x = np.linspace(-10, 10, 400)
        safe_expr = expr[2:].replace("^", "**")
        safe_expr = re.sub(r'(?<!\w)sin\(', 'np.sin(', safe_expr)
        safe_expr = re.sub(r'(?<!\w)cos\(', 'np.cos(', safe_expr)
        safe_expr = re.sub(r'(?<!\w)tan\(', 'np.tan(', safe_expr)
        safe_expr = re.sub(r'(?<!\w)sqrt\(', 'np.sqrt(', safe_expr)
        safe_expr = re.sub(r'(?<!\w)pi\b', 'np.pi', safe_expr)
        y = eval(safe_expr, {"np": np, "x": x, "__builtins__": {}})
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.axhline(0, color='gray', lw=0.5)
        ax.axvline(0, color='gray', lw=0.5)
        ax.set_xlabel("x"); ax.set_ylabel("y")
        ax.grid(True, alpha=0.3)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None
