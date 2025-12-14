import os
import sys
import tempfile

# ==========================================================
# 1) IMPORTANT: Fix Tcl/Tk when frozen (PyInstaller EXE)
#    Must run BEFORE importing tkinter.
# ==========================================================
import os, sys

import os, sys
import os, sys

import os, sys

def _sanitize_path(remove_keywords):
    parts = os.environ.get("PATH", "").split(os.pathsep)
    keep = []
    for p in parts:
        lp = p.lower()
        if any(k in lp for k in remove_keywords):
            continue
        keep.append(p)
    os.environ["PATH"] = os.pathsep.join(keep)

def _fix_runtime_paths():
    # Clear any global overrides that may point to old Tcl
    for k in ("TCL_LIBRARY", "TK_LIBRARY", "TCLLIBPATH"):
        os.environ.pop(k, None)

    # If running as EXE (PyInstaller)
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS

        # Remove any old Tcl/Tk paths (like tcl8.6.10) from PATH
        _sanitize_path(["tcl8.6.10", "tk8.6.10", "tcl", "tk"])

        # Force Tcl/Tk scripts from our bundled folders
        os.environ["TCL_LIBRARY"] = os.path.join(base, "tcl", "tcl8.6")
        os.environ["TK_LIBRARY"]  = os.path.join(base, "tcl", "tk8.6")

        # Force DLL loading priority: put our app folder first
        os.environ["PATH"] = base + os.pathsep + os.environ.get("PATH", "")

_fix_runtime_paths()


def _fix_tcl_tk_for_pyinstaller():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
        os.environ["TCL_LIBRARY"] = os.path.join(base, "tcl", "tcl8.6")
        os.environ["TK_LIBRARY"]  = os.path.join(base, "tcl", "tk8.6")

_fix_tcl_tk_for_pyinstaller()
import os, sys

def ensure_dot_available():
    # EXE mode: use bundled Graphviz
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        gv_bin = os.path.join(sys._MEIPASS, "_third_party", "graphviz", "bin")
        os.environ["PATH"] = gv_bin + os.pathsep + os.environ.get("PATH", "")
        dot = os.path.join(gv_bin, "dot.exe")
        return os.path.exists(dot)

    # DEV mode: rely on system Graphviz
    return True

import tkinter as tk

def _find_dir(root: str, target_name: str) -> str | None:
    """Find a directory named target_name somewhere under root."""
    for base, dirs, _files in os.walk(root):
        if target_name in dirs:
            return os.path.join(base, target_name)
    return None

def ensure_tcl_tk_runtime_for_exe():
    """
    Fixes:
      - Can't find a usable init.tcl
      - Tcl version conflict (8.6.10 vs 8.6.15)
    by forcing Tcl/Tk to use the packaged folders inside sys._MEIPASS.
    """
    if not getattr(sys, "frozen", False):
        return

    base = getattr(sys, "_MEIPASS", None)
    if not base or not os.path.isdir(base):
        return

    # Look for tcl8.6 and tk8.6 inside the bundle (exact subfolder may vary)
    tcl_dir = _find_dir(base, "tcl8.6")
    tk_dir  = _find_dir(base, "tk8.6")

    if tcl_dir:
        os.environ["TCL_LIBRARY"] = tcl_dir
    if tk_dir:
        os.environ["TK_LIBRARY"] = tk_dir

    # Remove possible conflicting env vars that point to other Tcl/Tk installs
    os.environ.pop("TCLLIBPATH", None)

# Must be called BEFORE tkinter import
ensure_tcl_tk_runtime_for_exe()

import tkinter as tk
from tkinter import messagebox, filedialog

# Optional deps
try:
    import graphviz
except Exception:
    graphviz = None

try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

import scanner_4
from parser_core import build_ast_from_token_dicts, ParserError, ASTNode


# ==========================================================
# 2) Graphviz PATH handling (Bundled + Installed)
# ==========================================================

def ensure_graphviz_path():
    """
    Ensures dot.exe is discoverable.

    - EXE (PyInstaller): uses bundled:
        <MEIPASS>/_third_party/graphviz/bin

    - DEV: tries installed Graphviz:
        C:\\Program Files\\Graphviz\\bin
    """
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
        gv_bin = os.path.join(base, "_third_party", "graphviz", "bin")
        if os.path.isdir(gv_bin):
            os.environ["PATH"] = gv_bin + os.pathsep + os.environ.get("PATH", "")
            return True
        return False

    gv_bin = r"C:\Program Files\Graphviz\bin"
    if os.path.isdir(gv_bin):
        os.environ["PATH"] = gv_bin + os.pathsep + os.environ.get("PATH", "")
        return True

    return False


# ==========================================================
# 3) Themes (Light / Dark)
# ==========================================================

LIGHT = {
    "name": "light",
    "bg": "#ffffff",
    "panel": "#f3f3f3",
    "text_bg": "#ffffff",
    "text_fg": "#111111",
    "muted": "#444444",
    "border": "#cfcfcf",
    "btn_bg": "#efefef",
    "btn_fg": "#111111",
    "btn_active_bg": "#dddddd",
    "btn_active_fg": "#000000",
    "tree_bg": "#ffffff",
    "gv_node_fill": "#ffffff",
    "gv_node_font": "#111111",
    "gv_edge": "#555555",
    "gv_seq_edge": "#777777",
}

DARK = {
    "name": "dark",
    "bg": "#1e1e1e",
    "panel": "#252526",
    "text_bg": "#1b1b1b",
    "text_fg": "#e6e6e6",
    "muted": "#bdbdbd",
    "border": "#3c3c3c",
    "btn_bg": "#2d2d2d",
    "btn_fg": "#e6e6e6",
    "btn_active_bg": "#3a3a3a",
    "btn_active_fg": "#ffffff",
    "tree_bg": "#1e1e1e",
    "gv_node_fill": "#1b1b1b",
    "gv_node_font": "#e6e6e6",
    "gv_edge": "#aaaaaa",
    "gv_seq_edge": "#888888",
}

CURRENT_THEME = {"theme": LIGHT}


def apply_theme(root_widget: tk.Widget):
    T = CURRENT_THEME["theme"]
    try:
        root_widget.configure(bg=T["bg"])
    except Exception:
        pass

    def _apply(w: tk.Widget):
        cls = w.winfo_class()

        if cls in ("Frame", "Labelframe"):
            try:
                w.configure(bg=T["panel"])
            except Exception:
                pass

        if cls == "Labelframe":
            try:
                w.configure(fg=T["text_fg"])
            except Exception:
                pass

        if cls == "Label":
            try:
                w.configure(bg=T["panel"], fg=T["text_fg"])
            except Exception:
                pass

        if cls == "Text":
            try:
                w.configure(
                    bg=T["text_bg"],
                    fg=T["text_fg"],
                    insertbackground=T["text_fg"],
                    selectbackground="#264f78",
                    selectforeground=T["text_fg"],
                )
            except Exception:
                pass

        if cls == "Scrollbar":
            try:
                w.configure(
                    bg=T["panel"],
                    troughcolor=T["bg"],
                    activebackground=T["btn_active_bg"],
                    highlightbackground=T["border"],
                )
            except Exception:
                pass

        if cls == "Button":
            try:
                w.configure(
                    bg=T["btn_bg"],
                    fg=T["btn_fg"],
                    activebackground=T["btn_active_bg"],
                    activeforeground=T["btn_active_fg"],
                    relief="raised",
                    bd=1,
                    highlightbackground=T["border"],
                )
            except Exception:
                pass

        if cls == "Canvas":
            try:
                w.configure(bg=T["tree_bg"], highlightbackground=T["border"])
            except Exception:
                pass

        for child in w.winfo_children():
            _apply(child)

    _apply(root_widget)


# ==========================================================
# 4) STNode + sibling bookkeeping
# ==========================================================

ELSE_EDGES = []
NO_SIBLINE_EDGES = []


class STNode:
    def __init__(self, label: str, kind: str):
        self.label = label
        self.kind = kind  # "stmt" or "expr"
        self.child = None
        self.sibling = None


STMT_KINDS = {"if", "repeat", "assign", "read", "write"}


def make_stree_from_ast(ast_root: ASTNode) -> STNode:
    ELSE_EDGES.clear()
    NO_SIBLINE_EDGES.clear()

    if ast_root.kind != "program":
        raise ValueError("Expected root.kind == 'program'")
    stmt_seq = ast_root.children[0]

    first_stmt = None
    prev_stmt = None
    for stmt_ast in stmt_seq.children:
        st = stmt_from_ast(stmt_ast)
        if first_stmt is None:
            first_stmt = st
        else:
            prev_stmt.sibling = st
        prev_stmt = st

    return first_stmt


def stmt_chain_from_seq(seq_ast: ASTNode):
    first = None
    prev = None
    for s_ast in seq_ast.children:
        st = stmt_from_ast(s_ast)
        if first is None:
            first = st
        else:
            prev.sibling = st
        prev = st
    return first, prev


def stmt_from_ast(node: ASTNode) -> STNode:
    kind = node.kind
    if kind not in STMT_KINDS:
        raise ValueError(f"Expected statement node, got {kind}")

    label = kind if node.value is None else f"{kind} ({node.value})"
    st = STNode(label, "stmt")

    if kind == "read":
        return st

    if kind == "write":
        st.child = expr_from_ast(node.children[0])
        return st

    if kind == "assign":
        st.child = expr_from_ast(node.children[0])
        return st

    if kind == "if":
        cond_ast = node.children[0]
        then_seq = node.children[1]
        else_seq = node.children[2] if len(node.children) > 2 else None

        cond_expr = expr_from_ast(cond_ast)
        st.child = cond_expr

        then_first, then_last = stmt_chain_from_seq(then_seq)
        cond_expr.sibling = then_first

        if else_seq is not None:
            else_first, _ = stmt_chain_from_seq(else_seq)
            then_last.sibling = else_first
            NO_SIBLINE_EDGES.append((then_last, else_first))
            ELSE_EDGES.append((st, else_first))

        return st

    if kind == "repeat":
        body_seq = node.children[0]
        cond_ast = node.children[1]

        body_first, body_last = stmt_chain_from_seq(body_seq)
        st.child = body_first

        cond_expr = expr_from_ast(cond_ast)
        body_last.sibling = cond_expr
        return st

    return st


def expr_from_ast(node: ASTNode) -> STNode:
    if node.kind == "op":
        st = STNode(f"op ({node.value})", "expr")
        left = expr_from_ast(node.children[0])
        right = expr_from_ast(node.children[1])
        st.child = left
        left.sibling = right
        return st
    if node.kind == "id":
        return STNode(f"id ({node.value})", "expr")
    if node.kind == "const":
        return STNode(f"const ({node.value})", "expr")
    raise ValueError(f"Unexpected expr node kind {node.kind}")


# ==========================================================
# 5) Tokens helpers
# ==========================================================

def format_tokens_lexeme_type(token_dicts):
    return "\n".join(f"{t['value']} , {t['type']}" for t in token_dicts)


def parse_tokens_text_to_dicts(tokens_text: str):
    out = []
    lines = tokens_text.splitlines()
    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue
        if "," not in line:
            raise ValueError(f"Bad token line {idx}: missing comma. Example: read , READ")
        left, right = line.split(",", 1)
        lexeme = left.strip()
        tok_type = right.strip()
        if not tok_type:
            raise ValueError(f"Bad token line {idx}: missing token type after comma.")
        out.append({"type": tok_type, "value": lexeme})
    return out


# ==========================================================
# 6) File helpers
# ==========================================================

def save_text_to_file(parent, text, title="Save file"):
    path = filedialog.asksaveasfilename(
        parent=parent,
        title=title,
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not path:
        return None
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def load_text_from_file(parent, title="Open file"):
    path = filedialog.askopenfilename(
        parent=parent,
        title=title,
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not path:
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ==========================================================
# 7) Graphviz rendering
# ==========================================================

def ensure_graphviz_ready():
    if graphviz is None:
        raise RuntimeError("Missing python package 'graphviz'. Run: pip install graphviz")
    if Image is None or ImageTk is None:
        raise RuntimeError("Missing Pillow. Run: pip install pillow")
    if not ensure_graphviz_path():
        raise RuntimeError("Graphviz dot.exe not found (PATH/bundled missing).")
    if not ensure_dot_available():
        raise RuntimeError("Graphviz dot.exe not found (PATH/bundled missing).")



def _graphviz_missing_help():
    return (
        "Graphviz is not ready.\n\n"
        "DEV mode:\n"
        "1) Install Graphviz (dot.exe)\n"
        "2) Ensure dot.exe is in PATH OR installed at:\n"
        "   C:\\Program Files\\Graphviz\\bin\n\n"
        "EXE mode:\n"
        "Bundle Graphviz as _third_party/graphviz/bin/dot.exe via PyInstaller.\n\n"
        "Python deps:\n"
        "pip install graphviz pillow"
    )


def stnode_to_graphviz_dot(root_node: STNode):
    ensure_graphviz_ready()
    T = CURRENT_THEME["theme"]

    g = graphviz.Digraph("TINY_SyntaxTree", format="png")

    g.attr(
        rankdir="TB",
        splines="spline",
        overlap="false",
        concentrate="true",
        nodesep="0.60",
        ranksep="0.95",
        pad="0.30",
        dpi="260",
        outputorder="edgesfirst",
        bgcolor=T["tree_bg"] if T["name"] == "dark" else "white",
    )

    g.attr(
        "node",
        fontname="Helvetica",
        fontsize="10",
        style="filled",
        fillcolor=T["gv_node_fill"],
        fontcolor=T["gv_node_font"],
        penwidth="1.2",
    )

    g.attr(
        "edge",
        arrowsize="0.7",
        dir="none",
        color=T["gv_edge"],
        penwidth="1.1",
    )

    ids = {}
    counter = 0

    def nid(obj):
        nonlocal counter
        k = id(obj)
        if k not in ids:
            counter += 1
            ids[k] = f"n{counter}"
        return ids[k]

    seen = set()
    nodes = []

    def collect(n):
        if n is None or id(n) in seen:
            return
        seen.add(id(n))
        nodes.append(n)
        collect(n.child)
        collect(n.sibling)

    collect(root_node)

    for n in nodes:
        shape = "box" if n.kind == "stmt" else "ellipse"
        g.node(nid(n), label=n.label, shape=shape)

    if_to_else = {}
    for (if_node, else_first) in ELSE_EDGES:
        if_to_else[id(if_node)] = else_first

    no_sib_pairs = set((id(a), id(b)) for (a, b) in NO_SIBLINE_EDGES)

    def draw_expr_subtree(expr: STNode, parent_id: str = None, visible=True, edge_style="solid"):
        expr_id = nid(expr)
        if parent_id is not None:
            if not visible:
                g.edge(parent_id, expr_id, style="invis")
            else:
                g.edge(parent_id, expr_id, style=edge_style)

        c = expr.child
        while c is not None:
            g.edge(expr_id, nid(c), style="solid", weight="2", minlen="1")
            if c.kind == "expr":
                draw_expr_subtree(c, parent_id=None)
            c = c.sibling

    def draw_stmt_children(stmt: STNode, stmt_id: str):
        if stmt.child is None:
            return

        if stmt.label.startswith("assign") or stmt.label.startswith("write"):
            draw_expr_subtree(stmt.child, parent_id=stmt_id, visible=True, edge_style="solid")
            return

        if stmt.label == "if":
            cond = stmt.child
            g.edge(stmt_id, nid(cond), style="solid", weight="3", minlen="1")
            if cond.kind == "expr":
                draw_expr_subtree(cond, parent_id=None)

            then_first = cond.sibling
            if then_first is not None and then_first.kind == "stmt":
                draw_stmt_chain(then_first, parent_id=stmt_id, visible=True, edge_style="solid")

            else_first = if_to_else.get(id(stmt))
            if else_first is not None:
                draw_stmt_chain(else_first, parent_id=stmt_id, visible=True, edge_style="dashed")
            return

        if stmt.label == "repeat":
            body_first = stmt.child
            if body_first is None:
                return

            draw_stmt_chain(body_first, parent_id=stmt_id, visible=True, edge_style="solid")

            cur = body_first
            while cur.sibling is not None and cur.sibling.kind == "stmt":
                if (id(cur), id(cur.sibling)) in no_sib_pairs:
                    break
                cur = cur.sibling

            test_expr = cur.sibling
            if test_expr is not None and test_expr.kind == "expr":
                draw_expr_subtree(test_expr, parent_id=stmt_id, visible=True, edge_style="solid")
            return

    def draw_stmt_chain(first_stmt: STNode, parent_id: str, visible=True, edge_style="solid"):
        prev_stmt_id = None
        cur = first_stmt
        visited = set()

        while cur is not None and cur.kind == "stmt":
            if id(cur) in visited:
                break
            visited.add(id(cur))

            cur_id = nid(cur)

            if parent_id is not None:
                if prev_stmt_id is None:
                    if not visible:
                        g.edge(parent_id, cur_id, style="invis")
                    else:
                        g.edge(parent_id, cur_id, style=edge_style, weight="3", minlen="1")
                else:
                    g.edge(parent_id, cur_id, style="invis")

            if prev_stmt_id is not None:
                g.edge(
                    prev_stmt_id,
                    cur_id,
                    constraint="false",
                    color=T["gv_seq_edge"],
                    penwidth="0.9",
                    weight="0.2",
                    minlen="1",
                )

            draw_stmt_children(cur, cur_id)

            prev_stmt_id = cur_id

            if cur.sibling is not None and (id(cur), id(cur.sibling)) in no_sib_pairs:
                break

            cur = cur.sibling

    draw_stmt_chain(root_node, parent_id=None, visible=True, edge_style="solid")
    return g


def render_graphviz_to_png(root_node: STNode) -> str:
    dot = stnode_to_graphviz_dot(root_node)
    outdir = tempfile.mkdtemp(prefix="tiny_tree_")
    outbase = os.path.join(outdir, "tree")
    png_path = dot.render(outbase, cleanup=True)
    return png_path


# ==========================================================
# 8) Tree viewer window (Syntax Tree)
# ==========================================================

_tree_win = None
_tree_canvas = None
_tree_photo = None
_tree_img_orig = None
_tree_img_id = None
_tree_scale = 1.0


def ensure_tree_window(root):
    global _tree_win, _tree_canvas

    if _tree_win is not None and _tree_win.winfo_exists():
        return _tree_win

    _tree_win = tk.Toplevel(root)
    _tree_win.title("Syntax Tree (Graphviz)")

    bar = tk.Frame(_tree_win)
    bar.pack(side=tk.TOP, fill=tk.X)

    tk.Button(bar, text="Zoom +", command=lambda: zoom_tree(1.15)).pack(side=tk.LEFT, padx=4, pady=3)
    tk.Button(bar, text="Zoom -", command=lambda: zoom_tree(1 / 1.15)).pack(side=tk.LEFT, padx=4, pady=3)
    tk.Button(bar, text="Reset Zoom", command=reset_tree_zoom).pack(side=tk.LEFT, padx=4, pady=3)

    frame = tk.Frame(_tree_win)
    frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    _tree_canvas = tk.Canvas(frame, width=1200, height=650)
    _tree_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    xscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=_tree_canvas.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    yscroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=_tree_canvas.yview)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)

    _tree_canvas.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

    def _on_ctrl_wheel(event):
        zoom_tree(1.15 if event.delta > 0 else (1 / 1.15))

    def _pan_start(event):
        _tree_canvas.scan_mark(event.x, event.y)

    def _pan_move(event):
        _tree_canvas.scan_dragto(event.x, event.y, gain=1)

    _tree_canvas.bind("<Control-MouseWheel>", _on_ctrl_wheel)
    _tree_canvas.bind("<ButtonPress-1>", _pan_start)
    _tree_canvas.bind("<B1-Motion>", _pan_move)

    apply_theme(_tree_win)
    return _tree_win


def show_tree_image(root, png_path: str):
    global _tree_photo, _tree_img_orig, _tree_img_id, _tree_scale

    ensure_tree_window(root)
    _tree_win.deiconify()
    _tree_win.lift()

    img = Image.open(png_path)
    _tree_img_orig = img
    _tree_scale = 1.0

    _tree_canvas.delete("all")
    _tree_photo = ImageTk.PhotoImage(img)
    _tree_img_id = _tree_canvas.create_image(0, 0, image=_tree_photo, anchor="nw")

    _tree_canvas.configure(scrollregion=(0, 0, img.width, img.height))


def zoom_tree(factor: float):
    global _tree_scale, _tree_photo, _tree_img_id
    if _tree_img_orig is None:
        return

    new_scale = _tree_scale * factor
    if new_scale < 0.12 or new_scale > 10.0:
        return

    _tree_scale = new_scale
    w = max(1, int(_tree_img_orig.width * _tree_scale))
    h = max(1, int(_tree_img_orig.height * _tree_scale))

    resized = _tree_img_orig.resize((w, h), Image.LANCZOS)
    _tree_photo = ImageTk.PhotoImage(resized)

    _tree_canvas.itemconfigure(_tree_img_id, image=_tree_photo)
    _tree_canvas.configure(scrollregion=(0, 0, w, h))


def reset_tree_zoom():
    global _tree_scale, _tree_photo
    if _tree_img_orig is None:
        return
    _tree_scale = 1.0
    _tree_photo = ImageTk.PhotoImage(_tree_img_orig)
    _tree_canvas.itemconfigure(_tree_img_id, image=_tree_photo)
    _tree_canvas.configure(scrollregion=(0, 0, _tree_img_orig.width, _tree_img_orig.height))


# ==========================================================
# 9) Main window (NO AST output panel)
# ==========================================================

root = tk.Tk()
root.title("TINY Pipeline: Scanner + Parser (Graphviz)")

top = tk.Frame(root)
top.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

# Right controls (top-right)
right_controls = tk.Frame(top)
right_controls.pack(side=tk.RIGHT)

def toggle_theme():
    CURRENT_THEME["theme"] = LIGHT if CURRENT_THEME["theme"] is DARK else DARK
    apply_theme(root)
    if _tree_win is not None and _tree_win.winfo_exists():
        apply_theme(_tree_win)
        try:
            _tree_canvas.configure(bg=CURRENT_THEME["theme"]["tree_bg"])
        except Exception:
            pass

def reset_all():
    src_box.delete("1.0", tk.END)
    scan_out.delete("1.0", tk.END)
    parse_in.delete("1.0", tk.END)

tk.Button(right_controls, text="Reset / Clear", command=reset_all).pack(side=tk.TOP, padx=6, pady=(0, 6))
tk.Button(right_controls, text="Toggle Dark/Light", command=toggle_theme).pack(side=tk.TOP, padx=6)

# Left button groups
btn_frame = tk.Frame(top)
btn_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

scanner_row = tk.LabelFrame(btn_frame, text="Scanner")
scanner_row.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

parser_row = tk.LabelFrame(btn_frame, text="Parser")
parser_row.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

pipeline_row = tk.LabelFrame(btn_frame, text="Pipeline")
pipeline_row.pack(side=tk.TOP, fill=tk.X)

# Source
src_frame = tk.Frame(root)
src_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=6, pady=6)

tk.Label(src_frame, text="TINY Source (used by Scanner):").pack(anchor="w")
src_box = tk.Text(src_frame, height=8)
src_box.pack(fill=tk.BOTH, expand=True)

# Middle: Scanner output + Parser input
mid = tk.Frame(root)
mid.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=6)

left = tk.Frame(mid)
left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

right = tk.Frame(mid)
right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

tk.Label(left, text="Scanner Output (tokens):").pack(anchor="w")
scan_out = tk.Text(left, wrap="none")
scan_out.pack(fill=tk.BOTH, expand=True)

scan_y = tk.Scrollbar(left, orient="vertical", command=scan_out.yview)
scan_y.pack(side=tk.RIGHT, fill=tk.Y)
scan_x = tk.Scrollbar(left, orient="horizontal", command=scan_out.xview)
scan_x.pack(side=tk.BOTTOM, fill=tk.X)
scan_out.configure(yscrollcommand=scan_y.set, xscrollcommand=scan_x.set)

tk.Label(right, text="Parser Input (tokens file/paste as: lexeme , TYPE):").pack(anchor="w")
parse_in = tk.Text(right, wrap="none")
parse_in.pack(fill=tk.BOTH, expand=True)

pi_y = tk.Scrollbar(right, orient="vertical", command=parse_in.yview)
pi_y.pack(side=tk.RIGHT, fill=tk.Y)
pi_x = tk.Scrollbar(right, orient="horizontal", command=parse_in.xview)
pi_x.pack(side=tk.BOTTOM, fill=tk.X)
parse_in.configure(yscrollcommand=pi_y.set, xscrollcommand=pi_x.set)


def _set_text(widget: tk.Text, text: str):
    widget.delete("1.0", tk.END)
    widget.insert("1.0", text)


def load_source_file():
    text = load_text_from_file(root, "Load TINY source file")
    if text is None:
        messagebox.showerror("File error", "No file was selected.")
        return
    _set_text(src_box, text)


def run_scanner():
    src = src_box.get("1.0", tk.END)
    if not src.strip():
        messagebox.showerror("Input error", "Source is empty.")
        return
    try:
        toks = scanner_4.scan_text(src)
        _set_text(scan_out, format_tokens_lexeme_type(toks))
    except Exception as e:
        messagebox.showerror("Scanner error", str(e))


def copy_scanner_output():
    text = scan_out.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Nothing to copy", "Scanner output is empty.")
        return
    root.clipboard_clear()
    root.clipboard_append(text)


def save_scanner_output():
    text = scan_out.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Scanner output is empty. Run Scanner first.")
        return
    try:
        save_text_to_file(root, text, "Save Scanner Output (tokens)")
    except Exception as e:
        messagebox.showerror("File error", str(e))


def load_tokens_file():
    text = load_text_from_file(root, "Load Tokens File (scanner output)")
    if text is None:
        messagebox.showerror("File error", "No file was selected.")
        return
    _set_text(parse_in, text)


def parse_to_syntax_tree():
    txt = parse_in.get("1.0", tk.END)
    if not txt.strip():
        messagebox.showerror("Input error", "Parser input tokens are empty.")
        return

    try:
        ensure_graphviz_ready()
    except Exception as e:
        messagebox.showerror("Graphviz setup", f"{e}\n\n{_graphviz_missing_help()}")
        return

    try:
        token_dicts = parse_tokens_text_to_dicts(txt)
        ast = build_ast_from_token_dicts(token_dicts)

        st_root = make_stree_from_ast(ast)
        png_path = render_graphviz_to_png(st_root)
        show_tree_image(root, png_path)

    except ParserError as e:
        messagebox.showerror("Parser error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"{e}\n\n{_graphviz_missing_help()}")


def scanner_plus_parser_full_pipeline():
    src = src_box.get("1.0", tk.END)
    if not src.strip():
        messagebox.showerror("Input error", "Source is empty.")
        return

    try:
        ensure_graphviz_ready()
    except Exception as e:
        messagebox.showerror("Graphviz setup", f"{e}\n\n{_graphviz_missing_help()}")
        return

    try:
        toks = scanner_4.scan_text(src)
        out = format_tokens_lexeme_type(toks)
        _set_text(scan_out, out)
        _set_text(parse_in, out)

        ast = build_ast_from_token_dicts(toks)
        st_root = make_stree_from_ast(ast)
        png_path = render_graphviz_to_png(st_root)
        show_tree_image(root, png_path)

    except ParserError as e:
        messagebox.showerror("Parser error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"{e}\n\n{_graphviz_missing_help()}")


# Buttons
tk.Button(scanner_row, text="Load Source File", command=load_source_file).pack(side=tk.LEFT, padx=4, pady=4)
tk.Button(scanner_row, text="Run Scanner", command=run_scanner).pack(side=tk.LEFT, padx=4, pady=4)
tk.Button(scanner_row, text="Copy Scanner Output", command=copy_scanner_output).pack(side=tk.LEFT, padx=4, pady=4)
tk.Button(scanner_row, text="Save Scanner Output", command=save_scanner_output).pack(side=tk.LEFT, padx=4, pady=4)

tk.Button(parser_row, text="Load Tokens File", command=load_tokens_file).pack(side=tk.LEFT, padx=4, pady=4)
tk.Button(parser_row, text="Parse → Syntax Tree", command=parse_to_syntax_tree).pack(side=tk.LEFT, padx=4, pady=4)

tk.Button(pipeline_row, text="Scanner + Parser (Full Pipeline)", command=scanner_plus_parser_full_pipeline).pack(
    side=tk.LEFT, padx=6, pady=6
)

apply_theme(root)
root.mainloop()
