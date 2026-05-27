import json
import time
import os
import sys
from typing import Any, Dict, List, Optional

# Load BEJSON Core
LIB_DIR = os.path.dirname(os.path.abspath(__file__))
if LIB_DIR not in sys.path:
    sys.path.append(LIB_DIR)

try:
    import lib_bejson_core as BEJSONCore
except ImportError:
    pass

class HTML3_List_Renderer:
    """
    Library:      lib_html3_list_renderer.py
    Family:       HTML3
    Version:      1.3.2 OFFICIAL
    Description:  Authoritative List Renderer with Action Hooks and Breadcrumbs.
    REMEDIATED:   Fixed brace escaping issue by using .format() instead of f-strings.
    """

    CORE_CSS = """
<style>
    .c-html3-list { font-family: 'Roboto Mono', monospace; color: #fff; max-width: 100%; box-sizing: border-box; }
    
    /* BREADCRUMBS */
    .c-html3-list__breadcrumbs { display: flex; gap: 8px; font-size: 0.7rem; color: #555; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; min-height: 1.2rem; }
    .c-html3-list__breadcrumb-item::after { content: '>'; margin-left: 8px; color: #333; }
    .c-html3-list__breadcrumb-item:last-child::after { content: ''; }
    .c-html3-list__breadcrumb-item.active { color: #DE2626; font-weight: bold; }

    /* TREE MODE */
    .c-html3-list--tree { background: #0a0a0a; border: 1px solid #333; border-radius: 8px; padding: 1.5rem; }
    .c-html3-list__tree { list-style: none; padding-left: 0; margin: 0; }
    .c-html3-list__item { margin: 4px 0; position: relative; }
    .c-html3-list__content { display: flex; align-items: flex-start; gap: 12px; padding: 10px 14px; background: #111; border: 1px solid #222; border-radius: 4px; transition: all 0.2s; cursor: pointer; position: relative; }
    .c-html3-list__content:hover { border-color: #DE2626; background: #1a0505; }
    .c-html3-list__content.is-selected { background: #DE2626 !important; border-color: #a01d1d !important; }
    .c-html3-list__content.is-selected * { color: #fff !important; }
    
    /* ACTION HOOKS */
    .c-html3-list__action { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); opacity: 0; transition: opacity 0.2s; }
    .c-html3-list__content:hover .c-html3-list__action { opacity: 1; }
    .c-html3-list__btn { background: #DE2626; color: #fff; border: none; padding: 4px 10px; border-radius: 2px; font-size: 0.65rem; font-weight: bold; cursor: pointer; text-transform: uppercase; text-decoration: none; }
    .c-html3-list__btn:hover { background: #fff; color: #DE2626; }

    .c-html3-list__toggle { width: 24px; color: #DE2626; font-weight: bold; text-align: center; }
    .c-html3-list__children { list-style: none; padding-left: 32px; border-left: 1px solid #222; margin-left: 11px; }

    /* SIDEBAR & DROPDOWN */
    .c-html3-list--sidebar { width: 100%; background: #050505; height: 100%; display: flex; flex-direction: column; }
    .c-html3-list__nav-item { display: block; padding: 12px 20px; color: #888; text-decoration: none; border-left: 3px solid transparent; font-size: 0.85rem; transition: all 0.2s; text-transform: uppercase; letter-spacing: 1px; cursor: pointer; }
    .c-html3-list__nav-item:hover { background: #111; color: #fff; border-left-color: #DE2626; }
    .c-html3-list__nav-item.is-active { background: #1a0505; color: #DE2626; border-left-color: #DE2626; font-weight: bold; }
    .c-html3-list__nav-sub { padding-left: 15px; background: #080808; }

    /* DROPDOWN */
    .c-html3-list--dropdown { position: relative; display: inline-block; min-width: 200px; }
    .c-html3-list__select { width: 100%; background: #111; color: #fff; border: 1px solid #333; padding: 10px; border-radius: 4px; outline: none; cursor: pointer; }
</style>
"""

    JS = """
<script>
    if (!window.html3_list_state) window.html3_list_state = {};

    if (!window.html3_list_toggle) {
        window.html3_list_toggle = function(el, cid, itemId) {
            const item = el.closest('.c-html3-list__item');
            const children = item.querySelector('.c-html3-list__children');
            const toggle = item.querySelector('.c-html3-list__toggle');
            
            if (children) {
                const isHidden = children.style.display === 'none';
                children.style.display = isHidden ? 'block' : 'none';
                if (toggle) toggle.textContent = isHidden ? '[-]' : '[+]';
            }
            
            const listRoot = el.closest('.c-html3-list');
            listRoot.querySelectorAll('.c-html3-list__content').forEach(c => c.classList.remove('is-selected'));
            el.classList.add('is-selected');
            
            if (window.html3_update_breadcrumbs) window.html3_update_breadcrumbs(cid, itemId);
        };
    }

    if (!window.html3_update_breadcrumbs) {
        window.html3_update_breadcrumbs = function(cid, itemId) {
            const bcContainer = document.querySelector("#" + cid + " .c-html3-list__breadcrumbs");
            if (!bcContainer) return;
            
            const data = window.html3_list_data[cid];
            const path = [];
            let curr = itemId;
            
            while(curr) {
                const item = data.find(i => i.id === curr);
                if (item) {
                    path.unshift(item.title);
                    curr = item.parent_id;
                } else break;
            }
            
            bcContainer.innerHTML = path.map((name, i) => 
                "<span class='c-html3-list__breadcrumb-item " + (i === path.length - 1 ? "active" : "") + "'>" + name + "</span>"
            ).join("");
        };
    }
</script>
"""

    TREE_TEMPLATE = """
{css}{js}
<div id="{cid}" class="c-html3-list c-html3-list--tree">
    <div class="c-html3-list__breadcrumbs">SELECT NODE TO VIEW PATH</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;border-bottom:1px solid #333;padding-bottom:0.8rem;">
        <div style="color:#DE2626;font-weight:bold;letter-spacing:2px;text-transform:uppercase;">{title}</div>
        <div style="font-size:0.7rem;color:#555;">v1.3.2</div>
    </div>
    <ul class="c-html3-list__tree">{nodes}</ul>
    <script>
        if(!window.html3_list_data) window.html3_list_data = {{}};
        window.html3_list_data['{cid}'] = {data_json};
    </script>
</div>
"""

    SIDEBAR_TEMPLATE = """
{css}
<div id="{cid}" class="c-html3-list c-html3-list--sidebar">
    <div style="padding:20px;border-bottom:1px solid #222;color:#DE2626;font-weight:bold;font-size:0.9rem;letter-spacing:2px;text-transform:uppercase;">{title}</div>
    <div style="flex:1;overflow-y:auto;">{nav_html}</div>
</div>
"""

    def __init__(self):
        pass

    def _build_hierarchy(self, doc):
        fields = doc.get("Fields", [])
        f_map = {f["name"].lower(): i for i, f in enumerate(fields)}
        
        id_idx = f_map.get("id", 0)
        pid_idx = f_map.get("parent_id", 1)
        title_idx = f_map.get("title", 2)
        desc_idx = f_map.get("description", 3)
        url_idx = f_map.get("url", -1)
        act_url_idx = f_map.get("action_url", -1)
        act_label_idx = f_map.get("action_label", -1)

        raw_items = []
        item_map = {}
        roots = []

        for row in doc.get("Values", []):
            if not row: continue
            item = {
                "id": row[id_idx],
                "parent_id": row[pid_idx],
                "title": row[title_idx],
                "description": row[desc_idx],
                "url": row[url_idx] if url_idx != -1 else None,
                "action_url": row[act_url_idx] if act_url_idx != -1 else None,
                "action_label": row[act_label_idx] if act_label_idx != -1 else "RUN",
                "children": []
            }
            raw_items.append(item)
            item_map[item["id"]] = item

        for item in item_map.values():
            parent_id = item["parent_id"]
            if parent_id and parent_id in item_map:
                item_map[parent_id]["children"].append(item)
            else:
                roots.append(item)
        
        return roots, item_map, raw_items

    def render(self, doc_path: str, mode: str = "TREE", **kwargs) -> str:
        try:
            doc = BEJSONCore.bejson_core_load_file(doc_path)
            if not doc: return "Error loading file"
        except: return "Error"

        roots, item_map, raw_items = self._build_hierarchy(doc)
        cid = kwargs.get("cid", f"lst_{int(time.time()*1000)}")
        on_click = kwargs.get("on_click", None)
        title = kwargs.get("title", "")
        
        if mode == "SIDEBAR": return self._render_sidebar(roots, cid, title, on_click)
        
        def build_node(item):
            has_children = len(item["children"]) > 0
            toggle = "[-]" if has_children else "[o]"
            action_html = f'<div class="c-html3-list__action"><a href="{item["action_url"]}" class="c-html3-list__btn">{item["action_label"]}</a></div>' if item["action_url"] else ""
            
            click_handler = f"window.html3_list_toggle(this, '{cid}', '{item['id']}');"
            if on_click:
                click_handler += f" {on_click}('{item['id']}');"
            
            html = f'<li class="c-html3-list__item">'
            html += f'<div class="c-html3-list__content" onclick="{click_handler}">'
            html += f'<div class="c-html3-list__toggle">{toggle}</div>'
            html += f'<div class="c-html3-list__item-info">'
            html += f'<div class="c-html3-list__item-title">{item["title"]}</div>'
            if item["description"]: html += f'<div class="c-html3-list__item-desc">{item["description"]}</div>'
            html += '</div>'
            html += action_html
            html += '</div>'
            if has_children:
                html += '<ul class="c-html3-list__children">'
                for child in sorted(item["children"], key=lambda x: str(x["title"])): html += build_node(child)
                html += '</ul>'
            html += '</li>'
            return html

        nodes_html = "".join([build_node(r) for r in sorted(roots, key=lambda x: str(x["title"]))])
        
        return self.TREE_TEMPLATE.format(
            css=self.CORE_CSS,
            js=self.JS,
            cid=cid,
            title=title,
            nodes=nodes_html,
            data_json=json.dumps(raw_items)
        )

    def _render_sidebar(self, roots, cid, title, on_click=None):
        def build_nav(item, level=0):
            indent = level * 15
            href = item["url"] if item["url"] else "#"
            
            click_attr = ""
            if on_click:
                click_attr = f"onclick=\"{on_click}('{item['id']}'); return false;\""
            
            html = f'<a href="{href}" {click_attr} class="c-html3-list__nav-item" style="padding-left:{20 + indent}px;">{item["title"]}</a>'
            if item["children"]:
                html += '<div class="c-html3-list__nav-sub">'
                for child in sorted(item["children"], key=lambda x: str(x["title"])): html += build_nav(child, level + 1)
                html += '</div>'
            return html

        nav_html = "".join([build_nav(r) for r in sorted(roots, key=lambda x: str(x["title"]))])
        return self.SIDEBAR_TEMPLATE.format(
            css=self.CORE_CSS,
            cid=cid,
            title=title,
            nav_html=nav_html
        )

if __name__ == "__main__":
    print("HTML3 Multi-Mode List Renderer v1.3.2 Loaded.")
