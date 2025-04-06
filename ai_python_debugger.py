
import tkinter as tk
from tkinter import scrolledtext
import traceback
import sys
import io

# Smart Error Fixer
def smart_fixer(error_type, line, code_lines):
    line_num = int(line) - 1
    original = code_lines[line_num].strip()

    if "SyntaxError" in error_type:
        if ":" not in original and any(k in original for k in ["if", "for", "while", "def"]):
            return original + ":"  # Suggest adding colon
        elif not original.endswith(")"):
            return original + ")"  # Missing closing bracket
    elif "NameError" in error_type:
        return "# NameError: Possibly undefined variable or typo"
    elif "IndentationError" in error_type:
        return "    " + original
    elif "ZeroDivisionError" in error_type:
        return original.replace("/ 0", "/ 1  # Avoid zero division")

    return "# General error. Review logic."

# Code Debugging Logic
def debug_code(user_code):
    code_lines = user_code.strip().split('\n')
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    try:
        exec(user_code, {})
        sys.stdout = sys.__stdout__
        result = output_buffer.getvalue()
        return f"✅ BUG FREE\n\nOutput:\n{result}"

    except Exception as e:
        sys.stdout = sys.__stdout__
        tb = traceback.extract_tb(e.__traceback__)
        last = tb[-1]
        error_type = type(e).__name__
        line_num = last.lineno
        message = str(e)

        suggestion = smart_fixer(error_type, line_num, code_lines)

        report = f"""
❌ BUGGY

Error Type: {error_type}
Line Number: {line_num}

Original Line:
> {code_lines[line_num - 1].strip()}

AI Suggestion:
> {suggestion}

Error Message:
{message}
"""
        return report

# Run the Debugger
def run_debugger():
    user_code = code_input.get("1.0", tk.END)
    result = debug_code(user_code)
    result_box.config(state='normal')
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result)
    result_box.config(state='disabled')

# GUI Setup
root = tk.Tk()
root.title("AI Python Debugger")
root.geometry("1000x700")
root.config(bg="#0f0f0f")

title = tk.Label(root, text="💡 AI Python Debugger", fg="#00f7ff", bg="#0f0f0f", font=("Consolas", 20, "bold"))
title.pack(pady=10)

code_input = scrolledtext.ScrolledText(root, height=15, width=110, bg="#1e1e1e", fg="#00ff90", insertbackground="white", font=("Courier", 12))
code_input.pack(pady=10)

run_button = tk.Button(root, text="🔍 Run AI Debugger", command=run_debugger, bg="#00f7ff", fg="#0f0f0f", font=("Consolas", 14, "bold"))
run_button.pack(pady=10)

result_box = scrolledtext.ScrolledText(root, height=15, width=110, bg="#111111", fg="#ff3cac", font=("Courier", 12))
result_box.pack(pady=10)
result_box.config(state='disabled')

root.mainloop()
