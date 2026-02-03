# 💀 Batruscator

<p align="center">
  <img src="https://img.shields.io/badge/Obfuscation-Extreme-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows" />
</p>

### �️ How to use
1. Put your `.bat` script in the folder.
2. Run this command:
   ```bash
   python batruscator_core.py your_file.bat
   ```
3. Get the result from `output/obfuscated.bat`.

### ⚙️ Config (`config.json`)
Customize your settings here:
```json
{
    "loader_inflation_count": 5,
    "inline_junk_min": 1,
    "inline_junk_max": 3,
    "inter_line_inflation_chance": 0.2,
    "map_count": 10,
    "output_dir": "output",
    "enable_decoration": true,
    "obfuscation_intensity": 0.7,
    "one_line": true
}
```

| Setting | What it does |
| :--- | :--- |
| `loader_inflation_count` | Adds junk code to the top. |
| `inline_junk_min/max` | Junk added per line. |
| `inter_line_inflation_chance` | Chance for random noise between lines. |
| `map_count` | Number of variable tables used. |
| `obfuscation_intensity` | How much of the code gets scrambled. |
| `one_line` | Smushes everything onto one line. |
| `enable_decoration` | Adds extra @ and ; symbols. |

---

<p align="center">
  <img src="https://img.shields.io/github/issues/70gd/Batruscator?style=flat-square&color=orange" />
  <img src="https://img.shields.io/github/last-commit/70gd/Batruscator?style=flat-square&color=green" />
  <img src="https://img.shields.io/github/repo-size/70gd/Batruscator?style=flat-square&color=blue" />
  <img src="https://img.shields.io/github/license/70gd/Batruscator?style=flat-square" />
</p>
