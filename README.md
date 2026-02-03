# 💀 Batruscator

<p align="center">
  <img src="https://img.shields.io/badge/Obfuscation-Extreme-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Stability-100%25-green?style=for-the-badge" />
</p>

### 🚀 Usage
1. Put your script in the folder.
2. Run:
   ```bash
   python batruscator_core.py your_file.bat
   ```
3. Get output from `output/obfuscated.bat`.

### ⚙️ Config (`config.json`)
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

| Key | What it does |
| :--- | :--- |
| `loader_inflation_count` | More starting junk. |
| `inline_junk_min/max` | Junk lines per line. |
| `inter_line_inflation_chance` | Random noise chance. |
| `map_count` | Number of variable tables. |
| `obfuscation_intensity` | How much is encoded. |
| `one_line` | Makes it a wall of code. |
| `enable_decoration` | Adds @@ and ; prefixes. |

![Stars](https://img.shields.io/github/stars/70gd/Batruscator?style=flat-square&color=yellow)
![Size](https://img.shields.io/github/repo-size/70gd/Batruscator?style=flat-square)
