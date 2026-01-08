"""
Fix const field issues in webhook models for Pydantic v1 compatibility.
"""

import os
import re
from pathlib import Path

def fix_const_fields(file_path: Path):
    """Replace const=True with default value and validation."""
    content = file_path.read_text()
    original_content = content
    
    # Pattern to match const=True fields
    # action: str = Field("value", const=True)
    pattern = r'(\w+):\s*str\s*=\s*Field\("([^"]+)",\s*const=True([^)]*)\)'
    
    def replacement(match):
        field_name = match.group(1)
        const_value = match.group(2)
        extra_params = match.group(3)
        
        # Replace with default value
        return f'{field_name}: str = Field(default="{const_value}"{extra_params})'
    
    updated_content = re.sub(pattern, replacement, content)
    
    # Handle cases with description and other params
    pattern2 = r'(\w+):\s*str\s*=\s*Field\("([^"]+)",\s*const=True,\s*([^)]+)\)'
    
    def replacement2(match):
        field_name = match.group(1)
        const_value = match.group(2)
        extra_params = match.group(3)
        
        return f'{field_name}: str = Field(default="{const_value}", {extra_params})'
    
    updated_content = re.sub(pattern2, replacement2, updated_content)
    
    # Write back if changed
    if updated_content != original_content:
        file_path.write_text(updated_content)
        print(f"Fixed const fields in: {file_path}")
        return True
    
    return False

def main():
    """Fix all const field issues."""
    webhook_models_path = Path("/home/sivaj/projects/AI-ML/AmzurGitHubAnalyzer/AmzurGitHubAnalyzer-WebHook/AmzurGitHubAnalyzer/backend/app/webhook_models")
    
    print("🔧 Fixing const field issues...")
    
    fixed_files = []
    
    # Find files with const issues
    const_files = [
        "member_added.py",
        "issues_opened.py", 
        "team_member_added.py",
        "pull_request_opened.py",
        "repository_created.py"
    ]
    
    for file_name in const_files:
        file_path = webhook_models_path / file_name
        if file_path.exists():
            if fix_const_fields(file_path):
                fixed_files.append(file_name)
    
    print(f"✅ Fixed {len(fixed_files)} files: {fixed_files}")
    
    # Also check for any other files with const
    print("\n🔍 Checking for remaining const issues...")
    for py_file in webhook_models_path.rglob("*.py"):
        if py_file.name not in const_files and py_file.name != "__init__.py":
            content = py_file.read_text()
            if "const=True" in content:
                fix_const_fields(py_file)
                print(f"Fixed additional const in: {py_file}")
    
    print("\n🎉 Const field fixes complete!")

if __name__ == "__main__":
    main()