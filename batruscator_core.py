import random
import string
import re
import os
import json

class Batruscator:
    def __init__(self):
        self.alphabet_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .:/\\-_"
        self.chinese_vars = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成會可主發年動同工也能下過子說產種面方最後多"
        
        self.config = {
            "loader_inflation_count": 55,
            "inline_junk_min": 7,
            "inline_junk_max": 10,
            "inter_line_inflation_chance": 0.35,
            "map_count": 25,
            "output_dir": "output",
            "enable_decoration": True,
            "obfuscation_intensity": 0.8
        }
        
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except Exception as e:
                print(f"[!] Warning: Could not load config.json: {e}")

    def _random_var(self, length=4):
        return "".join(random.choice(self.chinese_vars) for _ in range(length))

    def _generate_substrings(self, count=None):
        if count is None:
            count = self.config["map_count"]
        subs = {}
        for _ in range(count):
            key = self._random_var(random.randint(20, 40))
            alpha_list = list(self.alphabet_chars)
            random.shuffle(alpha_list)
            subs[key] = "".join(alpha_list)
        return subs

    def _obfuscate_line(self, line, subs):
        if not line.strip() or line.strip().startswith(':') or line.strip().startswith('::'):
            return line
        result = ""
        keys = list(subs.keys())
        i = 0
        intensity = self.config["obfuscation_intensity"]
        
        while i < len(line):
            if line[i] in ("%", "!"):
                char = line[i]
                if i + 1 < len(line) and line[i+1] == char:
                    result += char + char
                    i += 2
                    if i < len(line):
                        result += line[i]
                        i += 1
                    continue
                if char == "%" and i + 1 < len(line):
                    if line[i+1].isdigit() or line[i+1] == "~":
                        p_match = re.match(r"%~[a-z]*[0-9]", line[i:])
                        if p_match:
                            result += p_match.group(0)
                            i += len(p_match.group(0))
                            continue
                        elif line[i+1].isdigit():
                            result += "%" + line[i+1]
                            i += 2
                            continue
                end = line.find(char, i + 1)
                if end != -1:
                    result += line[i:end+1]
                    i = end + 1
                    continue
            c = line[i]
            if c in self.alphabet_chars and random.random() < intensity:
                valid_keys = [k for k in keys if c in subs[k]]
                if valid_keys:
                    k = random.choice(valid_keys)
                    val = subs[k]
                    idx = val.find(c)
                    result += f"%{k}:~{idx},1%"
                else:
                    result += c
            else:
                result += c
            i += 1
        return result

    def _generate_real_junk(self):
        v1 = self._random_var(random.randint(15, 30))
        v2 = self._random_var(random.randint(15, 30))
        common_cmds = [
            f"set /a {v1}=%random% %% 100",
            f"set \"{v1}=%{v2}%\" >nul 2>&1",
            f"if %random% LSS -1 (echo %random%)",
            f"set {v1}=%random%%random%",
            f"echo %date% >nul",
            f"for %%i in ({random.randint(1, 9)}) do set {v2}=%%i",
            f"cd .",
            f"set {v1}=%computername%"
        ]
        return random.choice(common_cmds)

    def _fake_guards(self):
        v1 = self._random_var(random.randint(20, 40))
        v2 = self._random_var(random.randint(40, 80))
        guards = [
            f"set \"{v1}={v2}\"",
            f"if defined {self._random_var(10)} (set {self._random_var(15)}=%random%)",
            f"if %random% GTR 32767 (exit /b 0)",
            f"echo %random%{v2}%random% >nul",
            f"for /l %%k in (1,1,1) do (set {v1}=%%k)",
            f"ver >nul"
        ]
        return random.choice(guards)

    def _random_decor(self, line):
        if not self.config["enable_decoration"]:
            return line
        t_line = line.strip()
        structural = [')', 'else', '(', 'if', 'for', 'setlocal', 'endlocal', ':', '::']
        lower_line = t_line.lower()
        if any(lower_line.startswith(s) for s in structural):
            return line
        r = random.random()
        if r < 0.2: line = "@@" + line
        elif r < 0.4: line = ";" + line
        return line

    def obfuscate(self, script_content):
        lines = [line.strip() for line in script_content.splitlines() if line.strip() and not line.strip().startswith("::")]
        subs = self._generate_substrings()
        header = ["@echo off", "chcp 65001 >nul", "setlocal disabledelayedexpansion"]
        for _ in range(self.config.get("loader_inflation_count", 0)): 
            header.append(f"@{self._generate_real_junk()}")
            header.append(f"@{self._fake_guards()}")
            
        for k, v in subs.items():
            header.append(f'set "{k}={v}"')
            for _ in range(random.randint(0, 1 if self.config.get("inline_junk_max", 0) > 0 else 0)):
                header.append(f"@{self._fake_guards()}")
                
        processed_lines = []
        for line in lines:
            junk_min = self.config.get("inline_junk_min", 0)
            junk_max = self.config.get("inline_junk_max", 0)
            if junk_max > 0:
                for _ in range(random.randint(junk_min, junk_max)):
                    if random.random() < 0.6:
                        processed_lines.append(f"@{self._generate_real_junk()}")
                    if random.random() < 0.5:
                        processed_lines.append(f"@{self._fake_guards()}")
            
            t_line = line.strip().lower()
            is_structural = any(t_line.startswith(s) for s in [')', 'else', '(', 'if ', 'for ', ':', '::'])
            obf = self._obfuscate_line(line, subs)
            
            if is_structural:
                processed_lines.append(obf)
            else:
                final_line = self._random_decor(obf)
                if not any(final_line.startswith(p) for p in ['@', ';']):
                    final_line = f"@{final_line}"
                processed_lines.append(final_line)
                
            if random.random() < self.config.get("inter_line_inflation_chance", 0):
                processed_lines.append(f"@{self._generate_real_junk()}")
                processed_lines.append(f"@{self._fake_guards()}")
                
        if self.config.get("one_line", False):
            combined = []
            for item in header + processed_lines:
                if not combined:
                    combined.append(item); continue
                
                prev = combined[-1].strip()
                curr = item.strip()
                p_low = prev.lower()
                c_low = curr.lower()
                
                can_join = True
                if "(" in prev or ")" in prev or "(" in curr or ")" in curr:
                    can_join = False
                elif any(c_low.startswith(s) for s in [':', 'if ', 'for ', 'else', 'setlocal', 'chcp', 'set ']):
                    can_join = False
                elif any(p_low.startswith(s) for s in ['if ', 'for ', 'else', 'setlocal', 'chcp', 'set ']):
                    can_join = False
                
                if can_join:
                    combined[-1] = f"{combined[-1]} & {item}"
                else:
                    combined.append(item)
            return "\n".join(combined)
            
        return "\n".join(header + processed_lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python batruscator_core.py <input.bat>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"[!] Error: File {input_file} not found.")
        sys.exit(1)
        
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    obfuscator = Batruscator()
    result = obfuscator.obfuscate(content)
    
    output_dir = obfuscator.config["output_dir"]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "obfuscated.bat")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
        
    print(f"[*] Obfuscation complete: {output_path}")
