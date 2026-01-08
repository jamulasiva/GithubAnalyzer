"""
Script to update webhook models for Pydantic v1 compatibility.
Fixes common issues and ensures models work with our backend.
"""

import os
import re
from pathlib import Path

def update_pydantic_config(file_path: Path):
    """Update Pydantic Config class for v1 compatibility."""
    content = file_path.read_text()
    
    # Fix common Pydantic v2 -> v1 issues
    replacements = [
        # Replace model_rebuild with update_forward_refs
        (r'\.model_rebuild\(\)', '.update_forward_refs()'),
        
        # Fix Config class issues
        (r'allow_population_by_field_name = True', 'allow_population_by_field_name = True'),
        (r'use_enum_values = True', 'use_enum_values = True'),
        (r'extra = "allow"', 'extra = "allow"'),
        
        # Ensure proper imports
        (r'from pydantic import BaseModel, Field', 'from pydantic import BaseModel, Field'),
    ]
    
    updated_content = content
    for pattern, replacement in replacements:
        updated_content = re.sub(pattern, replacement, updated_content)
    
    # Write back if changed
    if updated_content != content:
        file_path.write_text(updated_content)
        print(f"Updated: {file_path}")
    
    return updated_content != content

def main():
    """Update all webhook model files."""
    webhook_models_path = Path("/home/sivaj/projects/AI-ML/AmzurGitHubAnalyzer/AmzurGitHubAnalyzer-WebHook/AmzurGitHubAnalyzer/backend/app/webhook_models")
    
    print("🔄 Updating webhook models for Pydantic v1 compatibility...")
    
    updated_files = 0
    total_files = 0
    
    # Find all Python files
    for py_file in webhook_models_path.rglob("*.py"):
        if py_file.name != "__init__.py":
            total_files += 1
            if update_pydantic_config(py_file):
                updated_files += 1
    
    print(f"✅ Updated {updated_files}/{total_files} files")
    
    # Update model resolution for circular imports
    print("\n🔧 Adding model resolution...")
    
    # Update common/base.py to call update_forward_refs
    base_file = webhook_models_path / "common" / "base.py"
    if base_file.exists():
        content = base_file.read_text()
        
        # Add update_forward_refs calls at the end
        if "update_forward_refs" not in content:
            content += "\n\n# Update forward references for circular imports\n"
            content += "WebhookHeaders.update_forward_refs()\n"
            content += "WebhookBase.update_forward_refs()\n"
            
            base_file.write_text(content)
            print("✅ Added forward reference updates to base.py")
    
    print("\n🎉 Webhook models update complete!")

if __name__ == "__main__":
    main()