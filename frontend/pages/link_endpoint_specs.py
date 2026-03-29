import os
import re

# Use relative paths from root if run from root
PAGE_DIR = "docs/frontend/pages"
ENDPOINT_DIR = "docs/backend/endpoints"

def main():
    if not os.path.exists(PAGE_DIR):
        print(f"Error: {PAGE_DIR} not found.")
        return
        
    endpoint_map = {}
    for f in os.listdir(ENDPOINT_DIR):
        if f.endswith(".md"):
            key = f.replace("query_", "").replace("mutation_", "").replace("get_", "").replace("_graphql.md", "").replace(".md", "")
            endpoint_map[key.lower()] = f
            
    count = 0
    for filename in os.listdir(PAGE_DIR):
        if filename.endswith(".md") and filename not in ["README.md", "DESIGN_SYMBOLS.md", "index.md", "admin_surface.md"]:
            path = os.path.join(PAGE_DIR, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract ops
            ops = set(re.findall(r"GQL\s+([a-zA-Z0-9_]+)", content))
            ops.update(re.findall(r"\{\s*use([a-zA-Z0-9]+)\s*\}", content))
            
            if not ops: continue
            
            rows = []
            for op in sorted(list(ops)):
                f_match = endpoint_map.get(op.lower())
                if f_match:
                    rows.append(f"| {op} | [{f_match}](../../backend/endpoints/{f_match}) | Core data operation. |")
            
            if not rows: continue
            
            table = "| GraphQL Operation | Endpoint Spec | Description |\n|---|---|---|\n" + "\n".join(rows)
            
            # Simple marker-less replacement for now if markers missing
            marker_start = "<!-- AUTO:endpoint-links:start -->"
            marker_end = "<!-- AUTO:endpoint-links:end -->"
            
            if marker_start in content and marker_end in content:
                pattern = re.escape(marker_start) + r".*?" + re.escape(marker_end)
                new_section = f"{marker_start}\n\n### Backend endpoint specs (GraphQL)\n\n{table}\n\n{marker_end}"
                content = re.sub(pattern, new_section, content, flags=re.DOTALL)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                
    print(f"Updated {count} files.")

if __name__ == "__main__":
    main()
