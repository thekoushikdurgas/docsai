import os
import re

def get_markdown_files(root_dir):
    md_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(os.path.join(dirpath, f))
    return md_files

def extract_meaningful_lines(filepath):
    lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Skip code blocks and small lines
            if line.startswith('```'): continue
            if len(line) < 20: continue
            lines.append(line)
    return lines

def analyze_checklists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count checklist usages
    checked = len(re.findall(r'\[[xX]\]', content))
    unchecked = len(re.findall(r'\[\s\]', content))
    return checked, unchecked

def main():
    base_dir = r"d:\code\ayan\contact"
    analysis_dir = os.path.join(base_dir, "docs", "analysis")
    
    # Read target domains
    backend_files = get_markdown_files(os.path.join(base_dir, "docs", "backend"))
    frontend_files = get_markdown_files(os.path.join(base_dir, "docs", "frontend"))
    
    target_files = backend_files + frontend_files
    
    # Read target contents into memory (small enough for docs)
    target_contents = []
    for filepath in target_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                target_contents.append((filepath, f.read()))
        except Exception:
            pass

    analysis_files = get_markdown_files(analysis_dir)
    
    out_lines = []
    out_lines.append(f"Total analysis files: {len(analysis_files)}")
    out_lines.append(f"Total target files (back/front): {len(target_files)}")
    out_lines.append("-" * 50)
    
    # Separate cursor logs which are usually chat transcripts
    cursor_files = [f for f in analysis_files if "cursor" in os.path.basename(f).lower()]
    out_lines.append(f"Detected {len(cursor_files)} cursor transit logs (often obsolete).")
    
    # Analyze the files
    for filepath in analysis_files:
        filename = os.path.basename(filepath)
        checked, unchecked = analyze_checklists(filepath)
        
        # Determine check status
        if checked + unchecked > 0:
            if unchecked == 0:
                out_lines.append(f"[COMPLETED] {filename}: Fully checked ({checked} done, 0 pending) -> Safe to remove.")
            else:
                out_lines.append(f"[PENDING] {filename}: Has unchecked tasks ({unchecked} pending, {checked} done).")
        else:
            # Try to score overlap
            lines = extract_meaningful_lines(filepath)
            if not lines:
                out_lines.append(f"[EMPTY] {filename}: No meaningful content.")
                continue
                
            # Count how many lines appear exactly or strongly in target contents
            found_count = 0
            for line in lines:
                # Naive matching:
                if any(line in t_content for _, t_content in target_contents):
                    found_count += 1
            
            overlap_pct = (found_count / len(lines)) * 100
            
            if overlap_pct > 80:
                out_lines.append(f"[COVERED] {filename}: {overlap_pct:.1f}% content found in targets -> Safe to remove.")
            elif overlap_pct < 20 and filename.startswith('cursor'):
                out_lines.append(f"[CURSOR-LOW] {filename}: {overlap_pct:.1f}% overlap. Typical chat log -> Inspect for removal.")
            else:
                out_lines.append(f"[REVIEW] {filename}: {overlap_pct:.1f}% overlap. Contains unique content ({len(lines)} lines).")

    with open(r"d:\code\ayan\contact\tools\analysis_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
